# 12 — Rest Room Tanpa Dance (2026-10-24)

## Keputusan
**Nexus Saga TIDAK memakai mode dance/ritme.** Dihapus dari desain.

### Alasan (dari pemilik proyek, divalidasi)
1. **Copyright musik.** Mode ritme menuntut katalog lagu. Lisensi musik komersial rumit, mahal, dan berisiko hukum. Ini alasan utama.
2. **Biaya produksi.** Mode ritme butuh pipeline chart/not per lagu (AyoDance: tabel 1.791 gerakan + ratusan chart) — beban besar untuk tim solo.
3. **Fokus identitas.** Nexus Saga adalah **brawler**. Rest Room cukup jadi ruang sosial + hiburan ringan, tanpa menjadi "game kedua".

> Catatan teknis (bukan pembatal): secara teknis mode ritme bisa pakai musik original/royalty-free untuk menghindari lisensi. Tapi keputusan tetap **tanpa dance**, karena poin 2 & 3 juga berlaku. Riset ritme AyoDance tetap disimpan sebagai arsip, tidak dipakai untuk fitur.

## Masalah yang harus diisi penggantinya
Dance di AyoDance bukan sekadar minigame — ia **mesin pamer avatar** yang mendorong pembelian kosmetik. Menghapus dance berarti kita wajib punya cara lain untuk "pamer kostum", karena itulah inti monetisasi kita.

## Pengganti Rest Room (semua tanpa musik berlisensi)

### A. Mesin "pamer avatar" (menggantikan fungsi sosial dance)
| Fitur | Cara kerja | Kenapa cocok |
|---|---|---|
| **Fashion Contest / Catwalk** | Pemain tampil bergiliran di panggung dengan outfit-nya; penonton **voting** (bukan juri musik). Pemenang dapat Gold + badge musiman | Langsung mendorong ekonomi kosmetik — tujuan utama. Tanpa musik/chart |
| **Photo Booth / Studio** | Pose + emote + latar + filter; foto bisa disimpan/dibagikan di profil (ide dari AyoDance PhotoStudio) | Pamer avatar, konten sosial, murah dibuat |
| **Emote & pose** | Set emote (kosmetik, bisa dijual MiCash) | Ekspresi sosial tanpa minigame |

### B. Minigame ringan (hiburan + Gold kecil)
| Minigame | Teknologi | Reuse |
|---|---|---|
| **Fishing** | Minigame timing sederhana | Baru, kecil |
| **Kuis komunitas / Trivia** | Berbasis teks + timer, soal dari data server | Hampir nol aset |
| **Training Grounds / Combo Trial** | Pukul dummy, time-trial combo, parkour | **Reuse Combat Core** — gratis secara teknologi |
| **Target Range** | Tembak target dengan skill proyektil | **Reuse hitbox/proyektil Core** |
| **Brawl Ball (mini-sport)** | Dorong bola ke gawang pakai gerak + knockback | **Reuse physics Core** |

**Prioritas MVP/awal:** Fashion Contest (A) + Fishing + Kuis. Training Grounds menyusul karena butuh Combat Core jadi dulu.

### C. Ruang sosial murni
Rest Room tetap: chat lokal, hangout, couple room 18+ (verifikasi umur, block/report/mute). Tidak berubah.

## Dampak ke dokumen lain
- `01`, `04`, `11`: ganti "Dance Duel/ritme" → Fashion Contest + minigame non-dance.
- Riset ritme AyoDance (`ayodance-social-lobby-rhythm.md §C`) = **arsip**, bukan fitur.
- `4-key/8-key` dan "level = panjang urutan panah" **dibatalkan** sebagai fitur kita.
- Kapasitas room 6+30 penonton tetap berguna untuk **Fashion Contest** (6 tampil / 30 nonton & vote).

---

## Brainstorm v2 — referensi hub sosial (2026-10-24)

Insight pengarah: **ruang berkumpul = panggung pamer terbaik**. Di game komunitas (Splatoon, Tower Unite, Deep Rock, Monster Hunter), kosmetik dinilai organik saat pemain nongkrong/antre, bukan di panggung formal. Jadi Plaza + titik kumpul sudah separuh pekerjaan; Fashion Contest adalah versi aktif/berhadiahnya.

### Filter keputusan
| Fitur | Referensi | Status | Alasan |
|---|---|---|---|
| **Hub pasif** (api unggun, air mancur, titik kumpul, emote duduk) | Sky, LifeAfter, Tower Unite | ✅ Adopsi | Pamer avatar organik; murah; pamer Back/Wing saat duduk |
| **Lobby Chase / Tag / Petak umpet** (parkour vertikal) | Garry's Mod Prophunt, Roblox | ✅ Adopsi (prioritas) | **Reuse gerak+collision Core**; kostum/sayap menonjol saat lari/panjat |
| **Brawl Ball / Giga Ball** di tengah Plaza | Rocket League, lobby Destiny | ✅ Adopsi | **Reuse physics Core**; seru, netral |
| **Arcade Lounge** (biliar, dart, basket, arcade cabinet skill) | Tower Unite | ✅ Adopsi — **TANPA judi** | Avatar terlihat dekat saat main bareng; interaksi intens |
| **Casino / slot / poker / meja taruhan** | GTA Diamond Casino | ❌ **TOLAK** | Simulated gambling menaikkan rating toko (sering 17+) walau pakai Gold; risiko regulasi; langgar target 13+ & pilar non-judi |
| **Campfire + masak buff EXP** | LifeAfter | ⚠️ Adopsi bersyarat | Buff hanya **XP profil (non-kompetitif)**; dilarang menyentuh combat/Gold kompetitif/MMR |
| **Mount Racing** (hoverboard/skateboard kosmetik) | MapleStory 2, Tower Unite | ⏳ Tunda Fase 3+ | Scope besar (kategori mount + physics kendaraan). Mount **wajib nol stat**; balapan dinilai skill, reward kosmetik |

### Prioritas build (termurah dulu, reuse Core)
1. Hub pasif + emote (Fase 2, bareng Plaza)
2. Lobby Chase/Tag, Brawl Ball, Target Range (Fase 2–3, reuse Core)
3. Fishing, Photo Booth (Fase 3) — Fashion Contest DIHAPUS (doc 24)
4. Arcade Lounge non-judi (Fase 3)
5. Mount Racing (Fase 3+)

### Catatan tone
Tujuan tone: **netral/universal**, tidak terkesan satu gender. Aktivitas berbasis gerak 3D (chase, ball, race, arcade) memenuhi ini sekaligus memaksa avatar bergerak di layar depan → pamer kostom maksimal.

### Kategori kosmetik baru yang dikonfirmasi dari brainstorm ini
- **Mount/kendaraan ringan** (nol stat) — kategori wardrobe baru, Fase 3+.
- **Emote duduk / animasi hangout** (nol stat) — jual via MiCash.
- **Efek pijakan (footstep/aura)** — pengganti "Platform/DJ Booth" AyoDance.

