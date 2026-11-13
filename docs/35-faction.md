# 35 — Faksi ORDE / LEGION

Dua faksi abadi. **Keputusan user (2026-10-30):** Guest ikut memilih · akun lama tanpa faksi diminta memilih. **Revisi T3 (2026-11-13):** ~~terkunci satu season~~ → **pindah gratis 1× selama placement** (lihat MODEL) · layar pilih faksi **SETELAH layar hasil match pertama** (bukan sebelum lobby).

## LORE (docs/23) — dua-duanya abu-abu, sama-sama menarik
Deskripsi kartu onboarding **tidak boleh berat sebelah** (jangan satu terdengar jahat, satu pahlawan — bila tidak, pemain condong + bonus +15% macet di satu faksi). Keduanya punya alasan mulia & cara yang keras.
- **ORDE — Aegis Directorate.** Teks kartu: _"Pelindung Neo-Veridia — mengamankan Relic sebelum jatuh ke tangan yang salah. Techwear presisi."_ Emblem: **PERISAI**.
- **LEGION — Vanguard Syndicate.** Teks kartu: _"Kru jalanan merdeka — merebut Exo-Gear untuk distrik yang dilupakan kota. Glitch & neon."_ Emblem: **CHEVRON/taring**.
- Maks 2 baris, min 16px. Identitas penuh (korporasi vs sindikat) tetap di docs/23; kartu pakai pitch yang seimbang.

## MODEL
- `Player.Faction`: 0 belum pilih · 1 ORDE · 2 LEGION. (kolom sudah ada sejak `AddUserAccounts`.)
- **Aturan pindah (T3, backend ✅ 2026-11-13)**: pilihan pertama (0→1/2) **selalu boleh**. **PINDAH** (1↔2) **GRATIS 1×** selama placement ranked belum selesai (**<5** match ranked Finished = `LeaderboardService.PlacementMatches`, satu angka dgn syarat leaderboard). Setelah jatah dipakai **atau** placement selesai → **terkunci** (409).
  - `Player.FactionSwitchUsed` (bool, migrasi `AddFactionSwitchUsed`). Opsi lama `Game:FactionLocked` **dihapus** (diganti jendela placement).
  - Kenapa bukan "sebelum ranked pertama": layar faksi kini muncul **setelah** match pertama → kalau match itu ranked, jendela sudah lewat (nol). Placement 5 match memberi jendela nyata.
- ⚠️ **BELUM ADA SISTEM SEASON** → setelah terkunci, ganti faksi hanya lewat **endpoint admin** (yang juga **mengembalikan jatah pindah gratis**).

## ONBOARDING — pemicu (T3: SETELAH match pertama)
- **Keputusan T3**: layar pilih faksi muncul **SETELAH layar hasil match pertama** (mode apa pun), **tidak** sebelum lobby. Layar (`faction-screen`), badge, kunci & warna **dipakai ulang**; hanya **pemicunya** yang dipindah.
- ⏳ **Klien belum dipindah (butuh Unity)** — saat ini masih: login/guest + `faction==0` → `faction-screen` sebelum lobby (`NexusGame.NeedsFaction`). Pemindahan pemicu ke pasca-hasil-match-1 bergantung pada **poin e** (layar hasil UITK = Detail Match v2 mode `result`). Status: **Antre**.
- Guest **ikut** memilih. **Guest → daftar akun (K-10, 2026-11-13):** `POST /api/auth/upgrade` (login guest) memasang username+password ke **Player yang sama** → faksi, rating, riwayat, statistik terbawa. DeviceId dilepas (akun berpassword tak bisa dibuka hanya dengan deviceId). Akun terdaftar → 409. UI (tab Akun di Settings) = poin d.

## KESEIMBANGAN — "Butuh Pejuang"
- `FactionService` (cache 1 menit) hitung populasi akun **non-uji** per faksi, server-authoritative.
- Faksi **minoritas** (share < `FactionImbalanceThreshold`, default 0.45, bila total ≥ `FactionMinPopulation`) → ditandai **"Butuh Pejuang"** + badge `+{bonus}%` di kartu onboarding.
- **Bonus nyata**: pemain faksi minoritas dapat tambahan **XP** (`FactionJoinBonusPercent`, default 15%) tiap match (diterapkan di `MatchService.FinalizeAsync`). Bukan kosmetik.

