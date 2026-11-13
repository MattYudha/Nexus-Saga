# 00 — ROADMAP Nexus Saga: Chronicles (audit T3, 2026-11-13)

> **Cara baca.** Dokumen ini = **peta** (apa yang selesai, apa berikutnya, apa yang bertentangan).
> **Urutan kerja yang mengikat** tetap di `PROGRESS.md` (dikunci user). Keputusan resmi di `docs/90`.
> Status: **Selesai** · **Sedang** · **Antre** · **Diblok** (sebutkan pemblokir).
> Hasil audit docs 13–36, 90, 91 (T3). Konflik baru **tidak diputus sendiri** — lihat §3.

---

## 1. MILESTONE AKTIF — "Ranked 1v1 end-to-end"
Satu pemain bisa: **login → lobby → ruang ladder → match ranked 1v1 → layar hasil (UITK) → riwayat & leaderboard konsisten**, tanpa data dummy dan tanpa tombol palsu.

| # | Langkah alur | Item kerja (antrean PROGRESS) | Status | Catatan / pemblokir |
|---|---|---|---|---|
| 1 | Login | Akun username + guest, JWT, profil | **Selesai** | docs/26 (Postgres persisten). Akun uji eksplisit (poin b). |
| 2 | Faksi | Onboarding ORDE/LEGION, badge, PALET 4, audit admin (poin c) | **Selesai** | Diverifikasi editor 2026-11-13. docs/35. |
| 2a | Faksi | Pindah gratis 1× selama placement (`FactionSwitchUsed`) | **Selesai** | T3-6, backend + 4 tes, live. |
| 2b | Faksi | Pindahkan **pemicu** layar faksi ke **setelah hasil match pertama** | **Antre** | Bergantung #6 (layar hasil UITK, poin e). |
| 2c | Faksi | Guest → daftar akun: faksi terbawa | **Sedang** — backend selesai | K-10 diputus (opsi a): `POST /api/auth/upgrade`, live, 2 tes. UI tombol "Daftarkan akun" ikut Settings (poin d). |
| 3 | Lobby | Settings (1.6), lobby tidak kosong (1.7), tombol "Segera Hadir" | **Antre** | **Poin d**. Termasuk slider Ranked/Battle/teaser + tombol Street Room (T3-5). |
| 4 | Ruang ladder | Ruang ladder (struktur Lost Saga), papan + baris saya | **Selesai** | docs/27, docs/33. |
| 5 | Match | Ranked 1v1 first-to-5 KO, Glicko-2, invariant kills A = deaths B | **Selesai** | docs/32. |
| 5a | Match | **Pulihkan C4**: KO hanya 3 Break Stock (buang bleed-out), penalti bertingkat, Overload, bot prioritas Critical, AFK forfeit, `koTimeline`, timer 100 dtk + tie-break | **Sedang — kode selesai, menunggu tes editor** | NX-11 diputus (AFK 20 dtk, timer 100 dtk, gear→darah→seri). Backend live. Checklist di BOARD NX-12. |
| 6 | Layar hasil | Detail Match v2 sebagai **layar hasil** (mode `result`) menggantikan IMGUI | **Antre** | **Poin e**. Komponen dua mode sudah siap & terverifikasi (mode history). |
| 7 | Riwayat | Tab Riwayat + Detail Match v2 | **Selesai** | Diverifikasi editor 2026-11-13. docs/34. Tab "Jalannya Match" menunggu `koTimeline` (T2). |
| 8 | Leaderboard | Tier dari rating asli; urut tier → conservative → WR → match | **Selesai** | T3-2, tes Gladiator vs Rival. docs/33. |
| 9 | Warna | Semantik warna UI (token `--nx-*`) | **Selesai** | T1, diverifikasi editor. docs/90. |
| 10 | Docs | Audit + roadmap ini | **Selesai** | T3. |

