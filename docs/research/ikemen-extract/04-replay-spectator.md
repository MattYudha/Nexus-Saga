# 04 — Replay, spectator, killcam, anti-desync

Menutup ⬜ "replay/spectator/killcam" dan 🟡 "deteksi cheat".

## 1. Bukti di Ikemen (OBSERVED)

Karena simulasi deterministik, Ikemen tidak merekam state — hanya **input**:

| Fungsi | Lokasi | Isi |
|---|---|---|
| `RollbackSession.SetInput(time, player, bits, axes)` | `rollback.go:524` | kunci input pada tick tertentu |
| `RecordReplayFrame(time, inputs, axes)` | `rollback.go:549` | simpan frame replay |
| `TruncateReplayFrom(time)` | `rollback.go:571` | buang frame setelah rollback (input berubah) |
| `SaveReplay()` | `rollback.go:587` | tulis file replay |
| `simulateFrame()` | `rollback.go:229-241` | jalankan ulang dari input (inilah yang membuat replay mungkin) |
| `LiveChecksum()` | `rollback.go:844-898` | CRC32 atas state hidup (+ hash nama stage & karakter) |
| `GameState.Checksum()` | `state.go:436` | checksum khusus debug |
| `SaveGameState/LoadGameState` | `rollback.go:673-739` | clone penuh state untuk rollback |

Input satu frame = 14 boolean + 6 nilai analog per pemain (`InputBits`, `[6]int8`; `rollback.go:360-386`).

## 2. PROPOSED untuk Quantum

### 2.1 Format replay (server = sumber kebenaran)
```
Replay {
  version, matchId, configHash,          // tolak replay kalau config berubah
  seed, stageId, mode,
  players: [ { accountId, heroOrder[], team } ],
  inputLog: { [playerId]: bytes }         // 1 frame = MoveDir(1) Buttons(1) AimYaw(2) + PickHero(1)
  checkpoints: [ { tick, hash } ]         // tiap 60 tick
  result: { [team]: score, mvp, stats }   // hasil yang sudah divalidasi server
}
```
Ukuran: 5 byte/pemain/tick. Match 3 menit (10.800 tick) × 10 pemain ≈ **540 KB** mentah → ~60 KB setelah
RLE/zstd. Cukup kecil untuk disimpan di Postgres (bytea) atau object storage, tanpa menyimpan state penuh.

### 2.2 Spektator
Spectator menjalankan simulasi yang **sama** dengan input yang sama, delay 60–120 tick (1–2 dtk) supaya
input selalu tersedia (tidak pernah "menunggu"). Tanpa delay, spectator akan memicu rollback terus-menerus.
Data yang dikirim: input log + checkpoint hash, **bukan** posisi entity per frame.

### 2.3 Killcam
Rewind lokal N tick lalu putar ulang dengan delta lambat. Kalau Quantum versimu menyimpan riwayat frame
(cek `Game.Frames` / API rewind di 3.x), killcam = replay terarah; kalau tidak, simpan ring buffer 180 tick
posisi/anim untuk View saja. Killcam **hanya presentasi** — tidak boleh mengubah state sim.

### 2.4 Anti-cheat & kartu Disputed (poin g di PROGRESS)
| Lapis | Cara | Catatan |
|---|---|---|
| Desync detection | tiap 30 tick klien kirim `(tick, hash)` ke plugin server; server bandingkan antar klien | hash = FP state ringkas: Pos, Vel, Hp, HitStun, GuardGauge, frameIndex |
| Validasi hasil | server plugin hitung ulang dari input log (server autoritatif **untuk hasil**, bukan untuk frame) | ini yang benar untuk Quantum, bukan "server mengoreksi state" |
| Input mustahil | tolak input yang melanggar cooldown/state (mis. swap saat `HitStun` tanpa cancel) | validasi deterministik, bukan heuristik |
| Rate/telemetry | jumlah desync per pemain, pola rollback ekstrem | bukan bukti, hanya sinyal |
| Kartu Disputed | mismatch hash → match ditandai "TIDAK DIHITUNG", rating tidak berubah | implementasi klien = poin g |

**Batas jujur:** klien yang dimodifikasi tetap bisa memalsukan hash-nya sendiri. Deteksi desync menangkap
**perbedaan**, bukan niat. Untuk ranked serius, satu klien harus jadi "penghitung" (server-side simulation
headless) atau minimal replay direview asinkron. Ini keputusan biaya, bukan keputusan teknis.

### 2.5 Yang **tidak** boleh
- Menyimpan `Transform` Unity sebagai sumber replay.
- Memutar replay dengan `Time.timeScale`.
- Merekam posisi dari View (harus dari sim).
- Menyimpan state penuh tiap tick di server "supaya aman" — itu membunuh biaya CCU.
