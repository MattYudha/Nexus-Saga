# Riset: Avatar & Wardrobe AyoDance (2026-10-24)

Sumber: client AyoDance (Audition versi Indonesia) di `C:\Megaxus\AyoDance`, **analisis statis saja** (ada anti-cheat Xigncode). Game tidak dijalankan, enkripsi tidak dibongkar, data mentah tidak disalin ke repo.

Label: **OBSERVED** = bukti langsung (path/offset/hitungan) · **INFERRED** = dugaan beralasan · **UNKNOWN** = tidak bisa dipastikan.

> ⚠️ **Batas penting:** tabel item yang bisa dibaca berasal dari **2004–2005** (arsip lama tanpa enkripsi). Data versi sekarang (aksesori, pet, sayap, dye, makeup, sewa, AudiPass) ada di file **terenkripsi** → UNKNOWN. Temuan di sini menggambarkan **fondasi desain** AyoDance, bukan isi game saat ini.

---

## Ringkasan temuan (ID)
| Topik | Temuan | Status |
|---|---|---|
| Base body | 2 gender (m/f); tubuh terpisah per bagian (wajah, atas, bawah) | OBSERVED |
| Warna kulit | 3 varian tekstur: normal, `_w`, `_b` | OBSERVED (arti: INFERRED terang/gelap) |
| Wajah | Wajah = **item** (slot `f`), dipilih dari model jadi (±32–36 per gender), bukan slider | OBSERVED |
| Slot lama | **5 slot**: `h` rambut, `f` wajah, `j` atasan, `p` bawahan, `s` sepatu | OBSERVED |
| Set/dress | **Tidak ada slot "set"** — item mendaftar **semua slot yang ditempatinya** (mis. dress = `j,p`; full set = `f,h,j,p,s`) | OBSERVED |
| Topi | Bukan slot terpisah — topi/kacamata **menyatu dengan model rambut** | OBSERVED |
| Slot modern | Pet, mascot, Lumi, custom motion, sayap/prop (dari nama UI & efek partikel) | INFERRED; kode slot UNKNOWN |
| Efek partikel | 44 kelas efek yang menempel pada item (sepatu, celana, sayap, tongkat) | OBSERVED |
| Mata uang | Setiap item dijual **satu** mata uang: game money (500–600.000) **atau** cash (300–5.400); nilai `1` = tidak dijual di mata uang itu | OBSERVED |
| Sewa/durasi | Tidak ada kolom durasi di tabel lama | OBSERVED (sistem sekarang: UNKNOWN) |
| Warna item | Lama: **setiap warna = item terpisah** (rambut ±3× katalog). Kini ada Dyeing Room & Makeup Room (terenkripsi) | OBSERVED / isi UNKNOWN |
| Proporsi | Item wanita lebih banyak dari pria (mis. atasan 194 vs 142); unisex jarang (7) | OBSERVED |
| Couple | Konten couple = **animasi** (high-five, kiss), bukan pakaian | OBSERVED |
| Teknologi | Model `.rgm` ("Delight3D DynamicObjectFile"), tekstur `.dds`, data tabel `.slk` (SYLK spreadsheet) | OBSERVED |

---

## 1. Tubuh avatar
- **OBSERVED:** kolom `성별` (gender) bertipe `enum(m,f)`. File dasar di `DATA\001.acv`: wajah pria/wanita (`.rgm`), tekstur badan atas & bawah per gender (`.dds`).
- **OBSERVED:** tubuh tersusun dari **bagian terpisah** (wajah, badan atas, badan bawah); pakaian mengganti region tubuh.
- **OBSERVED:** 3 varian tekstur kulit per bagian (tanpa sufiks, `_w`, `_b`). **INFERRED:** terang/gelap.
- **OBSERVED:** wajah adalah item (slot `f`), 32–36 model per gender, masing-masing dengan 3 varian kulit. 6 wajah punya varian `_fc` (**INFERRED:** lapisan makeup/warna wajah).
- **INFERRED:** tidak ada slider bentuk tubuh; hanya `크기보정치` (koreksi skala) per item.

