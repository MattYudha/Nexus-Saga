# BOARD — Nexus Saga: Chronicles (checklist kerja ala Jira)

> **Ini papan kerja harian.** `PROGRESS.md` = urutan terkunci + log · `docs/00-ROADMAP.md` = peta & konflik ·
> `BOARD.md` (file ini) = **tiket yang dicentang**. Diperbarui setiap tiket berubah status.
> Status: ✅ selesai (ada di kode + diverifikasi) · ❌ belum · ⏳ sedang dikerjakan · 🚫 diblok (sebut pemblokir) · ❓ butuh keputusan user
> Terakhir diaudit terhadap kode: **2026-11-13** (grep `photon-backend` @ `9706ec8`).

<!-- FOCUS:START -->
## 🎯 FOKUS SEKARANG (WIP = 1)
**M1 alur inti LULUS tes editor (user 2026-11-16): NX-12 combat, NX-14 hasil, NX-15 faksi, NX-16 upgrade.** Backend 135 tes hijau (Claude-run).
Sisa M1: **NX-13 lobby** — fungsional (dilalui saat tes), tapi sedang **di-redesign** (NX-IN-LOBBY poin 1b/2/4) + **ranked-tanpa-bot ✅ kode** (PlayerCount 2/3/10, tanpa CodeGen) + **practice statistik tanpa DB ✅ kode** — menunggu tes editor.
Pilihan user untuk langkah berikut: (a) ranked-no-bot flag · (b) lanjut redesign lobby (loop screenshot) · (c) mulai M2 (NX-20 stats / NX-21 Disputed / NX-22 Hero Favorit — kode M2 sudah ada, perlu tes editor).
**Kerjaan baru → INBOX dulu** kecuali user menulis `OVERRIDE`.
<!-- FOCUS:END -->

## 🌅 RENCANA BESOK (2026-11-17) — urut prioritas
> Claude tak bisa screenshot/compile Unity → user jadi "mata". Backend bisa di-tes Claude (saat ini 135/126 hijau).
> Semua kode hari ini sudah di-push ke **mine = MattYudha/Nexuws-Backend** (BE) & **MattYudha/Nexus-Saga** (docs).

### A. VERIFIKASI dulu (tuntaskan yang menggantung) — butuh editor
- [ ] A1 Aim-assist PULSE: hadap menjauh → tembak → peluru ke bot (360°, range 22). Tuning di `NxTuning` bila perlu.
- [ ] A2 Practice Result: statistik benar (Kills+BotKills, skor per-tim) + layout = template ranked + elemen ranked (tier/ladder/MatchID/JALANNYA MATCH) tersembunyi + "Latihan tidak memengaruhi rating".
- [ ] A3 Ranked tanpa bot: 2 klien (editor + `game.exe -nxprofile 2`) → murni 1v1, nol bot.

### B. NX-13 / NX-IN-LOBBY — redesign lobby (loop screenshot: Claude edit → user screenshot → ulang)
- [ ] B1 (poin 1b) Ganti slider jadi 3 kartu mode: RANKED (ikon rank+W/L), QUICK MATCH, CUSTOM ROOM. Tombol MAIN di bawah.
- [ ] B2 (poin 2) Layar HERO SELECT baru: model besar tengah, grid hero, slot tim kiri/kanan, timer + LOCK IN.
- [ ] B3 (poin 4) Rapikan: HQ/Plaza/Street → sidebar kiri; chat lebih tinggi; Friends auto-tinggi; hapus gear duplikat; Squad(party) vs Guild(bottom nav); currency ikon+tooltip.
- [ ] B4 (poin 3b) Placeholder ikon bersih (kotak/lingkaran huruf) untuk fitur "Segera".

### C. M2 (kode sudah ada → tinggal TES EDITOR)
- [ ] C1 NX-21 kartu Disputed "TIDAK DIHITUNG".
- [ ] C2 NX-20 tab Statistik (ring Flawless, grid mekanik, radar).
- [ ] C3 NX-22 tab Hero Favorit.

### D. Utang rilis (jangan lupa)
- [ ] D1 Rotasi secret di `appsettings.Development.json` (JWT/webhook/auth) + pindah ke .env/user-secrets — ikut ter-push.
- [ ] D2 NX-R3: JWT `jti` + revokasi (logout semua perangkat).

**Mulai dari A (cepat, menutup yang menggantung), lalu pilih B atau C.**


