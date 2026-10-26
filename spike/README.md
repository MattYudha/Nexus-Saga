# Spike — Nexus Saga (Quantum-first)

Artefak teknis awal Spike Fase 1. Rencana & langkah: [`../docs/20-rencana-spike-fase1.md`](../docs/20-rencana-spike-fase1.md) (revisi v2 Quantum-first).

## Isi
| File | Isi | Langkah |
|---|---|---|
| `quantum/Nexus.qtn` | Data contract Quantum 3 (DSL): input, komponen `NxCombat` per pemain, global, signal | Q-02 |
| `quantum/NxCombatSystem.cs` | Skeleton sistem combat deterministik (tick pipeline, gerak 8 arah, guard lock-facing, timer) | Q-03/Q-05 |

> Ini **blueprint source** (ditulis sesuai API Quantum 3 dari `photon-backend`), **belum** proyek Unity+Quantum yang bisa di-build. Untuk menjalankan, perlu di-drop ke proyek Quantum (lihat Q-01).

## Keputusan yang MASIH DIBUTUHKAN sebelum lanjut (Q-01)
**Lokasi proyek spike:**
- **Opsi A — extend `C:\Users\US3R\photon-backend`**: reuse Unity 2022.3.62f1 + Quantum SDK 3.0.14 + CI Android + backend ASP.NET yang sudah jalan. Tercepat. Tapi mencampur dengan demo Pong (perlu rapikan/pisah folder).
- **Opsi B — repo Quantum baru** (salin fondasi dari photon-backend): bersih, tapi setup ulang Unity+Quantum+CI.

**Rekomendasi: Opsi A** (buat folder `game/Assets/QuantumUser/Simulation/Nexus` + `View/Nexus` di samping Pong; backend tambah endpoint match Nexus). Hemat waktu maksimal.

## Catatan
- `photon-backend` **privat** (SDK Quantum proprietary) — jangan commit SDK ke repo publik Nexus.
- Kode di sini = desain/blueprint, aman di repo docs.
