# 31 — Functional Completion Plan

Tujuan: **semua yang sudah tampil di UI benar-benar BERFUNGSI** sebelum fitur baru besar.
Dikerjakan per fase; **berhenti & lapor di akhir tiap fase** (selesai apa, cara uji, tertunda apa).

## STATUS (2026-10-29)
- **SELESAI**: 1.1 (match metadata backend+game, migrasi `AddMatchMeta` auto-apply), 1.2 (hide MMR, avatar inisial, emblem per tier [bentuk+warna], konsistensi stub), 1.3 Statistik (filter, 3 ring, grid, 2 grafik Painter2D). Perbaikan ladder (emblem bentuk, progres tier di kartu RANK, Rekaman hero+lawan, kartu isi tinggi).
- **BUG 1.3 SELESAI (2026-10-29)**: (1) filter Ranked kosong → backfill `Mode="ranked"` di `Program.cs` + compare **case-insensitive** (`ModeOf`); (2) Kill Tertinggi vs Kill bertentangan → **semua angka dari SATU sumber per-match** (`Mine(m)`), tak campur `/me`; (3) data lama (hero/durasi/KDA) → tampil **"–"** + label `stats-note` "Sebagian data dari pertandingan lama tidak tersedia"; (4) grafik WR label Y (0/50/100%) + rank Y (tier) + X tanggal (`FillDates`). Schema di `32-stats-schema.md`. Backend build OK.
- **STATS SCHEMA v2 (2026-10-29)**: docs/32 ditulis ulang penuh (audit mekanik, Lapisan 1/2, radar 5 sumbu, keamanan). **Backend SELESAI**: akumulator simulasi Quantum (damage/skill/block/dodge/guardCrush/critical/gearDrop/firstBlood/streak/maxDeficit + per-hero) di `NxCombat`/`NxDamage`/`NxHit`/`NxProjectile`/`NxCombatSystem`; payload hasil LENGKAP (`NexusGame.BuildStatsPayload`) + pembandingan backend (payload identik → Finished, beda → Disputed) + sanity-check (durasi/laju KO) + anti-kolusi (redam rating pasangan berulang); DB `AddDetailedStats` (kolom `MatchPlayer` + tabel `MatchPlayerHeroes`) auto-applied via Docker rebuild; endpoint `/api/me/stats` & `/api/players/{id}/stats` (agregat + flawless/comeback/close + radar persentil). 34 tes hijau. **CATATAN: buka Unity sekali untuk regen codegen Quantum** (field .qtn baru).
- **SELESAI (2026-10-29/30)**: 1v1 ranked (PlayerCount-based spawn, bleed-out credit, Kills vs BotKills, invariant kills A=deaths B + tes, `Match.Format` ranked1v1/battle/legacy5v5, `runInBackground` fix disconnect). **Leaderboard** (docs/33): placement ≥5, flag akun uji EKSPLISIT (default false, jalur tes), Poin Ladder 0–100 dari conservative rating, urut tier→poin→WR→match, cache 1 menit, `/api/leaderboard`+`/api/me/rank`, UI kolom+placement row. **Tab Riwayat** (docs/34): kartu ML 240×420 (hero placeholder TITAN/PULSE, Poin Ladder Δ, badge FLAWLESS/COMEBACK/FIRST BLOOD, FORMAT LAMA) + Detail scoreboard (juga layar hasil). 52 tes backend hijau.
- **SELESAI (2026-10-30)**: **Proteksi demosi** (opsi 1, docs/33): floor tier di layer tampilan (`Ranks.ApplyFloor`/`StepTierFloor`), state `Player.LastRankedTierOrder/TierFloorOrder/TierFloorLeft`, migrasi `AddTierFloor` (auto-apply, kolom terverifikasi di DB), grace `Game:DemotionGraceMatches`=3, dipakai profil+leaderboard+`/me/rank`, Glicko tetap murni, backfill akun lama. **58 tes hijau.**
- **BELUM (URUTAN BERIKUTNYA)**: UI Tab Statistik baru (ring Flawless, grid mekanik, radar) → 1.4 Hero Favorit → 1.6 Settings → 1.7 Lobby. Arena/respawn 1v1 ditunda (user main dulu).

## ATURAN UMUM (wajib)
- **Tanpa data dummy.** Tombol tampil = berfungsi; kalau belum siap → **disabled + "Segera Hadir"**.
- **Nama konsisten** = `display name` yang sama di semua layar (`NexusLobbyController.PlayerName`).
- **Design system** yang ada: `NexusTokens.uss`, sprite 9-slice, Chakra Petch / Exo 2.
- MMR mentah TIDAK ditampilkan ke pemain (tier + progress bar saja).

---

