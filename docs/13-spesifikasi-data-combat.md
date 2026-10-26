# 13 — Spesifikasi Data Combat (implementation-ready, 2026-10-24)

Hasil bedah mendalam source Ikemen GO v1.0.0 untuk menutup 5 celah implementasi (`state-machine-ikemen.md` = level desain; dokumen ini = level implementasi). Melengkapi `08`. **Spesifikasi data, bukan kode.**

Label: **OBSERVED** (fakta Ikemen, dengan `file:baris`) · **PROPOSED** (desain kita).

---

## 1. Skema data state

### 1a. StateDef
OBSERVED: `StateBytecode` (`bytecode.go:15504-15513`), default `Stand/Idle/None` (`:15517-15520`), header opsional `juggle, velset(x,y,z), anim, ctrl, poweradd, facep2, …` (`bytecode.go:4878-4942`). `velset` **sudah 3 komponen**.

PROPOSED skema:
| Field | Tipe C# | Default | Catatan |
|---|---|---|---|
| `id` | int | — | nomor state |
| `posture` | enum{Stand,Air,Down} | Stand | **tanpa Crouch** |
| `moveType` | enum{Idle,Attack,Hurt} | Idle | |
| `physics` | enum{Ground,Air,None} | None | Ground=friksi XZ, Air=gravitasi |
| `anim` | int | -1 | -1 = tak berubah |
| `ctrl` | bool? | null | null = tak berubah |
| `velSet` | Fix3? | null | **3D (x,y,z) lokal terhadap yaw** |
| `juggleCost` | int | 0 | |
| `armor` | enum{None,Super,Hyper} | None | tambahan kita |
| `invuln` | flags{Strike,Grab,All} | None | tambahan kita |
| `gearSkillSlot` | enum{None,Weapon,Armor,Helmet,Trinket} | None | tambahan kita |

**Dibuang (2D-only):** `facep2` (auto-turn ±1), varian `C` crouch, `sprPriority` (render). Facing diganti **yaw uint16**.

### 1b. StateController
OBSERVED: `StateBlock` (`bytecode.go:4551-4569`): `persistent`, `ignorehitpause`, `trigger`, `elseBlock`, `ctrls[]`. Eksekusi (`:4575-4732`): lewati saat hitpause kecuali `ignorehitpause`; `persistent` hitung mundur; `trigger` false → elseBlock; true → jalankan `ctrls` berurutan, berhenti saat satu mengembalikan true (ChangeState).

PROPOSED:
```
{ persistent:int=1, ignoreHitPause:bool=false,
  trigger:Condition, else:StateController[]?,
  action:{ type:enum, params } }
```
Action yang dibutuhkan: `ChangeState, VelSet, VelAdd, HitDef, SpawnProjectile, SetInvuln, SetArmor, PlaySfx/Fx, PosFreeze, TargetState/Bind` (grab). Loop/for Ikemen **dibuang** untuk MVP.

## 2. Sistem trigger — keputusan: **enum-condition, bukan bahasa ekspresi**
OBSERVED: Ikemen pakai VM bytecode berbasis stack (opcode `OC_*`, `bytecode.go:104-252`), struktur `triggerall₁ && … && (trigger1 || …)` (`compiler.go:7013-7045`).

PROPOSED (rekomendasi **(b)**): tiru VM = berminggu-minggu + risiko determinisme (tiap opcode harus fixed-point & rollback-safe). Trigger nyata KFM 95% hanya `AnimElem=N, Time=N, movecontact, ctrl, command=, stateno, hitdefattr`. Pakai **enum predikat tertutup**:
```json
"trigger": {
  "all": [ {"v":"StateTime","op":">","n":6} ],
  "any": [ {"v":"Command","s":"QCF_x"},
           {"v":"MoveContact","op":">","n":0},
           {"v":"CanCancel","flags":["Normal","Special"]} ]
}
```
`v` ∈ {StateTime, AnimElem, AnimTime, Ctrl, MoveContact, MoveHit, MoveGuarded, StateNo, Command, CanCancel, Pos{XYZ}, Vel{XYZ}, P2BodyDist{XYZ}, Juggle, Power, HitStunRemain}. Tiap klausa `{v, op∈[=,!=,<,<=,>,>=,in], n|range|s|flags}`.

- **Pro:** deterministik (banding integer fixed-point), serialisasi datar, validasi di build, tanpa VM di hot path, rollback trivial.
- **Kontra:** tanpa aritmetika di data. **Escape hatch:** kasus langka jadi named condition di C# yang dirujuk data lewat enum.

