# 00 — CHECKLIST KERJA Nexus Saga (2026-11-13)

> Satu tempat untuk melihat **sudah / belum**. Sumber kebenaran tetap: urutan kerja = `PROGRESS.md`,
> keputusan = `docs/90`, peta milestone = `docs/00-ROADMAP.md`.
> Aturan: **satu item → selesai → dicentang + lapor.** Jangan centang tanpa bukti (file/tes/layar).

Legend: `[x]` selesai · `[ ]` belum · `[!]` diblok (sebut ID) · `[-]` ditunda sengaja · `[X]` dilarang

---

## A. ANTREAN TERKUNCI (PROGRESS) — kerjakan berurut
- [x] **a** Demosi nonaktif + tier konsisten (2026-10-30)
- [x] **b** Deteksi akun uji eksplisit (2026-10-30)
- [x] **c** Faksi ORDE/LEGION + badge + palet (verifikasi editor 2026-11-13)
- [ ] **d** UI Lobby: Settings 1.6 · lobby tidak kosong 1.7 · tombol "Segera Hadir" · slider Ranked/Battle/teaser · tombol Street Room
- [ ] **e** Layar hasil = Detail Match v2 mode `result` (ganti IMGUI)
  - [ ] wiring result → NexusGame
  - [ ] pemicu layar faksi dipindah ke **setelah hasil match pertama** (2b)
- [ ] **f** Tab Statistik baru (ring Flawless, grid mekanik, radar)
- [ ] **g** Kartu Disputed "TIDAK DIHITUNG"
- [!] **h** Fase 2 sosial (presence, chat, teman) — **K-11**
- [ ] **T1** Kunci semantik warna UI — kode ✅, **swatch screenshot** & grep akhir belum
- [ ] **T2** Pulihkan C4 — **kode ada di working tree, MENUNGGU REVIEW + CodeGen** (audit: `t2-spec/02`)
  - [x] hapus bleed-out sebagai jalan KO (`CritTimer`/`CritBleedTicks`)
  - [x] penalti gerak 70/50/35 (dash terkunci sejak Critical) — `NxTuning.cs` + `CritSpeedMul`
  - [x] Overload: 480 tick → lock 90 tick, **tanpa pengali damage**, reset tiap kena pukul/guard
  - [x] bot prioritas Critical/Overload + penalti penumpukan (`BestTarget`)
  - [x] AFK: 15 dtk peringatan / 30 dtk forfeit akumulatif (`TrackActivity`)
  - [ ] indikator posisi Critical + ikon Overload (View/UI — kerja editor)
  - [ ] `koTimeline` — **ditunda**: sintaks array `.qtn` belum terverifikasi
  - [ ] invariant 1v1 hijau + 8 tes baru
  - [ ] review perbaikan (B1–B8) → CodeGen + tes editor user
- [x] **T3** Audit docs + `docs/00-ROADMAP.md`

## B. RISET — SELESAI (2026-11-13)
- [x] `research/ikemen-extract/` — 9 file: input buffer/cancel, juice, guard-dizzy-counter-juggle, replay/anti-desync, hero swap, kamera, `combat-tuning.json`, `07-patch-qtn.md`
- [x] `research/kebutuhan-lostsaga-ayodance.md` — checklist kebutuhan + rujukan bukti
- [x] `research/PROMPT-riset-legal.md` — prompt inisiator + aturan sumber
- [x] `research/backlog-riset-logic.md` — 11 domain
- [x] `research/hero-ability/` — 5 file (skema ability, formula, modifier, kit) · `02`/`03` = **arsip pasca-MVP**
- [x] `research/battle-flow/01-match-lifecycle.md` — lifecycle, timer, draw, putus, rematch
- [x] **rea** dibangun + dipakai ke `PhotonBackend.Api.dll` (evidence `ev_abe8dcae…`)

