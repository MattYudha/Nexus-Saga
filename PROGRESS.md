# Nexus Saga: Chronicles — Progres & Checklist

_Terakhir diperbarui: 2026-10-26_

Social-Competitive Action-RPG brawler hybrid. Dokumen ini ringkasan progres lintas fase.
Detail teknis ada di `docs/` (00–25) dan `docs/90-decision-log.md`.

**Legenda:** ✅ selesai & terverifikasi · 🧪 selesai, menunggu uji live · 🔜 berikutnya · ⬜ belum

---

## Fase 0 — Riset, RE, Desain (✅ selesai)
- [x] ✅ Konsep game & pilar (avatar-social + team brawler + ekonomi kosmetik non-P2W + MMR)
- [x] ✅ Tema "Hypebeast Meets Combat Exo-Gear", kota Neo-Veridia, faksi ORDE vs LEGION
- [x] ✅ Struktur kompetitif 4 jalur (Solo 1v1, Squad War, Faction War, Street Room)
- [x] ✅ Desain Combat Core (OBB+Sphere, Damage Gate→Critical→3 Break Stock→Gear Drop→KO, Guard 180)
- [x] ✅ RE clean-room `io3dengine.dll` (validasi rig/bone/hitbox/kamera) — tanpa salin kode/aset
- [x] ✅ Dokumen desain 00–24 + decision log + proposal (PDF confidential, tak di-push)
- [x] ✅ 3 aturan arsitektur (bone-attached OBB baked · split-session routing · anti-cheat checksum+replay)

## Fase 1 — Spike Netcode (✅ LULUS)
- [x] ✅ Spike Photon **Quantum 3** deterministik (FP, tanpa float/RNG)
- [x] ✅ Combat mini jalan: gerak 8 arah, lompat, dash i-frame, Guard 180, Critical+Gear Drop, KO
- [x] ✅ Multiplayer 2 klien via Photon, **stabil di 176ms ping**, tanpa freeze/desync
- [x] ✅ Keputusan GO: adopsi Quantum 3, **custom UDP dibatalkan** (doc 22)
- [x] ✅ Engine dikunci: Unity 2022.3.x (Built-in RP)

## Fase 2 — Vertical Slice (sedang berjalan)

### 2a. Combat & Hero (✅ terverifikasi di Unity)
- [x] ✅ 2 hero: **TITAN-01** (grappler/melee, skill lunge) & **PULSE-X** (zoner, projectile, charged shot)
- [x] ✅ Sistem projectile deterministik (`NxProjectile` + `NxProjectileSystem`)
- [x] ✅ Logika damage bersama (`NxDamage`) dipakai melee & projectile (satu sumber kebenaran)
- [x] ✅ Balance: peluru chip (anti-stunlock), dash lebih jauh, dummy zoner
- [x] ✅ **Layar Pilih Hero** (State 0, pilihan via input deterministik) + ganti hero live (H)

### 2b. Skala & Team Brawler (✅ terverifikasi — 60 FPS)
- [x] ✅ **5v5 = 10 fighter** (1 human + 9 bot), **stabil 60 FPS, tanpa freeze**
- [x] ✅ Skor per-tim (ScoreA/ScoreB)
- [x] ✅ Fix respawn: bleed-out timer (tak nyangkut di Critical)
- [x] ✅ `NxSeparationSystem` (pushbox ringan, anti-numpuk)

### 2c. Backend Meta — Solo 1v1 Ranked (✅ terverifikasi — 25/25 test)
- [x] ✅ .NET 8 SDK + alur build/test (DB in-memory, tanpa Docker)
- [x] ✅ **Glicko-2** gantikan Elo (RD+Volatility, EF migration) — cocok contoh resmi Glickman
- [x] ✅ **Matchmaking MMR** (join/status/leave, rating terdekat + region)
- [x] ✅ Auth tamu (device→JWT), profil, leaderboard, report-result "kedua lapor cocok" (semi anti-cheat)
- [x] ✅ Fallback DB in-memory untuk dev (`dotnet run` tanpa Postgres)
- [x] ✅ **25/25 test lolos** + smoke-test runtime end-to-end (login→antre→matched→report→Glicko-2→leaderboard)
- [x] ✅ Repo backend di-push → `github.com/MattYudha/be-Nexus-saga-` (tanpa SDK Quantum)