## 2. Slot wardrobe (tabel 2005, `DATA\020.acv : script\아바타.slk`)
| Kode | Slot | Skala default |
|---|---|---|
| `h` | Rambut | 1.1 |
| `f` | Wajah | 1.1 |
| `j` | Atasan | 0.85–0.95 |
| `p` | Bawahan | 0.75 |
| `s` | Sepatu | 1.1 |

- Tidak ditemukan file topi/kacamata/sayap/pet/tas/kalung di 20.101 entri arsip lama.
- **INFERRED:** slot tambahan muncul belakangan (UI `MascortPet`, `MandrakePet`, `LumiInventory`, `CustomMotionItem`); kodenya ada di file terenkripsi.
- **OBSERVED:** `SCRIPT\AvTblPtLst.dat` (teks) = daftar **44 kelas efek partikel** yang menempel pada item (contoh kategori: sepatu, celana, sayap, pedang, tongkat, lilin).

## 3. Format record item (SYLK; baris 1 = nama kolom, baris 2 = tipe)
| # | Kolom | Tipe | Arti |
|---|---|---|---|
| 1 | Nama | string | nama tampilan |
| 2 | Nama file | string | **kunci aset** (tidak ada ID numerik) |
| 3 | Part | set enum `s,p,j,f,h` | slot yang ditempati (boleh banyak) |
| 4 | Gender | set enum `m,f` | `m,f` = unisex |
| 5 | Deskripsi | string | dipakai sebagai nama warna |
| 6 | Harga game money | int | `1` = tidak dijual dengan mata uang ini |
| 7 | Harga cash | int | `1` = tidak dijual dengan mata uang ini |
| 8 | Koreksi skala | float | |
| 9 | Baru | 0/1 | ditambahkan ±2005 |

Pertumbuhan tabel: 2004 open beta ±219 item (8 kolom) → 2005 ±617 → 2005 akhir ±1.052 item (9 kolom). Ada 19 versi tabel di arsip lama.

## 4. Aturan tumpuk (layering)
- **OBSERVED:** item mendaftar semua slot yang ditempati. Di versi 020: `j,p` (dress) 9 item, `j,p,s` 2, `h,j,p,s` 4, `f,h,j,p,s` 4.
- **INFERRED:** aturannya "**menempati slot**" — memakai item multi-slot melepas/menyembunyikan isi slot-slot itu; tidak ada flag hide terpisah.
- **OBSERVED:** aksesori kepala lama menyatu dengan model rambut (goggle, bandana, mahkota).

## 5. Mata uang & sewa
- **OBSERVED:** 527 item game money, 493 item cash, 18 item default (tidak dijual).
- **UNKNOWN:** durasi sewa/permanen — kemungkinan di server atau file terenkripsi `CashInfo.bin`, `SGCashInfo.bin`, `GardenCashInfo.bin`, `EventCash.bin` (**INFERRED:** beberapa mata uang terpisah).

## 6. Warna, dye, makeup
- **OBSERVED:** sistem lama: warna = item terpisah (`헤어NN_MM`, MM = varian warna). 167 gaya rambut: 113 satu warna, 44 tiga warna.
- **OBSERVED:** sekarang ada `AvatarDyeingRoot.bin` (15 record, 2025) dan `AvatarMakupRoom.BIN` (313 record, 2025) — **terenkripsi**, isi UNKNOWN.