**Urutan sisa milestone:** T2 (5a) → poin d (3) → poin e (6, lalu 2b). Milestone tuntas bila #2b, #3, #5a, #6 selesai (dan K-10 diputus).

---

## 2. SETELAH MILESTONE
| Item | Status | Sumber / catatan |
|---|---|---|
| **Poin f** — Tab Statistik baru (ring Flawless, grid mekanik, radar) | Antre | docs/32 |
| **Poin g** — Kartu Disputed "TIDAK DIHITUNG" | Antre | docs/32 KEAMANAN |
| **Poin h** — Fase 2 sosial: presence, chat (ALL/PARTY/SQUAD/ROOM), teman | **Diblok** | **K-11 / docs/36** — pilih Photon Chat / SignalR / Nakama dulu |
| Fase 3 — Party (Ruang Tim tahap 2–4) | Antre | docs/29, docs/31 |
| Fase 4 — **Squad** (dulu "Guild") | Antre | docs/16; format Squad War = **K-09** |
| Fase 5 — Mail | Antre | docs/31 |
| Ikon per-badge + ikon baris statistik | Antre | Dikerjakan bersama T2 |
| Survival 1v1/3v3 (Race-to-6) | Antre | docs/24 §5a; papan poin = **K-12** |
| Battle 3v3 santai (bot isi slot) di slider | Antre | Bagian poin d (T3-5) |
| Street Room (room browser 1v1–3v3) | Antre | Bagian poin d (T3-5) |
| Faction War, Nexus Cup (5v5) | Antre (Fase 3+) | docs/24 §10 |
| Squad War + Squad Shop, Relic | Antre (Fase 3) | docs/24, K-09 |
| Sistem season (buka kunci faksi otomatis) | Antre | docs/35 |
| **Utang rilis**: admin berbasis role (ganti `X-Admin-Secret`) | Antre (wajib sebelum rilis) | docs/91 #10 |
| **Utang rilis**: aktifkan kembali proteksi demosi (`grace=3`) | Antre (wajib sebelum rilis) | docs/33 |

---

