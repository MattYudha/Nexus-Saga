# 33 — Leaderboard (Papan Peringkat Ranked)

Papan yang **bisa dipahami pemain**. Menggantikan urutan lama (rating mentah, akun uji ikut, akun 0 match di atas).

## 1. SYARAT MASUK
- **Selesai placement**: minimal **5 match ranked selesai** (`Match.Mode="ranked"`, `Status=Finished`). Akun W0/L0 / belum 5 match → tidak tampil.
- **Bukan akun uji**: `Player.IsTestAccount=true` → tidak tampil. **Default `false` untuk SEMUA akun baru, deviceId apa pun** (termasuk `fb-…` login asli). Ditandai uji **hanya EKSPLISIT** lewat jalur tes: `isTest=true` DAN server `Game:AllowTestAccounts=true` (hanya dev/test). **TANPA tebakan awalan deviceId.** Backfill SATU KALI untuk akun uji LAMA berbasis **NAMA saja** (`Ranks.IsLegacyTestName`: `e2e_`, `fb_`, `gate`, `persisttest`, `logintest`). Tes jaga: akun baru deviceId `fb-…` tanpa flag → BUKAN uji.
- Ban / Disputed berulang: TODO (belum ada sistem ban).

## 2. URUTAN & TIER (KONSISTEN di semua layar)
Angka tampil = **Poin Ladder** (`Ranks.LadderPoints`, 0–100 progres di dalam tier), BUKAN MMR mentah.
- **TIER & Poin yang DITAMPILKAN = dari RATING ASLI** (`p.Rating`) — **SAMA** di profil, lobby, ruang ladder, leaderboard, dan riwayat. (Sumber tunggal: `Ranks.TierFor`/`LadderPoints` atas rating asli.)
- **URUTAN POSISI** (T3, 2026-11-13): **(1) TIER TAMPIL turun** → **(2) conservative rating `rating − 2·RD` di DALAM tier** → **(3) win rate** → **(4) jumlah match**. Conservative HANYA untuk urutan, TIDAK untuk tier/poin yang tampil.
- Kenapa tier dulu: dulu urut conservative murni → Gladiator ber-RD tinggi bisa jatuh di bawah Rival (tier di papan terbalik). Sekarang tier di papan **selalu monoton turun** (tes `Position_TierFirst_HighRdGladiatorNotBelowRival`).
- Di dalam satu tier, dua "Rival" bisa beda posisi (RD lebih kecil di atas) — disengaja. `TierOrder` 0 Rookie … 5 Nexus Legend.

## 3. KOLOM
Peringkat · emblem+tier · nama · Poin Ladder · W/L · win rate. Baris pemain sendiri di-highlight.
- Di luar 100 besar tapi sudah placed → baris bawah: peringkat ASLI (`/api/me/rank`).
- Belum placement → baris bawah: "Selesaikan X match ranked lagi untuk masuk peringkat".

## 4. KONSISTENSI DATA
- **W/L sama di mana pun** (leaderboard = profil = kartu Win Rate) → sumber tunggal `Player.Wins/Losses`.
- **Legacy5v5 IKUT di W/L** (menang/kalah itu nyata), TAPI **tidak** di K/D (K/D hanya `ranked1v1`, lihat [[docs/32]]). Jadi: W/L = semua ranked Finished; K/D = ranked1v1 saja.

## 5. PERFORMA
`LeaderboardService` (singleton) hitung di backend + **cache 1 menit** (recompute saat stale). Endpoint tak hitung ulang tiap buka.

## ENDPOINT
- `GET /api/leaderboard?limit=100` → `[{rank, displayName, tier, ladderPoints, wins, losses, winRate, matches}]` (sudah terurut, sudah tersaring).
- `GET /api/me/rank` (auth) → `{placed:true, rank, tier, ladderPoints, wins, losses, winRate, matches}` atau `{placed:false, needed, rankedMatches}`.

## PROTEKSI DEMOSI (opsi 1 — ⛔ NONAKTIF selama development)
> **NONAKTIF** (`Game:DemotionGraceMatches=0`, default dev & produksi) → tier tampil SELALU = tier rating asli, floor tak pernah aktif. **Kode, kolom DB, dan tes dipertahankan. AKTIFKAN KEMBALI (nilai 3) SEBELUM RILIS PUBLIK.** Floor aktif sisa masa percobaan dibersihkan saat startup (`TierFloorLeft/Order=0`).

Saat diaktifkan (grace>0): floor tier di **layer tampilan**: setelah naik tier, tier tampil tak boleh turun `Game:DemotionGraceMatches` match ranked. **Glicko tetap murni** (rating/RD/matchmaking tak tersentuh).
- **State** (`Player`): `LastRankedTierOrder` (tier mentah setelah match terakhir → deteksi promosi), `TierFloorOrder` (floor aktif), `TierFloorLeft` (sisa match floor berlaku). Migrasi `AddTierFloor`.
- **Logika** (`Ranks.StepTierFloor`, murni & diuji): tier mentah > terakhir → promosi, pasang floor di tier baru + reset grace. Selain itu → grace −1; habis → floor lepas. Dipanggil di `MatchService.FinalizeAsync` untuk kedua pemain.
- **Tampil** (`Ranks.ApplyFloor(baseOrder, floorOrder, floorLeft)` = `floorLeft>0 ? max(base,floor) : base`): dipakai di **profil** (`/api/me`, base = rating asli) DAN **leaderboard** (base = **rating asli** juga — sejak poin a; dulu tertulis "conservative", sudah tidak berlaku; saat di-floor → Poin Ladder 0). `/api/me/rank` ikut lewat leaderboard. Stats/radar tetap pakai tier mentah (populasi pembanding jujur).
- **Backfill**: akun lama `LastRankedTierOrder` di-set ke tier mentah terkini (sekali, idempoten) agar match berikutnya tak salah dibaca promosi.
- Tes: `ApplyFloor` aktif/lepas, `StepTierFloor` promosi→tahan 3 match→turun, re-promosi reset grace, `TierName`↔`TierOrder`.

## Kebijakan RD (D12, 2026-11-13)
- **Lantai RD 30**: RD tidak pernah di bawah 30 → `conservative = rating − 2·RD` tetap memberi jarak keyakinan.
- **Inflasi saat pasif**: tiap 7 hari tanpa match ranked, RD naik `φ* = √(φ² + σ²)` per periode (maks 350), diterapkan
  tepat sebelum match berikutnya (`Player.LastRatedAt`). Pemain yang kembali → posisi papan lebih hati-hati.
- **Anti-kolusi**: match yang poinnya diredam tidak menurunkan RD.
- Seri tidak mengubah rating/RD (NX-11).
