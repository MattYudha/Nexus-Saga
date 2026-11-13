# 32 — Stats & Match Data Schema (v2)

Sumber kebenaran statistik Nexus Saga. Dipakai Tab Statistik (1.3), Hero Favorit (1.4), Riwayat (1.5), dan profil pemain lain.
**Prinsip:** statistik mengukur mekanik yang membuat game ini unik (warisan Lost Saga: Guard crush→Faint, Critical→gear drop, dash i-frame, ganti hero di tengah match) — bukan parameter generik MOBA.

Semua angka dikumpulkan **di simulasi Quantum (deterministik, FP, tanpa RNG non-seeded)**, bukan dihitung di UI. UI hanya menampilkan & menurunkan agregat.

---

## MEKANIK YANG ADA (hasil audit LANGKAH 0) — hanya ini yang boleh jadi statistik
Gerak 8 arah/lompat/dash(i-frame) · Skill per-hero (TITAN lunge, PULSE charged shot) · melee + projectile · **Guard 180°** (gauge, crush→**Faint**) · **Critical** saat HP=0 (3 Break Stock, **gear drop**) · knockback/launch/hitstun/hitpause · KO + respawn · **ganti hero di tengah match (tombol H)**. ~~bleed-out~~ **dihapus di T2** (lihat §C4 di bawah).
Format match: **first-to-5 KO** (tim pertama 5 KO menang). `ScoreA/ScoreB` = total KO kumulatif per tim (BUKAN ronde).

### TIDAK ADA (jangan dicatat; kandidat fitur, lihat bagian akhir)
Combo, parry, ronde, ring-out/environment kill, multi-kill, ekonomi/gold, surrender, mapId, draw, MVP.

---

## MODE & FORMAT (2026-10-29 — keputusan 1v1)
Mode dikirim deterministik ke simulasi lewat `RuntimeConfig.NexusMode` (0 Ranked, 1 Battle, 2 Practice).
- **RANKED = 1v1 MURNI, tanpa bot.** 2 manusia, first-to-5 KO satu sama lain. (Fallback: kalau cuma 1 manusia terisi → 1 bot, untuk uji.)
- **BATTLE** = tim; bot mengisi slot kosong agar match bisa mulai. K/D = kontribusi personal (sebagian lawan = bot).
- **PRACTICE** = latihan 1v1 vs 1 bot (offline/lokal).
Bot di-spawn saat match MULAI (`StartMatch`, setelah jumlah manusia pasti), BUKAN di `OnInit`.

### KILL/DEATH (deterministik di sim)
- `Kills` = KO terhadap **MANUSIA**. `BotKills` = KO terhadap **BOT** (dipisah; TIDAK dihitung ranked/leaderboard).
- `Kos` (deaths) = KO yang dialami (siapa pun pembunuhnya).
- ~~Bleed-out memberi kill ke penyerang terakhir~~ → **dihapus (T2, 2026-11-13)**: KO **hanya** lewat 3 Break Stock, jadi pembunuh selalu penyerang yang memecahkan stock terakhir. Field `CritTimer`/`LastHitBy*` dibuang dari `.qtn`.

### C4 — CRITICAL TANPA BLEED-OUT (T2, kode `NxCombatSystem`/`NxDamage`, angka di `NxTuning.cs`)
- HP 0 → Critical dengan 3 Break Stock. Tiap pukulan saat Critical memecah 1 stock + merontokkan 1 gear. Stock habis → **KO**. Tidak ada jalan KO lain.
- **Penalti gerak bertingkat**: 70% (stock 3) → 50% (stock 2) → 35% (stock 1). **Dash & lunge TITAN dikunci** selama Critical.
- **Overload**: 8 dtk (480 tick) di Critical tanpa kena damage → **terkunci 1,5 dtk** (90 tick), guard lepas, bisa dipukul. **Bukan KO**, tanpa pengali damage. Kena pukul/guard mereset timer.
- **Bot** memilih target dengan skor jarak² − 40 (Critical) − 80 (Overload) + 30 per kawan LAIN di dekat target.
- **Indikator Critical** untuk lawan: penanda merah di atas kepala / panah di tepi layar (HUD `NexusView`).

### AKHIR MATCH (T2 / NX-11, `NxMatch.cs`)
| Sebab (`endReason`) | Kapan | Pemenang |
|---|---|---|
| `ko` | satu tim mencapai 5 KO | tim itu |
| `time` | **100 dtk** habis | skor KO lebih tinggi → seri: **gear rontok terbanyak KALAH** → **darah tersisa paling sedikit KALAH** → masih sama = **SERI** |
| `forfeit` | **20 dtk** berturut-turut tanpa input (AFK/disconnect) | lawan; skor **tidak dipalsukan** |

- Seri: rating, Wins/Losses, floor tier **tidak berubah**; K/D + statistik tetap dicatat; di statistik seri dihitung terpisah (win rate = menang/(menang+kalah)).
- **`koTimeline`**: array ≤9 `{tick, killerSlot}` (tick relatif awal match), deterministik, **wajib sama** di kedua klien (beda → Disputed), disimpan per match → tab **"Jalannya Match"** di Detail Match v2.
- Backend memvalidasi per sebab (`MatchService.IsLegalResult`/`IsLegalTimeline`); klien lama tanpa `endReason` tetap aturan `ko`.

