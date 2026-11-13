# 07 — DRAF patch `.qtn` (DITAHAN — TIDAK diterapkan) + cara memakainya

> ⛔ **Status 2026-11-13: patch ini sudah di-REVERT** dan `NxInputSystem.cs` dihapus (deteksi rotasi/double-tap
> keliru; field tanpa pemakai). Field `.qtn` hanya ditambah lewat T2, bila ada sistem yang memakainya.
> Teks di bawah = rancangan, **bukan** kondisi kode. Jangan jalankan CodeGen berdasarkan dokumen ini.

File diubah: `photon-backend/game/Assets/QuantumUser/Simulation/Nexus/Nexus.qtn`
Sifat: **aditif**. Tidak ada field lama yang diubah/dihapus, **tidak ada komponen baru**
(maka tidak ada prototype di scene yang perlu diedit). Belum ada sistem yang membacanya.

## 1. Field yang ditambahkan

### `NxCombat`
| Field | Tipe | Guna | Sumber riset |
|---|---|---|---|
| `DirHistory` | ulong | 16 tick terakhir, 4 bit/tick (0 netral, 1..8 arah) | 01 |
| `BtnHistory` | ulong | 8 tick terakhir, 6 bit/tick (bit = `input.Buttons`) | 01 |
| `MotionMask` | byte | bit 1 QCF, 2 QCB, 4 DP, 8 DoubleTapFwd, 16 ChargeFwd | 01 |
| `MotionAge` | byte | tick sejak motion terakhir selesai (255 = tidak ada) | 01 |
| `StateId` | ushort | id state data-driven | 01 |
| `StateTime` | ushort | tick di state; **tidak naik saat `HitPause > 0`** | 01 |
| `FrameIndex` | short | indeks **frame data**, bukan frame klip Unity | 01 |
| `MoveType` | byte | 0 Idle, 1 Attack, 2 Hurt (dasar counter hit) | 03 |
| `Juggle` | byte | sisa budget juggle korban | 03 |
| `AttackId` | ushort | id ayunan, untuk dedup "1 target 1× per ayunan" | 03 |
| `CancelMask` | byte | bit jendela cancel yang terbuka | 01 |
| `ArmorTier` / `ArmorTicks` | byte/ushort | super armor (tidak ada di Ikemen) | 03 |
| `CounterHit` | byte | flag statistik | 03 |
| `JuiceSeq`/`Kind`/`Power`/`Ticks`/`Pos` | — | event presentasi | 02 |

### `global`
| Field | Guna |
|---|---|
| `KoSlowTicks` | sisa slow-mo KO (60 tick, 0.25×, ramp 45) |
| `SuperFreezeTicks` | sisa super freeze |
| `SuperFreezeSlot` | slot pemilik freeze (255 = tidak ada) |

## 2. Urutan update per tick (WAJIB, ini sumber desync kalau salah)

Mengikuti urutan Ikemen (`system.go:2794+`) yang sudah divalidasi di `state-machine-ikemen.md §1`:

```
1. Input history   → geser DirHistory/BtnHistory, hitung MotionMask   (per pemain)
2. Command/cancel  → evaluasi transition berdasarkan StateId/StateTime/CancelMask
3. State tick      → StateTime++ bila HitPause==0; FrameIndex dari data
4. Gerak & fisika  → Pos/Vel (FP)
5. Collision       → push SEBELUM hit
6. Hit resolve     → guard → armor → juggle → counter → terapkan reaksi (tick ini juga)
7. HitPause        → set penyerang & korban; nyalakan Juice
8. Juice decay     → JuiceTicks--, KoSlowTicks--
```

Aturan: **jangan** menaruh efek visual (partikel, kamera, audio) di langkah mana pun di atas.
Semua keluar lewat `Juice*`.

## 3. Bit-packing input (tanpa array, rollback aman)

```csharp
// dipanggil sekali per tick per pemain, di sistem paling awal
var c = frame.Get<NxCombat>(entity);

c.DirHistory = (c.DirHistory << 4) | (ulong)(input.MoveDir & 0xF);   // 16 sampel
c.BtnHistory = (c.BtnHistory << 6) | (ulong)(input.Buttons & 0x3F);  //  8 sampel

// tombol yang BARU ditekan (edge), bukan ditahan
var prev = (c.BtnHistory >> 6) & 0x3F;
c.CancelMask = (byte)(input.Buttons & ~prev & 0x3F);                 // sementara: dipakai sbg edge
```
Catatan: `MotionMask` dihitung dari `DirHistory`, bukan dari `MoveDir` saat ini — karena itu
input yang ditekan **sebelum** jendela cancel tetap valid (padanan `buffer.time` Ikemen).

