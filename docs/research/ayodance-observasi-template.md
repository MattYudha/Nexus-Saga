# Template Observasi Manual — AyoDance (untuk desain Nexus Saga)

> **Cara pakai:** buka AyoDance dengan akun Anda sendiri (ini legal — observasi gameplay biasa, bukan membobol proteksi), lalu isi kolom kosong di bawah. Boleh screenshot. Setelah terisi, kirim ke Claude untuk dirapikan menjadi dokumen riset final.
>
> **Yang TIDAK perlu dicatat:** nama ratusan item satu per satu. Kita butuh **struktur dan angka pola**, bukan katalog lengkap.
>
> Setiap bagian menyebut **"Dipakai untuk"** = keputusan Nexus Saga yang akan diisi oleh data ini. Kalau suatu baris tidak ada di AyoDance, tulis "tidak ada".

Legenda isi: tulis angka/teks apa adanya; kalau tidak yakin tulis `?`.

---

## 1. Slot Wardrobe (avatar)
**Dipakai untuk:** finalisasi daftar slot avatar di `08 §8` & sistem wardrobe (riset `ayodance-avatar-wardrobe.md`). Kita perlu tahu slot modern lengkap, karena data lama hanya punya 5 slot.

Buka menu ganti kostum / dressing room. Untuk tiap slot yang ada, isi:

| Nama slot (di game) | Contoh item | Bisa disembunyikan? | Catatan |
|---|---|---|---|
| Rambut (hair) | | | |
| Wajah (face) | | | |
| Atasan | | | |
| Bawahan | | | |
| Sepatu | | | |
| Set / full body | | | |
| Topi / headwear | | | |
| Kacamata / mata | | | |
| Aksesori wajah (masker, dll) | | | |
| Sarung tangan | | | |
| Punggung / sayap (wings) | | | |
| Pet / mascot | | | |
| Efek / aura | | | |
| Tangan / prop (pegang barang) | | | |
| Ekor | | | |
| (slot lain yang Anda lihat) | | | |

**Pertanyaan kunci:**
- Total ada berapa slot? → `___`
- Saat pakai **set/full body**, apakah slot atasan/bawahan otomatis kosong/terkunci? → `___`
- Saat pakai **topi**, apakah rambut berubah/hilang? → `___`

---

## 2. Kustomisasi tubuh & wajah
**Dipakai untuk:** keputusan "2 base body + slider ringan" vs "wajah = item" (riset wardrobe §1, §9).

| Pertanyaan | Jawaban |
|---|---|
| Pilih gender saat buat karakter? (ya/tidak) | |
| Bisa ubah bentuk tubuh (tinggi/gemuk)? Slider atau pilihan? | |
| Bisa ubah warna kulit? Berapa pilihan / bebas (color picker)? | |
| Wajah: pilih dari model jadi, atau ada slider (mata/hidung/mulut)? | |
| Ada makeup terpisah (lipstik, blush, eyeliner)? | |
| Bisa ganti warna rambut terpisah dari model rambut? | |

---

## 3. Sistem Dye / pewarnaan
**Dipakai untuk:** keputusan sistem Dye menggantikan "tiap warna = item" (riset wardrobe §9, decision log usulan 2026-10-24).

| Pertanyaan | Jawaban |
|---|---|
| Ada "Dyeing Room" / fitur ganti warna item? (ya/tidak) | |
| Item apa yang bisa di-dye? (semua / hanya tertentu) | |
| Pilih warna bebas (color picker) atau dari daftar? | |
| Dye pakai mata uang apa? Sekali pakai atau permanen? | |
| Satu item bisa berapa titik warna (1 warna / multi-zona)? | |

---

## 4. Mata uang & toko
**Dipakai untuk:** validasi model 3 mata uang Nexus Saga (`01`, `11 §15`) terhadap praktik nyata.

| Mata uang di AyoDance | Didapat dari | Dipakai untuk apa |
|---|---|---|
| (mis. "Dance") | | |
| (mis. "Cash") | | |
| (lainnya) | | |

**Pertanyaan kunci:**
- Ada berapa mata uang berbeda total? → `___`
- Apakah satu item kostum bisa dibeli dengan **lebih dari satu** mata uang, atau selalu satu saja? → `___`
- Ada mata uang khusus event/garden terpisah? → `___`

---

## 5. Opsi sewa / durasi item
**Dipakai untuk:** finalisasi sistem sewa 7/30 hari/permanen + rent-to-own (`08 §7`? bukan — `01`, `11 §15`). **Ini bagian paling penting yang datanya terenkripsi.**

