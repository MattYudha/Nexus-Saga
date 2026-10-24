# 07 — Readiness Checklist (cek 2026-10-24)

## A. Bahan riset
| Item | Path | Status |
|---|---|---|
| Ikemen GO v1.0.0 | `C:\Users\US3R\Nexus_Lab\Ikemen_Go-v1.0.0` | ✅ 230 file. Rilis biner + `chars/` & `data/` (file state `.cns` = yang kita butuhkan) |
| DDNet 20.1.1 | `C:\Users\US3R\Nexus_Lab\DDNet-20.1.1-win64` | ✅ 930 file. Source C++ ada di GitHub `ddnet/ddnet` bila perlu baca netcode |
| AyoDance | `C:\Megaxus\AyoDance` | ✅ 22 GB (statis saja, ada Xigncode) |
| **LostSaga** | `C:\Users\US3R\Nexus_Lab\LostSaga` | ❌ **Folder tidak ada.** Tidak ditemukan juga di Downloads/Desktop/Program Files |

## B. Tooling RE
| Item | Status | Masalah |
|---|---|---|
| REA MCP 6.7.0 | ✅ Terhubung | — |
| JDK 21.0.12 (Temurin) | ✅ Terinstal `C:\Program Files\Eclipse Adoptium\jdk-21.0.12.101-hotspot` | ❌ Tidak ada di PATH, `JAVA_HOME` kosong |
| JDK 25.0.4 (Temurin) | ✅ Terinstal | Hanya dibutuhkan Ghidra 12.2 |
| Ghidra 12.2 | ✅ Terekstrak | ❌ **REA 6.7.0 hanya menerima Ghidra 12.1.x** (verified 12.1.4, `GhidraReleasePolicy.js`). 12.2 berstatus *unsupported*. 12.2 juga mewajibkan Java ≥ 25 |
| `GHIDRA_INSTALL_DIR` | ⚠️ | Menunjuk ke `...\Nexus_Lab\ghidra_12.1.2_PUBLIC` yang **tidak ada** |
| Disk C: | ⚠️ 55 GB kosong | Cukup untuk sekarang; tidak cukup bila LostSaga + ekstrak arsip besar |

### Perbaikan Ghidra
1. Unduh **Ghidra 12.1.4** → ekstrak ke `C:\Users\US3R\Nexus_Lab\ghidra_12.1.4_PUBLIC`
2. ```
   setx GHIDRA_INSTALL_DIR "C:\Users\US3R\Nexus_Lab\ghidra_12.1.4_PUBLIC"
   setx JAVA_HOME "C:\Program Files\Eclipse Adoptium\jdk-21.0.12.101-hotspot"
   ```
3. Tutup Termul sepenuhnya → buka lagi → jalankan Claude Code.
4. Ghidra 12.2 boleh disimpan untuk dipakai manual (GUI) dengan JDK 25.

## C. Perancangan arsitektur — bisa mulai SEKARANG
Arsitektur tidak bergantung pada RE. Yang masih menahan:
| Keputusan | Status |
|---|---|
| Kamera: 3D free-roam + quarter-view tetap | ⏳ Menunggu konfirmasi |
| Avatar di arena: Opsi B + aturan siluet | ⏳ Menunggu konfirmasi |
| Engine client (Unity / Godot) | ⏳ Belum diputuskan |
| Backend (Nakama / custom) & netcode | ⏳ Belum diputuskan |

## D. Implementasi — belum bisa mulai
| Kebutuhan | Status |
|---|---|
| Engine terinstal (Unity Hub / Godot) | ❌ Belum ada |
| Docker Desktop (Nakama + Postgres lokal) | ❌ Belum ada (Postgres & Redis/Memurai lokal sudah jalan — bisa jadi alternatif) |
| Go | ✅ Terinstal (berguna jika pakai Nakama — runtime module Go) |
| Izin user untuk mulai coding | ❌ Belum diberikan (ground rule) |
