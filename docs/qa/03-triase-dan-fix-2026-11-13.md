# 03 — Triase & fix laporan tester (Q1–Q41), 2026-11-13

Sumber: `01-laporan-tester-2026-11-13.md` (Q1–Q20) dan `02-laporan-tester-view-input-queue.md` (Q21–Q41),
ditulis sesi DeepSeek. Setiap temuan **dicek ulang ke kode** (`photon-backend` setelah `83c98e0`).

**Catatan penting:** laporan 01 ditulis **sebelum** commit `83c98e0` mendarat, jadi banyak temuan S1 sudah
diperbaiki di sana. Status di bawah memisahkan yang **masih nyata** dari yang **basi**.

Status: ✅ FIX (commit di bawah) · ✔️ BASI (sudah benar di `83c98e0`) · ➖ TIDAK BERLAKU (alasan) ·
📥 INBOX (bukan milestone; masuk BOARD) · ⚖️ KEPUTUSAN USER (bukan bug).

## S1 — integritas data/rating
| ID | Status | Bukti / alasan |
|---|---|---|
| Q1 skor dipalsukan ke 5-4 | ✔️ BASI | Normalisasi dihapus di `83c98e0`; `NexusGame.ReportAsync` melapor skor apa adanya |
| Q2 endReason/winnerSlot/koTimeline tak dikirim | ✔️ BASI | Dikirim sejak `83c98e0` (`NexusGame.cs`, `NexusBackend.ResultReq`) |
| Q3 seri dianggap menang tim A | ✔️ BASI | Pemenang dari `WinnerTeam` sim (seri = 255 → -1), bukan `>=` |
| Q4 durasi pakai jam dinding | ✅ FIX | Durasi = `(f.Number − StartTick) / f.UpdateRate` → deterministik, sama di kedua klien |
| Q5 KoLog 9 vs Battle/Survival | ➖ | `KoTarget=5` untuk SEMUA mode → total KO maks 9. Jadi relevan saat target per mode diubah (lihat Q16) |
| Q6 timeline dibanding sebagai string mentah | ➖ | Backend me-*serialize ulang* list `KoEvent` yang sudah di-parse → kanonik, urutan properti klien tak berpengaruh |
| Q7 seri 255 vs -1 | ✔️ BASI | Pemetaan `WinnerTeam == Draw ? -1` di `NexusGame` |
| Q36 assignment matchmaking tanpa TTL | ✅ FIX | `MatchmakingAssignmentTtlSeconds=60`: klien crash → bisa antre lagi. Tes `ExpiredAssignment_AfterCrash_LetsPlayerQueueAgain` |

## S2 — gameplay
| ID | Status | Bukti / alasan |
|---|---|---|
| Q8 Overload tak mematikan guard | ✔️ BASI | `c->Guarding = 0` saat Overload mulai (`83c98e0`) |
| Q9 AFK saat di-combo | ➖ | AFK hanya bila **tidak ada input** 20 dtk berturut-turut; kena combo sambil menekan tombol tidak dihitung idle. Disengaja: dipukul tidak membuktikan pemain hadir |
| Q10 AFK 10/20 vs 15/30 | ⚖️ | Diputus user 2026-11-13 di sesi ini: **20 dtk** berturut-turut (docs/90). Spek 15/30 sudah ditandai digantikan |
| Q11 timer 100 dtk | ⚖️ | Diputus user (NX-11). Risiko "banyak match selesai karena waktu" sudah dicatat; angka di `NxTuning`, mudah diubah setelah playtest |
| Q12 timer jalan saat hitpause | ➖ | HitPause per-entity; timer = waktu nyata match (standar fighting game). Disengaja |
| Q13 KO & waktu habis di tick sama | ➖ | Urutan deterministik: timer dicek di awal `NxHitSystem` → pada tick terakhir waktu menang. Konsisten di kedua klien; selisih 1 tick |
| Q14 sisa DashTime saat masuk Critical | ➖ | Dash/lunge memberi `Invuln` ≥ `DashTime` → fighter tidak bisa dipukul selama dash, jadi tidak bisa masuk Critical di tengah dash |
| Q21 separation: posisi hampir sama tak didorong | ✅ FIX | Arah fallback sumbu X menurut `EntityRef.Index` (deterministik, berlawanan) |
| Q22 separation saat hitstop | ✅ FIX | Lewati fighter dengan `HitPause > 0` |
| Q26 tahan J = ayunan terus | 📥 | Desain combat (recovery/cooldown serang) — riset `hero-ability/04` (jab recovery). Butuh keputusan angka |
| Q31 rotasi kapsul bertanda negatif | ✅ FIX | `Euler(0, +yaw)` — konvensi sim `(sin, cos)` = Unity. (Tak terlihat pada kapsul simetris, tapi salah untuk model nanti) |
| Q37 penunggu antrean tanpa TTL (pemain hantu) | ✅ FIX | `MatchmakingWaiterStaleSeconds=10` (klien polling ~1 dtk). Tes `StaleWaiter_…` & `PollingWaiter_…` |

