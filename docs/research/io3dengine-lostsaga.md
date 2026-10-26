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

---

# DEEP-DIVE 5 SUBSISTEM (dekompilasi, 2026-10-26)
Dibedah dari fungsi nyata (alamat virtual; RVA = alamat − 0x10000000). OBSERVED kecuali ditandai.

## A. Perakitan karakter, equipment, anti-clipping rambut, socket
**Hierarki:** `ioEntityGroup` (karakter utuh) → `ioEntity` (part: badan/wajah/rambut/helm/armor/senjata) → `ioSubEntity` (batch per material, 0x40 byte). **Semua part skin ke SATU `ioSkeleton` bersama** (ptr @0x98). Builder `ioEntityGroupBuilder` mem-parse file grup: `ParsingMesh/Skeleton/Animation/CollisionMesh/AABox/Sphere/Effect`.

**Anti-clipping rambut-vs-helm = HIDE FLAG per-mesh** (bukan bone scaling, bukan swap mesh):
- Event animasi/equip `OnHideMesh` → `ioEntityGroup::SetEntityVisible(meshHash, false)`; `OnShowMesh` kebalikannya.
- Ada **whitelist** (`HideMeshExceptionCheck`) untuk mesh yang wajib tetap tampil.
- Instan & reversibel (boolean per entity).

**Socket/attach:** `AttachEffect(node, pos vec3, rot quat, localOrWorld)` → parent ke bone (`GetBiped(name)`) + offset. **Detach instan (gear drop):** `DetachEffect`/`SetEntityVisible(false)` — O(1), tanpa rebuild.

✅ **Adaptasi (dikunci):** gear = entity skin ke shared rig; **anti-clipping rambut via visibility flag** yang di-toggle event equip (lebih murah & deterministik dari swap mesh) + whitelist; senjata/trinket di **bone socket + offset+quat**; gear-drop = flip visibility + detach. Memvalidasi doc 19.

## B. Collision box, SAT, binding ke bone
**`ioOrientBox`:** center@0x00, 3 axis@0x0c/0x18/0x24, half-extent@0x30/34/38, **disable flag@0x40** (nonzero → skip). **`ioSphere`:** center@0x00, radius@0x0c.
- **OBB–Sphere** (`@0x10136c10`): transform ke box-local, closest-point, `Σ excess² ≤ r²` (squared, tanpa divide).
- **OBB–OBB** (`@0x10135d60`): **SAT 15-sumbu** (3 face A, 3 face B, 9 edge×edge), early-out sumbu pemisah pertama; out-param = **kedalaman penetrasi** (min overlap face-axis) → berguna untuk pushback.
- **Hitbox TIDAK di-bake per keyframe.** Box menempel ke **bone**; `CacheBipedMatrices` menghitung ulang matriks bone **sekali per frame** (guard anti-dobel), box ikut pose. Aktif/nonaktif per frame-window = **toggle flag@0x40** via event animasi.

✅ **Adaptasi (dikunci):** OBB+Sphere + SAT 15-sumbu + out-param penetrasi; **hitbox terikat bone + enable-flag per frame-window** (bukan bake per frame) — ini menyederhanakan Hitbox Editor kita (pasang box ke bone tangan/senjata, aktifkan di jendela aktif). Reimplementasi **fixed-point** (dot/abs/compare, squared).

## C. Event animasi + blending partial-body
**Event track:** `UpdateAniEvent` — tiap record `AniEventTime` 0x24 byte (waktu@0, string-param@0x14, gate@0x1c). Event memicu saat cursor melewati **`[prevTime, curTime)`** (model crossed-interval, ada penanganan loop-wrap), menyala **tepat sekali**, frame-rate independent. Satu handler ber-tipe meng-rute: `OnAutoSound`, `OnTrailStart/End`, `OnShow/HideMesh`, `OnAnimationEnd/Clear` (dan via mekanisme sama: hitbox-enable, dust).
**Partial-body (atas/bawah):** `BlendSkeleton` iterasi `ioAniTrack` (bone index@0x0c, **track weight@0x10**); sample `GetInterpolatedFrame(time)` → (pos, quat) → `BlendBiped(idx, globalWeight×trackWeight, pos, rot)`. **Tidak ada layer-mask terpisah** — mask = himpunan bone yang disentuh klip + bobotnya. Split atas/bawah **emergent** (klip kaki + klip badan atas dengan bobot per-bone).

