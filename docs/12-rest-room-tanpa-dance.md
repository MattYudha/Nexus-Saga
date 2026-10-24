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