### ATURAN 1v1 (WAJIB, divalidasi backend → pelanggar **Disputed**; ada tes otomatis)
Untuk match `mode=ranked` dengan payload lengkap (2 pemain):
1. `kills` pemain A = `deaths` pemain B (dan sebaliknya).
2. `deaths` pemain = skor lawan; `kills` pemain = skor timnya (pemenang = 5 bila `endReason=ko`; waktu habis/forfeit = skor apa adanya).
3. `botKills` = 0 (ranked tak boleh ada KO bot).
Lolos → `Match.Format = "ranked1v1"` (K/D valid). Tanpa payload → `"legacy5v5"` (K/D tak dihitung).

### FORMAT & DATA LAMA
- `Match.Format`: `"ranked1v1"` (valid) | `"battle"` | `"legacy5v5"` (match 5v5-bot LAMA).
- **Statistik ranked/K/D HANYA dari `Format="ranked1v1"`.** Match `legacy5v5` → K/D tampil **"–"** (tidak ditebak/dihitung ulang). Rating yang terlanjur berubah dibiarkan.
- Backfill: semua match Finished tanpa Format → `"legacy5v5"` saat startup backend.

## LAPISAN 1 — DATA MENTAH per pemain per match (disimpan di `MatchPlayer`)
Sudah ada: `Slot`(=team 0/1), `HeroId`, `Mode`, `DurationSec`, `Kills`, `Deaths`(=Kos), `RatingBefore`, `RatingDelta`, `PartySize`, `PartyId`, `IsWinner`.

**Ditambahkan (akumulator deterministik di `NxCombat`):**
| Field | Arti | Dicatat saat |
|---|---|---|
| `damageDealt` | total damage diberikan (FP→int round) | `NxDamage.ApplyHit` cabang "kena" |
| `damageTaken` | total damage diterima | ApplyHit cabang "kena" (sisi korban) |
| `skillsUsed` | tombol skill (K) berhasil dipakai | `HandleInput` cabang skill |
| `skillsHit` | skill yang mengenai lawan (kena, bukan di-guard/dodge) | ApplyHit bila `isSkill` & kena |
| `hitsBlocked` | serangan lawan yang **berhasil di-guard** | ApplyHit cabang Guard (bukan durasi guard) |
| `dodges` | serangan yang **lolos karena i-frame dash** | korban in-range saat `DashTime>0` (whiff) |
| `guardCrushes` | membuat lawan **Faint** (guard crush) | ApplyHit saat gauge habis |
| `criticals` | membuat lawan **masuk Critical** (HP→0) | ApplyHit saat HP menyentuh 0 |
| `gearDrops` | merontokkan gear lawan (pukulan saat Critical) | ApplyHit cabang Critical |
| `firstBlood` | 1 bila KO **pertama** di match ini | `Ko()` saat `FirstBloodTaken==0` |
| `maxKillStreak` | streak KO terpanjang tanpa mati | `Ko()` (reset saat jadi korban) |
| `maxDeficit` | selisih KO **terbesar saat tertinggal** (lawan unggul atas kita) | tiap tick dari `ScoreA/B` |
| `heroSwitches` | jumlah ganti hero (H) | `HandleInput` cabang swap |

**PER HERO dalam satu match** (karena bisa ganti hero) → tabel anak `MatchPlayerHeroes`:
`heroId`, `playTicks` (tick bermain sebagai hero itu), `kills`, `damage`.
→ **Hero Favorit & statistik per-hero dihitung dari tabel ini**, BUKAN dari satu `HeroId` per match. `MatchPlayer.HeroId` = hero dengan `playTicks` terbanyak (hero dominan match itu), hanya untuk ringkasan baris.

**Assist — DITUNDA** sampai mode tim. Definisi saat diaktifkan: memberi damage ke korban dalam **5 detik** sebelum KO. Di 1v1 jangan ditampilkan (bukan ditampilkan 0).

Representasi angka di payload: `FP` dikirim sebagai **int hasil `FPMath.RoundToInt`** (deterministik identik antar-klien). Waktu dikirim sebagai **tick** (int), UI konversi (60 tick/detik).

---

## LAPISAN 2 — STATISTIK TURUNAN (dihitung, tidak disimpan; boleh di-cache)
- **Agregat**: total match, menang, kalah, win rate, KDA; rata-rata per match & per menit; dapat difilter **per mode / per hero / per season**.
- **Rekor**: kill tertinggi (max `kills` 1 match), win streak tertinggi & saat ini, damage/menit tertinggi.
- **Flawless** = menang **5–0** (`skorMenang==5 && skorKalah==0`).
- **Comeback** = menang dengan `maxDeficit ≥ 3`.
- **Match ketat** = selisih KO akhir **1–2**.
- Akurasi skill = `skillsHit / skillsUsed`.