## 3. KONFLIK DITEMUKAN
| ID | Dokumen A | Dokumen B | Isi konflik | Resolusi | Status |
|---|---|---|---|---|---|
| K-01 | docs/90 (2026-10-24 "MVP 1v1 & 2v2"; 2026-10-26 "MVP tetap 1v1+2v2"; "Mode MVP Survival + TDM") | docs/24 §10 (MVP = Solo 1v1 + Street Room) | Mode MVP | T3-5: 2v2 dicabut; slider Ranked/Battle/teaser; Street Room = room browser | **Selesai** |
| K-02 | docs/24 §5 ("Survival berlaku utk 1v1 Solo Ranked") | docs/32 (Ranked = first-to-5 KO tanpa ronde) | Format Solo Ranked | T3-1: Solo Ladder ≠ Survival (docs/24 §5a) | **Selesai** |
| K-03 | docs/32 (bleed-out → auto-KO + kill ke penyerang terakhir); docs/90 2026-10-27 (fix respawn bleed-out; deaths termasuk bleed-out) | docs/90 2026-10-24 C4 ("penalti gerak/dash + indikator posisi, **tanpa bleed-out**") | Jalan KO selain 3 Break Stock | Diputus user: pulihkan C4 (T2). Kode + docs/32 diperbarui 2026-11-13 | **Selesai di kode — menunggu tes editor** |
| K-04 | docs/31 ("grace=3") | docs/33, PROGRESS (NONAKTIF, grace=0) | Status proteksi demosi | T3-7: docs/31 dikoreksi | **Selesai** |
| K-05 | docs/33 §2 + `LeaderboardService` (urut conservative murni) | Keputusan T3-2 | Tier di papan bisa terbalik | Kode + tes + docs/33 | **Selesai** |
| K-06 | docs/33 §2 ("conservative HANYA utk posisi") | docs/33 Proteksi demosi ("leaderboard base = conservative") | Kontradiksi internal (sisa sebelum poin a) | Kalimat basi diperbaiki: base = rating asli | **Selesai** |
| K-07 | docs/35 ("terkunci satu season", `FactionLocked`, onboarding sebelum lobby); docs/24 §3 ("ganti faksi cooldown per season") | Keputusan T3-6 | Aturan pindah & pemicu layar faksi | Backend + docs selesai; pemicu klien menunggu poin e | **Selesai (docs/backend)** · pemicu **Antre** |
| K-08 | docs/14, 24, 27, 31, 36, PROGRESS, UI ("Guild") | docs/16 ("Squad = guild/clan") | Penamaan | T3-4: Guild → Squad di semua docs/UI/chat | **Selesai** |
| K-09 🆕 | docs/24 §2 #2, §4 ("Squad War = rebut distrik, **TIDAK dihapus**"), koreksi L23 ("Guild War dihapus") | docs/24 §11 ("Guild War + Squad Shop; Squad War distrik **opsional**"), §12 Q5 (masih terbuka); docs/90 2026-10-26 ("Guild War → Guild Board") | **Format Squad War**: perebutan distrik Plaza, match squad-vs-squad langsung, atau keduanya? | Usul: ikuti §4/L23 (Squad War = district conquest, tanpa mode guild-match terpisah). **Tidak diputus sendiri.** | **Menunggu user** |
| K-10 🆕 | Keputusan T3-6 ("Guest → daftar akun: faksi ikut terbawa") | Kode `POST /auth/register` (selalu membuat Player **baru**; tak ada jalur upgrade guest) | Faksi — dan juga rating/riwayat guest — **hilang** saat guest mendaftar | **Diputus (a)** 2026-11-13: `POST /api/auth/upgrade` → Player sama, progres terbawa, deviceId dilepas | **Selesai (backend)** · UI di poin d |
| K-11 | docs/90 (2026-10-24 stack "+ Nakama"; 2026-10-26 Plaza/Excavation = Nakama; split-session routing); docs/14, 15, 16, 18, 19, 20, 22 (meta = Nakama) | Realita: ASP.NET `PhotonBackend.Api` sudah sumber kebenaran akun/rating/faksi/leaderboard (docs/36) | Dua sumber identitas bila Nakama diadopsi | docs/36 condong SignalR; Nakama hanya kandidat Plaza/Excavation. Docs 14–22 **tidak diubah** sampai diputus | **Menunggu user (docs/36)** |
| K-12 🆕 | docs/90 2026-10-26 ("alokasi poin per mode": Solo/F-War/Squad War/Custom) | docs/24 §5/§5a (Survival ada, papan tak disebut) | Survival memberi poin ke papan mana? | Tidak mendesak (Survival setelah MVP) | **Menunggu user** |
| K-13 | docs/24 §2 #4 (Street Room 1v1–5v5) | Keputusan T3-5 (1v1–3v3) | Kapasitas Street Room | docs/24 §2 diselaraskan | **Selesai** |
| K-14 | docs/24 §2 ("empat jalur, binding" — tanpa Battle) | Kode (`mode=1` Battle, filter Riwayat) + T3-5 | Battle tak tercatat sebagai jalur | T3-5: Battle = antrean kasual 3v3 (EXP/Gold, tanpa MMR); docs/24 §10a | **Selesai** |

---

## 4. YANG PERLU DIPUTUSKAN USER
1. **K-09** — Format Squad War (usul: rebut distrik, ikuti §4).
2. **K-10** — Guest → akun (usul: endpoint upgrade agar faksi + rating + riwayat terbawa).
3. **K-11 / docs/36** — Realtime Fase 2 (usul: SignalR; Nakama dicabut untuk meta inti).
4. **K-12** — Papan poin Survival (boleh ditunda sampai Survival digarap).
5. **T2** — Angka final AFK forfeit (diajukan saat T2 dimulai).
