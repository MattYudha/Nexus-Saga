# 03 — Guard, guard crush, dizzy, counter hit, juggle budget

Menutup 🟡/⬜ "guard crush, super armor, counter hit" dan memperkuat "juggle".

## 1. Guard (OBSERVED)
- State guard: 120–140 (start/guarding/end), 150–155 (guard-hit shake/knockback) — `state-machine-ikemen §3`.
- **Proximity guard** (`inguarddist`): ditandai saat hit detection (`char.go:13484, 13739`), di-reset tiap frame
  (`:12208-12210`), lalu auto-masuk state guard kalau tombol belakang ditahan (`:11744, 11975`).
  Komentar di `:13455`: MUGEN pakai `<` supaya jarak 0 tidak memicu proximity guard.
- Guard tinggi/rendah ditentukan dengan jongkok (kita buang: docs/08 → busur 180°).
- Guard damage & hitstop guard punya field sendiri (`guarddamage`, `guard_pausetime`, `guard_velocity`).

## 2. Guard break (OBSERVED)
Ikemen **punya** guard break, tapi bukan gauge:
- Option `GuardBreak bool` per mode (`config.go:68`, dibaca `char.go:8946-8952`).
- Flag `SCF_guardbreak` (`char.go:23`), setter `setGuardBreak` (`:4801-4806`).
- Efeknya: `ctrl()` jadi false (`:5423-5424`), jadi karakternya **tidak bisa apa-apa** — sama seperti dizzy.
- Dipicu lewat controller `GuardBreakSet` (`bytecode.go:12117-12130`) dan trigger `guardbreak` (`:3329-3330`).
Tidak ada angka gauge, tidak ada durasi baku → durasi ditentukan data karakter.

## 3. Dizzy (OBSERVED)
- `dizzypoints` default **1000** (`char.go:263, 293`), diisi dari `hitdamage × lifetodizzypointsmul`
  (`:940-954`, `default.lifetodizzypointsmul` / `super.…`).
- `SCF_dizzy` juga mematikan `ctrl` (`:5423-5424`) → state pusing.
Jadi "meter pusing" di Ikemen = akumulasi damage, bukan jumlah hit.

## 4. Counter hit (OBSERVED — penting)
**Ikemen TIDAK punya counter-hit bonus damage.** Yang ada hanya:
- `MoveCountered` / `counterHit` (`bytecode.go:14679-14680`, field `char.go:3294`, reset `:3562, 4638`):
  artinya **serangan kita dibalik** oleh `ReversalDef` lawan — dipakai untuk animasi "reversal", bukan damage.
- Sistem **prioritas/trade**: Hit-vs-Hit = trade, prioritas lebih tinggi menang, seri throw pakai RNG match
  (`char.go:10706-10790`).

→ "Counter hit" ala fighting game (pukul saat lawan startup → damage ekstra) **kita desain sendiri**.

## 5. Juggle budget (OBSERVED)
- `airjuggle` default **15** per karakter (`char.go:300`, dibaca `:4030`).
- Budget dicatat **per penyerang**: `targetedBy [][2]int32` = pasangan `{id penyerang, sisa juggle}`
  (`char.go:1035, 1232-1236`), dihitung `jugglePoints(id)` (`:5605-5616`).
- Konsekuensi: dua penyerang berbeda punya jatah terpisah → combo tag tidak saling memotong jatah.
  Ini persis kekhawatiran kita di docs/13 §7.2 (juggle milik korban jangan reset saat penyerang swap).

## 6. PROPOSED untuk Nexus

### 6.1 Guard gauge (bukan boolean break)
| Parameter | Nilai | Catatan |
|---|---|---|
| `GuardMax` | 100 | `NxCombat.GuardGauge` sudah ada |
| `GuardDrainMul` | 1.0 × `guardDamage` serangan | ringan 4–8, berat 15–25 |
| `GuardRegen` | 6 / tick | mulai setelah **30 tick** tanpa block |
| Crush | gauge ≤ 0 → `Faint` 45 tick | **bukan KO**; saat Faint: `ctrl=false`, tidak boleh guard |
| Setelah crush | gauge = 35 (bukan 100) | supaya tidak langsung crush lagi |
| Chip damage saat guard | 10% damage, **tidak** bisa mematikan | mati hanya lewat Break Stock (C4) |

### 6.2 Super armor (tidak ada di Ikemen → desain baru)
| Tier | Menahan | Roboh bila | Catatan |
|---|---|---|---|
| `None` | — | — | default |
| `Super` | hitstun & knockback (damage tetap masuk) | menerima ≥ `ArmorBreakDmg` (proposed 25% MaxHP) dalam 1 hit **atau** 3 hit dalam 20 tick | dipakai saat skill berat / gear Armor |
| `Hyper` | semua reaksi termasuk launcher | skill `Break` khusus / guard crush | hanya ultimate; durasi ≤ 30 tick |

Implementasi: dicek **sebelum** menerapkan reaksi di hit-resolve, setelah guard check. Deterministik karena
hanya membaca `NxCombat` + data serangan.

### 6.3 Counter hit (desain baru)
Definisi: hit mendarat saat korban `moveType = Attack` dan `frameIndex` ≤ akhir frame aktif.
Efek: damage ×1.15, hitstun +4 tick, hitstop +2, juggleCost −1 (min 1), spark & SFX berbeda,
flag `CounterHit` untuk statistik (bukan untuk ranked scoring langsung).
**Tidak** berlaku untuk proyektil (terlalu murah).

### 6.4 Juggle
Adopsi model per-penyerang Ikemen:
```
JuggleMax      = 12 (proposed, turun dari 15 karena match kita 5v5 & ada hero swap)
JuggleCost     = data per serangan (1 ringan … 6 launcher)
JuggleResetOn  = menyentuh tanah + 20 tick pemulihan
```
Disimpan per pasangan `(victim, attackerId)`; saat hero swap, jatah penyerang **baru** dihitung terpisah.
`JuggleRemaining` dipakai AI untuk memutuskan launcher (T2: bot prioritaskan target Critical).

### 6.5 Guard arc (sudah diputus, diulang untuk kelengkapan)
Busur **180° depan** (`docs/90`), `GuardYaw` dikunci saat guard aktif (Lock Facing). Serangan dari belakang
menembus. Guard hanya sah bila korban `Posture = Stand/Air` dan tidak `Faint`/`HitStun`.
