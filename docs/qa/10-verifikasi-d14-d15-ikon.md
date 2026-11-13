# 10 — QA pass 8: verifikasi D14/D15 + ikon (2026-11-13)

Baca-saja. ID lanjut Q86+.

## A. Verifikasi klaim
| Klaim | Bukti di kode | Status |
|---|---|---|
| Nama unik tanpa peduli huruf besar/kecil | `Services/NameRules.cs:11` `Normalize` = trim + ToLowerInvariant; kolom & index unik `NormalizedName` (migrasi `20261113103951_AddNormalizedName`) | ✅ benar |
| Nama staf ditolak | `NameRules.cs:14-19` `Exact` + `Prefixes`; `Compact()` (`:21-26`) membandingkan huruf+angka saja | ✅ benar |
| "Gman"/"Gmail" tetap boleh | `:42` `if (!char.IsLetter(next)) return true;` | ✅ benar |
| Guest tidak gagal karena nama | klaim; belum saya lihat loop fallback-nya | ⏳ belum diverifikasi |
| Rate limit 15/menit | `Program.cs:51-52` (`AuthPerMinute`/`GuestPerMinute` = 15) | ✅ benar (laporan sebelumnya menyebut 10 — sudah 15) |
| 12 sprite baru | `NexusUI/Sprites`: `ic_b_comeback/firstblood/flawless/party` (4) + `ic_s_accuracy/blocked/critical/damage/dodge/geardrop/guardcrush/streak` (8) | ✅ 12 file ada |

Catatan kecil: yang dibuat **8** ikon baris statistik, bukan 9 — baris ke-9 kemungkinan memakai ikon lama (`ic_sword`/`ic_trophy`). Perlu dipastikan tampilannya seragam.

## B. Temuan baru — keunikan & impersonasi

| ID | Sev | Lokasi | Temuan | Dampak / usul |
|---|---|---|---|---|
| **Q86** | **S2** | `NameRules.cs:11,21-26` | Normalisasi hanya `ToLowerInvariant` + filter huruf/angka; **homoglyph tidak dirapikan** | `Аdmin` (А = U+0410 Kiril) → Compact = `аdmin` ≠ `admin` → **lolos**. Di UI tampak persis "Admin". Jadi aturan D14 bisa dilewati untuk menyamar sebagai staf. Usul: Unicode FormKC + tabel confusable sederhana (Latin/Kiril/Yunani) sebelum Compact |
| **Q87** | S3 | `NameRules.cs:11` | Huruf lebar penuh (`Ｂｕｄｉ`) atau aksen (`Búdi`) tidak disatukan dengan `budi` | Dua akun bisa tampil nyaris identik padahal kolom unik menganggap berbeda. Usul: FormKC (NFKC) sebelum `ToLowerInvariant` |
| **Q88** | S4 | `NameRules.cs:14-19` | `Exact` memuat `guest`, tetapi `guest123` lolos (tidak ada di `Prefixes`); `GMz`/`GMan` juga lolos | Inkonsistensi kecil; keputusan desain — asal disengaja, cukup dicatat |
| **Q89** | S4 | `NameRules.cs:35` | `Compact` mengosongkan nama yang seluruhnya non-alfanumerik (mis. "★★★") → dianggap reserved (`c.Length == 0`) | Pesan error "nama tidak diizinkan" untuk nama simbol; sebaiknya pesan validasi karakter, bukan reserved |

## C. Temuan yang perlu diverifikasi (bukan klaim)
| ID | Sev | Hal |
|---|---|---|
| **Q90** | S2 | **Loop fallback nama guest**: bila nama bentrok, server memilih "Guest N" lain. Tidak jelas apakah jumlah percobaannya dibatasi. Bila tak dibatasi dan nama bentrok terus (mis. semua "Guest 100..999" terpakai), request bisa berputar/500 |
| **Q91** | S2 | **Race dua guest** dengan nama sama pada saat bersamaan: apakah `DbUpdateException` pada unique index ditangkap lalu diulang dengan nama lain, atau menghasilkan 500 |

## D. Status yang masih ⏳ dari pass sebelumnya
`Q66` (timing login), `Q71` (kolom match papan), `Q76/Q77/Q78` (guard UI). Belum saya periksa detailnya — tidak saya klaim ✅.

## E. Saran untuk keputusanmu (M1 vs M2)
- **Pilih opsi 1 (tunggu tes editor)** menurut saya lebih benar: kode klien yang belum pernah dijalankan sudah menumpuk (T2 + UI lobby + ikon + papan). Setiap bug baru di M2 akan menambah permukaan yang belum teruji.
- Kalau tetap ingin maju: **NX-21 (kartu Disputed)** paling aman karena backend-nya sudah ada dan tidak menyentuh combat.
- Sebelum M2, dua hal ini murah dan berdampak: **Q79** (guard `AuthSecret` kosong) dan **Q80** (`UseForwardedHeaders`).
