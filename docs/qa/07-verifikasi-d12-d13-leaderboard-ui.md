# 07 — QA pass 6: verifikasi D12/D13 + Leaderboard + state machine UI (2026-11-13)

Lanjutan `06`. Baca-saja.

---

## A. Verifikasi D12 (kebijakan RD)
| Klaim | Bukti di kode | Status |
|---|---|---|
| RD tidak turun < 30 | `Options.cs:39` `RdMin=30` → dipakai `MatchService.cs:387` `Math.Clamp(rd, RdMin, RdMax)` | ✅ benar |
| RD naik saat tidak aktif | `Glicko2.cs:21-32` `Inflate`: φ* = √(φ² + periods·σ²), cap `maxRd` | ✅ benar (rumus sesuai Glicko langkah 6) |
| Dihitung tepat sebelum match | `MatchService.cs:379-381` memakai `LastRatedAt` + `RdInactivityPeriodDays` | ✅ benar |
| Match diredam tidak menurunkan RD | `MatchService.cs:335-340` (komentar + jalur clamp) | ✅ benar (perilaku terlihat konsisten) |

Catatan: `Inflate` memakai `periods` utuh; bila pemain absen 90 hari, satu panggilan melompati banyak periode sekaligus — benar secara rumus, tapi perlu dipastikan `periods` dihitung dari `floor(days/7)` (bukan dibulatkan ke atas).

## B. Verifikasi D13 (dasar badge)
| Klaim | Bukti | Status |
|---|---|---|
| Badge hanya ranked1v1 + battle | `StatsEndpoints.cs:117,118,129` memakai `r.BadgeFmt` | ✅ benar |
| FLAWLESS hanya menang KO | `:118` `r.KoFinish` ditambahkan | ✅ **perbaikan Q53 terkonfirmasi** |
| K/D tetap hanya ranked1v1 | `r.KdValid` tidak berubah | ✅ benar |

## C. LeaderboardService

| ID | Sev | Lokasi | Temuan |
|---|---|---|---|
| **Q71** | S3 | `LeaderboardService.cs:84-90` | `Matches` yang ditampilkan = `Wins+Losses` (draw tidak dihitung), sedangkan syarat placement memakai jumlah match ranked (draw ikut). Pemain dengan 5 draw tampil "0-0, 5 match" secara tidak konsisten |
| **Q72** | S3 | `LeaderboardService.cs:63-66` | Placement hanya menghitung **jumlah** match ranked selesai, tanpa memeriksa apakah ada hasil valid. 5 match Disputed/format lama yang tercatat `ranked` tetap meloloskan pemain ke papan |
| **Q73** | S3 | `LeaderboardService.cs:20-22` | Cache 1 menit **per-instance**; multi-replika → peringkat bisa berbeda antar request (keluarga Q67) |
| **Q74** | S4 | `LeaderboardService.cs:36` | `RankOfAsync` mengembalikan `null` untuk pemain di bawah placement — pastikan UI menampilkan "belum ada peringkat", bukan kosong |
| **Q75** | S3 | `LeaderboardService.cs:60-72` | Recompute memuat **seluruh** pemain + seluruh match ranked per menit. Aman sekarang, tumbuh linear (keluarga Q56) |

Positif: `Wins++/Losses++` hanya di jalur ranked (`MatchService.cs:339-340`) → Battle **tidak** mengotori win rate papan. ✅

## D. State machine UI (`NexusGame.cs`)

| ID | Sev | Lokasi | Temuan | Dampak |
|---|---|---|---|---|
| **Q76** | S2 | `NexusGame.cs:118-119` | `QuickMatch`/`CreateRoom` adalah **`async void`** tanpa penjaga re-entrancy | Klik ganda cepat = dua `ConnectSafe` berjalan bersamaan → dua antrean/sesi, satu di antaranya menjadi hantu. `async void` juga menelan exception (tidak terlihat di log) |
| **Q77** | S3 | `NexusGame.cs:45,525` | `UiCancel` langsung memindahkan layar; `LeaveQueue` baru dipanggil dari loop ketika layar berubah | Bila sesi Photon sudah terbentuk, batal bisa meninggalkan pemain di room (lawan menunggu) |
| **Q78** | S3 | `NexusGame.cs:399-414` | `ConnectSafe` tidak memeriksa apakah sudah `InMatch` | Pemicu lain (tombol/otomatis) bisa memulai koneksi kedua saat match berjalan |

## E. Masih terbuka dari pass 5 (belum tersentuh)
| ID | Sev | Isi |
|---|---|---|
| **Q60** | **S1** | `deviceId` dibuat per-launch → guest baru tiap buka game (klien, bukan backend) |
| **Q61** | S2 | Tanpa rate limit (login & `/auth/guest` bisa dipakai flood DB) |
| **Q62** | S2 | `/auth/upgrade` tidak memeriksa deviceId → token bocor bisa mengunci akun |
| **Q63** | S2 | `DisplayName` bebas saat upgrade (impersonasi) |

## F. Prioritas lanjutan
1. **Q60** — satu-satunya temuan S1 yang masih terbuka dan berdampak langsung ke pemain.
2. **Q61/Q62** — keamanan akun.
3. **Q76** — klik ganda pada Quick Match.
4. **Q71/Q72** — konsistensi papan.

## G. Belum dipindai
`Announcements` (endpoint baru + admin) · Photon auth callback (`TryValidate` dipakai di mana) · alur `NexusLobbyController` (tombol "Segera Hadir", Settings).
