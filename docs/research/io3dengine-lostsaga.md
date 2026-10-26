# Riset: io3dengine.dll (LostSaga / LSRebirth) — engine 3D

Sumber: `C:\Program Files (x86)\LSRebirth\io3dengine.dll` (PE32 x86, SHA-256 `cb4ba828…9764`). Dibedah dengan REA + Ghidra 12.1.4. **Clean-room:** pelajari struktur/desain, tulis spesifikasi sendiri; tidak menyalin kode/aset, tidak membongkar proteksi.

Label: **OBSERVED** (bukti dari biner) · **INFERRED** · **UNKNOWN**.

> ⚠️ Logika combat/hitbox gameplay ada di `lostsaga.exe` (**Themida, tidak dibongkar**). Dokumen ini = sisi **engine 3D** (animasi skeletal, mesh, collision) sebagai **referensi** untuk animasi & hitbox 3D Combat Core kita (doc 13/18).

## Kabar baik
PDB (`io3DEngine.pdb`) tidak ada, **tapi** DLL ini mengandung **simbol C++ ter-mangle lengkap (RTTI/vtable)** di `.rdata`. Ghidra memulihkan **nama class + signature method** → arsitektur engine terbaca langsung tanpa menebak. 25.582 fungsi, 9.615 string. Engine berbasis **DirectX 9** (tipe `D3DXVECTOR3/QUATERNION/MATRIX`), C++ + STL, manajer **Singleton**, nama via **ioHashString**. Build path internal: `e:\forlunar\...\io3dengine\`.

---

## 1. Arsitektur skeleton: pola Resource/Instance (= shared rig kita)
OBSERVED (dari signature):
- **`ioRcSkeleton`** = skeleton **resource/referensi bersama** (dimuat dari file `.skl`).
- **`ioSkeleton`** = **instance** per-entity (punya blend, physics, extra-rotate).
- **`ioSkeletonManager`** (Singleton): `LoadFile(.skl)`, `CreateSkeleton` (resource), `CreateInstance` → instance, `GetSkeletonByName`, `ReLoad`.

➡️ **Persis pola kita** (doc 18 §4.1): shared rig (RcSkeleton) + instance per karakter. Divalidasi oleh engine nyata.

## 2. Bone = `ioBiped` (pose = posisi + quaternion)
OBSERVED:
- Skeleton menyimpan **daftar biped (bone)**: `CreateBiped`, `GetBiped(name|index)`, `GetBipedCnt`, `GetBipedIndex(ioHashString)`, `AllocBipedList`, `GenerateBipedList`, `BuildBipedIndexList`.
- Bone diakses via **nama (hash) ATAU index**.
- Pose per-bone: `BlendBiped(int idx, float weight, D3DXVECTOR3 pos, D3DXQUATERNION rot)` → blend pose per-bone dengan bobot.
- `CacheBipedMatrices(skeleton)` → hitung & cache **matriks bone** (pose akhir untuk render/skinning).

➡️ Model pose: **per-bone (posisi + quaternion), di-blend, lalu di-cache jadi matriks**. Standar skeletal animation.

## 3. Animasi: `ioAnimation` + `ioAniController` (track + blend)
OBSERVED:
- `ioAnimation`: `BuildAniTrackList(skeleton)` (animasi punya **track** per-bone), `BlendSkeleton(skeleton)` (terapkan animasi ke skeleton dengan blend).
- `ioAniController::UpdateSkeleton(float)` — controller menggerakkan skeleton seiring **waktu (float)**.
- `ioEffect::SetAnimation`, `ClearSkeletonAndAnimation`, `SetCustomSkeletonAniName`.

➡️ Alur: AniController(waktu) → Animation.BlendSkeleton → Skeleton(bone pose) → CacheBipedMatrices → render. **Catatan untuk kita:** ini semua **sisi visual client**. Combat Core kita **tidak** butuh matriks bone; Core hanya butuh `(animId, frame)` untuk lookup hitbox + root transform (doc 18 §5). Pemisahan ini valid.

## 4. 🔑 Attachment gear/kostum: `LinkedSkeleton` (butuh bone-count sama)
OBSERVED:
- `ioRcSkeleton::SetLinkedSkeleton / GetLinkedSkeleton / IsLinkedSkeleton / ReleaseLinkedSkeleton`.
- Error string: **"SetLinkedSkeleton - Not Same Biped Cnt (%d/%d)"** dan "%s Not Exist".

➡️ **Ini cara LostSaga memasang bagian terpisah (gear/kostum) ke skeleton tubuh**: dua skeleton di-*link* dan **wajib jumlah bone sama**. **Persis keputusan kita** (doc 19): gear memakai **shared humanoid rig** agar bisa dipertukarkan. Engine nyata membuktikan: attachment lintas-bagian menuntut struktur bone identik → **shared rig standar itu wajib, bukan opsional**.

## 5. Collision: OBB + Sphere + AABB (TANPA capsule)
OBSERVED — pustaka `ioMath` (static) + tipe geometri:
| Tipe | Class |
|---|---|
| OBB (oriented box) | `ioOrientBox` |
| AABB | `ioAxisAlignBox` |
| Sphere | `ioSphere` |
| Ray / Segment / Plane | `ioRay`, `ioSegment`, `ioPlane` |

- `ioOrientBox`: `SetCenter`, `SetExtents(axis, val)`, `SetAxis`, `SetBoxByMinMax`, `GetVertices`, `GetTransform()→D3DXMATRIX`, **`Transform(vec3 pos, quat rot)`** dan `Transform(matrix)`, `GetBoxRadius`.
- `ioMath::TestIntersection`: **OBB-OBB**, **OBB-Sphere**, OBB-Plane, Ray-OBB, Segment-OBB. `FindIntersection` (titik), `InBox`, `SphereTestLightly`.
- **Satu collision box per entity:** `ioEntityGroup::GetCollisionBox()→ioOrientBox`, `ioEffect::GetCollisionBox`.

➡️ **Memvalidasi pilihan OBB kita** (doc 13) dan pola **"OBB lokal → dunia via Transform(pos, quat)"** persis seperti rencana kita. **Temuan penting: LostSaga TIDAK pakai capsule** — brawler penuh cukup dengan **OBB + Sphere**. Lihat §9 (usul penyederhanaan).

## 6. Secondary physics: rope/cloth spring (kosmetik)
OBSERVED: `ioSkeleton::AddRopeSpringCurve(RopeSpringParam)`, `UpdateRopeSpringCurve(float)`, `HasRopeSpring`, `AddWorldForce(vec3)`, `DebugRopeCollisionBox(vector<ioOrientBox>)`.
➡️ Physics pegas untuk **jubah/rambut/tali** (jiggle), bertabrakan dengan OBB. **Client-only, kosmetik** — sejalan dengan aturan kita (VFX/physics kosmetik tidak pernah memengaruhi sim). Relevan untuk cape/aksesori streetwear kita.

## 7. Entity & aset
OBSERVED: `ioEntity`, `ioEntityGroup` (punya skeleton + collision box + nama skeleton), `ioEffect` (skeleton + anim + collision box), `ioModelParticle`, `ioMeshTrailer`/`ioMeshTrailDataManager` (trail senjata). `ioDecalMaker` (decal pakai OBB).
File: **`.skl`** (skeleton). Definisi entity berbasis **teks** (`ioEntityGroupBuilder::ParsingSkeleton`, `ioTextStream`, token `#SKELETON`, `skeleton_name`) + **biner** (`ioBinaryStream`, `IsSkeletonFile`).

