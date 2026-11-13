# 02 — Formula damage & mitigasi

> ## ⚠️ ARSIP PASCA-MVP (2026-11-13)
> MVP memakai **satu tipe damage** tanpa armor/MR/status-resist (lihat `04 §4`). Dokumen ini disimpan
> untuk fase setelah MVP, sesuai `backlog-riset-logic.md §3` yang memangkas sistem MOBA.
> Yang **tetap relevan sekarang** hanya: aturan pembulatan (§9) dan urutan pipeline (§1).

Semua di bawah ini **mekanik/formula**, bukan ekspresi. Ditulis ulang untuk FP.
Label `DERIVED` = disimpulkan dari dokumentasi publik `DK`; **verifikasi ulang di wiki** sebelum dipakai final.

## 1. Pipeline damage (PROPOSED urutan, penting untuk determinisme)
```
raw → (× damage amp) → blok/flat reduce → mitigasi sekolah → clamp ≥ 0 → bulatkan → terapkan
```
Sekolah damage:
| Sekolah | Dimitigasi oleh | Contoh di game kita |
|---|---|---|
| `physical` | armor | pukulan, proyektil peluru |
| `magical` | magic resistance | ledakan skill, aura |
| `pure` | tidak ada (kecuali flat block) | ultimate, damage "sejati" |
| `hp_removal` | tidak ada, **tidak memicu on-hit** | efek zona/hazard |

`DERIVED`: `pure` ada supaya ultimate tidak jadi tak berguna saat armor stacking — masalah yang sama
dihadapi Dota. Untuk brawler 2-hero, cukup `physical` + `magical` dulu; `pure` disimpan untuk T3.

## 2. Armor (DERIVED, formula Dota yang terdokumentasi)
```
mult = 1 − 0.06·A / (1 + 0.06·|A|)        // A = armor (boleh negatif)
damage_final = damage × mult
```
| Armor A | mult | Arti |
|---|---|---|
| 0 | 1.000 | — |
| 5 | 0.769 | −23.1% |
| 10 | 0.625 | −37.5% |
| 20 | 0.455 | −54.5% |
| −5 | 1.231 | +23.1% |
| −10 | 1.375 | +37.5% |

Sifat: **diminishing**, tidak pernah imun, dan armor negatif tidak pernah 100% (multiplier terbatas 1.375
pada −10 sudah cukup kuat). Ini yang membuat armor aman di-*tuning*.

Implementasi FP:
```csharp
static FP ArmorMult(FP a) {
    FP k = FP._0_06 * a;                 // 0.06 * A
    FP absk = k < 0 ? -k : k;            // |0.06A|
    return 1 - k / (1 + absk);           // 1 − 0.06A/(1+0.06|A|)
}
```
Clamp `a` ke `[-40, 60]` supaya tidak overflow dan hasil tetap masuk akal.

## 3. Magic resistance (DERIVED)
```
MR_total = 1 − Π(1 − MR_i)        // stacking multiplikatif
damage_final = damage × (1 − MR_total)
```
Contoh: base 25% + item 15% → `1 − 0.75×0.85 = 0.3625` → 36.25%.
Kalau ditambah (aditif) hasilnya 40% dan cepat jadi imun — karena itu multiplikatif.

## 4. Status resistance (DERIVED)
```
durasi_final = durasi × Π(1 − SR_i)
```
Berlaku untuk `HitStun`, `Faint`, `slow`, bukan untuk damage.
Rounding: **floor**, minimum **1 tick** (kalau tidak, CC bisa jadi 0 tick = tak terasa).
Contoh: hitstun 14 tick, SR 30% + 20% → `14 × 0.56 = 7.84 → 7 tick`.

## 5. Cooldown reduction (DERIVED)
```
cd_final = cd × Π(1 − CDR_i),  floor, minimum 1 tick
```
Jangan pernah aditif: 50% + 50% aditif = 0 detik.

## 6. Evasion & accuracy (DERIVED)
```
miss_chance = (1 − Π(1 − E_i)) × (1 − accuracy_bonus)   // clamp 0..1
```
Deterministik: pakai RNG match (`f.RNG`/seed tersinkron), **bukan** `UnityEngine.Random`.
Catatan desain: evade acak di brawler 3D terasa tidak adil untuk serangan berbayar cooldown.
PROPOSED: evade hanya untuk proyektil, **tidak** untuk melee.

## 7. Damage block / flat reduce (DERIVED)
```
damage = max(0, damage − block)
diterapkan SEBELUM mitigasi sekolah
```
Dipakai gear Armor di kita: `block 6` per hit, bukan % armor.

## 8. Damage amp / vulnerability (PROPOSED)
```
damage = damage × (1 + Σ amp_i)        // aditif untuk amp (jarang, mudah diprediksi)
```
Counter hit (`ikemen-extract/03 §6.3`) = `amp +15%` selama resolusi itu saja, **tidak** menjadi modifier
permanen — supaya tidak menumpuk dengan vulnerability gear.

## 9. Aturan pembulatan (WAJIB seragam)
| Besaran | Pembulatan | Alasan |
|---|---|---|
| Damage | FP penuh, jangan dibulatkan | HP sudah FP |
| Tick CC | floor, min 1 | jangan sampai 0 |
| Cooldown | floor, min 1 | idem |
| Persentase di data | simpan sebagai FP (`0.06`, `0.25`), bukan `6`/`25` | menghindari konversi implisit |
| Statistik akumulator | FP, baru dibulatkan saat dikirim ke backend | replay harus identik |

## 10. Contoh lengkap
TITAN heavy 18 `physical`, korban armor 10, gear Armor `block 6`:
```
18 − 6 = 12 → 12 × 0.625 = 7.5 damage
```
Korban armor −5, tanpa block: `18 × 1.231 = 22.16` → masuk Critical lebih cepat. Ini alasan armor
negatif harus dibatasi di gear, bukan di formula.
