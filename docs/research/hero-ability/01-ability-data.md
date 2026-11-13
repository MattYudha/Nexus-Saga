# 01 — Skema ability data-driven

## 1. Konsep yang dipelajari (OBSERVED/`DK`, ditulis ulang)
| Konsep Dota | Isi | Padanan kita |
|---|---|---|
| **Cast point** | jeda sebelum efek keluar; bisa diinterupsi sebelum selesai | `cast.point` (tick) |
| **Backswing** | ekor setelah efek; **boleh dibatalkan** dengan gerak → skill terasa responsif | `cast.backswing` + `cancelableAfter` |
| **Cast range / radius** | jarak & luas efek, divalidasi di server | `target.range/width` |
| **Cooldown mulai saat cast** | bukan saat efek kena | `cost.cooldown` dipasang di tick cast point selesai |
| **Charges** | beberapa pemakaian, recharge terpisah | `cost.charges`, `chargeRestore` |
| **Channel** | efek berkelanjutan, berhenti bila kena CC/gerak | `cast.channel` |
| **Target type** | diri, unit, titik, arah, area | `target.type` |

`DERIVED`: yang membuat gameplay terasa "modern" bukan angka besar, tapi **cast point pendek + backswing
yang bisa dibatalkan**. Ini juga murah secara teknis.

## 2. PROPOSED — satu skema untuk semua ability
```json
{
  "id": "titan_charge",
  "hero": "titan",
  "slot": "skill",
  "input": { "kind": "button", "buttons": ["Skill"] },

  "cast": {
    "point": 8,
    "backswing": 6,
    "channel": 0,
    "cancelableAfter": 8,
    "turnLockTicks": 8
  },

  "cost": { "cooldown": 48, "charges": 1, "chargeRestore": 48, "resource": 0 },

  "target": {
    "type": "direction",
    "range": 600,
    "width": 120,
    "requiresFacing": true,
    "lockOnAssist": true
  },

  "phases": {
    "start":    [ { "op": "SetVel", "forward": 17, "ticks": 15, "invuln": 15 } ],
    "contact":  [ { "op": "Damage", "amount": 18, "school": "physical",
                    "hitStun": 14, "knockback": 6, "juggleCost": 2 } ],
    "end":      [ { "op": "GotoState", "id": 0 } ]
  },

  "modifiersApplied": [],
  "vfx": "vfx_titan_charge",
  "sfx": ["sfx_charge_whoosh", "sfx_charge_impact"]
}
```

Aturan field:
- Semua durasi **tick** (60 Hz), bukan detik — padanan aturan Ikemen (`AnimTime`, `time`).
- `phases` = daftar **op tertutup**. Bukan bahasa ekspresi (docs/13 §2). Op minimum:
  `SetVel, Damage, GotoState, ApplyModifier, RemoveModifier, SpawnProjectile, SpawnJuice,
  SetInvuln, SetArmor, PlaySfx, CameraFx, GotoCharge`.
- `slot` ∈ `jab | heavy | skill | ultimate | dash | swap` → memetakan ke tombol (`Nexus.qtn` `input.Buttons`).

## 3. Urutan eksekusi per tick (PROPOSED, menyambung `ikemen-extract/07 §2`)
```
1. Input history (NxInputSystem)
2. Ability intent   → tombol + MotionMask + cooldown → mulai cast
3. Cast tick        → castPoint--; di 0 → jalankan phases.start / contact
4. Backswing        → boleh dipotong gerak/dash setelah cancelableAfter
5. Gerak & fisika   → Pos/Vel (FP)
6. Hit resolve      → damage pipeline (lihat 02)
7. Timers          → cooldown, charges, modifier durasi
```
Interupsi: kena `HitStun` saat **sebelum** cast point selesai → ability **hangus** (cooldown tetap jalan).
Sesudah cast point → ability **jalan** meski penyerang kena hit (kecuali ber-tag `interruptible`).

## 4. Cancel & "feel" (PROPOSED)
| Aturan | Nilai awal | Alasan |
|---|---|---|
| Backswing bisa dipotong gerak | ya, setelah `cancelableAfter` | responsif; ini trik Dota yang murah |
| Backswing bisa dipotong dash | ya (dash menang) | dash = komitmen, bukan animasi |
| Cast point bisa dipotong skill lain | **tidak** | mencegah "cancel-cast" untuk menghindari cooldown |
| Cooldown hangus bila cast diinterupsi | ya | menghukum spam |
| Buffer input saat cast | ya (4 tick) | pemain tidak perlu presisi 1 frame |

## 5. Determinisme & data
- State ability disimpan sebagai **id + timer** di komponen (`AbilitySlot`, `CastTick`, `Cd`), bukan
  delegate/coroutine. Tidak ada `List<>` di sim.
- Cooldown dihitung dengan formula `02 §5`, hasilnya **dibulatkan ke bawah** (konsisten antar klien).
- Validator build menolak: ability tanpa `phases.contact`, `range` negatif, `cooldown < point + backswing`,
  atau `op` tak dikenal.

## 6. Yang belum diputuskan
1. Resource: mana vs **energy** vs cooldown murni. Spike sekarang tanpa resource → usul **cooldown murni**
   untuk MVP (lebih mudah dibaca di brawler, tanpa bar tambahan).
2. Jumlah slot aktif per hero: 2 (sekarang) atau 4.
3. Apakah ability boleh mengubah `MoveType` (mis. skill yang membuat hero "attack" sehingga kena counter hit).
