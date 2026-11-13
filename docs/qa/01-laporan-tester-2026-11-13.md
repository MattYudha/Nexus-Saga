# 01 — Laporan tester: scan bug & gap (2026-11-13)

Peran: **tester**. Metode: baca kode (tidak mengubah apa pun), bandingkan dengan keputusan user
(`docs/90`, `PROGRESS.md`) dan kontrak backend. Semua temuan berlabel lokasi `file:baris`.

Severity: **S1** = data/rating rusak · **S2** = gameplay salah · **S3** = konsistensi/risiko · **S4** = catatan.

---

## A. Ringkasan eksekutif
1. **Kontrak klien↔backend tidak sinkron.** Backend sudah punya `EndReason`/`WinnerSlot`/`KoTimeline`
   dan memvalidasinya; klien **tidak mengirim satu pun** dari itu, dan masih **memanipulasi skor** ke 5-4.
2. Akibatnya match **seri** tercatat sebagai **menang 5-4**, match **waktu habis** dan **forfeit** juga
   tercatat sebagai **KO**, dan rating dihitung untuk hasil yang tidak pernah terjadi.
3. `koTimeline` sudah ada di sim (array 9) tapi **tidak pernah dikirim** → tab "Jalannya Match" tetap kosong.
4. Tiga keputusan user **belum tercermin di kode**: AFK 15/30 dtk, kapasitas `koTimeline` per mode,
   dan timer Ranked (BF-1 belum diputus, tapi kode memakai 100 dtk).
5. Bug gameplay T2 yang masih terbuka: Overload tidak mematikan guard, AFK berjalan saat pemain di-combo.

---

## B. Temuan

### S1 — Integritas hasil
| ID | Lokasi | Temuan | Dampak |
|---|---|---|---|
| **Q1** | `View/Nexus/NexusGame.cs:370-374` | Skor **dinormalisasi paksa** ke `KoTarget` sebelum dikirim ("pemenang = 5, kalah ≤4"), padahal `NxMatch` sengaja tidak memalsukan skor | Backend menerima hasil palsu; `time`/`forfeit`/`seri` tak pernah tercatat; statistik & riwayat bohong |
| **Q2** | `NexusGame.cs:376` | `EndReason`, `WinnerSlot`, `KoTimeline` **tidak dikirim** (API sudah menerima, `ApiEndpoints.cs:18`) | `EndReason` default `"ko"`; validasi `time`/`forfeit` tak pernah dipakai; `KoTimeline` selalu null |
| **Q3** | `NexusGame.cs:370-374` | Seri (`ScoreA == ScoreB`) diperlakukan sebagai **kemenangan tim A** (`>=`) | Draw → menang, rating berubah padahal backend punya jalur `IsDraw` (`MatchService.cs:294`) |
| **Q4** | `NexusGame.cs:375` | Durasi memakai `Time.realtimeSinceStartup` (wall clock) | Tidak deterministik; jeda/loading ikut terhitung; dua klien bisa beda → statistik durasi tak sahih |
| **Q5** | `NxMatch.cs:45-46` + `NxTuning.cs:26` + `Nexus.qtn` `array<NxKoEvent>[9]` | `KoLog` dikunci **9** dengan komentar "first-to-5"; Battle/Survival butuh 19/29 (keputusan user: kapasitas per mode) | Timeline terpotong → backend `IsLegalTimeline` (`MatchService.cs:246`) menolak karena `Count != left+right` |
| **Q6** | `MatchService.cs:140-141` | `ReportedKoTimeline` dibandingkan sebagai **string JSON mentah** antar-klien | Urutan properti/spasi berbeda = mismatch → match ditolak walau isinya sama; harus dibandingkan kanonik |
| **Q7** | `NxMatch.cs:14,74` + `NexusGame` | Seri dikirim sebagai `WinnerTeam = 255`, backend menuntut `-1` (`MatchService.cs:223`) | Kalau 255 diteruskan mentah → hasil ditolak; kalau dipetakan, belum ada kode pemetaan |