---

## 🔒 ATURAN FOKUS (gate wajib — berlaku untuk manusia & AI)
1. **WIP = 1.** Hanya satu tiket ⏳ pada satu waktu = tiket di 🎯 FOKUS.
2. **Mandatori dulu.** Tiket epic **M1** harus ✅ semua sebelum tiket M2/INBOX mulai dikerjakan.
3. **Ide/permintaan baru → INBOX**, beri ID `NX-IN-xx`, **tidak dikerjakan**. Pengecualian hanya bila user
   menulis **`OVERRIDE`** (dicatat di LOG + `docs/90` dengan alasannya).
4. **Riset hanya untuk tiket aktif.** Riset domain lain = INBOX. Riset tidak menyentuh kode.
5. **Definisi selesai (DoD):** semua sub-tugas ✅ + tes hijau (backend) / tes editor user (klien) + docs
   diperbarui + lapor ke user → baru tiket di-✅ dan 🎯 FOKUS pindah ke tiket berikutnya.
6. **Tiket ❓ menunggu user** tidak ditebak. Kerjakan sub-tugas yang tidak bergantung, sisanya tunggu.
7. **Bug yang ditemukan saat kerja:** bila merusak tiket aktif → sub-tugas tiket aktif; bila tidak → INBOX.

---

## EPIC M1 — "Ranked 1v1 end-to-end" (MANDATORI)
Login → lobby → ruang ladder → match ranked 1v1 → layar hasil UITK → riwayat & leaderboard konsisten.

### Selesai
| ID | Tiket | Status | Bukti |
|---|---|---|---|
| NX-01 | Login akun + guest, JWT, profil | ✅ | docs/26 |
| NX-02 | Faksi ORDE/LEGION: onboarding, `POST /me/faction`, badge, palet, admin + audit (poin c) | ✅ | editor 2026-11-13, docs/35 |
| NX-03 | Pindah faksi gratis 1× selama placement <5 (`FactionSwitchUsed`) | ✅ | `114216a`, 4 tes |
| NX-04 | Ruang ladder + papan + baris saya | ✅ | docs/27, 33 |
| NX-05 | Match Ranked 1v1 first-to-5 KO, Glicko-2, invariant kills A = deaths B | ✅ | docs/32 |
| NX-06 | Riwayat + Detail Match v2 (mode history) | ✅ | `17b815b`, editor 2026-11-13 |
| NX-07 | Leaderboard: tier rating asli, urut tier → conservative → WR → match | ✅ | `114216a`, tes Gladiator/Rival |
| NX-08 | Semantik warna UI (T1) | ✅ | editor 2026-11-13 |
| NX-09 | Proteksi demosi nonaktif + akun uji eksplisit (poin a, b) | ✅ | docs/33 |
| NX-10 | Audit docs → ROADMAP + Guild→Squad (T3) | ✅ | `69b5afe`, `9706ec8` |

### Belum
#### NX-11 ✅ Keputusan user untuk T2 (prasyarat NX-12) — diputus 2026-11-13
- ✅ AFK = disconnect: **20 dtk tanpa input/terputus → forfeit** (satu angka untuk keduanya)
- ✅ Timer Ranked: **100 dtk** (user; catatan: ~20 dtk/KO → banyak match berakhir karena waktu; nilai di config)
- ✅ Waktu habis & skor KO seri → tie-break: (a) **gear rontok terbanyak kalah** → (b) **darah tersisa paling sedikit kalah** → (c) masih sama = DRAW tanpa rating — **dikonfirmasi user**
<sub>Sumber: `docs/research/battle-flow/01-match-lifecycle.md` §6; keputusan di docs/90 2026-11-13.</sub>