## WARNA — PALET 4 "Terang vs Gelap" (dikunci user 2026-10-30)
Token faksi **tidak** memakai biru/merah tim (Detail Match tetap biru=kamu/merah=lawan) dan **tidak** memakai emas (emas eksklusif rank + MENANG).
- **ORDE**: bidang Ivory `#F5F3EC`, garis Platinum-baja `#AEB9C9`, teks Onyx `#15151A`, emblem **perisai**.
- **LEGION**: bidang Onyx `#15151A`, garis 2px + teks **Volt `#C6F000`** (volt TIDAK untuk bidang besar), emblem **chevron/taring**.
- **Beda tanpa warna**: bentuk emblem (perisai vs chevron) + teks nama — wajib terbaca untuk buta warna.
- **Pengecualian**: ilustrasi kartu di layar pilih faksi boleh glow lore penuh (cyan ORDE / crimson LEGION); tombol & teks tetap token UI. Sprite: `Sprites/fac_orde.png`, `fac_legion.png`.
- **Uji buta warna** (deuteranopia/protanopia): Volt vs hijau +Poin **tidak tertukar** — hue menyatu tapi kecerahan beda jauh (Volt→kuning terang, hijau→zaitun redup). Aturan: Volt hanya garis/teks di atas onyx, jangan bidang besar bersebelahan dengan hijau +Poin.

## BADGE KONSISTEN
Badge faksi di **semua layar** via helper tunggal `NexusLobbyController.SetFactionBadge` + kelas `.nxl-facbadge` (PALET 4: ORDE ivory+platinum, LEGION onyx+volt; sembunyi bila 0):
- Top bar (`player-faction`), Profil (`prof-faction`), Ruang Ladder header (teks ORDE/LEGION). Beda lewat **teks nama + warna token**, bukan biru/merah.

## ENDPOINT
- `POST /api/me/faction {faction:1|2}` (auth): validasi 1/2; idempoten bila sama; pindah gratis 1× selama placement <5, selain itu 409. → `{faction, switchAvailable, locked}`.
- `GET /api/factions` (publik): `{orde, legion, needsWarriors:0|1|2, bonusPercent}`.
- `POST /api/admin/faction {playerId, faction:0|1|2, adminSource?}` (header **`X-Admin-Secret`** = `Admin:Secret`; kosong = nonaktif): set/reset faksi **lewati kunci** (0 = reset → pemain pilih lagi · 1 ORDE · 2 LEGION). Untuk akun uji / dukungan sampai sistem season ada.
  - **Constant-time**: secret dibandingkan `SHA256` + `CryptographicOperations.FixedTimeEquals` (`SecretsEqual`), bukan `==`.
  - **Audit WAJIB**: tiap perubahan menulis `FactionAdminAudit` (sumber `adminSource@ip`, `playerId`, faksi **lama→baru**, waktu) + log `AdminFaction`. Respons memuat `previous`.
  - Reset **mengembalikan jatah pindah gratis** (`FactionSwitchUsed=false`) ✅ (T3).
  - ⚠️ **UTANG RILIS**: ganti `X-Admin-Secret` dengan **admin berbasis role di server + audit log resmi** (docs/90, docs/91) sebelum rilis publik.

## OPSI (`Game:*` / `Admin:*`)
`FactionMinPopulation=2` · `FactionImbalanceThreshold=0.45` · `FactionJoinBonusPercent=15` · `Admin:Secret=""` (set di env utk aktifkan endpoint admin). *(`FactionLocked` dihapus T3.)*

## TES
Backend: `FactionService` (seimbang→tanpa bonus, timpang→minoritas+bonus, di bawah min-pop, akun uji dikecualikan); API (`/api/factions`, admin reset lewati kunci + butuh secret + audit). **T3**: pindah gratis 1× lalu terkunci · 5 placement → terkunci · 4 placement → masih boleh · admin mengembalikan jatah. **72 hijau.** Klien faksi: ✅ diverifikasi editor user (2026-11-13).

## BELUM / NANTI
- **Sistem season** (buka kunci faksi otomatis) — sekarang kunci permanen, reset manual via admin. Faction War (Fase 3). Badge di baris leaderboard (opsional). Bonus selain XP (reward) bila diinginkan.
