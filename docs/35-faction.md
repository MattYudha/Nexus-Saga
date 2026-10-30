# 35 — Faksi ORDE / LEGION

Dua faksi abadi. **Keputusan user (2026-10-30):** terkunci satu season · Guest ikut memilih · akun lama tanpa faksi diminta memilih saat login berikutnya.

## LORE (docs/23) — dua-duanya abu-abu, sama-sama menarik
Deskripsi kartu onboarding **tidak boleh berat sebelah** (jangan satu terdengar jahat, satu pahlawan — bila tidak, pemain condong + bonus +15% macet di satu faksi). Keduanya punya alasan mulia & cara yang keras.
- **ORDE — Aegis Directorate.** Teks kartu: _"Pelindung Neo-Veridia — mengamankan Relic sebelum jatuh ke tangan yang salah. Techwear presisi."_ Emblem: **PERISAI**.
- **LEGION — Vanguard Syndicate.** Teks kartu: _"Kru jalanan merdeka — merebut Exo-Gear untuk distrik yang dilupakan kota. Glitch & neon."_ Emblem: **CHEVRON/taring**.
- Maks 2 baris, min 16px. Identitas penuh (korporasi vs sindikat) tetap di docs/23; kartu pakai pitch yang seimbang.

## MODEL
- `Player.Faction`: 0 belum pilih · 1 ORDE · 2 LEGION. (kolom sudah ada sejak `AddUserAccounts`.)
- **Terkunci**: setelah memilih (≠0), tak bisa pindah selama `Game:FactionLocked=true` (satu season).
- ⚠️ **BELUM ADA SISTEM SEASON** → kunci saat ini **efektif permanen**. Ganti/reset faksi hanya lewat **endpoint admin** (lihat ENDPOINT) sampai season dibangun.

## ONBOARDING (sebelum lobby)
- Setelah login/guest, jika `faction==0` → **layar pilih faksi** (bukan lobby). Klien: `NexusGame.NeedsFaction` → `NexusLobbyController` menampilkan `faction-screen` (dua kartu, deskripsi lore docs/23, emblem perisai vs chevron), tombol **KUNCI FAKSI** → `UiSetFaction` → `POST /api/me/faction`. Sukses → lobby.
- Guest **ikut** memilih (beda dari IMGUI lama yang hanya untuk akun terdaftar).

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
- `POST /api/me/faction {faction:1|2}` (auth): validasi 1/2, **terkunci** bila sudah pilih (409), idempoten bila sama. → `{faction, locked}`.
- `GET /api/factions` (publik): `{orde, legion, needsWarriors:0|1|2, bonusPercent}`.
- `POST /api/admin/faction {playerId, faction:0|1|2, adminSource?}` (header **`X-Admin-Secret`** = `Admin:Secret`; kosong = nonaktif): set/reset faksi **lewati kunci** (0 = reset → pemain pilih lagi · 1 ORDE · 2 LEGION). Untuk akun uji / dukungan sampai sistem season ada.
  - **Constant-time**: secret dibandingkan `SHA256` + `CryptographicOperations.FixedTimeEquals` (`SecretsEqual`), bukan `==`.
  - **Audit WAJIB**: tiap perubahan menulis `FactionAdminAudit` (sumber `adminSource@ip`, `playerId`, faksi **lama→baru**, waktu) + log `AdminFaction`. Respons memuat `previous`.
  - Reset juga **mengembalikan status pindah-gratis** begitu field `FactionSwitchUsed` ada (Tugas 3) — sekarang field belum ada (TODO di kode).
  - ⚠️ **UTANG RILIS**: ganti `X-Admin-Secret` dengan **admin berbasis role di server + audit log resmi** (docs/90, docs/91) sebelum rilis publik.

## OPSI (`Game:*` / `Admin:*`)
`FactionLocked=true` · `FactionMinPopulation=2` · `FactionImbalanceThreshold=0.45` · `FactionJoinBonusPercent=15` · `Admin:Secret=""` (set di env utk aktifkan endpoint admin).

## TES
Backend: `FactionService` (seimbang→tanpa bonus, timpang→minoritas+bonus, di bawah min-pop, akun uji dikecualikan); API (lock+validasi, `/api/factions`, **admin reset lewati kunci + butuh secret**). 68 hijau. Klien: butuh compile editor (tak bisa diuji headless).

## BELUM / NANTI
- **Sistem season** (buka kunci faksi otomatis) — sekarang kunci permanen, reset manual via admin. Faction War (Fase 3). Badge di baris leaderboard (opsional). Bonus selain XP (reward) bila diinginkan.
