# 04 — Brainstorm v2: Peta Seluruh Sistem (2026-10-24)

Tujuan dokumen: memastikan **semua** ide dari brief awal punya tempat, punya rencana riset, dan jelas kendalanya.

## A. Kesiapan Riset (Readiness Check)

| Komponen | Status | Catatan |
|---|---|---|
| REA MCP | ✅ Terhubung (6.7.0, 207 tools) | Analisis statis arsip, PE resource, .NET, SQLite, compare |
| Ghidra + JDK 21 | ❌ Belum | Hanya untuk dekompilasi kode native C++ (`.exe`) |
| AyoDance client | ✅ `C:\Megaxus\AyoDance` | `Audition.exe` (native), arsip `.acv` (~10 GB), `.tbm` (5.216 file), `lua5.1.dll`, `jsoncpp.dll`, folder `SCRIPT/`, `DATA/` |
| LostSaga client | ❌ Tidak ditemukan | Perlu disediakan (installer/folder). Alternatif: wiki, video frame-by-frame |
| Dota/MLBB server | — Tidak perlu | Pakai algoritma publik (OpenSkill / Glicko-2) |
| Python 3.11, .NET, Git, Node 24 | ✅ | Cukup untuk skrip parsing data nanti |

**Batasan riset (wajib):** AyoDance dilindungi **Xigncode** anti-cheat → hanya analisis **statis** file di disk. Tidak menjalankan game di bawah Frida/debugger, tidak menyentuh server resmi (risiko banned + melanggar ToS). Hasil riset = pemahaman desain, ditulis ulang sebagai spesifikasi sendiri.

## B. Peta 14 Sistem

Legenda status: 🟢 desain cukup jelas · 🟡 butuh riset/keputusan · 🔴 terblokir

| # | Sistem | Inti desain usulan | Sumber riset | Status |
|---|---|---|---|---|
| 1 | Akun & Role | Player / Mentor / Moderator / GM / Developer; role di server | Desain sendiri | 🟢 |
| 2 | Avatar & Wardrobe | Slot: hair, face, top, bottom, shoes, hat, glasses, back, pet, aura, emote. Avatar ≠ Hero | **AyoDance** (`SCRIPT/`, `DATA/`, `.acv`) | 🟡 REA siap |
| 3 | Plaza Hub | Kota kecil 30–60 player/instance, channel otomatis, layar besar menayangkan Leader Duel | AyoDance lobby/room, LostSaga plaza | 🟡 |
| 4 | Rest Room & Minigame | Room publik/privat, **Dance Duel** (ritme 60 detik, homage Audition), fishing, kuis, couple room | AyoDance (pola ritme/notes) | 🟡 REA siap |
| 5 | Party & Matchmaking | Solo/Duo/Trio/Full 5; party besar hanya lawan party ≥3 | OpenSkill (publik) | 🟢 |
| 6 | MMR & Tier | Hidden MMR + Rank Points; Bronze→Silver→Gold→Platinum→Diamond→Mythic (+Top 100); soft reset per season | Publik | 🟢 |
| 7 | Combat & State Machine | Idle/Run/Dash/Jump/Attack/Skill/Guard/Airborne/Down/Faint/Bound/Frozen/GetUp-invincible; gear/hero swap | **LostSaga** | 🔴 client belum ada |
| 8 | Hero Roster & Mastery | Hero dibeli Gold/MiCash; **Mastery** membuka kosmetik, bukan stat | LostSaga (mercenary) | 🟡 |
| 9 | Profil & Statistik | Win rate, KDA, hero favorit, stat per hero, match history, peak tier, badge | Publik (Dota/MLBB UI) | 🟢 |
| 10 | Squad, Squad War, Leader Duel | Squad HQ, war mingguan rebut distrik Plaza; pemenang mengubah tampilan distrik (bendera, patung) | LostSaga guild, CoC clan war | 🟡 |
| 11 | Relic (PvE) | Masuk pakai Gold = drop standar; pakai **Ticket** = peti Relic dengan rate dipublikasikan + pity | LostSaga Relic | 🟡 |
| 12 | Ekonomi & Toko | Gold/Ticket/MiCash, sewa 7/30 hari/permanen, gacha + pity, **rent-to-own** | LostSaga, Genshin (pity) | 🟢 |
| 13 | Live-ops & Content Pipeline | Semua angka di tabel data server; season 8–10 minggu; battle pass kosmetik; event rotasi | AyoDance (`DATA/` sebagai contoh pola tabel) | 🟢 |
| 14 | Dev Mode, GM Tools, Moderasi, Anti-cheat | Panel GM berbasis role + audit log; Dev Lounge; server-authoritative | Desain sendiri | 🟢 |

## C. Ide Baru (v2)

1. **Plaza yang berubah karena komunitas** — hasil Squad War mengganti bendera/warna distrik selama seminggu; patung avatar Mythic #1 muncul di alun-alun. Dunia terasa hidup tanpa open-world berat.
2. **Dance Duel** — DNA Audition: tantangan ritme singkat di Plaza antar-avatar, hadiah Gold kecil + emote. Jembatan antara sisi sosial dan kompetitif.
3. **Rent-to-own** — setiap kali menyewa item (7/30 hari), sebagian harga jadi kredit untuk versi permanen. Player merasa sewa tidak "hangus" → konversi ke MiCash lebih sehat.
4. **Mastery = kosmetik** — main hero berkali-kali membuka border, emote, warna skin; gengsi tanpa stat.
5. **Squad HQ dekorasi** — "Roblox-lite": furnitur dari toko/Relic untuk menghias markas squad. World building digerakkan player.
6. **Mentor system** — player Diamond+ jadi mentor newbie; keduanya dapat reward jika newbie naik tier. Membangun komunitas dan retensi.
7. **Spectate di layar Plaza** — Leader Duel dan final Squad War ditayangkan di layar besar Plaza.
8. **Gacha transparan** — rate tertulis, pity terlihat (counter), duplikat jadi shard → bisa tukar item pilihan.

## D. Ruang Lingkup MVP (usulan vertical slice)
1. Login + role
2. Plaza 1 distrik + chat + emote
3. Wardrobe 5 slot + toko Gold (sewa 7/30/permanen)
4. Arena 1v1 & 2v2, 4 hero, state machine dasar
5. MMR + tier + profil sederhana
6. Panel Dev (spawn item, set MMR, kick/ban) dengan audit log

Sisanya (Squad War, Relic, Rest Room minigame, gacha, battle pass) di fase 2–3.

## E. Kendala yang Tersisa
| Kendala | Jenis | Solusi |
|---|---|---|
| LostSaga client tidak ada | Bahan riset | User menyediakan folder/installer; sementara pakai wiki + video |
| Ghidra belum terpasang | Tooling | JDK 21 + Ghidra 12.1.x + `GHIDRA_INSTALL_DIR` (hanya jika data tabel tidak cukup) |
| Keputusan desain inti | Keputusan user | Lihat `91-open-questions.md` #2–#6 |
