# Analisis: photon-backend (Quantum 3 scaffold milik user) — bisa dipakai di Nexus Saga?

Sumber: `C:\Users\US3R\photon-backend` (proyek Anda; repo `cds-id/photon-backend`, domain `photon.ciptadusa.com`). Nama resmi: "Photon Pong" — demo multiplayer minimal di atas **Photon Quantum 3**.

Ringkas: **Ya, ini sangat berharga** — ini persis "Plan B netcode" kita yang **sudah jadi**, dan mengubah kalkulasi spike. Tapi ada tegangan dengan 2 keputusan terkunci (netcode custom UDP, backend Nakama). Saya bahas jujur + rekomendasi.

---

## 1. Apa isinya (OBSERVED)
| Komponen | Isi |
|---|---|
| **Netcode** | **Photon Quantum 3** (deterministik, predict-rollback). Sim jalan **di semua client**, Photon Cloud hanya merelai **input** + sinkron clock |
| **Simulasi** | `Pong.qtn` (DSL) + `PongSystem.cs`. State di **globals**, math **FP** (fixed-point), **tanpa RNG** (sudut serve dari skor). `#pragma max_players 2` |
| **Backend** | ASP.NET Core 8 + PostgreSQL + EF Core + Docker. Endpoint: guest auth (JWT), Photon custom auth, Photon webhooks (game create/close/result), match result cross-check + **Elo (K=32)**, leaderboard |
| **Trust model** | Hasil match dirating **hanya bila 2 pemain lapor skor sama**; webhook secret; JWT. Client-simulated, bukan server-authoritative |
| **Client** | Unity 2022.3 + Quantum SDK 3.0.14, CI build Android APK (GitHub Actions, self-hosted runner) |
| **Status** | Backend **verified** (16 test lulus, jalan vs PostgreSQL nyata); simulasi verified vs SDK; client build APK OK; **match end-to-end di device belum diverifikasi** |

**Fakta arsitektur kunci:** Quantum non-Enterprise **tidak punya game server authoritative** yang kita tulis. Server authoritative butuh Plugin SDK (Enterprise, berbayar). Jadi "backend" = web service biasa yang dipanggil Photon (auth/webhook) + client (profil/hasil).

---

## 2. Kecocokan untuk Nexus Saga

### 2A. Netcode — ini "Plan B" kita yang sudah jadi
Keputusan terkunci kita (doc 20): spike **pure .NET custom UDP server-authoritative** dulu, **Quantum sebagai cadangan** (S-13: uji Quantum 2–3 hari). **Proyek ini = Quantum sudah di-scaffold** (toolchain, CI, backend, auth, webhook). Artinya:
- Pekerjaan netcode custom UDP (risiko & effort TERBESAR proyek — berkali saya flag) bisa **dilewati** kalau Quantum lolos.
- Spike Quantum yang direncanakan S-13 **sebagian sudah dikerjakan** oleh Anda.

⚠️ **Kekurangan jujur Quantum (vs keputusan server-authoritative kita):**
1. **Client-simulated, bukan server-authoritative.** README sendiri mengakui: "Colluding players can fabricate a result." Untuk game kompetitif + ekonomi uang asli, ini lebih lemah dari model kita.
   - **Mitigasi (elegan, ada di README):** simpan replay (input) → **re-simulasi di backend pakai Quantum sim DLL yang sama** (`QuantumDotnetBuildSettings`) → verifikasi hasil **tanpa percaya client**. Karena sim deterministik, backend bisa menjalankan ulang dan mengecek. Ini memberi **otoritas server pasca-match** dengan kode sim yang sama. Menutup sebagian besar celah cheat hasil.
   - Desync (cheat yang mengubah state) terdeteksi otomatis via checksum Quantum.
2. **5v5 = 10 pemain.** Pong `max_players 2`. Quantum mendukung lebih, tapi biaya rollback naik dengan (jumlah pemain × ukuran state). 10 pemain brawler berat **wajib diuji** — ini justru yang harus diukur spike.
3. **Combat Core ditulis ulang** sebagai Quantum systems + `.qtn` (pakai FP/ECS Quantum), bukan loop sendiri. Desain data-oriented kita (doc 10 A1) memudahkan, dan **toolchain Anda sudah siap**.
4. **Biaya & lock-in.** Quantum Cloud = harga per-CCU (naik dengan pemain); custom UDP tadinya "self-host murah". Untuk solo dev, waktu yang dihemat kemungkinan sepadan; biaya di skala besar nyata.

### 2B. Room / matchmaking 5v5 — **cocok**
Lapisan room = **Photon Realtime** (di bawah Quantum): quick match (`JoinRandomRoom`, RoomName null), private room (kode 4-digit), **room properties** untuk filter matchmaking (mode/mmr/region), `maxPlayers` per room (10 untuk 5v5), webhook lifecycle (create/close/join/leave).

