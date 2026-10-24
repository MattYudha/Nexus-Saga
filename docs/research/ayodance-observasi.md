# Observasi Manual AyoDance (dari gameplay akun sendiri, 2026-10-24)

Sumber: observasi langsung oleh pemilik proyek di dalam game (legal; melengkapi bagian yang terenkripsi pada riset statis). Melengkapi `ayodance-avatar-wardrobe.md` dan `ayodance-social-lobby-rhythm.md`.

---

## 1. Slot wardrobe modern — 13 slot (OBSERVED)
Data lama hanya 5 slot; versi sekarang **13 slot**:

| # | Slot | Catatan |
|---|---|---|
| 1 | Hair | |
| 2 | Face | wajah/ekspresi |
| 3 | Top | |
| 4 | Bottom | |
| 5 | Shoes | |
| 6 | **Set** (one-piece) | **mengunci Top & Bottom** bila dipakai |
| 7 | Hand / Accessory | barang dipegang (tas, lolipop, tongkat); sub-slot kiri/kanan spesifik |
| 8 | Back / Wing | sayap / tas punggung |
| 9 | Face Accessory | kacamata, masker |
| 10 | Head Accessory | topi, bando, mahkota |
| 11 | Pet | ikut menari |
| 12 | Badge / Ring | cincin couple / emblem di papan nama |
| 13 | Platform / DJ Booth | efek pijakan kaki kosmetik di room |

**Aturan tumpuk:** Set mengeksklusi Top+Bottom; aksesori tangan terikat ke sub-slot spesifik (tidak bebas bertumbukan).

## 2. Kustomisasi tubuh (OBSERVED)
- **Tidak ada slider.** Fixed base body, proporsi sama antar gender.
- Perbedaan fisik hanya ilusi visual (ukuran baju, sepatu platform, sayap besar).

## 3. Dye (OBSERVED)
- **Tidak ada sistem Dye.** Tiap warna = item terpisah (merah & biru = 2 pembelian).
- (Catatan: riset statis menemukan `AvatarDyeingRoot.bin` terenkripsi dan shader `_ColorMaskMap`. Kemungkinan dye sangat terbatas/baru/tidak untuk baju umum. Untuk desain kita, anggap AyoDance **tidak** punya dye baju.)

## 4. Mata uang — 3 jenis (OBSERVED)
| Mata uang | Jenis | Sumber | Penggunaan |
|---|---|---|---|
| **DEN** | soft (gratis) | dance battle, ritme, story, battle party | item standar, sewa durasi pendek, bikin Club |
| **Mi-Cash** | hard (uang asli, via Megaxus/UniPin) | top-up Rupiah | kosmetik premium (White Label), item permanen, tiket gacha, ganti nama, **booster EXP/DEN** |
| **Crown/Hearts** | relasional | Couple Dance, naik level cincin | eksklusif Couple Shop, syarat lisensi pernikahan |

Item umumnya dijual **satu** mata uang (DEN **atau** Mi-Cash), bukan keduanya.

## 5. Sewa & durasi (OBSERVED) — paling krusial
| Durasi | Mata uang | Rentang harga kasar |
|---|---|---|
| 7 hari | DEN / Mi-Cash | DEN 10.000–30.000 · Mi-Cash 1.000–3.000 |
| 30 hari | DEN / Mi-Cash | DEN 40.000–90.000 · Mi-Cash 3.000–6.000 |
| Permanen | **mayoritas hanya Mi-Cash** | Mi-Cash 10.000–30.000+ (≈ Rp100rb–300rb+); via DEN sangat jarang & sangat mahal (ratusan ribu–jutaan DEN) |

- **Saat sewa habis:** item otomatis terkunci/hilang dari inventory aktif; tampilan kembali ke base body atau item permanen di bawahnya.
- **Tidak ada rent-to-own.** Tidak ada konversi sewa→permanen; harus beli ulang manual.

## 6. Gacha (OBSERVED)
- Fashion Box / Slot Machine mingguan; **RNG murni, tanpa hard-pity**. Transparansi rendah.

## 7. Lobi & room (OBSERVED)
- **Kapasitas: 6 penari + sampai 30 penonton** (spectator duduk di bangku, ngobrol, tanpa menari).
- Opsi bikin room: judul, password, mode (Single/Team Battle/Couple/Club/Space Pang Pang/Battle Party), pilihan lagu/BPM (lambat s/d >190 BPM), map/stage, dan **pengaturan key: 4-Key (panah) atau 8-Key (numpad, lanjutan)**.

## 8. Mode ritme (OBSERVED)
- Mayoritas: urutan tombol arah di sepanjang Bar Time, lalu Spacebar tepat di bulatan Beat (Beat Up, Choreography, One-Two Party, Guitar).

## 9. Sosial (OBSERVED)
- Club House (aliansi/squad); Couple/Marriage dengan cincin berlevel; blokir chat kasar.

## 10. Live-ops (OBSERVED)
- Patch bulanan; Attendance harian (hadiah item 7–30 hari); Special Package musiman (bundel Mi-Cash + kosmetik).

---

## Dampak ke keputusan Nexus Saga

### A. Yang DIKONFIRMASI (lanjutkan rencana)
| Hal | Keputusan kita |
|---|---|
| Sewa 7/30 hari/permanen nyata ada | **Pertahankan.** Struktur harga kita bisa meniru pola: sewa murah, permanen mahal |
| Permanen didominasi hard currency | **Pertahankan + perbaiki**: hero/kosmetik permanen kita tetap ada jalur Gold (anti-P2W), beda dari AyoDance |
| Item cosmetic nol stat (kostum) | **Pertahankan** |
| Room 6 pemain + 30 spectator | **Adopsi** untuk **Fashion Contest** (6 tampil, 30 nonton+vote) & spectate Plaza; **bukan** untuk dance |
| 4-key / 8-key | **DIBATALKAN** — tanpa mode dance (12) |
| Set mengunci Top+Bottom | **Adopsi** (model "item menempati set slot") |

