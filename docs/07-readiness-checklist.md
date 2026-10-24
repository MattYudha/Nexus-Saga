# 07 — Readiness Checklist (cek 2026-10-24)

## A. Bahan riset
| Item | Path | Status |
|---|---|---|
| Ikemen GO v1.0.0 | `C:\Users\US3R\Nexus_Lab\Ikemen_Go-v1.0.0` | ✅ 230 file. Rilis biner + `chars/` & `data/` (file state `.cns` = yang kita butuhkan) |
| DDNet 20.1.1 | `C:\Users\US3R\Nexus_Lab\DDNet-20.1.1-win64` | ✅ 930 file. Source C++ ada di GitHub `ddnet/ddnet` bila perlu baca netcode |
| AyoDance | `C:\Megaxus\AyoDance` | ✅ 22 GB (statis saja, ada Xigncode) |
| LostSaga (LSRebirth) | `C:\Program Files (x86)\LSRebirth` | ✅ 66 file, 1,6 GB. Lihat bagian E |

## B. Tooling RE
| Item | Status | Masalah |
|---|---|---|
| REA MCP 6.7.0 | ✅ Terhubung | — |
| JDK 21.0.12 (Temurin) | ✅ Terinstal | Cadangan bila JDK 25 bermasalah |
| JDK 25.0.4 (Temurin) | ✅ Dipakai REA (`JAVA_HOME` di config MCP REA) | — |
| Ghidra 12.1.4 | ✅ **Available di REA** (`...\ghidra_12.4_PUBLIC\ghidra_12.1.4_PUBLIC`, env di config MCP REA). Uji `iopac.dll` sukses | — |
| Ghidra 12.2 | Terekstrak, untuk GUI manual saja | REA 6.7.0 hanya menerima 12.1.x |
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

## E. Temuan awal LostSaga (LSRebirth) — cek ulang 2026-10-24
Observasi statis (tidak menjalankan game):
| File | Temuan | Dampak |
|---|---|---|
| `lostsaga.exe` (17 MB, x86 32-bit) | Nama section acak (`usesrdol`, `dhreteyn`, kosong), entropi 7,77–7,99 → **ter-pack/terproteksi** | Ghidra hanya melihat data acak. **Tidak akan di-unpack** (membongkar proteksi = di luar batas riset kita) |
| `io3dengine.dll` | Section normal (`.text` entropi 6,5) → **tidak ter-pack** | Bisa didekompilasi: engine render/fisika/animasi |
| `iopac.dll` | Pembaca arsip `.iop`. Ghidra: hanya 63 fungsi, `.text` 264 KB tapi section data bernama aneh (`.data_.t` 864 KB, `.data__` 652 KB) → **indikasi terproteksi/ter-pack sebagian** | Perlu dicek lebih lanjut sebelum dijadikan dasar parser |
| `rs.iop` (458 MB), `map.iop` (1,1 GB) | Header `PK` (ZIP) dengan folder `config/`, tapi **struktur ZIP dimodifikasi** — ditolak oleh Python `zipfile` dan REA `inspect_artifact` | Perlu parser khusus untuk membaca daftar/isi `config/` (tabel skill, gear, state) |
| Anti-cheat | Folder `EasyAntiCheat` + `GameGuard`, `start_protected_game.exe` | Analisis statis saja; jangan jalankan di bawah debugger/Frida |

Rencana: (1) baca `config/` dari `rs.iop` lewat analisis format arsip (`iopac.dll` di Ghidra jika perlu), (2) `io3dengine.dll` untuk struktur animasi/hitbox, (3) observasi video untuk timing state.