#### NX-12 ⏳ T2 — Pulihkan C4 (KO hanya 3 Break Stock) — kode+backend ✅ (135 tes), **blok A combat DONE (user 2026-11-16)**; sisa: cek koTimeline 2-klien
Legend sub-tugas di sini: ✅ = kode ada + **ter-compile** (CodeGen headless identik Unity + compile 3 assembly) · 🧪 = perlu dibuktikan di editor.
- ✅🧪 Bleed-out dihapus (`CritTimer`/`CritBleedTicks`/`LastHitBy*` dibuang) — KO hanya 3 Break Stock
- ✅🧪 Penalti gerak 70% → 50% → 35%; dash **dan lunge TITAN** dikunci saat Critical
- ✅🧪 Indikator Critical lawan (penanda merah / panah tepi layar, `NexusView`)
- ✅🧪 Overload 8 dtk → terkunci 1,5 dtk (guard lepas, rentan, bukan KO, reset saat kena/guard)
- ✅🧪 Bot prioritas Critical/Overload (+ hitung penumpukan tanpa dirinya sendiri)
- ✅🧪 Batas waktu **100 dtk** + tie-break gear rontok → darah → SERI (`NxMatch.cs`) + timer HUD
- ✅🧪 AFK/disconnect **75 dtk** berturut-turut → forfeit (peringatan HUD 60 dtk) — keputusan user 2026-11-16 (>1 mnt); skor tidak dipalsukan; respawn tidak mereset AFK
- ✅🧪 `koTimeline` (array `.qtn` ≤9) → dilaporkan → disimpan per match → dibandingkan antar-klien
- ✅🧪 Tab "Jalannya Match" + label SERI/Waktu habis/WO di Riwayat & Detail Match v2
- ✅ Backend: `endReason`/`winnerSlot`/`koTimeline`, seri tanpa rating, migrasi `AddMatchEndReason` **live** (`ef5b095`), **84 tes hijau**
- ✅ Nilai di `NxTuning.cs` (satu tempat)
- ✅ Docs: docs/32 (§C4 + akhir match) + docs/90; **K-03 ditutup** (menunggu tes)
- ✅ CodeGen: file `Generated/` sudah diperbarui (identik byte dengan CodeGen Unity) → user **tidak wajib** CodeGen manual
- ✅ **Triase laporan tester Q1–Q41** (`docs/qa/03-triase-dan-fix-2026-11-13.md`): fix Q4 durasi dari tick, Q21/Q22 separation, Q31 rotasi, Q15 guard TickRate, Q18 WinnerTeam awal, **Q36/Q37 matchmaking TTL** (klien crash tak lagi terkunci; pemain hantu dibuang) — backend **87 tes**. Q1–Q3/Q7/Q8/Q32 basi (sudah benar di `83c98e0`)
- ✅ QA pass 3 (`docs/qa/05-…`): Q42 TTL assignment 180 dtk, **Q43 retry laporan hasil** + pesan bila gagal, Q44 separation hitstop berdua
- ✅ QA pass 4 (`docs/qa/06-…`): **Q53 FLAWLESS hanya menang KO** (backend+klien), 91 tes; Q48/Q49/Q51/Q55 → keputusan D12/D13
- ❌ Tes simulasi otomatis (Critical 30 dtk, Overload, skor tetap) — **belum ada harness Quantum headless**; diganti checklist editor di bawah
- ✅🧪 Ikon per-badge (FLAWLESS emas, COMEBACK, FIRST BLOOD, PARTY) + ikon 9 baris statistik Detail Match — 12 sprite baru `Sprites/ic_b_*` & `ic_s_*` (glyph putih, diwarnai via tint token)
- 🧪 Tes editor user — checklist:
  1. Console bersih setelah Unity import (tanpa error compile)
  2. Ranked/practice 1v1: gerak/guard/hit/KO normal; timer 1:40 turun di atas layar
  3. Lawan Critical tak disentuh 30 dtk → **tidak KO**; tiap 8 dtk muncul OVERLOAD 1,5 dtk; skor tetap
  4. Saat Critical: kecepatan turun per stock; Shift (dash) & K TITAN tidak jalan
  5. Diam 10 dtk → peringatan AFK; 20 dtk → match selesai "AFK — WO", lawan menang
  6. Biarkan waktu habis → "WAKTU HABIS — … MENANG/SERI"; Riwayat menampilkan label + tab **Jalannya Match** berisi urutan KO
  7. Practice vs bot: bot mengejar target Critical

  → **Runbook gabungan NX-12..NX-16 (sekali duduk): `docs/qa/12-runbook-tes-editor-M1.md`**

#### NX-12b ⏳ PRACTICE mode (user 2026-11-16) — kode selesai, **menunggu tes editor**
- ✅ Tombol **PRACTICE** di slider lobby (mode ke-3, "MULAI") → `NexusGame.UiPractice()`
- ✅ `StartPracticeAsync`: sesi Quantum **Local** (offline, tanpa Photon/backend), `PlayerCount=2` → 1 pemain + bot isi lawan
- ✅ Hasil match practice **tidak dilaporkan** (rating tak berubah) — guard di `Update()` saat `State==2`
- ✅🧪 Hanya recompile (tak ada `.qtn` berubah → tanpa CodeGen). Butuh tes editor: tombol → pilih hero → lawan bot

