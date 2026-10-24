# Ringkasan Temuan Riset AyoDance (data referensi)

Kompilasi semua yang **didapat** dari riset AyoDance: statis (`ayodance-avatar-wardrobe.md`, `ayodance-social-lobby-rhythm.md`) + observasi manual (`ayodance-observasi.md`). Ini **fakta tentang AyoDance**, bukan keputusan kita (keputusan ada di `90-decision-log.md`).

Label: **FAKTA** (observasi/bukti) · **UNKNOWN** (terenkripsi/tidak terbaca).

---

## 1. Avatar & tubuh
- FAKTA: 2 gender (pria/wanita), **fixed base body** (tanpa slider bentuk tubuh), proporsi sama antar gender.
- FAKTA: perbedaan fisik hanya ilusi visual (ukuran baju, sepatu platform, sayap besar).
- FAKTA: 3 varian warna kulit (normal/`_w`/`_b`).
- FAKTA: wajah dijual sebagai item (pilih model jadi, bukan slider); ada varian makeup `_fc` pada sebagian wajah.
- FAKTA: tubuh tersusun bagian terpisah (wajah, badan atas, badan bawah); pakaian mengganti region.

## 2. Wardrobe — 13 slot
| # | Slot | Catatan |
|---|---|---|
| 1 | Hair | topi lama menyatu dengan rambut |
| 2 | Face | |
| 3 | Top | |
| 4 | Bottom | |
| 5 | Shoes | |
| 6 | Set (one-piece) | **mengunci Top+Bottom** |
| 7 | Hand/Accessory | barang dipegang; sub-slot kiri/kanan |
| 8 | Back/Wing | |
| 9 | Face Accessory | kacamata, masker |
| 10 | Head Accessory | topi, bando, mahkota |
| 11 | Pet | ikut menari, **nol stat** |
| 12 | Badge/Ring | cincin couple, emblem |
| 13 | Platform/DJ Booth | efek pijakan kosmetik |

- FAKTA (aturan tumpuk): item mendaftar **semua slot yang ditempatinya**; Set mengeksklusi Top+Bottom.
- FAKTA (data lama): item dikunci oleh **nama file** (tidak ada ID numerik); tiap warna = item terpisah (tanpa dye baju); ada nilai **skala per item**.

## 3. Ekonomi — 3 mata uang
| Mata uang | Jenis | Sumber | Dipakai untuk |
|---|---|---|---|
| **DEN** | soft/gratis | battle, ritme, story, battle party | item standar, sewa pendek, bikin Club |
| **Mi-Cash** | hard (uang asli) | top-up Rupiah | kosmetik premium, item permanen, gacha, ganti nama, **booster EXP/DEN** |
| **Crown/Hearts** | relasional | Couple Dance, level cincin | eksklusif Couple Shop, syarat Love Party |

- FAKTA: 1 item umumnya dijual **satu** mata uang saja (DEN **atau** Mi-Cash).

## 4. Sewa & durasi (paling berharga — data ini terenkripsi, didapat dari observasi)
| Durasi | Mata uang | Harga kasar |
|---|---|---|
| 7 hari | DEN / Mi-Cash | DEN 10.000–30.000 · Mi-Cash 1.000–3.000 |
| 30 hari | DEN / Mi-Cash | DEN 40.000–90.000 · Mi-Cash 3.000–6.000 |
| Permanen | mayoritas Mi-Cash | Mi-Cash 10.000–30.000+ (≈ Rp100rb–300rb+); DEN permanen sangat jarang & mahal |

- FAKTA: sewa habis → item terkunci/hilang dari inventory, tampilan kembali ke default/permanen di bawahnya.
- FAKTA: **tidak ada rent-to-own** (tidak ada konversi sewa→permanen).

## 5. Transaksi antar pemain
- FAKTA: **tidak ada trading/market** antar pemain. `DenItemReSell` = jual balik ke sistem (refund DEN kecil).
- FAKTA: **gifting aktif** — beli untuk diri / kirim ke nickname → PresentBox; mayoritas item Mi-Cash saja yang bisa di-gift (item DEN dikunci, cegah farming antar akun).

## 6. Progres pemain
- FAKTA: **Level akun, mata uang, dan rank terpisah.**
  - Level akun: dari akumulasi EXP bermain (Lv.1–100+, ikon pangkat).
  - Mata uang: tidak terikat level.
  - Rank: leaderboard dinamis (EXP terbanyak, skor mode, level Club).
- FAKTA: ada **booster EXP X2** dijual Mi-Cash (ini praktik P2W-adjacent).

