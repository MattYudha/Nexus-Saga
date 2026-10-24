# 20 — Rencana Eksekusi Spike Fase 1 (detail, 2026-10-24)

Rencana teknis langkah demi langkah untuk Spike Netcode. **Belum dieksekusi** (butuh izin coding, S-00). Mengacu `08`, `13`, `19`, `research/netcode-ddnet.md`.

## Prinsip spike
- **Headless, tanpa engine 3D.** Spike mengukur netcode + Combat Core. Kelima metrik (`10 §E5`) tidak butuh render. Jadi spike = **pure .NET console** (Core + server + bot client + network simulator). Ini jalur tercepat & paling de-risk; keputusan engine client (`21`) tidak memblokir spike.
- **Visualisasi minimal opsional:** dump posisi ke log/CSV atau viewer 2D top-down sederhana (ASCII/PNG per tick) untuk verifikasi mata — bukan game.
- Output akhir: `docs/12-laporan-spike.md` + keputusan Go/No-Go.

## Struktur solusi (.NET)
```
NexusSaga.sln
├─ src/NexusSaga.Core/         (netstandard2.1) — deterministik, tanpa deps
│   ├─ FixedMath/   Fix64, FixVec3, yaw(uint16), trig/sqrt deterministik
│   ├─ Sim/         tick pipeline T0–T10, state machine, collision primitif
│   ├─ Combat/      HitDef, hitbox capsule/OBB, Critical/BreakStock, juggle
│   ├─ Loadout/     gear drop, hero swap
│   ├─ Data/        skema state/hero (13), loader JSON→struct
│   └─ Net/         InputFrame, Snapshot, delta, quantize (kontrak S-02)
├─ src/NexusSaga.Server/       (.NET 8 console) — loop 60Hz, UDP, lag-comp, warm-pool stub
├─ src/NexusSaga.BotClient/    (.NET 8 console) — bot kirim input, prediksi, ukur metrik
├─ src/NexusSaga.NetSim/       — simulator latency/jitter/loss (in-proc atau proxy UDP)
└─ tests/NexusSaga.Tests/      — determinisme, round-trip, collision, replay
```

## Langkah (S-00 → S-14)

### S-00 — Izin coding (gerbang)
Pemilik proyek menyetujui mulai coding. Dicatat di `90-decision-log.md`.

### S-01 — Toolchain
- Pasang **.NET 8 SDK** (saat ini hanya runtime). Verifikasi `dotnet --list-sdks` → 8.x.
- IDE: Rider / VS / VS Code + C# Dev Kit.
- Belum perlu Unity/Godot/Blender untuk spike.
- **Selesai bila:** `dotnet new`, `dotnet build`, `dotnet test` jalan.

### S-02 — Kontrak data (paling kritis; kunci dulu)
Definisikan struct yang **tidak boleh berubah** sembarangan:
```
InputFrame (per tick): { tick:uint, moveDir:byte(0-8), buttons:ushort(bitmask),
                         aimYaw:ushort }   // (19: 1 struct lintas platform)
Snapshot: { tick:uint, entities:[ EntityState ] }
EntityState: { id, posX/Y/Z:Fix, yaw:ushort, stateId:ushort, stateTime:ushort,
               hp:short, breakStock:byte, gearFlags:byte, hitstun:byte, cooldowns... }
   // TANPA kosmetik (19 G1)
Packet header: { sessionToken:ulong, seq:uint, mac:... }   // 19 #4 + anti-replay A
```
- Serializer + delta + quantize (DDNet-style). Test round-trip.
- **Selesai bila:** encode→decode identik; delta vs full konsisten; ukuran snapshot 10 entity terukur.

### S-03 — FixedMath
Fix64 (atau Q32.32), FixVec3, yaw uint16, sin/cos/sqrt deterministik (LUT atau integer).
- **Selesai bila:** test determinisme lulus di 2 run; tidak ada `float` di jalur sim.

### S-04 — Core: gerak + arena
2 entitas kapsul, gerak 8 arah + lompat/gravitasi, collision vs **collider primitif** (box/ramp/DropZone) dari arena data (`19 #2`), simpan `lastGroundedPos`.
- **Selesai bila:** replay input sama 2× → checksum identik (determinisme).

