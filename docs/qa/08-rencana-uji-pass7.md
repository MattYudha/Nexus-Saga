# 08 — Rencana uji pass 7 + acceptance fix `e5f1aa7` (2026-11-13)

> **Status jujur:** verifikasi kode untuk `e5f1aa7` **belum saya lakukan** — upaya baca file ditolak di sesi ini.
> Jadi dokumen ini **bukan** klaim "sudah terverifikasi"; isinya rencana uji yang bisa dijalankan sekarang,
> plus daftar yang harus saya periksa begitu akses baca diizinkan.

---

## A. Acceptance test untuk fix yang baru (jalankan berurutan)

| ID | Langkah uji | Harapan | Bukti yang dicatat |
|---|---|---|---|
| Q60 | Buka build, login guest, catat nama; tutup; buka lagi | **Nama & identitas sama**, bukan "Guest###" baru | screenshot dua sesi + `playerId` di log |
| Q60 | Jalankan build kedua dengan `-nxprofile 2` | Akun berbeda dari build pertama | dua `playerId` berbeda |
| Q60 | Edit file profil → hapus → buka game | Akun guest baru (jalur pemulihan) | perilaku jelas, bukan crash |
| Q61 | 11× `POST /auth/login` dalam 1 menit dari IP sama | 10 pertama diproses, ke-11 **429** | respons + header Retry-After |
| Q61 | 11× `/auth/guest` | 429, **tidak** ada baris Player baru | hitung baris tabel sebelum/sesudah |
| Q62 | Upgrade memakai token guest **tanpa** deviceId yang cocok | **403/409**, username tidak terpasang | akun tetap guest |
| Q63 | Upgrade sambil mengirim `displayName` lain | Nama **tidak berubah** | `/api/me` sebelum/sesudah |
| Q66 | Login username yang tidak ada vs password salah | Waktu respons setara (selisih < 50 ms, uji 20×) | rata-rata & p95 |
| Q71 | Pemain dengan 2 seri + 3 menang: lihat papan | Kolom match = **5**, WR = 3/5 atau 60% sesuai definisi yang dipilih | angka papan vs DB |
| Q76 | Klik "Quick Match" dua kali cepat | **satu** antrean, satu sesi | log backend: satu `/matchmaking/join` |
| Q77 | Klik batal saat "Menyambung" | Tidak masuk match; tidak ada ghost di room | daftar pemain room |
| Q78 | Picu koneksi saat `InMatch` | Ditolak/abaikan | tidak ada sesi kedua |

## B. Tiga area yang belum dipindai (butuh akses baca)

### B1. `Announcements` (endpoint baru + admin)
- Apakah GET publik, POST/DELETE **hanya** admin (`X-Admin-Secret` — utang rilis NX-R3)?
- Validasi panjang teks & encoding: teks ditampilkan di UITK → cek apakah ada jalur HTML/rich text.
- Idempotensi/hapus ganda, urutan tampil, zona waktu `StartsAt/EndsAt`.
- Rate limit untuk POST admin (brute force secret).
- Apakah pengumuman bocor ke pemain sebelum waktunya (filter waktu di server, bukan klien).

### B2. Photon auth callback (`TokenService.TryValidate`)
- **Apakah benar-benar dipasang** ke `ICallbackGameAuth`/`IPhotonPeerListener`? Kalau tidak, siapa pun bisa
  join room Photon dengan AppId tanpa JWT → bypass seluruh kontrol backend.
- Apakah `playerId` hasil validasi dipakai untuk memetakan slot (bukan nama bebas dari klien)?
- Apakah token kedaluwarsa ditolak saat **reconnect** (bukan hanya saat connect pertama)?
- Perilaku bila `Sub` bukan Guid → harus 401, bukan 500.

### B3. `NexusLobbyController` (UI)
- Semua tombol berlabel: berfungsi atau nonaktif + "Segera Hadir" (aturan PROGRESS).
- Settings: nilai tersimpan (PlayerPrefs/profil), diterapkan tanpa restart, dan tidak menimpa profil lain (`-nxprofile`).
- Tombol yang memicu backend: guard klik ganda (keluarga Q76).
- Pemicu layar faksi: harus **setelah hasil match pertama** (2b) — cek apakah masih sebelum lobby.
- Papan/leaderboard: menangani `RankOfAsync` null (Q74).

## C. Hal yang tetap harus diuji manusia (bukan kode)
1. **Tes editor T2 (NX-12)** — 7 langkah; tanpa ini UI lobby, layar hasil, dan pemicu faksi tetap terkunci.
2. **Dua klien nyata** untuk Q76/Q77 dan sinkronisasi `koTimeline`.
3. **Papan setelah 1 hari data nyata** — Q71/Q72 baru terlihat saat ada seri & match disputed.

## D. Yang saya minta izin untuk periksa (read-only)
1. `Program.cs` — bukti rate limiter benar-benar terpasang ke endpoint (bukan hanya dideklarasikan).
2. `ApiEndpoints.cs` — `UpgradeGuest` membandingkan deviceId; `Announcements` guard admin.
3. `NexusGame.cs` / `NexusLobbyController.cs` — profil persisten + penjaga klik ganda.
4. Pemakaian `TryValidate` (Photon callback) — titik paling berisiko bila tidak tersambung.
