# Riset: io3dengine.dll (LostSaga / LSRebirth) — engine 3D

Sumber: `C:\Program Files (x86)\LSRebirth\io3dengine.dll` (PE32 x86, SHA-256 `cb4ba828…9764`). Dibedah dengan REA + Ghidra. **Clean-room:** pelajari struktur/desain, tulis spesifikasi sendiri; tidak menyalin kode/aset, tidak membongkar proteksi.

Label: **OBSERVED** (bukti dari biner) · **INFERRED** · **UNKNOWN**.

> ⚠️ **Batas:** `io3dengine.dll` adalah **engine render/3D** (tidak ter-pack → bisa didekompilasi). Logika combat/hitbox gameplay kemungkinan di `lostsaga.exe` yang **ter-pack Themida → TIDAK dibongkar**. Jadi target realistis di sini: **struktur animasi skeletal, format model/mesh, scene, dan collision/physics engine** — sebagai **referensi** untuk animasi & hitbox 3D Combat Core kita (doc 13/18), bukan menyalin.

## Tujuan (apa yang dicari)
1. **Animasi skeletal:** struktur bone/skeleton, matriks bone, keyframe/clip, blending, sampling per frame.
2. **Model/mesh:** format mesh, skinning, attachment/socket (relevan untuk gear di socket, doc 19).
3. **Collision/physics:** bentuk collision (box/capsule/mesh?), deteksi tabrakan, raycast.
4. **Scene/transform:** hierarki node, transform, kamera.
5. **API surface (exports):** apa yang DLL ini sediakan ke game.

## Rencana bedah (fokus, hemat)
1. `binary_overview` — jumlah fungsi/string/segment (RUNNING).
2. `list_names` (exports) — permukaan API engine.
3. `search_strings` kata kunci: anim, bone, skeleton, skin, mesh, model, collision, bound, frame, matrix, quaternion, keyframe, hitbox, vertex, io3d.
4. Dari string/exports → temukan fungsi kunci → `procedure_pseudo_code` beberapa yang relevan.
5. Tulis temuan + **spesifikasi adaptasi** untuk Combat Core kita.

---

## Hasil

### 0. Gambaran (binary_overview)
_menunggu analisis Ghidra…_

### 1. API surface (exports)
_TBD_

### 2. Animasi skeletal
_TBD_

### 3. Model / mesh / skinning
_TBD_

### 4. Collision / physics
_TBD_

### 5. Scene / transform / kamera
_TBD_

---

## Adaptasi untuk Nexus Saga (diisi setelah temuan)
Fokus: apa yang relevan untuk **animasi sampling (tanpa root motion)** dan **hitbox 3D** Combat Core — bandingkan dengan doc 13 (format hitbox per frame) & doc 18 (skema animasi). Hanya pola/struktur yang diadopsi, ditulis ulang sendiri.

## File lain LostSaga (status)
| File | Status RE |
|---|---|
| `io3dengine.dll` | ✅ Tidak ter-pack → sedang dibedah (dokumen ini) |
| `lostsaga.exe` | ❌ Themida → tidak dibongkar |
| `iopac.dll` | ⚠️ Terproteksi sebagian (doc 07 §E) → ditunda |
| `rs.iop`/`map.iop` | ZIP termodifikasi → parser khusus, belum |
| Engine DLL lain (`iofreetype`, `iovoicechat`, `townportal`, `il`, `imc`) | Belum dicek; prioritas rendah |