### S-05 — Core: state machine + hit
State minimal (Idle, Run, Attack, Hit, Launched, Down, GetUp) + HitDef minimal + hitbox capsule/OBB + resolusi (prioritas→id, juggle, guard arc 180°). Data via JSON (`13 §5`).
- **Selesai bila:** test transisi & hit lulus; Damage Gate + 1 Break Stock jalan.

### S-06 — Server loop + UDP
Loop 60Hz catch-up, LiteNetLib UDP, input per tick keyed by tick, input-timing feedback, snapshot 30Hz delta, packet MAC + session token + anti-replay (`19 #4/A`).
- **Selesai bila:** 2 bot client connect, bermain, sinkron.

### S-07 — Prediksi client + rekonsiliasi
Rollback-replay pemain lokal dari snapshot terakhir; interpolasi entity lain.
- **Selesai bila:** gerak lokal terasa instan (0-frame); koreksi halus.

### S-08 — Predicted hit reaction (metrik #1)
Korban remote masuk mode prediksi saat hit-confirm lokal (HitDef), dikoreksi snapshot.
- **Selesai bila:** reaksi korban ≤ 1 frame setelah hit lokal.

### S-09 — Lag compensation
Histori hurtbox 300 ms; serangan di-resolve pada tick yang dilihat penyerang; rewind ≤ 150 ms.
- **Selesai bila:** hit pada ping tinggi konsisten client-server.

### S-10 — Network simulator
Sisipkan latency 150 ms + jitter 20 ms + loss 2% (in-proc wrapper atau proxy UDP). Bisa di-tuning.
- **Selesai bila:** semua skenario uji jalan di kondisi buruk.

### S-11 — Harness metrik + bot otomatis
Bot menjalankan skenario combo standar; instrumentasi ukur 5 metrik:
| # | Metrik | Target |
|---|---|---|
| 1 | Reaksi korban (layar penyerang) | ≤ 1 frame |
| 2 | Hit-confirm/combat-state misprediction | < 5% |
| 3 | Koreksi posisi korban | < 0,5 m (95%), halus ≤ 6 frame |
| 4 | Kapasitas server | ≥ 20 match × 10 pemain / 1 vCPU |
| 5 | Bandwidth | < 64 kbps/pemain |
- **Selesai bila:** laporan angka otomatis (CSV/JSON).

### S-12 — Uji kapasitas
N match bot headless di 1 vCPU (batasi afinitas/core). Ukur match/vCPU + bandwidth.
- **Selesai bila:** metrik #4/#5 terukur.

### S-12b — Lightweight Debug Viewer (opsional, ringan — TANPA engine 3D)
Visualisasi mata untuk melihat kelancaran juggle di ping 150 ms, di luar metrik matematis.
- **Bentuk:** satu file **HTML5 Canvas + WebSocket** (server kirim state per tick) atau jendela 2D sederhana. Top-down/side 2D, bukan game.
- **Tampilkan:** 2 kapsul (posisi), **hitbox (merah) & hurtbox (biru)** per frame, dan **bayangan Client Prediction vs Server Snapshot** (2 warna) agar koreksi rollback terlihat.
- **Overlay:** tick, ping simulasi, stateId, Break Stock, hitstun.
- **Selesai bila:** bisa melihat combo juggle real-time + selisih prediksi vs server secara visual.
- Catatan: read-only (hanya menggambar state dari server); tidak memengaruhi sim/determinisme.

### S-13 — Pembanding Photon Quantum (2–3 hari)
Sampel brawler Quantum; bandingkan effort + rasa + metrik #1–3. Catatan perbandingan.
- **Selesai bila:** ada rekomendasi berbasis bukti.

### S-14 — Laporan + Go/No-Go
`docs/12-laporan-spike.md` (hati-hati: nomor 12 sudah dipakai Rest Room → pakai `docs/22-laporan-spike.md`). Keputusan: lanjut custom netcode atau pindah Quantum. Dicatat di decision log.

## Gerbang keputusan
- Metrik #1–3 gagal → evaluasi/pindah **Photon Quantum** (Core data-oriented memudahkan port).
- Metrik #4–5 gagal → **optimasi**, bukan ganti stack.

## Catatan
- Semua angka tuning (fall damage, cooldown, frame data) dari `13 §4` sebagai titik awal.
- Arena spike dibuat via pipeline Blender headless (`21`) → collider JSON → langsung dipakai S-04. Ini sinergi: pipeline aset menghasilkan input untuk spike.