✅ **Adaptasi (dikunci):** model event crossed-interval (`prev ≤ t < cur` + loop-wrap), satu event handler ber-tipe untuk sound/VFX/dust/**hitbox-on-off**; **upper/lower split via track weight per-bone** (untuk PULSE-X lari sambil menembak), bukan sistem layer. Blend = quaternion nlerp + lerp; fixed-point jika timing hit bergantung, client-side jika hanya visual.

## D. Kamera — quarter-view follow + spring (TANPA shake di engine)
`ioTargetLookAtCameraController` (`UpdatePos @0x101180d0`): camPos, lookAt, restDist, min/maxDist, **distSpringK/Damp**, **moveSpringK/Damp**, rotateSpeed, yaw, pitch. **Tidak ada simbol `Shake`** → screen shake/hit-zoom = **tanggung jawab client**, bukan engine.
Alur: lookAt track objek (tinggi di-blend → karakter melompat/terlempar tetap ter-follow mulus) → `curDist` spring-damp + clamp → yaw/pitch dari input (sens **0.1**/**0.07**, `ArrangeHead`/`LimitPitch`) → `camPos = lookAt + quat(yaw,pitch)·back(dist)` via spring → **occlusion pull-in** (ray vs sphere; jika terhalang, pindah ke titik kontak). Konstanta: spring ×2, snap threshold 1.0, colinear 0.99, frameDt 1/60.

✅ **Adaptasi (dikunci):** template kamera quarter-view kita = **3 spring** (jarak + posisi + yaw/pitch) + occlusion pull-in agar target terlempar tetap ter-frame. **Screen shake + hit-zoom di layer client** (offset/FOV pulse additif skala "berat" hit) — **jangan di Core deterministik** (murni presentasi). Semua frame-dt scaled → aman client-only.

## E. Physics sekunder (rope/spring pada bone)
`AddRopeSpringCurve(name, RopeSpringParam*)`: ambil root bone, **telusuri anak bone** (≥2) jadi rantai; solver 100 byte. `RopeSpringParam` = 5 scalar (INFERRED: stiffness, damping, gravity/force, angle limit, drag/mass) + sub-struct@0x14 (config rantai).
**Integrasi:** `UpdateRopeSpringCurve(dt)` → **substep tetap 1/60 s** (`substeps = max(1, dt/0.01667)`), spring-damper/Verlet per-node, **frame-rate independent**. Forcing eksternal via `AddWorldForce(vec3)` (angin, knockback). Collide vs `ioOrientBox`.

✅ **Adaptasi (dikunci):** jiggle hoodie/jaket/trinket (tema hypebeast) = rantai (root bone + anak ≥2), param {stiffness, damping, gravity, angle limit, drag}, **integrator substep tetap 1/60 s**, inject world force per tick (angin + knockback hit berat), clamp vs pushbox/OBB. **Client-only**, tidak menyentuh Core.

## Lintas-subsistem (pola kunci)
**"Pose sekali per tick, semua baca matriks bone yang di-cache"** — animasi (C), collision (B), socket (A), jiggle (E) semua membaca pose yang sama. Engine memisahkan **deterministik** (OBB/Sphere/SAT, pose blend → fixed-point Core) dari **presentasi** (kamera spring, rope jiggle, shake → client float). **Persis pemisahan visual/sim kita.** Tidak ada `Shake`/`AttackBox` di engine — shake & gating hitbox via flag+event di client/gameplay.
