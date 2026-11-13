# BOARD — Nexus Saga: Chronicles (checklist kerja ala Jira)

> **Ini papan kerja harian.** `PROGRESS.md` = urutan terkunci + log · `docs/00-ROADMAP.md` = peta & konflik ·
> `BOARD.md` (file ini) = **tiket yang dicentang**. Diperbarui setiap tiket berubah status.
> Status: ✅ selesai (ada di kode + diverifikasi) · ❌ belum · ⏳ sedang dikerjakan · 🚫 diblok (sebut pemblokir) · ❓ butuh keputusan user
> Terakhir diaudit terhadap kode: **2026-11-13** (grep `photon-backend` @ `9706ec8`).

<!-- FOCUS:START -->
## 🎯 FOKUS SEKARANG (WIP = 1)
**NX-12 — T2: Pulihkan C4** (epic M1, MANDATORI) — ⏳ **kode selesai, menunggu tes editor user** (checklist di NX-12). Sisa: ikon badge (usul dipecah).
Tiket mandatori tersisa di M1: NX-12, NX-13, NX-14, NX-15, NX-16.
**Kerjaan baru apa pun → tulis ke INBOX dulu, JANGAN dikerjakan** sampai M1 ✅ (kecuali user menulis `OVERRIDE`).
<!-- FOCUS:END -->

---

## 🔒 ATURAN FOKUS (gate wajib — berlaku untuk manusia & AI)
1. **WIP = 1.** Hanya satu tiket ⏳ pada satu waktu = tiket di 🎯 FOKUS.
2. **Mandatori dulu.** Tiket epic **M1** harus ✅ semua sebelum tiket M2/INBOX mulai dikerjakan.
3. **Ide/permintaan baru → INBOX**, beri ID `NX-IN-xx`, **tidak dikerjakan**. Pengecualian hanya bila user
   menulis **`OVERRIDE`** (dicatat di LOG + `docs/90` dengan alasannya).
4. **Riset hanya untuk tiket aktif.** Riset domain lain = INBOX. Riset tidak menyentuh kode.
5. **Definisi selesai (DoD):** semua sub-tugas ✅ + tes hijau (backend) / tes editor user (klien) + docs
   diperbarui + lapor ke user → baru tiket di-✅ dan 🎯 FOKUS pindah ke tiket berikutnya.
6. **Tiket ❓ menunggu user** tidak ditebak. Kerjakan sub-tugas yang tidak bergantung, sisanya tunggu.
7. **Bug yang ditemukan saat kerja:** bila merusak tiket aktif → sub-tugas tiket aktif; bila tidak → INBOX.

---

## EPIC M1 — "Ranked 1v1 end-to-end" (MANDATORI)
Login → lobby → ruang ladder → match ranked 1v1 → layar hasil UITK → riwayat & leaderboard konsisten.

### Selesai
| ID | Tiket | Status | Bukti |
|---|---|---|---|
| NX-01 | Login akun + guest, JWT, profil | ✅ | docs/26 |
| NX-02 | Faksi ORDE/LEGION: onboarding, `POST /me/faction`, badge, palet, admin + audit (poin c) | ✅ | editor 2026-11-13, docs/35 |
| NX-03 | Pindah faksi gratis 1× selama placement <5 (`FactionSwitchUsed`) | ✅ | `114216a`, 4 tes |
| NX-04 | Ruang ladder + papan + baris saya | ✅ | docs/27, 33 |
| NX-05 | Match Ranked 1v1 first-to-5 KO, Glicko-2, invariant kills A = deaths B | ✅ | docs/32 |
| NX-06 | Riwayat + Detail Match v2 (mode history) | ✅ | `17b815b`, editor 2026-11-13 |
| NX-07 | Leaderboard: tier rating asli, urut tier → conservative → WR → match | ✅ | `114216a`, tes Gladiator/Rival |
| NX-08 | Semantik warna UI (T1) | ✅ | editor 2026-11-13 |
| NX-09 | Proteksi demosi nonaktif + akun uji eksplisit (poin a, b) | ✅ | docs/33 |
| NX-10 | Audit docs → ROADMAP + Guild→Squad (T3) | ✅ | `69b5afe`, `9706ec8` |

### Belum
#### NX-11 ✅ Keputusan user untuk T2 (prasyarat NX-12) — diputus 2026-11-13
- ✅ AFK = disconnect: **20 dtk tanpa input/terputus → forfeit** (satu angka untuk keduanya)
- ✅ Timer Ranked: **100 dtk** (user; catatan: ~20 dtk/KO → banyak match berakhir karena waktu; nilai di config)
- ✅ Waktu habis & skor KO seri → tie-break: (a) **gear rontok terbanyak kalah** → (b) **darah tersisa paling sedikit kalah** → (c) masih sama = DRAW tanpa rating — **dikonfirmasi user**
<sub>Sumber: `docs/research/battle-flow/01-match-lifecycle.md` §6; keputusan di docs/90 2026-11-13.</sub>

