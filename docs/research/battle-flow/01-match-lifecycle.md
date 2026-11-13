# 01 — Lifecycle match: mulai, timer, menang, putus, selesai

Domain: **battle/match flow** (sesi riset, 2026-11-13). Keluaran dokumen; **tidak ada kode diubah**.

## Ringkasan (5 baris)
1. Model "ronde" Ikemen **tidak cocok** dengan Ranked kita (first-to-5 KO, tanpa ronde) — yang diambil hanya
   *lifecycle* & pelacakan skor, bukan rondenya.
2. Yang belum ada di kita: **timer match, aturan waktu habis, draw, pause, disconnect, rematch**.
3. Semua timer harus **tick simulasi**, bukan `Time.time`; countdown pun bagian dari sim.
4. Hasil harus **idempoten** dan divalidasi backend; mismatch checksum → kartu Disputed (poin g).
5. AFK/forfeit **milik T2**, bukan domain ini — di sini hanya titik sambungnya.

## Tabel
| Komponen | Sumber | Yang diambil | Artefak | Biaya | Risiko | Status |
|---|---|---|---|---|---|---|
| Lifecycle 4 fase | `IK` `system.go:1822` (roundState), `:1891` (roundOver), `:1629` (matchOver) | pemisahan state ronde vs match | §1 di bawah | kecil | rendah | ✅ riset |
| Pelacakan kemenangan | `IK` `system.go:80` (`winTeam`), `:82` (`winTrigger`) | satu sumber skor + sebab menang | §2 | kecil | rendah | ✅ |
| Timer | `IK` `system.go:3216` (`timeTotal`), `fightscreen.go:3226` (`round.time`) | timer sebagai state sim | §3 | kecil | sedang (harus deterministik) | ✅ |
| Menang karena waktu | konvensi fighting game (`DERIVED`) | skor lebih tinggi menang; seri = draw | §3 | kecil | sedang (kontroversi desain) | 🟡 butuh keputusan |
| Draw | `IK` `winTeam = -1` (`:2477`) | draw sebagai hasil sah | §3 | kecil | rendah | 🟡 |
| Pause | — (`IK` punya pause, mode arcade) | pause hanya non-ranked, 1×/match | §4 | kecil | sedang (abuse) | 🟡 |
| Disconnect/abandon | dokumentasi publik `DK` (pola penalti), `OM` (ticket lifecycle) | grace → forfeit, tanpa bot di ranked | §4 | sedang | **tinggi** (rating abuse) | 🟡 |
| Rematch | `OM` (re-queue), `IK` (post-match loop) | alur kembali ke antrean vs room sama | §4 | kecil | rendah | 🟡 |
| Finalisasi hasil | kode kita (`/api/match/...`, `FinalizeAsync`) | payload + idempotensi | §5 | kecil | rendah | 🟡 |
| Replay/killcam hook | `ikemen-extract/04` | matikan sim → kirim checksum | §5 | kecil | rendah | 🟡 |

## 1. Lifecycle (PROPOSED, menyambung `global.State` yang sudah ada)
```
0 Waiting   → layar pilih hero / lobby room
1 Countdown → 180 tick (3 dtk), input terkunci, sim jalan
2 Playing   → pertarungan
3 Ending    → 120 tick freeze dramatis (KO terakhir, slow-mo 60 tick)
4 Result    → tidak ada sim; klien menampilkan hasil, backend memfinalisasi
```
`OBSERVED`: sekarang kode hanya punya `State` 0/1/2 (`NxCombatSystem.cs:43, 80`) — belum ada Countdown
terpisah dan belum ada fase Result. Perubahan ini **tidak boleh** dikerjakan sebelum T2.

## 2. Kondisi menang (PROPOSED)
| Mode | Menang bila | Sumber aturan |
|---|---|---|
| Ranked 1v1 | skor tim mencapai **5 KO** | docs/00-ROADMAP T3-1 (first-to-5, tanpa ronde) |
| Battle 3v3 | skor tim mencapai target (usul 10) atau waktu habis | docs/24 §10a |
| Survival | race-to-6 dengan ronde 90 dtk + sudden death | docs/24 §5a (papan poin = K-12) |
| Training | tidak ada menang | — |