#### NX-13 ⏳ Poin d — UI Lobby — kode selesai, **menunggu tes editor** (ditumpuk di atas NX-12 atas permintaan user)
- ✅🧪 Settings 1.6: 5 tab (Grafis: resolusi/mode layar/VSync/batas FPS/kualitas · Audio: volume utama + bisu · Kontrol: daftar tombol · Antarmuka: tampil FPS · Akun: nama/akun/ID+salin/daftar akun/Logout), simpan PlayerPrefs, langsung diterapkan (`NexusSettings.cs`); Esc menutup. Musik/SFX terpisah, rebinding, ping, sosial = SEGERA HADIR
- ✅🧪 Lobby 1.7: hero terakhir dimainkan di tengah (default TITAN-01)
- ✅ Backend `/api/announcements` live
- ✅🧪 Lobby 1.7: panel Pengumuman kiri-atas — kosong → "Belum ada pengumuman", gagal → "Gagal memuat" (juga Q45)
- ✅🧪 Shop, Inventory, Hero Deck, Quest, Event, Squad, Mail, HQ, Plaza → nonaktif + tag SEGERA HADIR; tombol "+" mata uang disembunyikan
- ✅🧪 Slider = RANKED / BATTLE / teaser "FACTION WAR · NEXUS CUP" (MAIN nonaktif "SEGERA HADIR"), 3 titik
- ✅🧪 Tombol STREET (Street Room) di samping HQ/Plaza — SEGERA HADIR (room browser = NX-28)
- ✅ Bugfix T2: `SimVersion` dinaikkan ke `nx-sim-2026-11-13-t2` (klien + backend `RequiredSimVersion`, live) — build lama tak bisa dipasangkan dengan build T2
- 🧪 Tes editor: buka Settings → ubah tiap opsi (VSync/FPS/kualitas/volume langsung berubah; restart → tetap); tab Akun (guest) → daftar akun; lobby menampilkan pengumuman & hero; tombol SEGERA HADIR tidak bisa diklik; slider 3 mode

#### NX-14 ✅ Poin e — Layar hasil pasca-match — **LULUS tes editor (user 2026-11-16): statistik match muncul**
- ✅🧪 Selesai match → laporan → banner akhir ~1,5 dtk → keluar room → halaman **Result** (`NexusGame.Page.Result`)
- ✅🧪 `ProfileController` mencari match di Riwayat (coba ulang 1 dtk, maks 15 dtk, karena lawan mungkin belum melapor) → **Detail Match v2 `DetailMode.Result`** (animasi Poin Ladder, "NAIK TIER!", tombol LANJUT/Enter/Esc → lobby)
- ✅🧪 Tak ketemu (belum tercatat / Disputed / server mati) → ringkasan teks + alasan jujur + LANJUT
- ✅ Kotak hasil IMGUI tidak dipakai lagi saat `UseNewProfile` (aktif di `NexusOnline.unity`)

#### NX-15 ✅ Pemicu layar faksi → setelah hasil match pertama — **LULUS tes editor (user 2026-11-16)**
- ✅🧪 `NeedsFaction` = belum berfaksi **dan** sudah pernah menyelesaikan match (`MatchesPlayed > 0` atau baru selesai match di sesi ini). Pemain baru langsung ke lobby; layar faksi muncul setelah LANJUT dari hasil match pertama. Layar + backend dipakai ulang

#### NX-16 ✅ Guest → daftar akun membawa faksi/rating/riwayat (**K-10**) — **LULUS tes editor (user 2026-11-16)**
- ✅ Keputusan: opsi (a) endpoint upgrade (2026-11-13)
- ✅ Backend `POST /api/auth/upgrade`: Player sama, faksi/rating/riwayat terbawa, deviceId dilepas, akun terdaftar → 409 — 2 tes (**90 hijau**), live & diuji di server
- ✅🧪 UI: "Daftarkan akun" di Settings › Akun (hanya untuk guest) — menunggu tes editor

---