## 7. Pipeline aset
| Folder/format | Isi | Status |
|---|---|---|
| `ABM\*.tbm` (5.213), `*.abm`, `music.amp` | **Musik**, bukan avatar. Header `AuditionMusic`; 459 file `*_note.tbm` (**INFERRED:** chart not) | OBSERVED |
| `DATA\*.acv` lama (28 arsip) | Index tanpa enkripsi: u32 count + entri 176 byte (nama 160 B CP949, u32 ?, u32 size, u32 orig size, u32 offset); data zlib | OBSERVED |
| `DATA\*.acv` baru (302 arsip, ±213.057 entri) | Index **terenkripsi** (entropi ±7,95) | OBSERVED, tidak dibongkar |
| `.rgm` / `.dds` / `.cma` / `.pos` / `.slk` | Model 3D / tekstur / kamera / posisi dansa / tabel data | OBSERVED |

Penamaan aset: `kategori` + tag opsional + nomor + `_varian` opsional + sufiks kulit `_w`/`_b`. Jumlah nama unik (arsip lama): rambut 1.488, sepatu 1.083, atasan wanita 856, bawahan wanita 789, atasan pria 671, bawahan pria 566, set wanita 255, set pria 154, wajah ±150 per gender.

## 8. File terenkripsi / tidak terbaca (dihentikan sesuai aturan)
| File | Bukti |
|---|---|
| Semua `SCRIPT\*.bin` | Record: u32 panjang, u16 0, u16 jumlah blok, blok 8 byte terenkripsi; blok identik berulang → **INFERRED** cipher blok 8-byte mode ECB |
| `SCRIPT\*.loc` | Obfuskasi tingkat byte, entropi ±6,1–6,3 |
| 302 arsip `.acv` baru | Index terenkripsi |
| `Audition.exe` | **Dilindungi Themida** (section `.themida`, `.boot`, entropi ±7,9) |

---

## 9. Pelajaran untuk Nexus Saga (adopsi / ubah / buang)
| AyoDance | Keputusan Nexus Saga | Alasan |
|---|---|---|
| Item mendaftar **set slot yang ditempati** | **ADOPSI** | Dress, full set, jubah panjang tertangani tanpa kasus khusus |
| 2 gender, bagian tubuh terpisah, 3 tekstur kulit | **ADOPSI + UBAH** | Sudah sejalan dengan "2 base body"; warna kulit sebaiknya parameter shader (bukan tekstur ×3) |
| Wajah = model jadi yang dijual sebagai item | **UBAH** | Wajah dasar gratis + slider ringan (blendshape); wajah premium tetap bisa jadi item |
| Topi menyatu dengan rambut | **BUANG** | Kita pakai slot aksesori kepala terpisah + aturan "menempati slot" (topi menempati `hair-top`) supaya kombinasi lebih banyak |
| Setiap warna = item terpisah | **BUANG → sistem Dye** | Katalog membengkak ±3×; AyoDance sendiri kemudian menambah Dyeing Room |
| Item hanya dijual dalam satu mata uang | **UBAH** | Sesuai pilar kita: item bisa punya harga Gold (sewa) **dan** MiCash (permanen); dicatat per item |
| Koreksi skala per item | **ADOPSI** | Berguna untuk shared rig + 2 base body |
| Kunci item = nama file | **BUANG** | Pakai `itemId` numerik stabil + `assetKey` terpisah (aman untuk live-ops & lokalisasi) |
| Efek partikel menempel pada item | **ADOPSI** | Sejalan dengan skin/efek MiCash (nol stat) |
| Couple = animasi/emote | **ADOPSI** | Cocok untuk couple room 18+ dan emote sosial |
| Item wanita lebih banyak | **CATAT** | Pertimbangkan proporsi katalog berdasarkan data pemain kita sendiri |
| Data tabel di arsip terenkripsi | **CATAT** | Kita memakai content bundle ber-hash (sudah diputuskan); enkripsi bukan pengganti validasi server |

## 10. Belum diketahui (dan tidak akan dibongkar)
Kode slot modern (aksesori/pet/sayap/Lumi), mekanik dye & makeup, durasi sewa, hadiah AudiPass, isi file `.loc`. Bila diperlukan, jalur yang sah adalah **observasi gameplay** (rekaman layar akun sendiri) atau dokumentasi/wiki publik — bukan membongkar enkripsi.