➡️ **Ini memetakan bersih ke 4 jalur kita (doc 24):**
| Jalur kita | Photon room |
|---|---|
| Solo 1v1 Ranked | quick match, maxPlayers=2, prop {mode:ranked, mmr} |
| Street Room (custom) | create room + kode, prop {mode, size, map} |
| Squad War / Faction War | matchmaking by prop {mode, faction/squad} |
Jadi **schema room 5v5 bisa pakai Photon** — konsepnya sama dengan match-label Nakama yang kita rancang (doc 14 §4), hanya ganti penyedia.

### 2C. Backend meta — TIDAK menggantikan Nakama
Backend di sini **minimal & Pong-spesifik**: auth + match result + Elo + leaderboard. Nakama memberi jauh lebih banyak: party, guild, chat, shop, wallet, inventory, matchmaking properties, presence. **Backend ini bukan pengganti Nakama**, tapi **polanya bagus** (web service + Photon webhook + rating cross-check/replay-verify). Reusable: TokenService, auth guest, webhook handler, EF Core setup, Docker/CI.

---

## 3. Tegangan dengan keputusan terkunci
| Keputusan terkunci | Proyek ini | Konflik? |
|---|---|---|
| Netcode = **custom .NET UDP server-authoritative** (Plan A) | Quantum Cloud client-simulated | ⚠️ Ya — ini Plan B, bukan Plan A |
| Backend = **Nakama** | Custom ASP.NET + Photon Cloud | ⚠️ Sebagian — room via Photon; meta masih butuh Nakama/diperluas |
| Core = pure C# loop sendiri | Quantum systems + .qtn | ⚠️ Ditulis ulang di framework Quantum |
| Spike mulai dari custom UDP | Quantum sudah jadi | ✅ Justru mempercepat |

---

## 4. REKOMENDASI (jujur, untuk solo + AI)
**Balik urutan spike: mulai dari Quantum 3, bukan custom UDP.**

Alasan: netcode custom UDP server-authoritative adalah **risiko & effort terbesar** proyek ini (saya flag berulang). Anda **sudah** punya jalur Quantum yang jalan. Untuk solo dev, mengadopsi Quantum kemungkinan **menghemat berbulan-bulan**.

Langkah usulan (revisi doc 20):
1. **Spike Quantum dulu:** bangun 2-kapsul brawler (gerak 8 arah, 1 pukulan, OBB hit) di Quantum; ukur 5 metrik + **kelayakan 10 pemain** pada lag 150 ms.
2. **Uji verifikasi backend via replay re-sim** (tutup celah cheat hasil) — pakai sim DLL yang sama.
3. **Jika lolos di 10 pemain dengan rasa baik → ADOPSI Quantum**, buang rencana custom UDP server. Hemat besar.
4. **Jika gagal di 10 pemain** (rollback terlalu berat) → baru pertimbangkan custom UDP (atau kurangi scope ke mode kecil di Quantum + mode besar custom).
5. **Meta backend:** Photon Realtime untuk room/match; untuk party/guild/chat/shop/wallet → **Nakama** (atau perluas backend ASP.NET ini bertahap). Putuskan setelah spike.

**Yang langsung reusable dari proyek Anda:**
- Seluruh pola Quantum (DSL, systems, CI Android, PongSetup) → ganti Pong dengan brawler.
- Backend auth guest + JWT + Photon custom auth + webhook + Docker/CI → fondasi backend kita.
- Pola rating cross-check + (nanti) replay re-sim → anti-cheat hasil.
- Schema room Photon → mekanisme room 5v5 kita.

---

## 5. Dampak ke dokumen (usulan, menunggu konfirmasi)
- `20` (spike): **mulai dari Quantum**, bukan pure .NET UDP. Metrik + target 10 pemain tetap.
- `09`/`14`: netcode = Quantum (bukan custom UDP) bila spike lolos; backend = Photon Realtime (room) + Nakama/ASP.NET (meta).
- `10 A1`, `19`: koreksi — otoritas = **replay re-sim pasca-match**, bukan UDP real-time authoritative.
- Combat Core: tetap desain Ikemen-derived (OBB+sphere, doc 13), **diimplementasi sebagai Quantum systems**.

## 6. Keputusan terbuka
1. Setuju balik urutan spike: **Quantum dulu**?
2. Target 10 pemain Quantum: uji sebagai kriteria lanjut/tidak.
3. Meta backend: Nakama tetap, atau perluas backend ASP.NET Photon ini?
4. Biaya Quantum Cloud per-CCU: cek pricing untuk proyeksi.
5. Repo `photon-backend` privat (SDK Quantum proprietary) — jaga tetap privat; jangan commit SDK ke repo publik Nexus.
