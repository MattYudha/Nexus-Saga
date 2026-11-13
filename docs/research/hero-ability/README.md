# hero-ability — riset sistem ability & kit hero (2026-11-13)

Domain ini dipilih pertama karena **belum ada artefaknya sama sekali**, padahal langsung dipakai
TITAN-01 dan PULSE-X.

Sumber:
- `DK` = dokumentasi publik Dota 2 (Dota 2 Wiki, Liquipedia, dev blog). **Tidak ada source/aset yang dipakai.**
- `IK` = Ikemen GO v1.0.0 (MIT) — state machine & frame data.
- `SPIKE` = kode repo ini (`Nexus.qtn`, `NxCombatSystem.cs`, `NxDamage.cs`, `NxProjectileSystem.cs`).

Label: `OBSERVED` (dokumentasi/kode, dengan rujukan) · `DERIVED` (kesimpulan, rantai dijelaskan) ·
`PROPOSED` (desain kita). Rule set: **formula & mekanik dipelajari lalu ditulis ulang**; teks/model/audio
Dota tidak disalin.

## Isi
| File | Isi |
|---|---|
| `01-ability-data.md` | Skema ability data-driven: cast point, backswing, channel, cooldown, charge, target, event |
| `02-formulas.md` | Damage pipeline: physical/magical/pure, armor, magic resist, status resist, CDR, evasion, block + FP rounding |
| `03-modifiers-dispel.md` | Model modifier/buff: durasi, stacking, dispel, immunity, urutan deterministik |
| `04-kit-titan-pulse.md` | Kit konkret 2 hero memakai skema + angka PROPOSED yang cocok dengan spike sekarang |

## Status
Semua isi = **riset**. Tidak ada kode, `.qtn`, atau config yang diubah. Angka di `04` PROPOSED dan
harus disetujui dulu sebelum masuk `combat-tuning.json`.

## Posisi terhadap docs/13
docs/13 = spesifikasi state & HitDef. Folder ini **melengkapi**, bukan menggantikan: fokusnya
*bagaimana sebuah ability didefinisikan dan dieksekusi*, bukan *bagaimana state character berjalan*.