## S3/S4
| ID | Status | Catatan |
|---|---|---|
| Q15 TickRate vs UpdateFPS | ✅ FIX (guard) | `NxMatch.Begin` memperingatkan bila `f.UpdateRate != NxTuning.TickRate` |
| Q16 KoTarget 5 semua mode | 📥 | Target per mode saat Battle 3v3 digarap (NX-27); sekaligus perbesar KoLog |
| Q17 OnKo setelah Respawn | ➖ | Aman (Respawn tak menyentuh skor); dicatat |
| Q18 WinnerTeam default 0 | ✅ FIX | Di-set 255 (seri/belum ada) di `OnInit` |
| Q19 klien lama ditolak | ➖ | Tanpa `endReason` backend memakai aturan `ko` → klien lama (selalu 5-x) tetap diterima |
| Q20 respawn tak reset IdleTicks | ➖ | Disengaja (anti-AFK); ada di checklist tes NX-12 #5 |
| Q23 separation asimetris | 📥 | Deterministik; perbaiki saat pushbox per hero (Q24) |
| Q24 MinDist sama semua hero | 📥 | Pushbox per peran (docs/13 §8) |
| Q25 separation tak kecualikan respawn | 📥 | Rendah; spawn tim sudah terpisah ±6 |
| Q27 AimYaw selalu 0 | 📥 | Fitur aim belum ada |
| Q28 gamepad/touch | 📥 | Fitur input |
| Q29 PendingPick statis | 📥 | Hanya relevan untuk 2 pemain lokal (bukan mode saat ini) |
| Q30 ambang analog 0.3 | 📥 | Bersama Q28 |
| Q32 timer HUD saat pilih hero | ✔️ BASI | Blok HUD berada setelah `return` layar pilih hero |
| Q33 detik HUD dari TickRate | ➖ | Sama dengan Q15 (guard) |
| Q34 HUD hanya pemain lokal pertama | ➖ | Satu pemain lokal per klien |
| Q35 penanda off-screen membalik x,y | ➖ | Disengaja: proyeksi titik di belakang kamera terbalik, dibalik agar panah menunjuk benar |
| Q38 komentar slot 0 | ✅ FIX | Komentar diperbaiki ("lawan yang sudah ada di antrean = slot 0") |
| Q39 >1 replika API | 📥 | Sudah tercatat (store bersama/Redis) sebelum scale-out |
| Q40 region "" → 400 tanpa pesan | 📥 | UX kecil |
| Q41 VersionMismatch 200 | ➖ | Klien menangani `state == "VersionMismatch"` (`NexusGame.cs:131`) |

## Verifikasi
- Backend: **87 tes hijau** (+3 matchmaking).
- Game: CodeGen headless + compile `Quantum.Simulation`, `Quantum.Unity`, Assembly-CSharp → lolos.
- Tes editor tetap diperlukan (checklist BOARD NX-12).
