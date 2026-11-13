# 09 — QA pass 7: verifikasi `e5f1aa7` + Announcements/Photon/Lobby (2026-11-13)

Baca-saja, dengan izin user. ID lanjut Q79+.

---

## A. Verifikasi klaim fix (OBSERVED)
| ID | Bukti di kode | Status |
|---|---|---|
| Q60 | `NexusGame.cs:388-412` — `PlayerPrefs` + profil `main`/`editor`/`-nxprofile N`; nama guest ikut disimpan | ✅ benar |
| Q61 | `Program.cs:54-59` policy `auth`/`guest` + `:110 UseRateLimiter()`; `ApiEndpoints.cs:29-35` `RequireRateLimiting` | ✅ terpasang (bukan hanya deklarasi) |
| Q62 | `ApiEndpoints.cs:131` `SecretsEqual(p.DeviceId, req.DeviceId)` (constant-time) | ✅ benar |
| Q63 | `UpgradeRequest(Username, Password, DeviceId)` — `DisplayName` **dihapus dari request** | ✅ benar |
| Photon auth | `PhotonEndpoints.cs:64-100` — secret + `TryValidate(token)`, tolak token kedaluwarsa, balas `ResultCode` | ✅ tersambung |
| Webhook Photon | `PhotonEndpoints.cs:24-39` `RequireWebhookSecret` | ✅ benar |
| Announcements | `AnnouncementEndpoints.cs:19-22` GET publik, POST/DELETE di grup admin; filter waktu **di server** (`:27-32`); validasi kind/title/body/endsAt (`:44-47`) | ✅ benar |
| Q66, Q71, Q76, Q77, Q78 | belum saya periksa detailnya (waktu sesi) | ⏳ belum diverifikasi |

**Koreksi kecil pada laporan:** rate limit yang terpasang **15/menit**, bukan 10 (`Program.cs:51-52`, komentar D15).

## B. Temuan baru

| ID | Sev | Lokasi | Temuan | Dampak / usul |
|---|---|---|---|---|
| **Q79** | **S2** | `PhotonEndpoints.cs:69` | `SecretsEqual(photon.Value.AuthSecret, req.Query["secret"])` — bila `AuthSecret` **kosong** di konfigurasi, `"" == ""` = cocok | **Siapa pun bisa lolos auth Photon** (mendapat `UserId`). Usul: tolak start-up bila `AuthSecret` kosong/pendek, atau `if (string.IsNullOrEmpty(secret)) return 500` |
| **Q80** | S2 | `Program.cs:57-58` | Partisi limit memakai `Connection.RemoteIpAddress`, tetapi **tidak ada `UseForwardedHeaders`** | Begitu API di belakang reverse proxy/Cloudflare, semua pemain berbagi satu IP → **mass 429**; atau `"unknown"` untuk semua → limit gabungan |
| **Q81** | S3 | `Program.cs:51-52` | Limit **per IP, bukan per akun** | Warnet/NAT: 10 pemain login serentak bisa saling menghabiskan 15/menit. Brute force terdistribusi (banyak IP) tetap lolos |
| **Q82** | S3 | `PhotonEndpoints.cs:96` | `Nickname` diambil dari klaim JWT | Nama di room Photon bisa basi setelah pemain mengganti display name sampai token diperbarui |
| **Q83** | S3 | `ApiEndpoints.cs:309-322` | `/auth/guest` membuat Player per `deviceId` baru; limit hanya per IP | Flood DB terdistribusi masih mungkin (15 akun/menit/IP × banyak IP). Pertimbangkan batas harian global atau verifikasi perangkat |
| **Q84** | S4 | `AnnouncementEndpoints.cs:14,30` | `MaxActive = 5` hanya memotong saat **membaca**; admin bisa membuat lebih banyak tanpa peringatan | Pengumuman ke-6 dst hilang diam-diam; usul: tolak create bila sudah 5 aktif, atau nonaktifkan yang terlama |
| **Q85** | S4 | `NexusLobbyController.cs:243` | Layar faksi masih ditampilkan **di lobby**, bukan setelah hasil match pertama | Ini **status antre (2b)**, bukan bug baru — dicatat agar tidak terlupa saat poin e selesai |

## C. Yang masih perlu diuji manusia
1. **Tes editor T2 (NX-12)** — membuka UI lobby, layar hasil, pemicu faksi.
2. **Dua klien nyata** — Q76/Q77 (klik ganda, batal) dan sinkronisasi `koTimeline`.
3. **Papan setelah ada data seri & disputed** — Q71/Q72.
4. **Rate limit di server live** — pastikan 429 muncul dari IP yang benar (bukan dari proxy).

## D. Prioritas
1. **Q79** — satu baris guard, tetapi tanpanya seluruh auth Photon bisa terbuka karena salah konfigurasi.
2. **Q80** — wajib sebelum menaruh API di belakang reverse proxy.
3. **Q81/Q83** — pertimbangkan limit per akun + batas harian pembuatan guest.
4. Q82/Q84/Q85 — kecil.