## FASE 1 — DATA MATCH + PROFIL BERFUNGSI PENUH
### 1.1 Match metadata (backend + game)
- `MatchPlayer`: `HeroId`, `PartySize` (default 1), `PartyId` (nullable), `RatingBefore`; (Kills/Deaths/Assists sudah ada = `ReportedKills/Deaths/Assists`, `RatingDelta` sudah ada).
- `Match`: `Mode` (ranked/battle), `DurationSec`.
- `/api/matches/result`: terima `heroId, mode, durationSec, partySize`.
- `/api/matches`: kembalikan per match + **array `players`** (slot, displayName, heroId, K/D/A, ratingDelta, isWinner) → lawan/anggota + scoreboard detail.
- Game: `NexusGame.ReportAsync` kirim hero (dari `NxCombat.HeroId`), mode, durasi; `NexusBackend` DTO.
- Migration EF; backend auto-migrate saat start.

### 1.2 Bug fix
- Tab Statistik/Riwayat vs Tab Profil tak konsisten → gate empty-state pada `matchesPlayed` (yang sama).
- Lobby "Rating 1662" → **sembunyikan MMR**, tampilkan tier + **progress bar**.
- Avatar "N" padahal "Quade" → inisial avatar dari display name (semua layar).
- Emblem rank kotak "?" → **emblem per tier** (sprite generate: `emblem_<tier>.png`).

### 1.3 Tab STATISTIK
- Filter mode (Semua/Ranked/Battle) + periode (Semua; Season jika ada).
- 3 ring: Total Match, Win Rate, KDA. Grid: Menang/Kalah/Kill/Death/Assist/Kill tertinggi/Win streak/rata durasi.
- Grafik 1: win rate dari waktu (Painter2D). Grafik 2: perjalanan rank (komponen grafik ladder).

### 1.4 Tab HERO FAVORIT
- Agregasi `heroId` per match: jumlah match, win rate, KDA rata2 per hero, urut terbanyak.
- Grid kartu hero → klik tampil detail kiri. Top-1 juga di Tab Profil.

### 1.5 Tab RIWAYAT + DETAIL MATCH (scoreboard)
- Kartu per match: nama mode, badge PARTY (partySize>1), MENANG(emas)/KALAH(merah), hero+portrait, K/D/A, durasi, tanggal/jam, Δrank (ranked, tanpa MMR).
- Klik → **DETAIL MATCH**: header hasil+skor+durasi, dua sisi (biru kiri/merah kanan) hero/nama/KDA/Δrank/MVP, Match ID, Kembali. **Layout sama dipakai sebagai LAYAR HASIL** pasca-match.

### 1.6 SETTINGS (ikon gear lobby, simpan PlayerPrefs, langsung terapkan)
- Tab Grafis (resolusi/mode layar/VSync/FPS cap/kualitas), Audio (master/musik/SFX + mute), Kontrol (daftar key; rebinding "Segera Hadir"), Antarmuka (bahasa ID; tampil FPS/ping), Akun (info/ID salin/sosial/Logout). Tutup + Esc.

### 1.7 Lobby tidak kosong
- Tengah: hero terakhir dimainkan (portrait placeholder + nama) / hero default.
- Kiri atas: panel Pengumuman/Event dari `/api/announcements` (buat endpoint sederhana).

---

## FASE 2 — REAL-TIME + CHAT + TEMAN
- 2.1 **Pilih**: Photon Chat vs SignalR vs Nakama → perbandingan di **[[docs/36]]** (realtime-decision). **Tunggu approve user** (condong SignalR; Nakama dicabut utk meta inti). Tanpa kode sampai disetujui.
- 2.2 Presence (Online/Di Lobby/Di Ruang Tim/Dalam Match/Offline).
- 2.3 Chat channel (ALL/PARTY/GUILD/ROOM + whisper), format `[CH] Nama: pesan`, cooldown, filter kasar.
- 2.4 Teman: tab LOBBY (online di lobby), BUDDY (teman+presence), Add/terima/tolak/hapus/blokir, menu (profil/whisper/undang), counter Online asli.

## FASE 3 — PARTY (Ruang Tim Tahap 2–4, docs/29)
Undang teman/kode, gabung/keluar/kick/pindah ketua/siap, party chat, matchmaking party (1 tim, partyId → badge PARTY di riwayat).

## FASE 4 — GUILD
Buat/cari/gabung/keluar, peran (ketua/wakil/anggota)/kick, daftar anggota+presence, tab GUILD, guild chat.

## FASE 5 — MAIL
Inbox (sistem/permintaan teman/undangan guild/pesan), read/unread + badge amplop, hapus/tandai semua, lampiran hadiah "Segera Hadir" (sampai ekonomi).

---
**Urutan**: Fase 1 (1.1→1.7), lapor tiap sub-fase besar. Mulai 1.1 + 1.2.
