# 02 — QA pass 2: View, Input, Separation, Matchmaking (2026-11-13)

Lanjutan `01-laporan-tester-2026-11-13.md`. Baca-saja, tanpa ubah kode. ID lanjut dari Q20.

---

## A. NxSeparationSystem (pushbox)

| ID | Sev | Lokasi | Temuan | Dampak |
|---|---|---|---|---|
| **Q21** | S2 | `NxSeparationSystem.cs:27` | `if (dist <= FP._0_10) continue;` — dua fighter di posisi **hampir sama** dilewati, bukan didorong | Musuh/teammate yang spawn/respawn di titik sama **menumpuk permanen** (tidak pernah pisah) |
| **Q22** | S2 | `NxSeparationSystem.cs:18` | Hanya cek `State == 1`, **tidak cek `HitPause`** | Saat hitstop (game "beku"), badan tetap bergeser → melanggar aturan hitpause membekukan semua; juga menggeser korban keluar hitbox di tengah kombo |
| **Q23** | S3 | `NxSeparationSystem.cs:30` | `Pos` diubah **di dalam** loop bersarang | Koreksi pasangan A-B memengaruhi perhitungan B-C pada tick yang sama; deterministik tapi asimetris (yang diiterasi lebih dulu terdorong lebih banyak) |
| **Q24** | S3 | `NxSeparationSystem.cs:11` | `MinDist` tetap 1.5 untuk semua | Pushbox tidak mengikuti ukuran hero/gear (docs/13 §8 minta cylinder per peran); hero berat sama dengan zoner |
| **Q25** | S3 | `NxSeparationSystem.cs:22` | Tidak mengecualikan yang `Invuln`/baru respawn | Pemain yang baru respawn langsung terdesak, bisa didorong keluar zona spawn |

## B. NexusInput (klien)

| ID | Sev | Lokasi | Temuan | Dampak |
|---|---|---|---|---|
| **Q26** | S2 | `NexusInput.cs:47-57` | Tombol dibaca dengan `GetKey` (ditahan), bukan `GetKeyDown`; TITAN tidak punya cooldown serang | **Menahan J = ayunan terus-menerus** tiap kali `AttackTime` habis → spam tanpa ritme, mempermudah stunlock |
| **Q27** | S3 | `NexusInput.cs:33` | `AimYaw = 0` selalu | Field input `AimYaw` mati; klaim "aim 8 arah" di docs belum ada |
| **Q28** | S3 | `NexusInput.cs:1-65` | Keyboard saja | Gamepad/touch (docs/06, kebutuhan A) belum ada; tidak ada pengujian input alternatif |
| **Q29** | S4 | `NexusInput.cs:18` | `PendingPick` statis | Dalam satu proses dengan 2 pemain lokal, keduanya memilih hero yang sama |
| **Q30** | S4 | `NexusInput.cs:39-42` | Ambang `0.3` pada axis analog | Input diagonal bisa terbaca kartinal saat nilai sumbu rendah (mis. 0.29) → arah "berkedip" |

## C. NexusView (presentasi)

| ID | Sev | Lokasi | Temuan | Dampak |
|---|---|---|---|---|
| **Q31** | S2 | `NexusView.cs:80` | Rotasi kapsul `Euler(0, -yaw*Rad2Deg, 0)` — **tanda negatif**; sim memakai forward `(sin yaw, cos yaw)` | Arah hadap **tercermin** di layar; pemain membaca arah serangan/guard dengan keliru |
| **Q32** | S3 | `NexusView.cs:195-200` | Blok HUD timer/AFK berjalan juga saat `State == 0` | Layar pilih hero menampilkan `0:00` dan bar timer kosong |
| **Q33** | S3 | `NexusView.cs:188` | Detik di HUD dihitung dengan `NxTuning.TickRate` | Bila FPS sesi ≠ `TickRate`, waktu yang ditampilkan salah (terkait Q15) |
| **Q34** | S3 | `NexusView.cs:198` | `locals[0]` untuk menentukan "saya" | Uji lokal 2 pemain → hanya pemain pertama dapat HUD AFK/Critical |
| **Q35** | S4 | `NexusView.cs:229-232` | Penanda off-screen membalik `x` **dan** `y` saat `behind` | Panah penanda bisa muncul di kuadran salah |

## D. Matchmaking (backend)

| ID | Sev | Lokasi | Temuan | Dampak |
|---|---|---|---|---|
| **Q36** | **S1** | `MatchmakingService.cs:76-80`, cleanup hanya `:97-98` | `_assignments` **tanpa TTL**. Dibersihkan hanya bila klien memanggil `/matchmaking/leave` | Klien yang crash/force-close tetap punya assignment; `Join` berikutnya mengembalikan **match lama** terus-menerus → pemain tidak bisa antre lagi (stuck permanen) |
| **Q37** | S2 | `MatchmakingService.cs:29` | `_waiting` juga tanpa TTL | Antrean bocor (memori) dan pemain "hantu" bisa dipasangkan setelah `MaxWait` walau sudah menutup game |
| **Q38** | S3 | `MatchmakingService.cs:78-79` vs komentar `:78` | Komentar "yang menunggu lebih dulu = slot 0", kenyataannya slot 0 diberikan ke lawan dengan **rating terdekat** | Slot biru/oranye tidak stabil → menyulitkan reproduksi laporan bug & statistik per slot |
| **Q39** | S3 | `MatchmakingService.cs:19` | Komentar menyatakan in-process hanya valid 1 replika | Deploy >1 instance → dua pemain di replika berbeda **tidak akan pernah bertemu**, tanpa error |
| **Q40** | S3 | `ApiEndpoints.cs:211` | `region` wajib 1-32 karakter; klien mengirim apa adanya | Bila klien mengirim `""` (mis. dari config kosong) → 400 tanpa pesan jelas di UI |
| **Q41** | S3 | `ApiEndpoints.cs:220-221` | `VersionMismatch` dikembalikan sebagai **200 OK** dengan `state`, bukan error | Klien yang tidak menangani `state` akan terus polling selamanya |

---

## E. Ringkasan prioritas
1. **Q36** (assignment tanpa TTL) — pemain bisa terkunci permanen. Paling mendesak setelah Q1–Q3.
2. **Q21/Q22** (separation skip & jalan saat hitpause) — merusak combat feel dan stacking.
3. **Q31** (arah hadap tercermin) — salah baca visual, murah diperbaiki.
4. **Q26** (auto-swing) — memengaruhi balancing TITAN.
5. Sisanya konsistensi/TTL/UX.

## F. Catatan metode
Temuan dari pembacaan kode; Q21, Q22, Q26, Q31, Q36 butuh reproduksi di editor/2 instance.
