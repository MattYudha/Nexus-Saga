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

### 2d. Flow Ranked di Unity (🧪 selesai, menunggu uji live)
- [x] 🧪 `NexusBackend.cs` — REST client (auth, matchmaking, report)
- [x] 🧪 Tombol **Ranked Match (MMR)** di `NexusGame` (login→antre→room→main→lapor→tampil rating)
- [x] 🧪 Win-condition sim (tim pertama `KoTarget` KO → match selesai; aktif bila ≥2 manusia)
- [x] 🧪 Slot report = PlayerRef in-game (pemenang benar di Glicko-2) + skor di-clamp legal
- [ ] ⬜ **Uji live** editor+build (perbaiki bila ada error compile/runtime)

## Fase 2 — Sisa (🔜 berikutnya)
- [ ] 🔜 Uji live flow ranked → stabilkan
- [ ] ⬜ Hitbox dari animasi (bone-attached OBB baked) — butuh aset 3D + animasi
- [ ] ⬜ True 1v1 ranked (tanpa bot) / mode terpisah
- [ ] ⬜ Profil & ekonomi kosmetik (faction, currency, wardrobe/inventory, unlock hero)
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
