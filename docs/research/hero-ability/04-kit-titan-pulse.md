# 04 — Kit TITAN-01 & PULSE-X (KOREKSI 2026-11-13)

> **Status: PROPOSED, bukan pindahan.** Angka & combo route di sini **desain baru**, bukan deskripsi
> kode yang ada. Angka final ditentukan **setelah T2 lewat playtest**.
> **MVP = 2 hero, Ranked 1v1 first-to-5 KO.** Ultimate **ditunda**. Resource = **cooldown murni**.
> **Tidak ada sistem modifier** di MVP. **Satu tipe damage saja** — label physical/magical tidak dipakai.
> `pulse_overcharge` **keluar dari MVP** (butuh modifier).

## 1. Kondisi kode SEKARANG (OBSERVED)
| Hal | Kenyataan di `NxDamage.cs` / `NxCombatSystem.cs` |
|---|---|
| Damage | satu angka, tanpa tipe (tidak ada armor/MR) |
| Guard | kurangi `GuardGauge` **34/hit**; **tidak ada chip damage** sama sekali |
| Guard crush | gauge ≤ 34 → `Faint` 90 tick |
| TITAN skill | `DashTime` 15 + **`Invuln` 15 (kebal penuh)**, bukan armor |
| TITAN melee | `HitDamage` 18, `HitStun` 14, knockback 6 |
| PULSE shot / heavy | 9 / 18, cd 24 / 72 |
| Combo route | **tidak ada** — `AttackTime` di-reset ke 0 setiap kontak |

## 2. Kit usulan (PROPOSED — desain baru)
### TITAN-01 (grappler)
| Slot | Nama | Cast (tick) | Efek | Cooldown |
|---|---|---|---|---|
| Jab | `titan_jab` | point 4 / active 3 / recovery 8 | 11 damage | — |
| Heavy | `titan_heavy` | point 9 / active 4 / recovery 14 | 18 damage, knockback 6 | — |
| Skill | `titan_charge` | point 8, dash 15 | 18 damage; **Invuln 15 tick** | 48 |
| Dash | `titan_dash` | i-frame 10 | — | 24 |

Combo route usulan (**baru**, belum ada di kode):
```json
"cancels": [
  { "from": "titan_jab",    "to": "titan_heavy", "openTick": 4, "closeTick": 10, "require": "contact" },
  { "from": "titan_charge", "to": "titan_jab",   "openTick": 15, "closeTick": 30, "require": "contact" }
]
```
`Jab → Heavy` butuh **CancelMask** yang belum ada di `.qtn`. Jadi ini fitur baru, bukan pemindahan.

### PULSE-X (zoner)
| Slot | Nama | Cast (tick) | Efek | Cooldown |
|---|---|---|---|---|
| Shot | `pulse_shot` | point 5 / recovery 12 | 9 damage, proyektil speed 15, life 44 | 24 |
| Heavy | `pulse_heavy` | point 12 / recovery 18 | 18 damage, speed 20, life 54 | 72 |
| Dash | `pulse_dash` | i-frame 10 | — | 24 |

## 3. Yang dijaga angka ini
- TITAN harus bisa menutup jarak dalam < 0.5 dtk setelah kena poke → `titan_charge` cd 48 vs `pulse_shot` cd 24.
- PULSE tidak boleh menang jarak dekat: recovery 12 tick sesudah shot = jendela hukuman.
- Tidak ada chip kill: guard hanya menghabiskan gauge; KO tetap lewat 3 Break Stock (C4).

## 4. Keputusan MVP (dikunci user 2026-11-13)
| Pertanyaan | Keputusan |
|---|---|
| Pakai kit apa adanya? | **Belum** — angka final setelah T2 + playtest |
| Ultimate di MVP? | **Tunda** (tambah HUD, balancing, interaksi Break Stock) |
| Resource | **Cooldown murni**, tanpa energy bar |
| Modifier slot / Overcharge | **Tidak dibangun**; `Faint` tetap field biasa |

## 5. Kalau nanti ada sistem modifier
Baru saat itu `pulse_overcharge` masuk, dan `03` dipakai. Sampai itu, `03` = arsip.
