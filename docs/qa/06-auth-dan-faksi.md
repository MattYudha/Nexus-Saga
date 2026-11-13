# 06 — QA pass 5: auth, K-10 upgrade, FactionService (2026-11-13)

Lanjutan `05`. Baca-saja. Termasuk verifikasi klaim fix pass 3 (`1e1124d`) dan K-10 (`fa1b3a2`).

---

## A. Verifikasi klaim pass 3 (OBSERVED)
| ID | Bukti di kode | Status |
|---|---|---|
| Q42 | `Options.cs:48` TTL **180 dtk** (komentar menyebut alasan) | ✅ benar |
| Q43 | `NexusBackend.cs:171-181` retry backoff, hanya untuk transient; laporan idempoten | ✅ benar |
| Q44 | `NxSeparationSystem.cs:20,25` **keduanya** dicek `HitPause` | ✅ benar |
| Q47 | `MatchService.cs:136-141` skor **ikut** dibandingkan antar-klien | ✅ benar — temuan saya salah, diterima |
| Q45/Q46 | INBOX / disengaja | ✅ diterima |

## B. Temuan baru — auth & K-10

| ID | Sev | Lokasi | Temuan | Dampak |
|---|---|---|---|---|
| **Q60** | **S1** | `NexusGame.cs:379-380` | `_deviceId = "nx-" + Guid.NewGuid()` adalah **static per-launch**, tidak disimpan (tidak ada `PlayerPrefs`) | Setiap kali game dibuka, `/auth/guest` membuat **akun guest baru**: progres, faksi, dan rating guest **hilang tiap launch**. Nilai K-10 hanya bertahan bila pemain meng-upgrade **di sesi yang sama**. Juga mengotori populasi faksi & leaderboard dengan akun hantu |
| **Q61** | S2 | `Program.cs` (tidak ada `AddRateLimiter`) | **Tidak ada rate limiting** pada `/auth/login`, `/auth/register`, `/auth/upgrade`, dan `/auth/guest` | Brute force password (minimum hanya 6 karakter) dan **flood DB** lewat `/auth/guest` tanpa autentikasi — cukup kirim deviceId acak berulang |
| **Q62** | S2 | `ApiEndpoints.cs` `UpgradeGuest` | `/auth/upgrade` **tidak memeriksa DeviceId** pemanggil; siapa pun yang memegang token guest bisa memasang username+password | Token guest yang dicuri (mis. dari log) → penyerang **mengunci pemilik asli** dari akunnya. Usul: wajibkan `deviceId` yang cocok pada upgrade |
| **Q63** | S2 | `UpgradeGuest` | `DisplayName` boleh diganti bebas (1–24 char), tidak unik, tanpa filter kata/reserved | **Impersonasi** di leaderboard/riwayat: pemain bisa memakai nama pemain lain yang dikenal |
| **Q64** | S3 | `TokenService.cs:14-24` | `ValidateAudience = false`, tanpa `jti`, tanpa jalur revokasi; umur token dari `JwtOptions.LifetimeHours` (perlu dicek nilainya) | Token yang dicuri tetap sah sampai kedaluwarsa, termasuk setelah upgrade/pindah perangkat; tidak ada "logout semua perangkat" |
| **Q65** | S3 | `ApiEndpoints.cs` `GuestLogin` | `displayName` datang dari klien tanpa sanitasi yang terlihat; klien mengirim `"Guest"+Random(100,999)` | Nama acak tabrakan (Guest123 dipakai banyak orang) → membingungkan di daftar lawan |
| **Q66** | S3 | `Login` | `player is null` dan `PasswordHash is null` mengembalikan respons yang sama, tapi jalur pertama keluar lebih cepat | Enumerasi username lewat timing (risiko rendah, tetapi nyata) |

## C. Temuan baru — FactionService

| ID | Sev | Lokasi | Temuan |
|---|---|---|---|
| **Q67** | S3 | `FactionService.cs:10-13` | Cache **per-instance** (1 menit). Dengan >1 replika API, bonus "Butuh Pejuang" bisa **berbeda** antar request yang dilayani replika berbeda |
| **Q68** | S3 | `FactionService.cs:47-60` | Populasi menghitung **guest** yang memilih faksi; karena Q60 membuat guest baru tiap launch, angka populasi dan `NeedsWarriors` bisa **bias** |
| **Q69** | S4 | `FactionService.cs:31-32` | `Invalidate()` mengubah `_at` tanpa lock; balapan dengan `GetAsync` bisa menghasilkan satu recompute ekstra (tidak berbahaya) |
| **Q70** | S4 | `FactionService.cs:52` | `total >= FactionMinPopulation` — bila populasi di bawah ambang, `NeedsWarriors = 0` dan **bonus tidak pernah aktif**; perlu dipastikan ambangnya sesuai ekspektasi UI |

## D. Prioritas
1. **Q60** — simpan `deviceId` di `PlayerPrefs`/file; tanpa ini K-10 nyaris tidak berguna untuk pemain.
2. **Q61** — rate limit dasar (login & guest), mis. 5/menit per IP + batas pembuatan akun per menit.
3. **Q62** — upgrade wajib cocok deviceId (atau verifikasi ulang).
4. **Q63** — reserved/unik displayName minimal untuk nama yang tampil di papan.
5. **Q67/Q68** — setelah Q60 selesai, populasi faksi jadi lebih jujur; cache multi-replika menyusul.

## E. Belum dipindai
`LeaderboardService` (tie-break vs docs/33, cache) · state machine UI `NexusGame` (match ganda, tombol dobel) · `Announcements` (endpoint baru) · Photon auth callback (`TryValidate`).
