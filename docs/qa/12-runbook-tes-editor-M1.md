# 12 — RUNBOOK TES EDITOR M1 (NX-12…NX-16) — 2026-11-16

> Tujuan: satu sesi tes (~30–40 mnt) yang **membuka M1**. Jalankan berurutan, isi kolom **Hasil**.
> Semua langkah diturunkan dari checklist BOARD NX-12..NX-16. Tombol dari `NexusInput.cs`.
> Aku tak bisa menjalankan Unity — ini untuk kamu eksekusi; lapor balik yang GAGAL saja.

## 0. Setup
| Hal | Nilai |
|---|---|
| Scene online | `Assets/Scenes/NexusOnline.unity` |
| Build kedua di 1 PC | jalankan `.exe` dengan argumen **`-nxprofile 2`** (profil guest berbeda) |
| Editor | otomatis profil `editor` (akun beda dari build) |
| Tombol | Gerak **WASD/panah** · Serang **J** · Skill **K** · Lompat **Space** · Dash **Shift kiri** · Guard **L** · Ganti hero **H** |
| Backend | pastikan API live (`/api/factions` membalas) sebelum mulai |

Cara match 1v1: jalankan **editor** + **build (`-nxprofile 2`)**, keduanya Quick Match → saling ketemu.
Praktik vs bot: satu klien saja, mode practice (bot mengisi lawan).

---

## A. NX-12 — T2 combat (inti M1)
| # | Langkah | Harapan | Hasil |
|---|---------|---------|-------|
| 1 | Import selesai, lihat Console | **tanpa error compile** | ☐ |
| 2 | Mulai 1v1, amati atas layar | timer **1:40** turun; gerak/guard(L)/hit(J)/KO normal | ☐ |
| 3 | Buat lawan Critical, **jangan sentuh 30 dtk** | **TIDAK KO**; tiap 8 dtk muncul **OVERLOAD 1,5 dtk**; skor tetap | ☐ |
| 4 | Saat kamu Critical, coba gerak | kecepatan turun per stock (70→50→35%); **Shift & K TITAN tidak jalan** | ☐ |
| 5 | Diam total (tanpa WASD/J/K/Space/Shift/L) | 60 dtk → peringatan AFK di HUD; **75 dtk → "AFK — WO"**, lawan menang | ☐ |
| 6 | Main biasa, biarkan **timer habis** | "WAKTU HABIS — … MENANG" atau "SERI"; Riwayat punya label + tab **Jalannya Match** (urutan KO) | ☐ |
| 7 | Practice vs bot, buat 1 bot Critical | bot **mengejar target Critical**, bukan yang sehat | ☐ |
| 8 | 1v1 penuh sampai 5 KO | menang di 5 KO; Detail Match v2 muncul; `koTimeline` konsisten dua klien | ☐ |

**Watch (QA):** langkah 5 — pastikan **guard (L) ditahan terus TIDAK** memicu AFK (desain: guard = aktif). Langkah 3 — Overload **tidak menambah damage** (hanya lock).

## B. NX-13 — UI Lobby (poin d)
| # | Langkah | Harapan | Hasil |
|---|---------|---------|-------|
| 1 | Buka Settings (gear), ubah VSync/FPS/kualitas/volume | **langsung berubah**; restart → **tetap** (PlayerPrefs) | ☐ |
| 2 | Esc di Settings | menutup | ☐ |
| 3 | Tab Akun (guest) | nama/ID + salin + **"Daftarkan akun"** (hanya guest) | ☐ |
| 4 | Lobby | hero terakhir di tengah (default TITAN-01); panel Pengumuman kiri-atas | ☐ |
| 5 | Pengumuman kosong vs server mati | "Belum ada pengumuman" vs **"Gagal memuat"** (beda — Q45) | ☐ |
| 6 | Klik Shop/Inventory/Squad/Mail/HQ/Plaza/STREET | nonaktif + **SEGERA HADIR**; tombol "+" mata uang tersembunyi | ☐ |
| 7 | Slider mode | RANKED / BATTLE / teaser FACTION WAR (MAIN nonaktif), **3 titik** | ☐ |

## C. NX-14 — Layar hasil (poin e)
| # | Langkah | Harapan | Hasil |
|---|---------|---------|-------|
| 1 | Selesaikan 1 match | banner ~1,5 dtk → keluar room → halaman **Result** | ☐ |
| 2 | Di Result | Detail Match v2 (animasi Poin Ladder, "NAIK TIER!" bila naik), tombol **LANJUT/Enter/Esc → lobby** | ☐ |
| 3 | Match tak tercatat/Disputed (paksa 2 klien skor beda) | ringkasan teks + **alasan jujur** + LANJUT (bukan layar kosong) | ☐ |

## D. NX-15 — Pemicu faksi setelah match pertama
| # | Langkah | Harapan | Hasil |
|---|---------|---------|-------|
| 1 | Akun baru tanpa faksi, **belum pernah match** | langsung ke lobby, **tanpa** layar faksi | ☐ |
| 2 | Selesaikan match pertama → LANJUT | **layar faksi muncul** di sini (bukan sebelum lobby) | ☐ |
| 3 | Pilih ORDE/LEGION | badge faksi konsisten (top bar + profil) | ☐ |

## E. NX-16 — Guest → daftar akun (K-10)
| # | Langkah | Harapan | Hasil |
|---|---------|---------|-------|
| 1 | Guest: catat faksi + rating + 1 match di Riwayat | — | ☐ |
| 2 | Settings › Akun › **Daftarkan akun** (username+password) | sukses; **faksi/rating/riwayat tetap** (Player sama) | ☐ |
| 3 | Logout → login username baru | masuk ke akun yang sama (deviceId sudah dilepas) | ☐ |
| 4 | Coba upgrade lagi | ditolak 409 (sudah terdaftar) | ☐ |

**Watch (QA Q63):** di langkah 2, kamu **tidak** bisa mengganti display name lewat upgrade.

---

## F. Bonus — amati temuan QA terbuka saat tes (tanpa langkah khusus)
- **Q86** daftar akun bernama `Аdmin` (A Kiril) → harusnya **ditolak** (homoglyph). Kalau lolos → bug masih ada.
- **Q92/Q93** bandingkan angka **"match" & "win rate"** di papan vs tab Profil → harus sama; beda = Q93.
- **Q94** klik **Quick Match 2× cepat** → hanya satu antrean (bukan dua).

## G. Keputusan setelah tes
- Semua ☐ di A–E jadi ✅ → **M1 LOLOS**: centang NX-12..NX-16 di BOARD, pindah FOKUS ke M2 (NX-20/21/22).
- Ada yang GAGAL → lapor nomornya saja; itu jadi tiket fix (tetap di dalam M1, bukan kerja baru).