### RADAR 5 SUMBU (persentil terhadap pemain **tier yang sama**, minimal **10 match** agar tampil)
| Sumbu | Rumus |
|---|---|
| **Serangan** | `damageDealt / menit` |
| **Pertahanan** | `(hitsBlocked + dodges) / menit` |
| **Tekanan** | `(guardCrushes + criticals) / menit` |
| **Ketahanan** | `damageTaken / KO diterima` (makin banyak dipukul sebelum tumbang = makin tangguh) |
| **Clutch** | `jumlah comeback + win rate di match ketat` |

Nilai sumbu = **persentil** metrik pemain terhadap distribusi metrik pemain lain di tier sama (≥10 match). Bila populasi pembanding belum cukup → "Radar muncul setelah 10 pertandingan & cukup pembanding".

---

## TAMPILAN TAB STATISTIK
- **3 Ring**: Total Pertandingan · Win Rate · **Flawless** (mode solo). (MVP ditunda — tak ada rumus MVP di 1v1.)
- **Grid detail** (hanya yang datanya ada): Menang/Kalah/Kill/Death/Kill Tertinggi/Win Streak/Rata-rata Durasi · Damage diberikan & diterima · Akurasi Skill · Hits Blocked · Dodge Berhasil · Guard Crush · Criticals · Gear Drops · First Blood · Comeback.
- **Radar chart** 5 sumbu (kanan) + **grafik Win Rate dari waktu** (sumbu Y 0/50/100%, X tanggal) + grafik Perjalanan Rank (band tier).
- Data lama (pra-migrasi akumulator) tak punya field baru → tampil **"–"** + catatan "Sebagian data dari pertandingan lama tidak tersedia". JANGAN ditebak.

---

## ENDPOINT
- `GET /api/matches` → per match + array `players[]` (slot, displayName, heroId, K/D/A, ratingDelta, isWinner) + field baru Lapisan 1 + `heroes[]`.
- `GET /api/me/stats?mode=&season=` → agregat + rekor + flawless/comeback/closeWins + radar (nilai persentil bila `radarReady`, else `radarReady=false`).
- `GET /api/players/{id}/stats` → sama, untuk profil pemain lain (tanpa MMR mentah).

---

## KEAMANAN HASIL RANKED
**Kondisi lama:** backend hanya membandingkan **skor** dua klien (beda → Disputed). K/D/A & hero dipercaya penuh dari laporan sendiri → statistik/rekor bisa digelembungkan klien modifikasi.

**MINIMUM (diimplementasi sekarang):** karena simulasi deterministik, kedua klien melihat statistik **identik** untuk SEMUA pemain. Tiap klien mengirim **payload hasil lengkap** (statistik semua slot, hero, durasi). Backend menyimpan payload tiap pelapor dan **menolak (Disputed) bila ada field berbeda**.
**Sanity-check** saat finalize:
- Durasi minimal masuk akal (`durationSec ≥ MinMatchSeconds`).
- Laju KO wajar (`(skorKiri+skorKanan) / durationSec ≤ MaxKoPerSecond`).
- **Anti-kolusi**: bila pasangan `PlayerId` yang sama bertemu berkali-kali dalam waktu singkat → **kurangi perolehan rating** (faktor redam) & **tandai anomali di log**.

**OTORITAS SERVER (fase tersendiri, WAJIB sebelum Nexus Cup berhadiah / rilis publik besar):** backend menyimpan input-log/checksum Quantum dan **replay** untuk menghitung hasil otoritatif. Belum diimplementasi. Dicatat sebagai milestone keamanan.

---

## KANDIDAT FITUR (ditunda — butuh desain combat/mode baru; catat, jangan diam-diam diimplementasi)
**Combo** (rantai serangan dasar — sumber skill-ceiling khas brawler Lost Saga, layak jadi fitur combat tersendiri) · **Ronde** · **Ring-out / environment kill** · **Multi-kill** (double/triple) · **Ekonomi/gold** · **Surrender** · **Map/mapId** · **Draw** · **MVP** (butuh rumus) · **Assist** (aktif di mode tim).

---

## ATURAN KONSISTENSI (tetap berlaku)
1. **Satu sumber**: semua angka Tab Statistik dari **data per-match** (`/api/matches` / `/api/me/stats`), bukan campuran agregat `/me` + match.
2. Field yang tak bisa dihitung dari data lama → **"–"**, bukan ditebak/0.
3. Angka tampil tak boleh saling bertentangan.
4. **Mode** seragam lowercase `"ranked"`/`"battle"`, dibandingkan case-insensitive (`ModeOf`).

## BACKFILL
Match `Finished` `Mode` kosong (pra-`AddMatchMeta`) → `"ranked"` saat startup backend. Field akumulator baru pada match lama tetap null → UI tampil "–". Lihat [[nexus-backend-deploy]] (ubah backend → `docker compose up -d --build api`).

## TIER (Glicko-2, `NexusRankConfig`)
Rookie<1200 · Contender<1400 · Rival<1600 · Gladiator<1800 · Conqueror<2000 · Nexus Legend≥2000.