## C. RISET — BELUM (usul hari ini, berurut)
- [x] **R1** `research/t2-spec/01-rules-and-numbers.md` — aturan & angka T2 (+ temuan: `koTimeline` maks 9 hanya valid untuk 1v1)
- [ ] **R2** `research/realtime-k11.md` — SignalR vs Photon Chat vs Nakama → **membuka h**
- [ ] **R3** `research/guest-upgrade-k10.md` — 3 opsi + migrasi + UU PDP → **membuka 2c**
- [ ] **R4** `research/matchmaking/01-queue-rules.md` — window, region, party MMR, bot fill, anti-smurf
- [ ] **R5** `research/result-payload.md` — kontrak data untuk poin e (tanpa dummy)
- [ ] `research/animation/` · `research/map/` · `research/sound/` · `research/vfx/` — **belum jadi penghalang**, jangan dikerjakan dulu

## C2. QA — TEMUAN TERBUKA (lihat `docs/qa/01-laporan-tester-2026-11-13.md`)
- [ ] **Q1** klien memalsukan skor ke 5-4 (`NexusGame.cs:370`)
- [ ] **Q2** `EndReason`/`WinnerSlot`/`KoTimeline` tidak dikirim klien
- [ ] **Q3** seri dihitung menang
- [ ] **Q5** `KoLog` tetap 9 (butuh 19/29 per mode)
- [ ] **Q8** Overload tidak mematikan guard
- [ ] **Q9** AFK berjalan saat pemain di-combo
- [ ] **Q10** AFK 10/20 (keputusan: 15/30 akumulatif)
- [ ] **Q11** timer 100 dtk belum diputus
- [x] **Q21** separation dist≈0 → didorong deterministik (fix eec328f)
- [x] **Q22** separation saat hitstop (fix eec328f, sisa catatan Q44)
- [ ] **Q26** tahan J = auto-swing (tanpa cooldown)
- [ ] **Q31** rotasi kapsul `-yaw` → arah hadap tercermin
- [x] **Q36** assignment TTL 60 dtk (fix eec328f) → **Q42**: TTL < durasi match 100 dtk
- [ ] **Q43** report tanpa retry → hasil match bisa hilang
- [ ] **Q47** skor tidak ikut dibandingkan antar-klien (verifikasi)
- [ ] **Q48/Q49** RD Glicko tanpa clamp bawah & tanpa inflasi pemain pasif
- [ ] **Q53** FLAWLESS dihitung dari skor lawan 0 (menang waktu/WO ikut terhitung)
- [ ] **Q55** basis statistik tidak seragam antar format
- [ ] **Q56** radar memuat seluruh riwayat per request
- [ ] **Q60** `deviceId` per-launch → guest baru tiap buka game (S1)
- [ ] **Q61** tidak ada rate limit login/guest
- [ ] **Q62** `/auth/upgrade` tidak cek deviceId
- [ ] **Q63** DisplayName bebas pada upgrade (impersonasi)
- [ ] **Q67/Q68** cache faksi per-instance + populasi guest
- [ ] **Q71/Q72** papan: hitungan match vs draw & placement tanpa validasi hasil
- [ ] **Q79** `AuthSecret` kosong = auth Photon terbuka (guard satu baris)
- [ ] **Q80** tanpa `UseForwardedHeaders` → limit per-IP salah di belakang proxy
- [ ] **Q81/Q83** limit per akun + batas pembuatan guest
- [ ] **Q86** homoglyph Cyrillic lolos larangan nama staf (S2)
- [ ] **Q87** NFKC: nama lebar penuh/aksen lolos keunikan
- [x] **Q90** fallback nama guest terbatas
- [ ] **Q91** race nama guest → 500 (S2)
- [ ] **Q93** `/me` vs papan: definisi match/win rate berbeda
- [ ] **Q94** bukti guard klik ganda
- [ ] **Q76** QuickMatch `async void` tanpa penjaga klik ganda

