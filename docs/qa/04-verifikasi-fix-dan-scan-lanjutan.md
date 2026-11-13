# 04 — Verifikasi fix + scan lanjutan (2026-11-13)

Lanjutan `01`, `02`, triase `03`. Metode: baca kode **setelah** `83c98e0` + `eec328f`. Tanpa ubah kode.
Tujuan: (a) konfirmasi fix benar-benar ada di kode, (b) temuan baru di permukaan yang belum dipindai.

---

## A. Verifikasi klaim fix (OBSERVED)
| ID | Klaim | Bukti di kode | Status |
|---|---|---|---|
| Q4 | durasi dari tick sim | `NexusGame.cs:344` `(frame.Number - StartTick) / frame.UpdateRate` | ✅ benar |
| Q15 | peringatan FPS sesi | `NxMatch.cs:20-21` `Log.Warn` bila `UpdateRate != TickRate` | ✅ benar |
| Q18 | pemenang awal = seri | `NxCombatSystem.cs:44` `WinnerTeam = NxMatch.Draw` | ✅ benar |
| Q21 | fighter bertumpuk didorong | `NxSeparationSystem.cs:27-29` arah deterministik dari `EntityRef.Index` | ✅ benar |
| Q22 | tidak bergeser saat hitstop | `NxSeparationSystem.cs:20` `if (self->HitPause > 0) continue;` | ✅ benar |
| Q31 | yaw kapsul | klaim diperbaiki; tidak terlihat di kapsul (primitif simetris) | ✅ tidak bisa diverifikasi visual |
| Q36 | assignment kedaluwarsa | `MatchmakingService.cs:34-41` `Prune` + `MatchmakingAssignmentTtlSeconds=60` | ✅ ada (lihat Q43) |
| Q37 | penunggu hantu dibuang | `_waiting` prune 10 dtk + `LastSeen` | ✅ benar |
| Q1/Q2/Q3/Q7/Q8/Q32 | sudah benar sejak `83c98e0` | diterima (saya tidak menemukan kontradiksi di `NexusGame.cs` sekarang) | ✅ diterima |

Catatan: Q5/Q6/Q9/Q12/Q13/Q14/Q17/Q19/Q20/Q33/Q34/Q35/Q41 saya terima sebagai tidak berlaku
(penjelasan triase masuk akal: timeline dinormalkan backend, dash = invuln, dsb).

---

## B. Temuan baru

| ID | Sev | Lokasi | Temuan | Dampak / usul |
|---|---|---|---|---|
| **Q42** | S2 | `MatchmakingService.cs:48-60` + `Options.cs:47-48` | **TTL assignment 60 dtk < durasi match 100 dtk** (`NxTuning.MatchSeconds`). `Prune` jalan di setiap `Join`/`Status`/`Leave` | Bila klien memanggil `/matchmaking/status` saat match masih berjalan, assignment dilepas di detik ke-60 → `Join` berikutnya bisa membuat **match kedua** sementara match pertama belum dilaporkan → dua laporan rating. Usul: TTL ≥ `MatchSeconds + margin`, atau refresh `At` selama status `Matched` |
| **Q43** | S2 | `NexusGame.cs:318` + `:387` | `_reported = true` dipasang **sebelum** HTTP report; `HttpClient.Timeout = 10 dtk` (`NexusBackend.cs:40`), tanpa retry/outbox | Timeout sesaat = **hasil match hilang permanen**; lawan melapor sendirian → backend bisa menandai Disputed/missing rating. Usul: retry dengan backoff sampai ACK, atau antrean lokal |
| **Q44** | S3 | `NxSeparationSystem.cs:20` | Hitstop dicek pada **diri sendiri** saja | Bila A kena hitstop dan B tidak, B tetap menggeser diri relatif ke A selama A beku → jarak berubah saat "freeze". Konsisten antar-klien, tapi perlu keputusan: freeze = keduanya, atau hanya pelaku |
| **Q45** | S3 | `NexusBackend.cs:181,197` | `JsonUtility.FromJson<T>("{\"items\":" + res + "}")` | Respons error (`{error:...}`) membuat parse gagal/silent; UI hanya kosong tanpa pesan. Usul: parse array pembungkus yang benar + tampilkan `error` |
| **Q46** | S3 | `MatchService.cs:173-189` | Validasi 1v1 hanya untuk `Mode == "ranked"`; Battle masuk `legacy5v5` tanpa validasi | K/D battle bisa apa saja (klien nakal). Untuk kasual boleh, tapi catat sebagai lubang yang disengaja |
| **Q47** | S3 | `MatchService.cs:139-141` | Kesepakatan antar-klien membandingkan `ReportedEndReason`, `ReportedWinnerSlot`, `ReportedKoTimeline` — **skor tidak terlihat dibandingkan di blok ini** | Bila skor tidak ikut dibandingkan, satu klien bisa mengaku 2-2 (draw) sementara yang lain 2-1. **Perlu verifikasi**: pastikan `ScoreLeft/ScoreRight` juga dibandingkan sebelum finalisasi |

---

## C. Permukaan yang belum saya pindai
| Area | Risiko yang dicari |
|---|---|
| `Glicko2.cs` | skala 173.7178, update RD saat seri, periode rating, clamp |
| `StatsEndpoints.cs` | double counting (match + akumulator), streak/draw, pembagian nol pada akurasi |
| `FactionService.cs` | bonus faksi dihitung dua kali (join + finalize), populasi race |
| `auth` (`GuestLogin`/`Register`/`Login`) | rate limit, enumerasi username, hash/iterasi password, token expiry |
| `LeaderboardService.cs` | tie-break konsisten dengan docs/33, cache basi |
| `NexusGame.cs` alur UI | state machine layar (bisa masuk match dua kali, tombol ganda) |

## D. Prioritas lanjutan
1. **Q42** dan **Q43** — keduanya bisa menghasilkan laporan/rating yang hilang atau ganda.
2. **Q47** — verifikasi cepat; kalau benar, ini celah integritas.
3. Lanjut pindai `Glicko2` + `StatsEndpoints` + `auth`.