### 2d. Flow Ranked di Unity (✅ terverifikasi live)
- [x] ✅ `NexusBackend.cs` — REST client (auth, matchmaking, report)
- [x] ✅ Tombol **Ranked Match (MMR)** di `NexusGame` (login→antre→room→main→lapor→tampil rating)
- [x] ✅ Win-condition sim (tim pertama `KoTarget` KO → match selesai; aktif bila ≥2 manusia)
- [x] ✅ Slot report = PlayerRef in-game (pemenang benar di Glicko-2) + skor di-clamp legal
- [x] ✅ Device-id unik per-launch (2 instance = akun beda → matchmaking pasti jalan)
- [x] ✅ Matchmaking retry bersih (Leave-before-Join) + Cancel menghentikan pencarian
- [x] ✅ UX Pilih Hero: feedback hijau "terpilih" + "menunggu pemain lain (X/Y siap)"
- [x] ✅ Arena dibersihkan saat match selesai (background hasil bersih)
- [x] ✅ **UI Leaderboard** di menu (ambil `/api/leaderboard` → top rating + W/L)
- [x] ✅ **Uji live editor+build LULUS** — loop ranked penuh jalan tanpa bug

### 2e. Sistem Akun, Profil & Statistik (✅ backend terverifikasi — 31/31 test)
Schema dari riset (doc 15 §3 + doc 24 §2.3), bukan karangan:
- [x] ✅ Register & Login (username + password, hash ASP.NET PasswordHasher) + Guest
- [x] ✅ **Progres 3 lapis**: Account Rank (Trainee→Colonel dari XP), Solo Ladder tier (**Rookie→Contender→Rival→Gladiator→Conqueror→Nexus Legend**), Faction (Orde/Legion)
- [x] ✅ **Statistik tempur**: kills/deaths/assists/**KDA**, wins/losses/win-rate, matches, account level/XP
- [x] ✅ Sim melacak **Kills per-pemain** (kredit killer) + deaths (termasuk bleed-out) → klien lapor saat match selesai
- [x] ✅ `/me` profil penuh + match report terima kills/deaths + akumulasi + XP
- [x] ✅ UI Unity: **halaman Profil sendiri** (3 lapis rank, statistik, riwayat match, faction picker), layar Login/Register/Guest, leaderboard
- [x] ✅ Repo BE di-update ke `github.com/MattYudha/be-Nexus-saga-`
- [x] ✅ **DB + Docker** (doc 26): PostgreSQL persisten via Docker-in-WSL2, migration auto-apply, `localhost:5080` dari Windows — **persistensi terbukti** (data bertahan setelah recreate container)
- [ ] ⬜ Uji live UI akun+profil di Unity (CodeGen field Kills + recompile + rebuild .exe)

## Fase 2 — Sisa (🔜 berikutnya)
- [ ] 🔜 Profil & ekonomi kosmetik (faction, currency, wardrobe/inventory, unlock hero) — backend, bisa dites
- [ ] ⬜ Hitbox dari animasi (bone-attached OBB baked) — butuh aset 3D + animasi
- [ ] ⬜ True 1v1 ranked (tanpa bot) / mode terpisah
- [ ] ⬜ Aset 3D (shared rig + streetwear/exo-gear, pipeline Blender)
- [ ] ⬜ Split-session routing (Photon hanya Arena, Plaza=Nakama)
- [ ] ⬜ Anti-cheat backend replay re-sim

---

## Lokasi kode
- **Dokumen desain** (repo ini): `github.com/MattYudha/Nexus-Saga` (publik)
- **Backend meta** (ASP.NET Core 8): `github.com/MattYudha/be-Nexus-saga-`
- **Game Quantum 3** (`photon-backend`, PRIVAT — SDK Quantum proprietary): lokal, tidak di-push

## Cara jalankan (ringkas)
```
# Backend (dev, cukup .NET 8 SDK)
cd backend && dotnet test
dotnet run --project src/PhotonBackend.Api --urls http://localhost:5080

# Game: buka photon-backend/game di Unity 2022.3.x → scene NexusOnline → Ranked Match
```
