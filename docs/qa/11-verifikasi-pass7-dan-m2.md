# 11 — QA pass 9: verifikasi pass 7 + sisa ⏳ (2026-11-13)

Baca-saja.

## A. Verifikasi klaim pass 7
| ID | Bukti | Status |
|---|---|---|
| **Q79** | `PhotonEndpoints.cs:58` `if (expected.Length == 0) return false;` | ✅ **temuan saya salah — dibatalkan** |
| Q80 | mekanisme `KnownProxies` sesuai; header tidak dipercaya tanpa didaftarkan | ✅ benar (aman untuk sekarang) |
| Q81 | `guard.RecordFailure/RecordSuccess` per username; lockout di jalur login | ✅ mekanisme ada (batas 10/15 mnt belum saya hitung ulang) |
| Q83 | `guard.TryCreateGuest()` mengembalikan 429 saat kuota global habis (`:320-322`) | ✅ benar |
| Q84 | pesan peringatan saat pengumuman aktif > 5 | ✅ diterima |
| Q66 | `VerifyHashedPassword` pada `TimingDummyHash` ketika user tidak ada (`:164`) | ✅ **benar, timing setara** |
| Q71 | `LeaderboardService.cs:80` `rows.Add(..., rm, ...)` → kolom match = hitungan ranked (seri ikut) | ✅ **benar** |
| Q90 | `FreeGuestNameAsync` memeriksa reserved + bentrok, dipanggil sebelum insert | ✅ ada (loop terbatas, tidak berputar) |
| Q76–Q78 | hanya terlihat `IsConnecting => _screen == Page.Connecting`; penjaga klik ganda tidak terlihat di grep | ⏳ belum terverifikasi |

## B. Temuan baru

| ID | Sev | Lokasi | Temuan | Dampak / usul |
|---|---|---|---|---|
| **Q91** | **S2** | `ApiEndpoints.cs:350-355` | Menangkap `DbUpdateException` lalu **membaca ulang berdasarkan `DeviceId`**. Konflik bisa juga terjadi pada index unik **`NormalizedName`** (dua device memilih nama guest sama pada saat bersamaan) → baris dengan deviceId kita **tidak ada** → `FirstAsync` melempar `InvalidOperationException` → **500** | Dua pemain baru yang kebetulan dapat nama guest sama bisa membuat salah satunya gagal total. Usul: bedakan jenis konflik; bila bukan milik device ini, ulangi `FreeGuestNameAsync` lalu insert lagi (maks 3×) |
| **Q92** | S3 | `LeaderboardService.cs:78-80` | Kolom `Matches` = hitungan ranked (seri ikut), tetapi `WinRate` memakai `Wins+Losses` (seri tidak) | Kartu papan bisa tampil "5 match · 3-0 · 100%" — pemain melihat 2 match "hilang". Usul: tampilkan `3-0-2` atau beri label "WR (tanpa seri)" |
| **Q93** | S3 | `ApiEndpoints.cs:374-376` (`Me`) | `/api/me` menghitung `matches = Wins+Losses` dan win rate dari itu, sementara papan memakai hitungan ranked | Angka "match" dan "win rate" **berbeda antara profil dan papan** untuk pemain yang punya seri. Satu definisi harus dipilih |
| **Q94** | S3 | `NexusGame.cs` | Klaim "klik ganda tidak membuat dua antrean" belum terlihat penjaganya (tidak ada `_starting`/interlock; hanya cek `_screen`) | Perlu bukti: kalau `ConnectSafe` men-set `_screen` setelah `await`, klik kedua masih bisa lolos. Verifikasi dengan log dua klik cepat |

## C. M2 (NX-21, NX-22) — belum saya periksa
Belum saya buka kodenya; tidak ada klaim. Bila mau, pass berikutnya saya fokus ke:
1. `Disputed` — alasan tersimpan, tampil di Riwayat + layar hasil, tidak mengubah statistik/papan (pastikan query benar-benar memfilter `Finished`).
2. `/api/me/heroes` — agregasi per hero: apakah K/D hanya ranked1v1, apakah seri dihitung, dan apakah query bisa lambat seperti radar (Q56).

## D. Prioritas
1. **Q91** — satu-satunya bug fungsional baru (500 pada race nama guest).
2. **Q93** — satukan definisi "match"/"win rate" antara `/me` dan papan.
3. **Q92/Q94** — tampilan & bukti guard.