#### NX-12 ⏳ T2 — Pulihkan C4 (KO hanya 3 Break Stock) — 🎯 FOKUS · kode selesai, **menunggu tes editor user**
Legend sub-tugas di sini: ✅ = kode ada + **ter-compile** (CodeGen headless identik Unity + compile 3 assembly) · 🧪 = perlu dibuktikan di editor.
- ✅🧪 Bleed-out dihapus (`CritTimer`/`CritBleedTicks`/`LastHitBy*` dibuang) — KO hanya 3 Break Stock
- ✅🧪 Penalti gerak 70% → 50% → 35%; dash **dan lunge TITAN** dikunci saat Critical
- ✅🧪 Indikator Critical lawan (penanda merah / panah tepi layar, `NexusView`)
- ✅🧪 Overload 8 dtk → terkunci 1,5 dtk (guard lepas, rentan, bukan KO, reset saat kena/guard)
- ✅🧪 Bot prioritas Critical/Overload (+ hitung penumpukan tanpa dirinya sendiri)
- ✅🧪 Batas waktu **100 dtk** + tie-break gear rontok → darah → SERI (`NxMatch.cs`) + timer HUD
- ✅🧪 AFK/disconnect **20 dtk** berturut-turut → forfeit (peringatan HUD 10 dtk); skor tidak dipalsukan; respawn tidak mereset AFK
- ✅🧪 `koTimeline` (array `.qtn` ≤9) → dilaporkan → disimpan per match → dibandingkan antar-klien
- ✅🧪 Tab "Jalannya Match" + label SERI/Waktu habis/WO di Riwayat & Detail Match v2
- ✅ Backend: `endReason`/`winnerSlot`/`koTimeline`, seri tanpa rating, migrasi `AddMatchEndReason` **live** (`ef5b095`), **84 tes hijau**
- ✅ Nilai di `NxTuning.cs` (satu tempat)
- ✅ Docs: docs/32 (§C4 + akhir match) + docs/90; **K-03 ditutup** (menunggu tes)
- ✅ CodeGen: file `Generated/` sudah diperbarui (identik byte dengan CodeGen Unity) → user **tidak wajib** CodeGen manual
- ❌ Tes simulasi otomatis (Critical 30 dtk, Overload, skor tetap) — **belum ada harness Quantum headless**; diganti checklist editor di bawah
- ❌ Ikon per-badge + ikon baris statistik — **belum** (kosmetik; usul dipecah jadi tiket sendiri, menunggu user)
- 🧪 Tes editor user — checklist:
  1. Console bersih setelah Unity import (tanpa error compile)
  2. Ranked/practice 1v1: gerak/guard/hit/KO normal; timer 1:40 turun di atas layar
  3. Lawan Critical tak disentuh 30 dtk → **tidak KO**; tiap 8 dtk muncul OVERLOAD 1,5 dtk; skor tetap
  4. Saat Critical: kecepatan turun per stock; Shift (dash) & K TITAN tidak jalan
  5. Diam 10 dtk → peringatan AFK; 20 dtk → match selesai "AFK — WO", lawan menang
  6. Biarkan waktu habis → "WAKTU HABIS — … MENANG/SERI"; Riwayat menampilkan label + tab **Jalannya Match** berisi urutan KO
  7. Practice vs bot: bot mengejar target Critical

#### NX-13 ❌ Poin d — UI Lobby
- ❌ Settings 1.6: tab Grafis / Audio / Kontrol / Antarmuka / Akun+Logout, simpan lokal, langsung diterapkan (overlay sekarang kosong, `LobbyMain.uxml:50`)
- ❌ Lobby 1.7: hero terakhir di tengah
- ❌ Lobby 1.7: panel Pengumuman/Event + endpoint `/api/announcements`
- ❌ Semua tombol belum berfungsi → nonaktif + "Segera Hadir" (Shop, Inventory, Hero Deck, Quest, Event, Squad, Mail, HQ, Plaza)
- ❌ Slider = Ranked / Battle 3v3 / 1 teaser "Segera Hadir"
- ❌ Tombol Street Room di samping HQ/Plaza

#### NX-14 ❌ Poin e — Layar hasil pasca-match
- ❌ `NexusGame` memanggil Detail Match v2 `DetailMode.Result` (animasi Poin Ladder, "NAIK TIER!")
- ❌ Hapus layar hasil IMGUI (`NexusGame.cs:443 OnGUI`)

#### NX-15 ❌ Pemicu layar faksi → setelah hasil match pertama
- ❌ Pindahkan pemicu (bergantung NX-14); layar + backend dipakai ulang