## EPIC M2 — Setelah milestone (ANTRE — jangan mulai sebelum M1 ✅)
| ID | Tiket | Status | Catatan |
|---|---|---|---|
| NX-20 | Poin f — UI Tab Statistik baru (ring Flawless, grid mekanik, radar) | ❌ | backend radar sudah ada (`StatsEndpoints.cs`) |
| NX-21 | Poin g — kartu Disputed "TIDAK DIHITUNG" di UI | ⏳ kode selesai, menunggu tes editor | `DisputeReason` (mismatch/sanity/invariant) + `/api/matches?includeDisputed=true` → kartu abu + alasan di Riwayat & layar hasil; statistik/papan tak berubah |
| NX-22 | 1.4 Tab Hero Favorit (agregasi per hero) | ⏳ kode selesai, menunggu tes editor | `GET /api/me/heroes` (per hero dominan; ranked1v1+battle; K/D hanya ranked1v1; menit main) + grid kartu hero + hero teratas di tab Profil; 126 tes |
| NX-23 | Poin h — Fase 2: presence, chat ALL/PARTY/SQUAD/ROOM, teman | 🚫 | **K-11** stack realtime |
| NX-24 | Fase 3 — Party | ❌ | docs/29 |
| NX-25 | Fase 4 — Squad | 🚫 | **K-09** format Squad War |
| NX-26 | Fase 5 — Mail | ❌ | docs/31 |
| NX-27 | Battle 3v3 santai (bot isi slot) | ❌ | docs/24 §10a |
| NX-28 | Street Room — room browser 1v1–3v3 | ❌ | tombolnya di NX-13 |
| NX-29 | Survival 1v1/3v3 | 🚫 | **K-12** papan poin |
| NX-30 | Faction War / Nexus Cup 5v5 | ❌ | Fase 3+ |

## EPIC R — Utang wajib sebelum rilis
| ID | Tiket | Status |
|---|---|---|
| NX-R1 | Admin berbasis role (ganti `X-Admin-Secret`) — docs/91 #10 | ❌ |
| NX-R3 | JWT: jti + revokasi ("logout semua perangkat"), cek audience/umur token (Q64) | ❌ |
| NX-R2 | Aktifkan kembali proteksi demosi `grace=3` — docs/33 | ❌ |

---