Deteksi QCF (relatif hadap, 4 sampel, lebar jendela 15 tick):
```
nib(i) = (DirHistory >> (4*i)) & 0xF      // 0 = tick ini, 3 = 3 tick lalu
lokal  = putar nib relatif yaw Pemain (1..8 → 0..7)
QCF    = ada i<j<k, dengan lokal(i)=5 ∧ lokal(j)∈{4,6} ∧ lokal(k)∈{2,8} sisip
```
Implementasi praktis: tiga loop kecil (i,j,k ≤ 15) tanpa alokasi. Semua integer → deterministik.

## 4. Jendela cancel

`CancelMask` berisi bit jendela yang **sedang terbuka** pada tick ini, diisi dari data attack:
```
bit 0 = Special, 1 = Super, 2 = Dash, 3 = Swap, 4 = Chain
```
Sistem transisi hanya boleh pindah state kalau `(CancelMask & izin) != 0` **dan** `require` terpenuhi
(`contact` = `AttackId` ini sudah pernah resolve hit/guard). Ini mengganti model trigger bebas Ikemen
dengan model tertutup yang bisa divalidasi saat build.

## 5. Juice: sim → View

```csharp
// SIM (saat hit resolve)
c.JuiceSeq++;
c.JuiceKind  = 1;                      // 1 hit, 2 guard, 3 crush, 4 ko, 5 superfreeze
c.JuicePower = (byte)(damage * 255 / maxDamageRef);
c.JuiceTicks = 4;
c.JuicePos   = contactPoint;

// VIEW (di Update, bukan FixedUpdate)
if (combat.JuiceSeq != lastSeq) { lastSeq = combat.JuiceSeq; PlaySpark(combat); }
```
Satu event per tick per entity. Kalau dua hit terjadi di tick yang sama, **yang terkuat** yang dikirim
(atau pecah jadi 2 entity proyektil terpisah). Ini batasan yang diterima untuk MVP.

## 6. Slow-mo KO & super freeze

- `KoSlowTicks` turun 1 per tick. Selama > 0, delta simulasi dikali `slow_speed` yang di-ramp
  (`ratio = (fade - sisa) / fade`). **Harus** lewat konfigurasi delta Quantum (semua klien sama),
  **bukan** `Time.timeScale`.
- `SuperFreezeTicks > 0`: semua entity dengan slot ≠ `SuperFreezeSlot` di-skip di gerak & hit resolve.
  View hanya menambahkan darken/vignette.

## 7. Setelah patch ini: langkah user

1. Buka Unity → jalankan **Quantum CodeGen** (`.qtn` berubah).
2. Cek Console: tidak boleh ada error generator.
3. Tidak perlu edit prototype (tidak ada komponen baru).
4. Jalankan match 1v1 lama → **harus tetap jalan** (field baru belum dibaca siapa pun).
5. Baru setelah itu T2 dikerjakan seperti antrean.

## 8. Belum dikerjakan (sengaja)
- `NxCombatSystem`/`NxHitSystem` belum membaca field baru → tidak ada perubahan perilaku.
- T2 (Critical/BreakStock/Overload/AFK) **tidak disentuh**.
- Tabel frame data per serangan belum dibuat; `FrameIndex` masih akan 0 sampai data hero ada.
  Usulan skema ada di `01 §4.3` + angka di `combat-tuning.json`.

---

## 9. Sistem pertama (2026-11-13, menyusul patch)
`Simulation/Nexus/NxInputSystem.cs` — **data-only**, tidak menyentuh gerak/hit/KO:
- geser `DirHistory`/`BtnHistory`, hitung `MotionMask` (rotasi ± dan double-tap),
- `StateTime++` hanya saat `HitPause == 0`,
- turunkan `MoveType` dari `HitStun`/`Faint`/`AttackTime`,
- decay `JuiceTicks`.

Gesture sengaja melaporkan **arah rotasi mentah** (bit `RotCw`/`RotCcw`/`Tap2`), bukan "QCF":
di 3D free-roam "maju" bergantung yaw, jadi pemetaan ke skill harus lewat data, bukan kode.

**Registrasi:** `Assets/Editor/NexusSetup.cs` — `NxInputSystem` ditambahkan **sebelum** `NxCombatSystem`
di kedua jalur (Local & Online). Karena sistem disimpan di **asset** `NexusSystemsConfig`, urutan baru
berlaku setelah menu **`Nexus > Create Local Spike Scene`** dijalankan ulang (atau tambahkan manual ke
asset SystemsConfig). Tanpa itu, sistem tidak pernah dipanggil.

**Batas yang diketahui:** `StateTime` ushort akan wrap setelah 65.535 tick (~18 menit) — cukup untuk satu
match; reset saat ganti state nanti di sistem state. `MotionWindow = 15` tapi histori 16 nibble, jadi
gesture yang lebih lambat dari 15 tick tidak terdeteksi (sesuai `command.time`).