## 3. Hitbox: 2D Clsn → 3D
OBSERVED: `.air` menyimpan persegi AABB per frame: `Clsn1`=attack, `Clsn2`=hurt, `x1,y1,x2,y2` lokal (Y ke bawah negatif). Contoh stand `Clsn2[0]=-13,0,16,-79` (`kfm.air:8-10`). `clsnOverlap` (`system.go:2092-2156`): mirror X bila `facing<0`, skala, **OBB path** bila `angle` di-set (`:2138-2143`). Z **terpisah** sebagai interval kedalaman `zAxisOverlap` (`system.go:2082-2091`).

> **Validasi dari RE LostSaga `io3dengine.dll`** (`research/io3dengine-lostsaga.md`): engine LostSaga pakai **OBB + Sphere, TANPA capsule**, transform OBB via (pos, quat) — persis pola di bawah. Pertimbangkan drop capsule → OBB+Sphere saja untuk sederhana.

PROPOSED format 3D:
```
Volume {
  kind: enum{Capsule, OBB, Sphere}
  role: enum{Hurt, Attack}
  // lokal: origin di kaki, +Y atas, +X depan, +Z kanan; diputar yaw saat runtime
  Capsule{ p0:Fix3, p1:Fix3, radius:Fix }   // badan, tungkai, tongkat
  OBB{ center:Fix3, halfExtents:Fix3, localYaw:uint16 }   // tebasan
  Sphere{ center:Fix3, radius:Fix }   // proyektil
}
Frame { duration:int(tick), hurt:Volume[], attack:Volume[] }
```
- Koordinat lokal terhadap yaw; transform saat hit (pos + rotasi yaw) menggantikan mirror ±1.
- Hurt volume **default-persist** antar frame (siluet standar); attack hanya di frame aktif.
- **Hurtbox = konstanta bersama** semua pemain (`08 §5.2`), bukan per hero.
- Resolusi (urut, cocok `08 §3 T6` & `char.go:14158-14214`): kumpulkan pasangan attack×hurt beda tim → tolak invuln → cek juggle → prioritas/trade (seri throw = RNG match) → **guard arc 180°** → terapkan serentak tick berikut. Urut prioritas lalu entity id.

## 4. Frame data acuan (tick @60 Hz)
OBSERVED (dari `kfm.cns`): Stand LP pausetime 8,8 / grd.hittime 11 / air 15 / slide 5 / juggle 1 (`kfm.cns:270-292`); Sweep 12,12 / 17 / slide 10 / juggle 7 / fall (`:665-687`); Launcher 12,12 / 20 / recover 40 (`:2160-2182`); Throw p2stateno=820 (`:881-895`). Gravitasi `yaccel=.44`.

PROPOSED tabel tuning MVP (tick):
| Properti | Grappler (jab / grab) | Zoner (poke / proyektil) |
|---|---|---|
| Startup ringan | 4 | 6 |
| Startup berat/launcher | 11 | 14 |
| Active | 2–4 | 3 / spawn |
| hitpause (atk,vic) | 8,8 / 12,12 | 8,8 / 10,10 |
| Ground hittime | 11 / 17 | 12 |
| Air hittime | 15 (min ≥10) | 15 |
| slidetime | 5 / 10 | 6 |
| Knockback (fwd,up) lokal | ringan (−4,0); launcher (−2,−9) | poke (−3,0); proj (−4,−2) |
| juggleCost | 1 / 7 | 2 / 3 |
| down recovertime | 40 | 40 |
| getup i-frame | 10 | 10 |

Minimal hitstun ≥ 10 tick (tutup 1 RTT, `08 §5.1`). Yang disalin adalah **rasio**, bukan nilai piksel mentah.

## 5. Format authoring — paket hero JSON
OBSERVED: `.cmd` punya `name`, `command` (simbol `~` release, `/` hold, `$` 4-arah, `+` bareng, `>` strict), `time`, `buffer.time` (`kfm.cmd:155-215`); cancel di `[Statedef -1]` (`:379-400`); buffer **beku saat hitpause** (`input.go:2448-2451`).

