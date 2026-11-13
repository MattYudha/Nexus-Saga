# ikemen-extract — mekanik Ikemen GO untuk Nexus Saga (2026-11-13)

Sumber: `C:\Users\US3R\Nexus_Lab\src\Ikemen-GO` tag **v1.0.0** (`81c6da7`, 2026-09-11), lisensi **MIT**.
Metode: **baca source saja** (tidak menjalankan, tidak memodifikasi, tidak mengambil aset karakternya).
Label sama seperti docs/13: **OBSERVED** = fakta Ikemen + `file:baris` · **PROPOSED** = desain kita.

## Kenapa folder ini ada
Tabel kebutuhan di `docs/research/kebutuhan-lostsaga-ayodance.md` punya banyak baris ⬜. Enam dokumen di sini
menutup baris-baris itu dengan angka dan mekanisme yang bisa langsung dipakai, **tanpa** menyentuh client
LostSaga/AyoDance. Gap yang ditutup: input buffer & cancel, juice/hit-feedback, guard-crush-counter-juggle,
replay/anti-desync, hero swap, kamera.

## Isi
| File | Menutup |
|---|---|
| `01-input-buffer-cancel.md` | Input buffer, jendela cancel, combo route, animasi terikat tick |
| `02-juice-hit-feedback.md` | Hitstop, screen shake, hit spark, superpause, slow-mo KO, corner push |
| `03-guard-dizzy-counter-juggle.md` | Guard gauge/crush, dizzy, counter hit, juggle budget |
| `04-replay-spectator.md` | Rekaman input, checksum anti-desync, spectator, killcam |
| `05-hero-swap-tag.md` | TagIn/TagOut, standby, state yang terbawa |
| `06-camera-views.md` | Fighting/Follow/Free view, bounds, zoom |
| `combat-tuning.json` | Angka usulan siap dipakai (tick @60 Hz, fixed-point) |

## Aturan pemakaian (jangan dilanggar)
1. **Turunkan desain, jangan salin kode.** Kalau ada kode MIT yang benar-benar dipakai, wajib simpan notice lisensi.
2. **Tidak ada aset Ikemen** (sprite, suara, karakter KFM) yang masuk game. Yang diambil = struktur & angka.
3. Semua yang berbau **sim** harus fixed-point & deterministik (aturan `Nexus.qtn`). Efek presentasi dipisah.
4. Angka Ikemen adalah **acuan rasa**, bukan hukum. Tuning kita di `combat-tuning.json`, diubah di config, bukan hardcode.

## Peta ke kode kita
`photon-backend/game/Assets/QuantumUser/Simulation/Nexus/Nexus.qtn` sudah punya `HitStun`, `HitPause`,
`GuardGauge`, `Faint`, `SkillCd`, `Invuln`, `HeroId`. Yang **belum** ada dan diusulkan di folder ini:
frame index & frame data, input history/motion buffer, cancel window, juggle counter, `HitId`, `CounterHit`,
`JuiceEvent` (buffer presentasi), replay/checksum. **Jangan tambah field sebelum T2 selesai** (antrean dikunci).