#### NX-16 🚫 Guest → daftar akun membawa faksi/rating/riwayat (**K-10**)
- ❓ Keputusan user (usul: endpoint upgrade guest→akun)
- ❌ Implementasi + tes

---

## EPIC M2 — Setelah milestone (ANTRE — jangan mulai sebelum M1 ✅)
| ID | Tiket | Status | Catatan |
|---|---|---|---|
| NX-20 | Poin f — UI Tab Statistik baru (ring Flawless, grid mekanik, radar) | ❌ | backend radar sudah ada (`StatsEndpoints.cs`) |
| NX-21 | Poin g — kartu Disputed "TIDAK DIHITUNG" di UI | ❌ | backend sudah menandai |
| NX-22 | 1.4 Tab Hero Favorit (agregasi per hero) | ❌ ❓ | **terlewat dari antrean a–h** — posisi menunggu user (usul: setelah NX-14) |
| NX-23 | Poin h — Fase 2: presence, chat ALL/PARTY/SQUAD/ROOM, teman | 🚫 | **K-11** stack realtime |
| NX-24 | Fase 3 — Party | ❌ | docs/29 |
| NX-25 | Fase 4 — Squad | 🚫 | **K-09** format Squad War |
| NX-26 | Fase 5 — Mail | ❌ | docs/31 |
| NX-27 | Battle 3v3 santai (bot isi slot) | ❌ | docs/24 §10a |
| NX-28 | Street Room — room browser 1v1–3v3 | ❌ | tombolnya di NX-13 |
| NX-29 | Survival 1v1/3v3 | 🚫 | **K-12** papan poin |
| NX-30 | Faction War / Nexus Cup 5v5 | ❌ | Fase 3+ |

## EPIC R — Utang wajib sebelum rilis
| ID | Tiket | Status |
|---|---|---|
| NX-R1 | Admin berbasis role (ganti `X-Admin-Secret`) — docs/91 #10 | ❌ |
| NX-R2 | Aktifkan kembali proteksi demosi `grace=3` — docs/33 | ❌ |

---

## ❓ KEPUTUSAN MENUNGGU USER
| # | Keputusan | Menghambat | Usul |
|---|---|---|---|
| D1 | ~~Ambang AFK/disconnect~~ | NX-12 | ✅ **20 dtk → forfeit** (2026-11-13) |
| D2 | ~~Timer Ranked~~ | NX-12 | ✅ **100 dtk** (2026-11-13) |
| D3 | ~~Waktu habis seri~~ | NX-12 | ✅ **gear rontok → darah → DRAW** (2026-11-13) |
| D4 | K-10 guest → akun | NX-16 | endpoint upgrade |
| D5 | Posisi Hero Favorit di antrean | NX-22 | setelah NX-14 |
| D6 | Model juggle (S1 vs per-penyerang) | tuning combat | S1 |
| D7 | K-09 format Squad War | NX-25 | rebut distrik |
| D8 | K-11 stack realtime | NX-23 | SignalR |
| D9 | K-12 papan Survival | NX-29 | tunda |
| D10 | Pause & rematch (battle-flow §6 #4–5) | M2 | tanpa pause Ranked; rematch casual saja |
| D11 | Effekseer vs VFX bawaan Unity | fase aset | tunda |

---

## 📥 INBOX (ide/permintaan baru — TIDAK dikerjakan sampai M1 ✅)
| ID | Isi | Asal |
|---|---|---|
| NX-IN-01 | Riset domain lain di `docs/research/backlog-riset-logic.md` (room, matchmaking, animasi, map, sound, VFX, ekonomi) | backlog riset |
| NX-IN-02 | Input buffer/cancel/juice dari `ikemen-extract` → implementasi (draf `07-patch-qtn.md` ditahan) | riset Ikemen |
| NX-IN-03 | Kit hero data-driven (`hero-ability/04`), ultimate, modifier | riset hero-ability |
| NX-IN-04 | Replay, spectator, killcam | riset Ikemen 04 |
| NX-IN-05 | **Mode Deathmatch ala LostSaga** (tafsiran dikoreksi user): waktu habis → **darah semua jadi 0**; setelah itu tiap pukulan **merontokkan gear satu per satu** (kepala, aksesoris, baju, senjata, dst). Pemain yang **gear-nya habis duluan kalah**. Mirip mekanik Break Stock kita | user 2026-11-13 |

---

## LOG BOARD
- 2026-11-13: BOARD dibuat dari audit PROGRESS + docs/31 + ROADMAP + grep kode. Fokus = NX-12 (T2).
- 2026-11-13: NX-11 ✅. NX-12 kode selesai (lanjutan kode sesi DeepSeek + 5 bug diperbaiki + timer/tie-break/koTimeline/HUD/Riwayat), backend live, 84 tes; menunggu tes editor.
