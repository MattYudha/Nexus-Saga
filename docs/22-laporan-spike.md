# 22 — Laporan Spike Fase 1 & Keputusan Go/No-Go (2026-10-26)

## Keputusan: ✅ **GO — adopsi Photon Quantum 3.** Netcode custom UDP dibatalkan.

## Apa yang diuji
Brawler deterministik minimal di **Photon Quantum 3** (di atas fondasi `photon-backend` milik user), diimplementasi langsung di Unity:
- Combat Core: gerak 8 arah, lompat, dash (i-frame), **Guard 180° + lock-facing + guard crush/faint**, attack + knockback, **Damage Gate → Critical → 3 Break Stock → Gear Drop → KO/respawn**, dummy AI.
- Collision: **OBB + Sphere** (sesuai amandemen doc 13), semua **fixed-point** (FP), tanpa float/RNG non-seeded.
- Networking: `NexusGame` connect ke Photon Cloud **tanpa backend/auth** (disederhanakan), quick match, region pin "asia".
- Uji lag: toggle simulasi **~150 ms** (terukur **176 ms ping** di game).

## Hasil (rasa, pada 176 ms ping)
| Kriteria | Hasil |
|---|---|
| Gerak pemain sendiri instan (prediksi lokal) | ✅ |
| Pukulan nyambung / responsif | ✅ |
| Tidak freeze / tidak desync | ✅ |
| Lawan dikoreksi halus (rollback) | ✅ stabil |
| 2 client (editor + build) konek & main | ✅ |

**Verdict:** memenuhi kriteria teknis. Rollback Quantum menjaga rasa instan walau lag tinggi.

## Keputusan yang mengikat
1. **Netcode = Photon Quantum 3** (predict-rollback). Custom UDP server-authoritative **dibatalkan**.
2. **Engine client = Unity** (sudah dikunci; bake-off Godot batal).
3. Combat Core = desain Ikemen-derived (OBB+Sphere, state machine, Critical/Gear) **diimplementasi sebagai Quantum systems**.
4. 3 aturan arsitektur tetap berlaku (doc 20 rev v2): **bone-attached OBB + offline pose baking**, **split-session routing** (Photon hanya di Arena, Plaza=Nakama), **anti-cheat checksum + backend replay re-sim**.

## Yang BELUM diuji (untuk fase berikut, bukan blocker keputusan)
- **10 pemain** (baru 2–3 entity). Perlu uji skala rollback nanti.
- Backend replay re-sim nyata (anti-cheat hasil).
- Jitter + packet loss tinggi (baru lag murni).

## Status kode (di `photon-backend`, terpisah dari Pong)
```
Simulation/Nexus/ : Nexus.qtn, NxCombatSystem.cs, NxHitSystem.cs
View/Nexus/       : NexusInput.cs, NexusView.cs, NexusGame.cs
Editor/           : NexusSetup.cs (Create Local/Online Scene)
```
Scene: `NexusLocal.unity` (local play), `NexusOnline.unity` (networked). Region `asia`.

## Langkah berikutnya (Fase 2 — Vertical Slice, di atas Quantum)
Prioritas (ambil bertahap):
1. **2 hero nyata**: TITAN-01 (grappler) & PULSE-X (zoner) dengan skill + gear (data-driven).
2. **Hitbox dari animasi** (bone-attached OBB → bake ke Quantum Asset).
3. **Uji 10 pemain** (skala rollback + bandwidth).
4. **Backend meta**: auth, profil, **MMR Solo 1v1 (Glicko-2)**, matchmaking 4 jalur (doc 24), shop/wardrobe. Nakama atau perluas ASP.NET photon-backend.
5. **Aset 3D**: shared humanoid rig + streetwear/exo-gear (pipeline Blender, doc 21).
6. **Split-session routing** (Photon hanya Arena).
7. **Anti-cheat**: backend replay re-sim.
