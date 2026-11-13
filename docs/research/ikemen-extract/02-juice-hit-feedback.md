# 02 — "Juice": hitstop, screen shake, hit spark, superpause, slow-mo KO

Menutup ⬜ "hit spark, screen shake, slow-mo saat KO, suara berlapis, announcer".

## 1. Prinsip: dua lapisan (WAJIB)

| Lapisan | Isi | Boleh fixed-point? | Disimpan di snapshot? |
|---|---|---|---|
| **Sim** | HitPause, corner push, superpause timer, slow-mo (kalau mengubah delta), damage, hitstun | ya, semua FP/int | ya |
| **Presentasi** | Partikel spark, kamera shake, flash warna, audio, haptic, angka damage | boleh float/Unity | tidak (tapi **event**-nya di sim) |

Mekanismenya: sim menghasilkan **event** (`NxJuice { kind, tick, pos, power, team }`) lalu View mengonsumsinya.
Kalau efek dibuat langsung di View dari "delta HP", klien dengan rollback akan memutar efek dua kali / hilang.
Ini kesalahan paling umum di game Quantum.

## 2. Hitstop / hitpause (OBSERVED)

Ikemen: `HitDef.pausetime[0]` untuk penyerang, `[1]` untuk korban (`char.go:548-626`). Selama pause,
state `time` **tidak** naik dan input buffer **membeku** (`input.go:2448-2451`), kecuali controller bertanda
`ignorehitpause`. Contoh KFM stand LP: `pausetime = 8,8`; sweep `12,12` (`kfm.cns:270-292, 665-687`).

PROPOSED (tick): lihat `combat-tuning.json`. Aturan implementasi:
- `HitPause` di `NxCombat` = penghitung; selama > 0: `Pos`, `Vel` dibekukan, `AttackTime` tidak maju,
  tombol tetap **direkam** dan langsung dipakai saat pause habis (buffer beku, sama seperti Ikemen).
- Pause **tidak** membekukan `HitPause` itu sendiri (harus turun tiap tick) dan **tidak** membekukan
  proyektil yang sudah aktif? → **Tidak**: proyektil juga dibekukan, kalau tidak, hit-trade jadi tak adil.

## 3. Screen shake (OBSERVED)

`EnvShake` (`system.go:6670-6680`): `time, freq, ampl, phase, mul, dir, diradd, decay, curTime, curOffset[2]`.
Dipicu dari HitDef lewat 8 field `envshake_*` (`char.go:638-645`) atau controller `EnvShake`/`FallEnvShake`
(`bytecode.go:11100-11125`). Default: `freq = 60`, `ampl = -4`, `mul = 1.0` (`char.go:770-772`).
Diterapkan setelah hit detection (`char.go:11677-11692`), jadi spark & shake memakai posisi **sebelum** push.

PROPOSED: shake = offset presentasi, **jangan** masuk `Camera.Pos` sim. Amplitudo dari event `power`
(0..1 dinormalisasi dari damage/hitstop), bukan dari nilai mentah Ikemen.

## 4. Hit spark (OBSERVED)

`hitspark()` (`char.go:11469-11510`): posisi = `p2.pos - p1.pos` dikoreksi `sizeWidth` + `facing`, lalu
`+ sparkxy` (offset data, lokal), hasilnya dipakai `spawnExplod(animNo)`; spark guard punya pasangan sendiri
(`guard_sparkno`, `guard_sparkangle`, `guard_sparkscale`). `sparkangle` = rotasi, `sparkscale[2]` = skala.
Efek tambahan di fungsi yang sama: `PalFX` flash pada korban (`char.go:11514-11520`).

PROPOSED: spark = prefab VFX (bukan sprite MUGEN), diposisikan di titik kontak hasil hit resolve
(bukan di tengah badan). Guard spark beda warna/arah. Skala dari `power`.

## 5. Superpause / "freeze" (OBSERVED)

Controller `SuperPause` (`bytecode.go:10447-10551`), default: `time = 30`, `movetime = 0`,
`unhittable = true`, `darken` → `brightness = 0.5`, `anim = 100`, `p2defmul = super.targetdefencemul`.
`setSuperPauseTime` (`char.go:9173-9211`) menyimpan: `superMovetime` (= penyerang tetap boleh bergerak
N tick), `unhittableTime`, `ignoreDarkenTime`, dan **pengali defense per tim** (`superDefenseMulBuffer`),
yang bertumpuk kalau dua pemain memicu pause berdekatan.

PROPOSED untuk Nexus (Critical/skill ultimate):
- `SuperFreeze { ticks = 30, moveTicks = 8, darken = 0.5, defenseMul = 0.8 }` di config.
- Efek **sim**: semua entity berhenti kecuali pemilik selama `ticks`, `moveTicks` pertama pemilik bergerak.
- Efek **presentasi**: vignette/darken + zoom kamera + SFX. Jangan pakai `Time.timeScale`.

## 6. Slow-mo KO (OBSERVED)

`system.go:2929-2939`: saat `slowtime > 0` dan bukan `GSF_nokoslow`, kecepatan render dikali `slow_speed`,
dan **di-ramp** ke 1.0 selama `slow_fadetime` terakhir:
`ratio = (fade - st) / fade; slowSpeed += (1 - slowSpeed) * ratio`.
Default (`fightscreen.go:3176-3178`): `slow_time = 60`, `slow_fadetime = 45` (= 0.75 × time, `:3298`),
`slow_speed = 0.25`. Jadi: 15 tick pertama 0.25×, lalu naik linear ke 1.0 sampai tick ke-60.

PROPOSED: sama, tapi dengan **dua syarat**:
1. Perubahan kecepatan harus **deterministik** dan sama di semua klien → jangan `Time.timeScale` (itu hanya
   memperlambat View; sim tetap jalan → posisi desync terhadap yang dilihat). Kalau Quantum versimu punya
   `SimulationSpeed`/delta di config, ubah lewat situ **sebagai event sim**, bukan dari UI.
2. Slow-mo hanya kosmetik untuk **KO terakhir**; jangan dipakai saat match masih berjalan (mengubah timing
   hurtbox → menguntungkan satu pihak).

## 7. Suara berlapis (PROPOSED, tidak ada di Ikemen sebagai sistem)

| Layer | Pemicu | Catatan |
|---|---|---|
| Whoosh | frame startup pertama attack | volume ∝ berat serangan |
| Impact | tick kontak | pitch ±5% acak **dari RNG match** (bukan `UnityEngine.Random`) |
| Guard | kontak ke guard | logam/palu, beda dari impact |
| Voice | hanya hit ≥ heavy (hitstop ≥ 12) atau KO | hindari spam |
| Announcer | round start, Critical, KO, perfect | satu channel, prioritas |

Voice/announcer = sampel berlisensi atau original (docs/21). **Jangan** ambil dari client mana pun.

## 8. Angka usulan
Lihat `combat-tuning.json` → blok `juice`, `hitPauseByWeight`, `koSlowMotion`, `superFreeze`.