## C3. STATUS IMPLEMENTASI 2026-11-13 (kode selesai, BELUM dites editor)
**Klien (Quantum)**
- [x] T2: bleed-out dihapus, AFK 15/30 dtk, Overload 480/90 (tanpa pengali), penalti 70/50/35 + dash lock, bot prioritas, `koTimeline` 9, timer 100 dtk (`NxMatch.cs`, `NxTuning.cs`)
- [x] Poin d: lobby Settings 5 tab, pengumuman, hero terakhir, tombol "Segera Hadir", slider 3 mode, Street Room
- [x] Poin e: layar hasil Detail Match v2 (mode result) + pemicu faksi setelah match pertama
- [x] NX-12 sisa: ikon badge + ikon baris statistik (4 badge + 8 statistik)
- [x] NX-21/NX-22: kartu Disputed + tab Hero Favorit (UI)

**Backend (126 tes hijau, live)**
- [x] D12 RD policy (`RdMin=30`, inflasi 7 hari, `LastRatedAt`)
- [x] D13 dasar badge (`BadgeFmt` + `KoFinish`)
- [x] D14 nama unik case-insensitive + reserved (homoglyph/NFKC di `3062696`)
- [x] D15 rate limit 15/mnt; lockout username; kuota guest global 300/mnt
- [x] NX-21 alasan Disputed tersimpan; NX-22 `/api/me/heroes`
- [ ] **Tes editor M1 (NX-12..NX-16) — satu-satunya penghalang**

**QA terbuka**
- [ ] **Q92** papan: `Matches` vs `WinRate` beda basis
- [ ] **Q93** `/me` vs papan: definisi match/win rate berbeda
- [ ] **Q94** bukti guard klik ganda
- [ ] **Q86/Q87/Q89/Q91** sudah diperbaiki di `3062696` → **perlu verifikasi ulang tester**
- [ ] **NX-R3** JWT `jti` + revokasi (utang rilis)
- [ ] **Keamanan:** `appsettings.Development.json` ter-track berisi JWT/webhook/auth secret asli → rotasi + pindah ke user-secrets

## D. KEPUTUSAN MENUNGGU USER (memblokir)
- [ ] **K-09** Format Squad War (usul: rebut distrik)
- [ ] **K-10** Guest → akun (usul: upgrade in-place)
- [ ] **K-11** Realtime Fase 2 (usul: SignalR)
- [ ] **K-12** Papan poin Survival (boleh ditunda)
- [ ] **T2-AFK** angka final forfeit
- [ ] **BF-1** Timer Ranked: tanpa / 300 dtk / 240 dtk
- [ ] **BF-2** Waktu habis seri: DRAW / sudden death 30 dtk / damage terbanyak
- [ ] **BF-3** Grace disconnect: 20 dtk / 45 dtk / batal
- [ ] **BF-4** Pause: tidak ada / 1×30 dtk casual
- [ ] **BF-5** Rematch: casual saja / semua mode
- [ ] **HA-1** Angka kit di `hero-ability/04` (final setelah T2 + playtest)

## E. UTANG RILIS (wajib sebelum publik)
- [ ] Admin berbasis role (ganti `X-Admin-Secret`) — docs/91 #10
- [ ] Aktifkan kembali proteksi demosi (`grace=3`) — docs/33
- [ ] PSE Kominfo · IGRS · UU PDP · ToS/privacy · cek merek "Nexus Saga"

## F. DILARANG (jangan diusulkan lagi)
- [X] Ekstrak model/tekstur/audio/logic dari client LostSaga/AyoDance
- [X] Bongkar Xigncode/VAC/EAC/packer apa pun
- [X] Pakai source bocor atau private server
- [X] Mode dance/ritme (docs/12 — arsip)

---

## G. CARA PAKAI (biar tidak berantakan)
1. Ambil **satu** item dari **A** (atau **C** kalau A sedang diblok).
2. Kerjakan → lapor bukti (file / baris tes / layar) → **baru** centang.
3. Kalau item butuh keputusan, pindahkan ke **D** dan hentikan item itu — jangan dikerjakan setengah.
4. Riset tidak boleh menyentuh kode (`.qtn`, `.cs`, scene). Field `.qtn` hanya lewat T2.
5. Setiap selesai: catat 1 baris di `PROGRESS.md` + keputusan di `docs/90` bila mengubah arah.