## ❓ KEPUTUSAN MENUNGGU USER
| # | Keputusan | Menghambat | Usul |
|---|---|---|---|
| D1 | ~~Ambang AFK/disconnect~~ | NX-12 | ✅ **75 dtk → forfeit** (user 2026-11-16, >1 mnt; was 20) |
| D2 | ~~Timer Ranked~~ | NX-12 | ✅ **100 dtk** (2026-11-13) |
| D3 | ~~Waktu habis seri~~ | NX-12 | ✅ **gear rontok → darah → DRAW** (2026-11-13) |
| D4 | ~~K-10 guest → akun~~ | NX-16 | ✅ **endpoint upgrade** (2026-11-13) |
| D5 | ~~Posisi Hero Favorit~~ | NX-22 | ✅ dikerjakan setelah NX-14 (OVERRIDE M2) |
| D6 | Model juggle (S1 vs per-penyerang) | tuning combat | S1 |
| D7 | K-09 format Squad War | NX-25 | rebut distrik |
| D8 | K-11 stack realtime | NX-23 | SignalR |
| D9 | K-12 papan Survival | NX-29 | tunda |
| D10 | Pause & rematch (battle-flow §6 #4–5) | M2 | tanpa pause Ranked; rematch casual saja |
| D11 | Effekseer vs VFX bawaan Unity | fase aset | tunda |
| D12 | ~~Glicko RD~~ | kualitas leaderboard | ✅ **lantai 30, inflasi per 7 hari maks 350, RD tak turun saat anti-kolusi** (2026-11-13, live) |
| D13 | ~~Basis badge~~ | statistik | ✅ **ranked1v1 + battle; K/D tetap ranked1v1; format lama tanpa badge** (2026-11-13, live) |
| D14 | ~~Nama tampil~~ | impersonasi | ✅ **unik case-insensitive + nama terlarang (admin/GM/staff/…)**; guest bentrok → nama Guest lain otomatis (2026-11-13, live) |
| D15 | ~~Batas rate limit~~ | Q61 | ✅ **15/menit per IP** (auth & guest), bisa diubah via konfigurasi (2026-11-13, live) |

---

## 📥 INBOX (ide/permintaan baru — TIDAK dikerjakan sampai M1 ✅)

| NX-IN-TOOL | **Besty Unity-Skills** (REST localhost:8090, MIT, editor-only) = jembatan Claude⇄Unity: baca error compile + screenshot + recompile sendiri → hapus friksi "tak bisa lihat Unity". Pasang ke `game/Packages/` + Window>UnitySkills server ON. Unity-Tech/skills = rujukan (ui-uitk, localize). Analisis: docs/research/unity-skills-analysis.md | user 2026-11-17 |

| NX-IN-ASSET | **Pipeline aset = main core** (keputusan user 2026-11-17): Blender MCP (model 3D) + unity-mcp CoplayDev (otomasi Unity, MCP-native, v10 asset-gen). Legal/orisinal. Aktif = setup + buka app + restart Claude. Besty = cadangan. Detail: docs/research/asset-pipeline-mcp.md; memory nexus-modeling-pipeline | user 2026-11-17 || NX-IN-LOBBY | Redesign lobby (user 2026-11-16, butuh loop screenshot — Claude tak bisa screenshot Unity): **1** hapus hero tengah (✅1a) → 3 kartu mode (RANKED+rank/WL, QUICK, CUSTOM ROOM) + MAIN; **2** layar Hero Select baru (model besar, grid, slot tim kiri/kanan, timer, LOCK IN); **3** ikon SEGERA HADIR overflow (✅ badge pojok) + placeholder ikon bersih; **4** HQ/Plaza/Street ke sidebar, chat lebih tinggi, Friends auto-tinggi, hapus gear duplikat, Squad vs Guild, currency ikon+tooltip | user 2026-11-16 |
| NX-IN-ART | ✅ kode selesai (2026-11-16): art user dipasang di hero_titan/pulse.png + Resources; HeroCard (potret+skill) di NexusView — **menunggu tes editor** | user 2026-11-16 || ID | Isi | Asal |
|---|---|---|
| NX-IN-01 | Riset domain lain di `docs/research/backlog-riset-logic.md` (room, matchmaking, animasi, map, sound, VFX, ekonomi) | backlog riset |
| NX-IN-02 | Input buffer/cancel/juice dari `ikemen-extract` → implementasi (draf `07-patch-qtn.md` ditahan) | riset Ikemen |
| NX-IN-03 | Kit hero data-driven (`hero-ability/04`), ultimate, modifier | riset hero-ability |
| NX-IN-04 | Replay, spectator, killcam | riset Ikemen 04 |
| NX-IN-06 | Desain serangan: tahan J = ayunan terus (Q26) → recovery/cooldown serang per hero | QA Q26 |
| NX-IN-07 | Pushbox per hero + separation simetris + kecualikan respawn (Q23–Q25) | QA |
| NX-IN-08 | Input: aim (AimYaw), gamepad/touch, ambang analog, PendingPick per pemain (Q27–Q30) | QA |
| NX-IN-09 | KoTarget per mode + KoLog lebih besar saat Battle 3v3 (Q16, Q5) | QA |
| NX-IN-10 | Matchmaking multi-replika (store bersama) + pesan error region kosong (Q39, Q40) | QA |
| NX-IN-11 | UI: bedakan "gagal memuat" vs "kosong" saat respons server error (Q45) — kerjakan bersama NX-13 | QA Q45 |
| NX-IN-12 | Radar: cache agregat populasi + desain sumbu ketahanan (Q56, Q58) — bersama poin f | QA |
| NX-IN-05 | **Mode Deathmatch ala LostSaga** (tafsiran dikoreksi user): waktu habis → **darah semua jadi 0**; setelah itu tiap pukulan **merontokkan gear satu per satu** (kepala, aksesoris, baju, senjata, dst). Pemain yang **gear-nya habis duluan kalah**. Mirip mekanik Break Stock kita | user 2026-11-13 |

---

## LOG BOARD
- 2026-11-13: BOARD dibuat dari audit PROGRESS + docs/31 + ROADMAP + grep kode. Fokus = NX-12 (T2).
- 2026-11-13: **OVERRIDE oleh user** ("sembari implement di atas"): M2 dimulai sebelum tes editor M1 lolos — alasan: seluruh kode M1 selesai & menunggu tes. Dimulai NX-21.
- 2026-11-13: NX-11 ✅. NX-12 kode selesai (lanjutan kode sesi DeepSeek + 5 bug diperbaiki + timer/tie-break/koTimeline/HUD/Riwayat), backend live, 84 tes; menunggu tes editor.
