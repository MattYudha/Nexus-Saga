# 33 — Leaderboard (Papan Peringkat Ranked)

Papan yang **bisa dipahami pemain**. Menggantikan urutan lama (rating mentah, akun uji ikut, akun 0 match di atas).

## 1. SYARAT MASUK
- **Selesai placement**: minimal **5 match ranked selesai** (`Match.Mode="ranked"`, `Status=Finished`). Akun W0/L0 / belum 5 match → tidak tampil.
- **Bukan akun uji**: `Player.IsTestAccount=true` → tidak tampil. Deteksi (`Ranks.IsTestIdentity`): guest game asli pakai `deviceId "nx-*"`; selain itu (`e2e-`, `fb-`, `device-`, `gate`, `persisttest`, `logintest`, dll.) = uji. Di-set saat buat akun + backfill startup.
- Ban / Disputed berulang: TODO (belum ada sistem ban).

## 2. URUTAN (bisa dipahami)
Angka tampil = **Poin Ladder** (`Ranks.LadderPoints`, 0–100 progres di dalam tier), BUKAN MMR mentah.
Urut: **tier tertinggi → Poin Ladder → win rate → jumlah match.**
Posisi pakai **conservative rating = `rating − 2·RD`** (bukan rating mentah) → tier & poin dihitung dari conservative, jadi akun sedikit-match (RD tinggi) tak melompat ke puncak. `TierOrder` 0 Rookie … 5 Nexus Legend.

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

## PROTEKSI DEMOSI (opsi 1 — IMPLEMENTASI 2026-10-30)
Floor tier di **layer tampilan**: setelah naik tier, tier tampil tak boleh turun `Game:DemotionGraceMatches` match ranked (default **3**). **Glicko tetap murni** (rating/RD/matchmaking tak tersentuh).
- **State** (`Player`): `LastRankedTierOrder` (tier mentah setelah match terakhir → deteksi promosi), `TierFloorOrder` (floor aktif), `TierFloorLeft` (sisa match floor berlaku). Migrasi `AddTierFloor`.
- **Logika** (`Ranks.StepTierFloor`, murni & diuji): tier mentah > terakhir → promosi, pasang floor di tier baru + reset grace. Selain itu → grace −1; habis → floor lepas. Dipanggil di `MatchService.FinalizeAsync` untuk kedua pemain.
- **Tampil** (`Ranks.ApplyFloor(baseOrder, floorOrder, floorLeft)` = `floorLeft>0 ? max(base,floor) : base`): dipakai di **profil** (`/api/me`, base = rating mentah) DAN **leaderboard** (base = conservative; saat di-floor → Poin Ladder 0). `/api/me/rank` ikut lewat leaderboard. Stats/radar tetap pakai tier mentah (populasi pembanding jujur).
- **Backfill**: akun lama `LastRankedTierOrder` di-set ke tier mentah terkini (sekali, idempoten) agar match berikutnya tak salah dibaca promosi.
- Tes: `ApplyFloor` aktif/lepas, `StepTierFloor` promosi→tahan 3 match→turun, re-promosi reset grace, `TierName`↔`TierOrder`.