### B. Yang kita BEDAKAN secara sengaja (keunggulan Nexus Saga)
| AyoDance | Nexus Saga | Alasan |
|---|---|---|
| Tidak ada rent-to-own | **Punya rent-to-own** | Sewa terasa tidak hangus → konversi ke MiCash lebih sehat; ini pembeda |
| Tiap warna = item terpisah; tanpa dye baju | **Sistem Dye** (color mask) | Katalog tidak membengkak; lebih ramah pemain. **Catatan: ini divergensi, bukan adopsi** |
| Gacha RNG tanpa pity | **Gacha transparan + hard pity + dupe→shard** | Lebih adil, sesuai regulasi loot box |
| Slot machine | **Dibuang** | Risiko dianggap judi; rating 13+ |

### C. Yang data ini MUNCULKAN sebagai keputusan baru (menunggu konfirmasi)
1. **Mata uang ke-4 relasional (Crown/Hearts)?** AyoDance memisahkan mata uang couple. Kita sudah putuskan 3 mata uang (Gold/Ticket/MiCash). **Usulan: jangan tambah mata uang ke-4.** Konten couple pakai **token event/relasi** non-tradable yang bukan mata uang inti, supaya ekonomi tetap sederhana.
2. **Booster EXP/DEN dijual MiCash.** Ini **P2W-adjacent** (mempercepat progres berbayar). **Usulan: TOLAK.** Di Nexus Saga, MiCash tidak boleh mempercepat progres kompetitif (Gold/XP). Boleh hanya untuk kosmetik & kenyamanan non-kompetitif (ganti nama, slot loadout).
3. **Pet, Badge/Ring, Platform/DJ Booth sebagai slot kosmetik.** Ide bagus untuk ekspresi. **Usulan: adopsi sebagai kosmetik nol stat.** Pet **wajib nol stat** (di AyoDance pet hanya ikut menari — aman untuk ditiru).
4. **Set slot (13 slot) → final daftar slot avatar kita.** Usulan daftar slot Nexus Saga: Hair, Face, Top, Bottom, Shoes, Set, Hand(L/R), Back/Wing, Face-Acc, Head-Acc, Pet, Badge/Ring, Aura/Platform. **Terpisah dari slot gear tempur** (Senjata/Helm/Armor/Trinket di `08`).

### D. Celah kecil yang masih berguna (opsional, tidak memblokir)
Kalau sempat saat main lagi, catat:
1. **Trading antar pemain?** Ada `DenItemReSell` di file — apakah pemain bisa jual/beli/tukar item ke pemain lain? (memengaruhi apakah kosmetik kita tradable)
2. **Gifting** item ke teman? (ada `PresentBox` di file)
3. **Level akun/pemain** terpisah dari mata uang? (apakah ada progres level selain rank)
4. **Durasi item dari Attendance**: hadiah login itu sewa (7/30 hari) atau permanen?
5. **Couple ring berlevel** memberi apa selain akses Couple Shop? (pastikan tidak ada stat)

Jika tidak diisi pun, desain bisa lanjut dengan asumsi yang dicatat di C.

---

## Jawaban celah D (observasi lanjutan, 2026-10-24)
| # | Temuan AyoDance | Keputusan Nexus Saga |
|---|---|---|
| 1 | **Tidak ada trading antar pemain.** `DenItemReSell` = jual balik ke sistem (refund DEN kecil), bukan pasar pemain | **Kosmetik untradeable** antar pemain untuk MVP. Market/Auction House = keputusan terpisah bila nanti diinginkan (bukan sekarang) |
| 2 | **Gifting aktif.** Beli untuk diri / kirim ke nickname → masuk PresentBox. Item DEN umumnya **tidak** bisa di-gift (cegah transfer kekayaan antar akun farming); gift mayoritas Mi-Cash | **Adopsi gifting**, dengan aturan: hanya item **MiCash** bisa di-gift; item Gold tidak (anti-farming). Semua gift tercatat di ledger |
| 3 | **Level akun, mata uang, rank terpisah.** Level akun murni dari EXP bermain (ikon pangkat Lv.1–100+); saldo tak terikat level; rank = leaderboard dinamis | **Adopsi struktur 3 lapis**: Account Level (dari bermain, **kosmetik/profil saja, nol efek kompetitif**), Wallet, dan MMR/Rank. XP **tidak** bisa dibeli |
| 4 | **Attendance:** mayoritas hadiah **sewa 7–30 hari** + tiket EXP; sesekali **avatar permanen** di hari terakhir event besar | **Adopsi**: login harian beri item sewa + Gold; hadiah permanen hanya di event besar sebagai insentif retensi |
| 5 | **Couple ring = NOL STAT** (murni kosmetik/sosial). Level naik (Sugar→Honey→Orchid) → ikon cincin makin mewah, syarat Love Party, efek room romantis | **Adopsi penuh**: couple ring nol stat, progres relasional memberi **kosmetik & akses sosial saja**. Mengonfirmasi prinsip anti-P2W |

### Catatan penting dari #3: Account Level harus nol efek kompetitif
AyoDance menjual **tiket EXP X2** dengan Mi-Cash. Karena kita menolak booster berbayar (decision log 2026-10-24), **Account Level di Nexus Saga tidak boleh memberi keuntungan tempur apa pun** — hanya membuka kosmetik, gelar, dan slot profil. Dengan begitu, meng-grind atau top-up tidak memengaruhi arena.