PROPOSED (satu paket hero, ringkas):
```json
{
  "heroId": "grappler",
  "stats": { "moveSpeed": 1280, "weight": 120, "defenseMul": 0.9 },
  "anims": [
    { "id": 200, "frames": [
      { "dur": 2, "hurt": ["body"] },
      { "dur": 4, "hurt": ["body"],
        "attack": [ { "kind":"OBB","center":[220,-300,0],
                      "halfExtents":[180,90,120],"localYaw":0 } ] },
      { "dur": 3, "hurt": ["body"] } ] }
  ],
  "hitdefs": [
    { "id":"jab", "attr":{"posture":["Stand","Air"],"type":"Normal"},
      "damage":60, "guardDamage":8, "priority":3,
      "hitPause":[8,8], "hitStun":{"ground":11,"air":15}, "slideTime":5,
      "knockback":{"fwd":-1024,"up":0}, "reaction":"stand",
      "juggleCost":1, "guardBreak":6, "gearKnock":0 } ],
  "states": [
    { "id":200, "posture":"Stand", "moveType":"Attack", "physics":"Ground",
      "anim":200, "ctrl":false, "juggleCost":1, "gearSkillSlot":"none",
      "controllers": [
        { "trigger":{"all":[{"v":"AnimElem","op":"=","n":2}]},
          "action":{"type":"HitDef","ref":"jab"} },
        { "trigger":{"all":[{"v":"AnimTime","op":"=","n":0}]},
          "action":{"type":"ChangeState","value":0,"ctrl":true} } ] } ],
  "commands": [ { "name":"QCF_P","input":"~D,DF,F,P","time":20,"bufferTime":4 } ],
  "cancels": [
    { "fromState":200, "toState":500,
      "trigger":{"all":[{"v":"Command","s":"grab"}],
                 "any":[{"v":"MoveContact","op":">","n":0}]} } ],
  "gear": { "Weapon":{"skillStates":[500,501]}, "Armor":{"skillStates":[300]},
            "Helmet":{"skillStates":[310]}, "Trinket":{"skillStates":[320]} }
}
```
Pipeline: JSON → validator build (referensi state valid, attack frame tak kosong, siluet dalam batas, `08 §10`) → biner. `cancels[]` = padanan `[Statedef -1]`. Buffer command **beku saat hitpause** supaya special yang di-buffer menyala di frame cancel pertama (rasa combo responsif).

## 6. Adaptasi 3D (ringkas)
- **B/F → 8-arah + aimYaw:** arah command dihitung terhadap sumbu layar (kamera terkunci → arah layar = dunia). Motion `~D,DF,F` diuji sebagai **rotasi relatif stik** (quarter-circle), bukan B/F absolut. `aimYaw` (uint16) terpisah dari arah gerak.
- **Facing → yaw:** semua perkalian `facing ±1` diganti rotasi yaw (velSet, knockback, hitbox).
- **Guard:** High/Low/Air Ikemen diganti **busur depan 180°** + Lock Facing + guard gauge (`08 §5.3`, G1/G2).
- **Determinisme:** fixed-point + RNG per match (Ikemen pakai float32 + RNG global).

## 7. Keputusan terbuka (dari agen)
1. Titik sisip **Gear Drop/Hero Swap**: konfirmasi T8 loadout pass (`08 §3`) + swap = snapshot persisten (`08 §6.1`), bukan controller transien. Tidak ada preseden di Ikemen.
2. **Juggle budget milik korban** (S1) — jangan di-reset saat penyerang swap.
3. Lingkup **escape hatch** ekspresi: trigger mana yang benar-benar butuh aritmetika sebelum enum dikunci.
4. Berapa attack MVP butuh **OBB** vs capsule (membatasi kode collision).
5. **Payload rewind minimal** untuk lag comp (`08 §9`): cukup transform + anim-frame untuk rekonstruksi volume (tak perlu clone seluruh state).

---

## 8. AMANDEMEN collider (2026-10-26, dari RE io3dengine.dll)
Pisahkan 3 peran collider — **jangan satu bentuk untuk semua**:
| Peran | Bentuk | Alasan |
|---|---|---|
| **Hitbox (serang)** | **OBB + Sphere** | Ayunan senjata = OBB; ledakan/proyektil = Sphere. Fixed-point bersih; sesuai io3dengine (OBB+Sphere, tanpa capsule) |
| **Hurtbox (badan kena)** | **OBB + Sphere** | Sama; **drop capsule** (jarak segmen 3D rawan overflow di fixed-point) |
| **Pushbox (gerak lantai/dinding antar-pemain)** | **Upright Cylinder (lingkaran X-Z + tinggi Y)** atau Sphere | Lingkaran X-Z **tidak terpengaruh yaw** → tidak nyangkut di sudut saat berputar di tepi dinding/tangga. OBB sudutnya melebar saat berputar = nyangkut |

Collision Core final: **OBB + Sphere** (hit/hurt) + **Upright Cylinder** (pushbox/arena). Capsule dibuang.