## 7. Lobi & room
- FAKTA: alur server → distrik/channel → tipe lobi (utama/club/shop); guild bisa beli channel privat.
- FAKTA: **kapasitas room 6 penari + sampai 30 penonton** (spectator ngobrol tanpa menari).
- FAKTA: opsi bikin room: judul, password, mode, pilihan lagu/BPM (s/d >190), map/stage, pengaturan key (4-key panah / 8-key numpad).
- FAKTA: voice chat grup per room (mute per pemain, kontrol mic); quick-chat makro F5–F8; tabel kata kasar.

## 8. Gameplay ritme (ARSIP — tidak dipakai Nexus Saga)
- FAKTA: inti = **level N = urutan panah sepanjang N**, dikonfirmasi Space tepat di beat; tiap urutan → klip animasi dansa (tabel 1.791 gerakan).
- FAKTA: tabel lagu 264 baris (lama): artis, judul, file, level 0–19, BPM ≤ 178, flag aktif/baru.
- FAKTA: mode: Beat Up, Choreography, One-Two Party, Guitar, Couple, Club, Space Pang Pang, dll.
- FAKTA: file musik `ABM\` (5.213 file) + chart `*_note.tbm`; **terenkripsi** setelah header.
- Catatan: dihapus dari desain kita (copyright musik + biaya). Lihat `12-rest-room-tanpa-dance.md`.

## 9. Sosial & komunitas
- FAKTA: Guild ("Fam") sangat dalam: bank, board, **roll book (absensi)**, family tree, house, **butler NPC**, ranking, **boss battle**, channel berbayar, sponsor turnamen.
- FAKTA: Couple/Marriage: registrasi → wedding (uang hadiah) → **Couple Garden** (bank book, shop, slot machine) → Secret Garden.
- FAKTA: **Couple ring berlevel = NOL STAT** (Sugar→Honey→Orchid): hanya ikon makin mewah, syarat Love Party, efek room romantis.
- FAKTA: Messenger, whisper, find friend, megaphone (shout), **Photo Studio + sticker**, MyHome, profil.
- FAKTA: moderasi — block list, block per slot room, tabel kata kasar.

## 10. Monetisasi & live-ops
- FAKTA: Fashion Mall: cart, **gifting (PresentBox)**, **outfit tersimpan (MyCodi)**, deal harian (OneDayMarket), Black/White Label, Showcase, Preview.
- FAKTA: **gacha** (Fashion Box / Slot Machine) — **RNG murni, tanpa hard-pity**, transparansi rendah; ada UI peluang (ChanceHelp).
- FAKTA: **slot machine** judi mingguan (di Couple Garden & gacha).
- FAKTA: **AudiPass** (battle pass) + Renewal; **Attendance** harian (hadiah item 7–30 hari, kadang permanen di event besar); referral.
- FAKTA: banyak mata uang event terpisah (Garden cash, SG cash, Event cash).
- FAKTA: patch bulanan; Special Package musiman (bundel Mi-Cash + kosmetik); banner launcher dari server.

## 11. Teknologi client
- FAKTA: `Audition.exe` dilindungi **Themida** (packer) — tidak dibongkar.
- FAKTA: data `.acv`/`.bin`/`.loc` versi sekarang **terenkripsi** — tidak dibongkar.
- FAKTA: anti-cheat **Xigncode** (kernel-level) — game tidak dijalankan di bawah debugger.
- FAKTA: Direct3D 9, FMOD lama, DirectInput, keyboard hook (matikan tombol Windows), jsoncpp (2024), WinINet, Lua 5.1 (penggunaan tak pasti).
- FAKTA: shader modern dengan `_ColorMaskMap` (color mask) — mendukung pewarnaan.
- FAKTA: Patcher = aplikasi .NET 4.7.2; tabel desain lama = SYLK spreadsheet bertipe, ada versi "untuk server" (data dibagi client–server).

## 12. UNKNOWN (terenkripsi — tidak dibongkar, sesuai etika riset)
- Kode slot modern persis, mekanik dye/makeup room, isi AudiPass, mekanik Lumi (gacha/upgrade), data lagu/mode versi sekarang, isi file `.loc`, opsi room detail.
- Jalur sah untuk melengkapi: observasi gameplay akun sendiri atau dokumentasi publik.

---

## Cara pakai data ini
- Untuk **meniru pola** (bukan menyalin): lihat kolom "FAKTA".
- Untuk **keputusan Nexus Saga** (adopsi/ubah/buang/tolak): lihat `90-decision-log.md` dan bagian "Pelajaran/Dampak" di tiap dokumen riset.
- Angka harga/durasi di §4 = **titik awal balancing** ekonomi kita, bukan nilai final.