`DERIVED`: karena Ranked tanpa ronde, konsep `decisiveRound`/`perfect` Ikemen **dibuang**. Yang diadopsi
hanya satu hal: **sebab kemenangan dicatat** (`winTrigger`), supaya statistik bisa membedakan
menang-KO vs menang-waktu. Ini gratis dan berguna untuk leaderboard nanti.

## 3. Timer & waktu habis (PROPOSED)
- Durasi Ranked: **tanpa timer** (usul) atau **300 dtk** (5 menit) — lihat keputusan #1.
- Timer berjalan di dalam sim (`CountdownTicks`), ikut rollback; UI hanya membaca.
- Saat timer 0: **skor lebih tinggi menang**. Skor sama → **DRAW** (bukan sudden death, bukan adu damage).
  Alasan: sudden death memperpanjang match yang sudah lambat, dan adu damage sulit dijelaskan.
- Survival memakai aturan berbeda (sudden death) — jangan campur implementasinya.

## 4. Pause, putus, rematch
| Situasi | Aturan usul | Kenapa |
|---|---|---|
| Pause | **hanya** Battle/casual, 1 pause 30 dtk per pemain, otomatis lanjut | Ranked pause = alat intimidasi |
| Disconnect | grace **20 dtk** (sim tetap jalan, pemain AFK) → **forfeit**, skor diberikan ke lawan | lebih jelas daripada "match batal" |
| Ganti bot saat putus | **tidak** di Ranked; **ya** di Battle casual | bot pengganti = celah farming rating |
| Rematch | Ranked: **tidak** (kembali ke antrean, hindari win-trading); casual: boleh, seed baru | — |

`DERIVED`: ini juga menjawab AFK T2 — bedanya, T2 mengurus **deteksi** (tanpa input N dtk),
domain ini mengurus **konsekuensi skor**. Keduanya harus memakai satu ambang yang sama, jangan dua angka.

## 5. Finalisasi & anti-desync
```
Ending selesai → sim berhenti menerima input
  → klien kirim {matchId, skor, checksum akhir, inputLog}
  → backend: FinalizeAsync (idempoten per matchId)
  → checksum berbeda antar klien → tandai Disputed, rating tidak berubah
```
`OBSERVED`: backend sudah punya jalur finalisasi (dipakai Ranked 1v1); idempotensi perlu diverifikasi
saat implementasi. Killcam/replay memakai input log yang sama (`ikemen-extract/04`).

## 6. Keputusan yang dibutuhkan user (maks 5)
1. **Timer Ranked**: (a) tanpa timer, (b) 300 dtk, (c) 240 dtk.
2. **Waktu habis seri**: (a) DRAW tanpa perubahan rating, (b) sudden death 30 dtk, (c) menang ke damage terbanyak.
3. **Disconnect**: (a) grace 20 dtk lalu forfeit, (b) 45 dtk, (c) batalkan match (tanpa rating).
4. **Pause**: (a) tidak ada, (b) 1×30 dtk khusus casual.
5. **Rematch**: (a) hanya casual, (b) semua mode.

## 7. Tidak bisa diambil (dan alternatifnya)
| Kebutuhan | Kenapa tidak | Alternatif |
|---|---|---|
| Ambang penalti abandon Dota (angka internal) | tidak dipublikasikan & tidak relevan | tentukan sendiri; mulai 20 dtk + 3 pelanggaran/season |
| Logika matchmaking internal Dota | tertutup | Open Match/Glicko-2 (sesi domain matchmaking) |
| Animasi/UI hasil match | aset berhak cipta | buat sendiri (sudah ada Detail Match v2) |

## 8. File yang ditulis
`docs/research/battle-flow/01-match-lifecycle.md` (ini), `README.md`, plus koreksi `hero-ability/02,03,04`.
