# 02 — Audit kode T2 (untuk reviewer; riset, bukan perubahan)

Kode T2 **sudah ada di working tree** (belum di-commit) dan **sengaja dibiarkan** oleh user.
Dokumen ini memetakan apa yang tertulis di kode vs keputusan, lalu mendaftar temuan supaya reviewer
(Claude user) bisa memperbaiki tanpa menebak. **Tidak ada kode yang diubah di sesi ini.**

## 1. Peta kode (OBSERVED)
| Lokasi | Isi |
|---|---|
| `NxTuning.cs` (baru) | semua ambang: AFK 900/1800, Overload 480/90, penalti 700/500/350, bobot bot |
| `NxCombatSystem.cs:106` | `TrackActivity(f, c)` — AFK |
| `NxCombatSystem.cs:112` | `UpdateCriticalPressure(c)` — Overload |
| `NxCombatSystem.cs:115-118` | lock Overload: Vel XZ = 0, `Physics`+`Timers`, return |
| `NxCombatSystem.cs:141-154` | `TrackActivity`: reset oleh `MoveDir`/`ActionButtons`; forfeit set skor = `KoTarget`, `State = 2` |
| `NxCombatSystem.cs:171-178` | `CritSpeedMul` (700/500/350 per-mille) |
| `NxCombatSystem.cs:246` | dash dikunci saat `Critical != 0` |
| `NxCombatSystem.cs:290,319-339` | `BestTarget`: skor jarak² − 40/ − 80 + 30×crowd, tie-break `e.Index` |
| `NxDamage.cs:51,71,85` | reset Overload saat guard / kena / masuk Critical |
| `NxDamage.cs:131` | `Global->KoTotal++` |
| `NxDamage.cs:154` | respawn membersihkan IdleTicks/Overload |
| `Nexus.qtn:56-58, 108-109` | `IdleTicks`, `OverloadCharge`, `OverloadLock`, `KoTotal`, `Forfeit` |

## 2. Temuan — BUG / celah perilaku
| # | Severity | Temuan | Usul perbaikan |
|---|---|---|---|
| B1 | **tinggi** | Forfeit **memaksa `ScoreB = KoTarget`** (`:151-152`). Skor asli hilang; `NexusGame.cs:370` menormalisasi hasil, tapi riwayat/statistik backend akan mencatat 5-0, bukan skor nyata | simpan skor apa adanya + `Forfeit`; pemenang ditentukan dari `Forfeit`, bukan dari skor |
| B2 | **tinggi** | `TrackActivity` dipanggil **sebelum** cek `HitPause`. Pemain yang sedang di-combo panjang tanpa menekan tombol tetap dihitung idle → bisa kalah WO saat sedang diserang | reset `IdleTicks` bila `HitStun > 0` atau saat menerima damage di `NxDamage` |
| B3 | **sedang** | Overload lock **tidak mematikan `Guarding`**. Karena guard dicek di `NxDamage` (bukan di sistem combat), pemain bisa "terkunci sambil guard" → tetap menahan damage, jadi Overload tidak benar-benar rentan | set `Guarding = 0` saat lock dimulai |
| B4 | rendah | `DashTime > 0` yang tersisa dari sebelum masuk Critical tetap mendorong penuh (`Physics` menimpa Vel saat dash) | kalikan Vel dash dengan `CritSpeedMul` atau nolkan `DashTime` saat masuk Critical |
| B5 | rendah | `CritTimer` kini **dead field** (masih di-reset di `Respawn`, tapi tidak pernah dinaikkan) | hapus saat CodeGen berikutnya, jangan sekarang |
| B6 | rendah | `AfkWarnTicks` hanya dibaca View; di sim tidak dipakai | dokumentasikan sebagai ambang presentasi (jangan dianggap kode mati) |
| B7 | rendah | `BestTarget` O(n³) (10 entitas ≈ 1000 iterasi/tick) | terima untuk MVP; optimasi bila 5v5 + 10 bot |
| B8 | catatan | Menahan guard terus-menerus = tidak AFK. Ini **sesuai keputusan user**, tapi konsekuensinya AFK-farming dengan guard | putuskan: guard hanya menghitung aktif bila `GuardGauge` berubah / ada kontak |

## 3. Temuan — risiko kompilasi (belum terverifikasi)
| # | Titik | Kalau gagal |
|---|---|---|
| C1 | `FP._1` (`:173`) | ganti `(FP)1` |
| C2 | `EntityRef.Index` (`:338`) | hapus tie-break; urutan iterasi tetap deterministik |
| C3 | `GetComponentBlockIterator` bersarang (`:331-336`) | pindahkan hitung crowd ke array sementara |
| C4 | `(FP)pm / 1000` (`:177`) | ganti `FP.FromInt(pm) / 1000` |

## 4. Temuan — belum ada (jangan dianggap selesai)
| Item | Status |
|---|---|
| `koTimeline` (9/19/29 + `TotalKos`) | belum; sintaks array `.qtn` belum terbukti di proyek ini |
| Indikator posisi Critical + ikon Overload | View/UI, kerja editor |
| 8 tes invariant (`01 §7`) | belum ada project tes Quantum |
| Kirim `Forfeit` ke backend | belum; backend sedang punya pekerjaan paralel `AddMatchEndReason` |
| Pemetaan `Forfeit` → `MatchEndReason` | belum; enum/kolom di backend dibuat sesi lain |

## 5. Pertanyaan yang harus dijawab reviewer
1. WO sebaiknya **mengubah skor** (5-0) atau **menyimpan skor nyata** + alasan? (B1)
2. Pemain yang sedang di-combo boleh kena AFK? (usul: tidak) (B2)
3. Overload saat guard: lock saja, atau paksa guard turun? (usul: paksa turun) (B3)
4. Menahan guard tanpa kontak dihitung aktif? (B8)

## 6. Keselarasan dengan pekerjaan backend yang sudah ada
`photon-backend` punya migrasi `20261113085957_AddMatchEndReason` + perubahan `Entities`, `ApiEndpoints`,
`StatsEndpoints`, `MatchService`, `ApiTests` yang **bukan dari sesi ini**. Sebelum menggabungkan:
- pastikan nama alasan (KO / waktu / WO / putus) cocok dengan `Forfeit` (1 = tim 0, 2 = tim 1),
- putuskan apakah skor final dikirim mentah (usul B1),
- jangan commit kode klien + backend dalam satu commit tanpa memisahkan asalnya.