### S2 — Gameplay
| ID | Lokasi | Temuan | Dampak |
|---|---|---|---|
| **Q8** | `NxCombatSystem.cs:115-119` | Lock Overload menghentikan gerak, **tidak mematikan `Guarding`**; guard dicek di `NxDamage.cs:47` | Pemain "terkunci" tetap menahan damage → Overload tidak benar-benar rentan (tujuan mekanik gagal) |
| **Q9** | `NxCombatSystem.cs:141-152` | `TrackActivity` jalan **sebelum** `HitPause`; tidak reset saat menerima damage | Pemain yang di-combo tanpa menekan tombol bisa **kalah WO saat sedang diserang** |
| **Q10** | `NxTuning.cs:19-20` | AFK **10 dtk / 20 dtk berturut-turut**; keputusan user **15 dtk / 30 dtk akumulatif** | Deviasi keputusan; lebih keras dari yang disetujui |
| **Q11** | `NxTuning.cs:14` | Timer match **100 dtk** — BF-1 belum diputus | First-to-5 dalam 100 dtk hampir mustahil → mayoritas match berakhir "waktu", tie-break HP memicu main aman |
| **Q12** | `NxMatch.cs:50-55` | Timer berjalan **selama hitpause** (dipanggil dari `NxHitSystem` tiap tick) | Waktu efektif lebih pendek dari yang dirasakan; deterministik tapi tidak adil saat combo panjang |
| **Q13** | `NxHitSystem.cs:20 | Urutan**: `TickTimer` dieksekusi sebelum loop hit | KO pada tick yang sama dengan habisnya waktu **kalah oleh timer** (selalu, di semua klien) — perlu keputusan siapa menang |
| **Q14** | `NxCombatSystem.cs:246` vs `Physics` | Dash dikunci saat Critical, tapi `DashTime` sisa dari sebelum masuk Critical tetap mendorong penuh | Kebocoran kecepatan kecil; bisa dipakai menghindar setelah masuk Critical |

### S3 — Konsistensi & risiko
| ID | Lokasi | Temuan |
|---|---|---|
| **Q15** | `NxTuning.cs:11` | `TickRate` harus sama dengan `SessionConfig.UpdateFPS`; tidak ada pemeriksaan. FPS sesi lain → timer & semua ambang bergeser |
| **Q16** | `NxCombatSystem.cs:39` | `KoTarget` tetap **5 untuk semua mode**; roadmap Battle 3v3 = target 10 → belum ada |
| **Q17** | `NxDamage.cs:130-147` | `NxMatch.OnKo` dipanggil **setelah** `Respawn`; aman sekarang, tapi urutan ini rapuh bila `Respawn` nanti mengubah skor/statistik |
| **Q18** | `Nexus.qtn` global | `WinnerTeam` default 0 (bukan 255) → sebelum `Begin`, pembacaan `WinnerTeam` bisa disalahartikan sebagai "tim 0 menang" |
| **Q19** | `NexusGame.cs:376` | Klien lama mengirim tanpa field baru → `IsLegalResult(Time/Forfeit)` menolak (`winnerSlot` null). Perlu versi protokol |
| **Q20** | `NxDamage.cs:154` | `Respawn` sengaja **tidak** reset `IdleTicks` (anti-AFK). Konsekuensi: pemain yang mati lalu menunggu respawn 0,7 dtk tetap dihitung idle — benar secara aturan, tapi harus diuji |

### S4 — Catatan
- `CritTimer` masih ada di komponen tetapi tidak pernah dinaikkan (dead field) — jangan bingungkan dengan mekanik baru.
- `AfkWarnTicks` hanya untuk HUD; bukan kode mati.
- `NxCombatSystem.cs:319-339` `BestTarget` O(n³); aman untuk 10 entitas, perlu dicatat untuk 5v5 + 10 bot.
- `array<NxKoEvent>[9]` membuktikan sintaks array `.qtn` **didukung** → catatan "belum terverifikasi" di `t2-spec/02` sudah usang.

---

## C. Gap vs keputusan (docs)
| Keputusan | Kode saat ini | Status |
|---|---|---|
| AFK 15 dtk / 30 dtk **akumulatif** | 10 dtk / 20 dtk **berturut** | ❌ |
| `koTimeline` kapasitas **per mode** (9/19/29) | tetap 9 | ❌ |
| Timer Ranked | 100 dtk (belum diputus) | ⚠️ |
| Seri = tanpa perubahan rating | klien mengubah seri jadi menang | ❌ |
| Skor tidak dipalsukan (`NxMatch.cs:8`) | `NexusGame.cs:370` memalsukan | ❌ |

---

## D. Urutan perbaikan yang disarankan (untuk Claude user)
1. **Q1/Q2/Q3** — hapus normalisasi skor; kirim `EndReason`, `WinnerSlot` (`-1` untuk seri), `KoTimeline`.
2. **Q5/Q6** — kapasitas timeline per mode + bandingkan JSON kanonik di backend.
3. **Q8/Q9** — matikan guard saat Overload; reset `IdleTicks` saat menerima damage/hitstun.
4. **Q10/Q11** — selaraskan angka AFK dengan keputusan; putuskan timer Ranked.
5. **Q4/Q15** — durasi dari tick simulasi, bukan wall clock; validasi `TickRate` vs `UpdateFPS`.
6. Lain-lain (Q12–Q20) setelah lima di atas hijau.

## E. Yang belum bisa saya uji
Tidak ada tes otomatis yang bisa saya jalankan (Unity + 2 instance). Semua temuan di atas berasal dari
pembacaan kode dan kontrak API. Butuh tes editor + 2 klien untuk konfirmasi Q1–Q9.
