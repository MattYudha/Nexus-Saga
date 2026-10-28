# 28 — Profile Page Redesign Plan (UI Toolkit)

Rombak total halaman Profil Pemain (IMGUI → UI Toolkit penuh, gaya ML, design system `NexusLobby.uss`).
Dokumen ini sumber kebenaran untuk profil. Lihat juga [27 — lobby](27-lobby-redesign-plan.md).

## ISTILAH (baku)
- **Level** = progres berbasis XP (mis. "Lv 1"). JANGAN sebut "Account Rank".
- **Rank/Tier** = hanya untuk ranked (mis. "Rival").
- **MMR mentah TIDAK ditampilkan** ke pemain. Tampilkan tier + progres (bila ada field-nya).

## TAHAP A — AUDIT DATA (hasil)
Sumber: `NexusBackend.cs` (`/api/me` → `MeRes`, `/api/matches` → `MatchRow[]`). TANPA data dummy.

### ADA di backend (boleh ditampilkan)
| Data | Field | Catatan |
|---|---|---|
| ID pemain | `playerId` | untuk "salin ID" |
| Nama | `username`, `displayName` | guest hanya displayName |
| Faction | `faction` (0/1/2) | 0 none, 1 ORDE, 2 LEGION |
| **Level** | `accountLevel`, `accountXp` | progres XP; `accountRank` = label level (mis "Recruit"), BUKAN rank ranked |
| Ranked tier | `rankTier` | string tier |
| Statistik agregat | `wins`, `losses`, `matchesPlayed`, `winRate`, `kills`, `deaths`, `assists`, `kda` | |
| Riwayat match | `MatchRow`: `won`, `scoreLeft/Right`, `ratingDelta`, `endedAt`, `slot`, `gameId` | per match |

### BELUM ADA di backend (→ empty state / "Segera Hadir", JANGAN dibuat dummy)
- **Rank points / progress-to-next-tier yang visible** — hanya ada `rating` (MMR mentah, WAJIB disembunyikan). Jadi progress bar ranked **belum punya sumber**. → tampilkan tier saja + "Selesaikan 5 placement" bila unranked.
- **Rank Tertinggi (peak tier)** — tak ada field. → sembunyikan / "Segera Hadir".
- **Data per hero** (Hero Favorit) — tak ada. → Tab Hero empty state.
- **Pencapaian/badge** — tak ada. → empty state "Belum ada pencapaian".
- **Per-match: hero dipakai, mode (Ranked/Battle), durasi** — `MatchRow` tak punya. → kartu riwayat tanpa hero/mode/durasi (atau "Segera Hadir").
- **Season split** (Season Ini vs Semua Season) — tak ada. → tampilkan hanya "Semua Season".
- **Statistik lanjutan** (kill tertinggi, win streak) — tak ada. → sembunyikan.
- **Radar chart** — butuh ≥5 metrik bermakna; belum cukup → **dilewati**, dicatat sebagai pekerjaan berikutnya.

### Kesimpulan audit
Profil baru = **struktur lengkap + banyak empty state jujur**. Yang benar-benar berisi data: header (nama/ID/faction/Level/XP), tier ranked (nama saja), statistik agregat, dan daftar riwayat (menang/kalah/skor/Δpoin/waktu). Sisanya empty state sampai backend menyusul.

## STRUKTUR (rencana, acuan 1920×1080)
Layar penuh, vignette navy, lobby disembunyikan. Back (panah + "Kembali") kiri atas + Esc. Sidebar kiri 260px
(Profil / Statistik / Hero Favorit / Riwayat, item aktif highlight cyan). Konten kanan, judul tab 32px Chakra Petch.
Bisa dipakai utk profil pemain lain (sembunyikan elemen self-only). Buka dari klik avatar top bar.
- **Tab Profil**: header (avatar 128, nama 28, ID+salin, Level+XP, badge faction), rank saat ini (tier) + rank tertinggi (empty), ringkasan (match, win rate), hero favorit kecil (empty), pencapaian (empty).
- **Tab Statistik**: hanya "Semua Season"; filter mode (mode yg ada data); 3 ring (Match, Win Rate, KDA); grid stat relevan brawler (Menang/Kalah/Kill/Death/Assist); TANPA stat MOBA (Farm/Push/Gold/Turret); radar dilewati; empty state bila 0 match.
- **Tab Hero Favorit**: empty state (data per hero belum ada).
- **Tab Riwayat**: kartu match scroll (MENANG emas / KALAH merah, skor, Δpoin, waktu); hero/mode/durasi "Segera Hadir"; empty state bila 0.
- Loading = skeleton abu-abu; error = pesan + "Coba Lagi".
- File: `ProfilePage/Sidebar/TabMain/TabStats/TabHeroes/TabHistory.uxml` + `ProfileController` (toggle seperti `useNewLobby`).

## KEPUTUSAN (disetujui)
1. **Progress bar rank** = posisi MMR relatif thd batas bawah-atas tier (bar saja, **tanpa angka MMR**). Config di SATU tempat: `Assets/NexusUI/NexusRankConfig.cs` (`Bands` min/max per tier — placeholder, samakan dgn backend). `ProfileController.Fill` pakai `NexusRankConfig.Progress(tier, rating)`; bar disembunyikan bila tier tak dikenal.
2. **Backend (PENDING, belum dikerjakan)**: mulai catat **hero dipakai, mode, durasi** tiap match selesai → tambahkan ke `/api/matches` (dan game kirim saat `ReportResultAsync`). Data lama biarkan kosong; kartu riwayat lama tanpa art hero. → ini membuka Tab Riwayat (D) & Hero (E) berisi data.
3. Rank tertinggi, pencapaian, season split, statistik lanjutan = tetap empty state / "Segera Hadir".

## URUTAN
- **Tahap A (SELESAI): audit.**
- **Tahap B (SELESAI):** `ProfilePage/Sidebar/TabMain + stub Stats/Heroes/History.uxml`, `ProfileController.cs` (UIDocument sendiri, toggle `NexusGame.UseNewProfile`, Back + Esc → `UiProfileBack`, sidebar 4 tab, Tab Profil terisi dari `NexusBackend`: nama/ID+salin/faction/Level+XP/rank tier+progress/match/winrate; sisanya empty state). Buka dari klik avatar top bar. IMGUI `DrawProfile` disuppress saat `UseNewProfile`.
- Tahap C: Statistik (3 ring + grid relevan brawler, tanpa stat MOBA, radar dilewati) · Tahap D: Riwayat (butuh backend #2) · Tahap E: Hero Favorit (butuh backend #2).