---

## 8. Ringkasan class penting (peta)
| Class | Peran |
|---|---|
| `ioRcSkeleton` / `ioSkeleton` / `ioSkeletonManager` | Skeleton resource / instance / manager |
| `ioBiped` / `ioRcBiped` | Bone (instance/resource) |
| `ioAnimation` / `ioAniController` | Klip animasi + kontroler waktu |
| `ioEntity` / `ioEntityGroup` | Objek dunia (skeleton + collision + mesh) |
| `ioEffect` | Efek dengan skeleton+anim+collision |
| `ioOrientBox` / `ioAxisAlignBox` / `ioSphere` | Volume collision |
| `ioMath` | Uji perpotongan geometri |
| `ioMeshTrailer` | Trail senjata |
| `ioHashString` | Kunci nama (hash) |

---

## 9. Adaptasi untuk Nexus Saga (apa yang dikonfirmasi / dipertimbangkan)
| Temuan LostSaga | Dampak ke kita |
|---|---|
| Rc(shared) + Instance skeleton | ✅ **Konfirmasi** shared rig + instance (doc 18). Lanjutkan |
| Bone via index + name-hash | ✅ Adopsi: bone list standar + lookup hash |
| Pose = per-bone (pos, quat) → matriks cache | ✅ Visual client; Core kita cukup `(animId, frame)` + root — pemisahan valid (doc 18 §5) |
| **LinkedSkeleton butuh bone-count SAMA** | ✅ **Membuktikan shared rig wajib** untuk gear/kostum tukar-pasang (doc 19). Kunci daftar bone standar sejak awal |
| Collision **OBB + Sphere** (Transform via pos+quat) | ✅ **Konfirmasi OBB** (doc 13). Pola transform sama |
| **TIDAK ada capsule** | 🔧 **Usul penyederhanaan:** pertimbangkan **OBB + Sphere saja** (seperti LostSaga), drop capsule, agar kode collision Core lebih sederhana & cepat. Capsule hanya jika benar-benar perlu untuk badan silinder |
| 1 collision box per entity | 💡 LostSaga 1 OBB/entity. Kita **lebih granular** (hurt/attack per frame, ala Ikemen) — tetap, tapi bisa pakai **1 OBB "pushbox" badan** + volume per-frame untuk hit/hurt |
| Rope/cloth spring physics (kosmetik) | 💡 Untuk cape/rambut/aksesori streetwear — **client-only**, tidak menyentuh sim |
| `.skl` teks+biner, entity text format | 💡 Referensi; kita pakai glTF + data JSON (doc 13/18), konsepnya sejajar |

**Kesimpulan:** engine nyata LostSaga **memvalidasi hampir semua keputusan arsitektur 3D kita** (shared rig, OBB, transform pos+quat, pemisahan visual/sim). Satu usul konkret baru: **evaluasi OBB+Sphere tanpa capsule** untuk menyederhanakan collision Core.

## 10. File lain LostSaga (status RE)
| File | Status |
|---|---|
| `io3dengine.dll` | ✅ **Selesai dibedah** (dokumen ini) |
| `lostsaga.exe` | ❌ Themida — tidak dibongkar |
| `iopac.dll` | ⚠️ Terproteksi sebagian — ditunda |
| `rs.iop`/`map.iop` | ZIP termodifikasi — parser khusus, belum |
| DLL lain (`iofreetype`, `iovoicechat`, `townportal`, `il`, `imc`) | Belum; prioritas rendah |

## 11. Tindak lanjut opsional
- Dekompilasi `ioMath::TestIntersection(OBB,OBB)` untuk melihat algoritma SAT (referensi, bukan salin).
- Dekompilasi `CacheBipedMatrices` untuk urutan transform bone (jika perlu detail).
- Cek `ioEntityGroup` loader untuk format socket/attachment detail.
Semua opsional — arsitektur inti sudah cukup untuk referensi desain.