Saat beli 1 item kostim, catat pilihan durasi yang muncul:

| Pilihan durasi yang tersedia | Harga (mata uang apa) |
|---|---|
| 1 hari | |
| 7 hari | |
| 30 hari | |
| 90 hari | |
| Permanen | |
| (lainnya) | |

**Pertanyaan kunci:**
- Apakah harga permanen jauh lebih mahal dari 30 hari? (perbandingan kasar, mis. "10x") → `___`
- Saat item sewa habis, apa yang terjadi? (hilang dari inventory / jadi abu-abu / bisa diperpanjang) → `___`
- Ada sistem "cicil jadi permanen" (rent-to-own)? → `___`
- Item cash (uang asli) apakah selalu permanen, atau juga ada versi sewa? → `___`

---

## 6. Gacha / chance
**Dipakai untuk:** aturan gacha transparan + pity (`11 §15`), dan keputusan membuang slot machine.

| Pertanyaan | Jawaban |
|---|---|
| Ada gacha / kotak keberuntungan? (ya/tidak) | |
| Peluang (drop rate) ditampilkan di layar? | |
| Ada jaminan setelah N tarik (pity)? | |
| Pakai mata uang apa? | |
| Ada slot machine / mesin judi? (kita akan HINDARI — cuma konfirmasi) | |
| Item duplikat dari gacha jadi apa? | |

---

## 7. Lobi, channel & room
**Dipakai untuk:** desain Plaza & Custom Room (`03`, `04`, `09 §6`), dan kapasitas room sosial (riset sosial §B).

| Pertanyaan | Jawaban |
|---|---|
| Alur masuk: ada pilih server → channel → lobi? Jelaskan singkat. | |
| Berapa maksimal pemain dalam 1 room main? | |
| Berapa pemain terlihat di 1 lobi/channel sekaligus (kira-kira)? | |
| Room bisa diberi password? | |
| Ada mode tim (vs) dan solo? | |
| Saat bikin room, opsi apa saja yang bisa diatur? (mode, lagu, jumlah pemain, level, dll) | |
| Ada penonton (spectator)? | |
| Ada voice chat di room? | |

---

## 8. Mode permainan ritme
**Dipakai untuk:** desain minigame Dance Duel (`04`, riset sosial §F — "level = panjang urutan panah").

| Pertanyaan | Jawaban |
|---|---|
| Sebutkan mode yang ada (Normal/Beat Up/Couple/Guitar/dll) | |
| Mode dasar: menekan urutan panah lalu Space di akhir? Benar? | |
| Tingkat kesulitan: apakah makin susah = urutan makin panjang? | |
| Ada mode couple (2 orang pasangan)? | |
| Berapa lama 1 lagu kira-kira? | |

---

## 9. Sosial & komunitas
**Dipakai untuk:** desain Squad, couple room, Rest Room, moderasi (`04`, `08`?, `11 §13`).

| Pertanyaan | Jawaban |
|---|---|
| Ada guild/club ("Fam")? Fitur apa saja (bank, rumah, absensi, boss)? | |
| Ada sistem couple/pacaran? Sampai wedding/garden? | |
| Ada batasan umur untuk fitur couple? | |
| Fitur chat: whisper, teman, megaphone? | |
| Ada block/report pemain? | |
| Ada foto studio / sticker? | |

---

## 10. Live-ops & retensi
**Dipakai untuk:** desain season/event/battle pass (`11 §17`).

| Pertanyaan | Jawaban |
|---|---|
| Ada battle pass (AudiPass)? Berapa lama 1 season? | |
| Ada login harian (attendance)? Hadiahnya kosmetik atau mata uang? | |
| Event biasanya seperti apa? (puzzle, bingo, dll) | |
| Ada banner berita/iklan di launcher atau lobi? | |
| Seberapa sering update/patch (perkiraan)? | |

---

## 11. Hal lain yang menarik (bebas)
Catat apa pun yang menurut Anda bagus untuk ditiru atau justru dihindari di Nexus Saga:

```
(tulis bebas di sini)
```

---

## Prioritas (kalau waktu terbatas)
Isi dulu yang paling menutup lubang data terenkripsi, berurutan:
1. **Bagian 5** (opsi sewa / durasi) — paling krusial, datanya terkunci.
2. **Bagian 1** (slot wardrobe modern).
3. **Bagian 4** (mata uang).
4. **Bagian 7** (kapasitas & opsi room).
5. Sisanya menyusul.
