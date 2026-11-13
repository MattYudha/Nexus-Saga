# 00 — PROMPT SESI BERIKUTNYA (2026-11-13)

## Cara menjalankan
```bash
cd C:\Users\US3R\NyxCreats
claude --continue
```
`--continue` melanjutkan percakapan **terakhir di folder itu**. Semua kerja hari ini berjalan dengan
working directory `C:\Users\US3R\NyxCreats`, jadi perintah di atas melanjutkan thread yang sama.

Kalau `--continue` tidak menemukan sesi (mesin lain / sesi kedaluwarsa):
```bash
cd C:\Users\US3R\NyxCreats
claude
```
lalu tempel prompt di bawah.
`claude --resume` menampilkan daftar sesi kalau ingin memilih manual.

**Catatan folder:** kode ada di `C:\Users\US3R\photon-backend` (repo terpisah). Sesi Claude Code terikat
per-folder — untuk melanjutkan diskusi docs/riset/QA, jalankan di `NyxCreats`.

---

## PROMPT (tempel apa adanya)

```
Peran: TESTER + peneliti untuk Nexus Saga. Baca dulu, jangan langsung kerja:
PROGRESS.md, docs/00-CHECKLIST.md (§C3 = status implementasi), docs/00-ROADMAP.md,
docs/90-decision-log.md, docs/qa/ (01–11), docs/research/ (ikemen-extract, hero-ability,
battle-flow, t2-spec).

Status per 2026-11-13:
- Klien (Quantum): T2 + poin d + poin e + ikon NX-12 + NX-21/NX-22 UI = kode selesai,
  BELUM dites di editor. Single blocker: tes editor M1 (NX-12..NX-16).
- Backend: D12 (RD policy), D13 (badge), D14 (nama), D15 (rate limit), Disputed reason,
  /api/me/heroes = live, 126 tes hijau.
- Repo: docs → github.com/MattYudha/Nexus-Saga (pushed).
  Kode → github.com/MattYudha/Nexuws-Backend (pushed, upstream `mine`).
  `origin` backend menunjuk cds-id/photon-backend — JANGAN push ke sana (bukan repo kita).

Aturan:
1. Jangan implementasi/ubah kode tanpa izin eksplisit. Default: analisis + dokumen.
2. Setiap temuan wajib label OBSERVED (file:baris) / DERIVED / PROPOSED. Jangan mengarang.
3. Jangan push ke `origin` backend. Hanya `mine`.
4. WIP=1: M1 harus lolos tes editor sebelum M2 dilanjutkan (kecuali user menulis OVERRIDE).
5. Jangan ekstrak aset/bongkar anti-cheat dari client komersial.

Tugas berurut:
A. Verifikasi ulang fix di commit 3062696: Q86 (homoglyph Kiril), Q87 (NFKC/fullwidth),
   Q89 (nama simbol), Q91 (race nama guest → dulu 500).
B. Temuan terbuka: Q92 (papan: Matches vs WinRate beda basis), Q93 (/me vs papan),
   Q94 (bukti guard klik ganda), Q48/Q49 (RD — sudah D12, pastikan), Q67/Q73/Q75 (cache & skala).
C. Periksa M2 yang belum diaudit: alasan Disputed benar-benar tersimpan + tampil,
   statistik/papan hanya menghitung Finished, /api/me/heroes (akurasi + performa).
D. Keamanan: `appsettings.Development.json` ter-track berisi JWT/webhook/auth secret asli →
   susun langkah rotasi + placeholder (tanpa mengubah histori tanpa izin).
E. Siapkan daftar langkah tes editor M1 yang bisa dijalankan user tanpa saya.

Lapor ringkas: apa yang diverifikasi, apa yang masih ⏳, temuan baru ber-ID (Q95+).
```

---

## Ringkasan kondisi repo (untuk verifikasi cepat)
| Repo | Remote | Ujung |
|---|---|---|
| `NyxCreats` (docs) | `origin` = MattYudha/Nexus-Saga | `e3d0864` |
| `photon-backend` (kode) | `mine` = MattYudha/Nexuws-Backend | `4486257` |
| `photon-backend` | `origin` = cds-id/photon-backend | `7916a52` (**jangan push**) |

## Utang yang jangan hilang
- Rotasi 3 secret + pindah ke `.env`/user-secrets.
- **NX-R3**: JWT `jti` + revokasi (logout semua perangkat).
- Ikon statistik baris ke-9 memakai ikon lama — cek keseragaman saat tes editor.
