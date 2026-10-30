# 35 — Faksi ORDE / LEGION

Dua faksi abadi. **Keputusan user (2026-10-30):** terkunci satu season · Guest ikut memilih · akun lama tanpa faksi diminta memilih saat login berikutnya.

## MODEL
- `Player.Faction`: 0 belum pilih · 1 ORDE · 2 LEGION. (kolom sudah ada sejak `AddUserAccounts`.)
- **Terkunci**: setelah memilih (≠0), tak bisa pindah selama `Game:FactionLocked=true` (satu season). Reset saat pergantian season (nanti).

## ONBOARDING (sebelum lobby)
- Setelah login/guest, jika `faction==0` → **layar pilih faksi** (bukan lobby). Klien: `NexusGame.NeedsFaction` → `NexusLobbyController` menampilkan `faction-screen` (dua kartu ORDE biru / LEGION merah), tombol **KUNCI FAKSI** → `UiSetFaction` → `POST /api/me/faction`. Sukses → lobby.
- Guest **ikut** memilih (beda dari IMGUI lama yang hanya untuk akun terdaftar).

## KESEIMBANGAN — "Butuh Pejuang"
- `FactionService` (cache 1 menit) hitung populasi akun **non-uji** per faksi, server-authoritative.
- Faksi **minoritas** (share < `FactionImbalanceThreshold`, default 0.45, bila total ≥ `FactionMinPopulation`) → ditandai **"Butuh Pejuang"** + badge `+{bonus}%` di kartu onboarding.
- **Bonus nyata**: pemain faksi minoritas dapat tambahan **XP** (`FactionJoinBonusPercent`, default 15%) tiap match (diterapkan di `MatchService.FinalizeAsync`). Bukan kosmetik.

## BADGE KONSISTEN
Badge faksi (ORDE biru / LEGION merah, sembunyi bila 0) di **semua layar** via helper tunggal `NexusLobbyController.SetFactionBadge` + kelas `.nxl-facbadge`:
- Top bar (`player-faction`), Profil (`prof-faction`), Ruang Ladder header (teks ORDE/LEGION). 

## ENDPOINT
- `POST /api/me/faction {faction:1|2}` (auth): validasi 1/2, **terkunci** bila sudah pilih (409), idempoten bila sama. → `{faction, locked}`.
- `GET /api/factions` (publik): `{orde, legion, needsWarriors:0|1|2, bonusPercent}`.

## OPSI (`Game:*`)
`FactionLocked=true` · `FactionMinPopulation=2` · `FactionImbalanceThreshold=0.45` · `FactionJoinBonusPercent=15`.

## TES
Backend: `FactionService` (seimbang→tanpa bonus, imbang­ang→minoritas+bonus, di bawah min-pop, akun uji dikecualikan); API (lock+validasi, `/api/factions`). Klien: butuh compile editor (tak bisa diuji headless).

## BELUM / NANTI
- Season reset (buka kunci faksi). Faction War (Fase 3). Badge di baris leaderboard (opsional). Bonus selain XP (reward) bila diinginkan.
