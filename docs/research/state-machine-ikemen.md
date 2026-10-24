# Riset: State Machine Ikemen GO v1.0.0 (2026-10-24)

Sumber:
- Engine: `C:\Users\US3R\Nexus_Lab\src\Ikemen-GO\src\` (clone tag v1.0.0, open-source, hanya dibaca).
- Data: `C:\Users\US3R\Nexus_Lab\Ikemen_Go-v1.0.0\`. Common state ada di `data\common1.cns.zss` (format ZSS); `common1.cns` klasik tidak ada di v1.0.0.

"unverified" = belum dikonfirmasi dari kode.

## 1. Urutan proses per frame
- Logic 60 Hz; saat rollback dikunci 60 Hz (`system.go:4424-4437`).
- Urutan di `System.action()` (`system.go:2794+`):
  1. Stage dan timer pause.
  2. `charList.action()` (`char.go:13376-13400`): `updateRunOrder` → `commandUpdate` (input) → `actionPrepare` → `actionRun` → `actionFinish`.
  3. `charUpdate`.
  4. `globalCollision`: trade proyektil, lalu `collisionDetection` (`char.go:14158-14214`). Karakter diurutkan per prioritas (ReversalDef > HitDef > lainnya, seri dipecah dengan id) → **push dulu** → hit pemain → hit proyektil.
  5. `globalTick` (`system.go:3180-3191`).
  6. Kamera, lalu explod/hit spark (harus setelah hit detection).
- `Char.actionRun` (`char.go:11922-12045`):
  1. State -4/-3/-2/-1 (lapisan command → ChangeState).
  2. `stateChange2` menerapkan perubahan state yang di-buffer.
  3. Controller state aktif, lalu cek guard (-10).
  4. Jika ada ChangeState, state baru **langsung dijalankan di frame yang sama**.
  5. Di luar hitpause: getup paksa 5110→5120, `posUpdate`, auto-landing, `time++`.
- **Get-hit diterapkan satu tick setelah kena**. `Char.tick` mengirim ke 150-154 (guard) atau 5000/5010/5020/5070/5080 (`char.go:12561, 12590-12625`).
- Determinisme: posisi/velocity `float32` (`char.go:3375,3378`). RNG Park-Miller global (`common.go:30-41`), seed dari `time.Now()` (`system.go:187`), disinkronkan host saat netplay (`netplay.go:580-592`).

## 2. Model state
- Header StateDef (`bytecode.go:15504-15556`):
  - type: S / C / A / L
  - movetype: I / A / H
  - physics: S / C / A / N
  - Opsional: `juggle`, `velset (x,y,z)`, `anim`, `ctrl`, `poweradd`, `facep2`, `hitdefpersist`, … (`bytecode.go:4878-4945`)
  - Juggle di-reset bila movetype ≠ A.
- Physics (`char.go:9839-9856`): S/C = friksi X dan Z; A = gravitasi; N = tidak ada.
- Controller = `StateBlock{persistent, ignorehitpause, trigger, else, ctrls}` (`bytecode.go:4551-4725`):
  - Dilewati saat hitpause kecuali `ignorehitpause`.
  - Trigger: `triggerall` AND (`trigger1` OR …) (`compiler.go:7017-7040`).
- ChangeState (`char.go:6727-6756`):
  - Set `prevno`, `no`, `time=0`.
  - Re-run di frame yang sama, dibatasi `MaxLoop`.
- `time` naik sekali per frame non-hitpause. `AnimElem` dihitung dari waktu elemen animasi (`char.go:5245-5249`).
- Contoh `kfm.cns:256-266`: `type=S, movetype=A, physics=S, juggle=1, ctrl=0, anim=200`.

## 3. Common states (`common1.cns.zss`)
| No | Arti |
|---|---|
| 0 / 10-12 / 20 | Stand / crouch / walk |
| 40-52 | Jump start, air jump, naik, turun, landing |
| 100 / 105 / 106 | Run / back hop / back hop land |
| 120-140 | Guard start, guarding, guard end |
| 150-155 | Guard-hit (shake, knockback) |
| 5000/5001, 5010/5011 | Kena pukul berdiri / jongkok (shake → knockback) |
| 5020 → 5030 → 5035 → 5040 / 5050 | Kena di udara → terlempar → transisi → recover / jatuh |
| 5070/5071 | Trip |
| 5080/5081 | Kena saat terbaring |
| 5100 / 5101 | Menghantam tanah / bounce |
| 5110 | Terbaring |
| 5120 | Bangun |
| 5150 | KO terbaring |
| 5200 / 5210 | Recovery darat / udara |

Rantai transisinya:
- 5000 → (Y velocity atau `fall`) 5030, selain itu 5001.
- 5050 → recovery 5200/5210, atau menyentuh tanah → 5100.
- 5100 → 5110 (tanpa bounce) atau 5101 → 5110.
- 5110 → 5150 jika mati. Getup **dipaksa engine** saat `down_recovertime` habis → 5120 → 0.

## 4. HitDef & resolusi hit
- Field penting HitDef (`char.go:548-626`):
  - `attr`, `hitflag`, `guardflag`
  - `priority` + tipe (Hit/Miss/Dodge)
  - `damage` / `guarddamage`, `pausetime[2]`, `guard_pausetime`
  - `ground/air.type`, `slidetime`, `hittime`, `velocity[3]`
  - `air_juggle`, `p1stateno` / `p2stateno`
  - `fall`, `down.bounce`, `down.recover`
- Contoh `kfm.cns:268-292`: trigger `AnimElem=3`, `pausetime=8,8`, `ground.hittime=11`, `air.hittime=15`.
- Box: `Clsn1` (serang) dan `Clsn2` (hurt) **per frame animasi**, berupa persegi 2D di file `.air`. Z hanya dicek sebagai interval kedalaman (`system.go:2082-2092`).
- Urutan cek (`char.go:13432+`):
  1. Proximity guard.
  2. Juggle budget.
  3. Prioritas/trade: ReversalDef menang; prioritas lebih tinggi menang; Hit-vs-Hit = trade; seri throw = `Rand` (`char.go:10706-10790`).
  4. Overlap Z.
  5. Overlap Clsn 2D.
  6. Guard (H/L/A vs statetype S/C/A; guard ditolak bila guard damage akan membunuh).
  7. Hitpause penyerang `pausetime[0]`, korban `pausetime[1]`.

## 5. Cancel & buffer input
- Cancel = trigger biasa di state -1. Contoh (`kfm.cmd:630-705`):
  - `ctrl`
  - `stateno=200 && time>6`
  - `movecontact`
  - `hitdefattr = SC, NA, SA, HA`
- `movecontact` / `movehit` / `moveguarded` dihitung dari `mctime` (`char.go:5639-5665`).
- Command punya `time` (jendela input) dan `buffer.time`. Buffer **dibekukan saat hitpause** (`input.go:2448-2451`), sehingga input yang ditekan saat hitpause masuk ke jendela cancel.
- B/F relatif terhadap arah hadap ±1 (hanya 1D).

## 6. Netplay & snapshot
- Ada delay-lockstep (`netplay.go`) dan GGPO rollback (`rollback.go`). Input rollback hanya untuk 2 pemain (`rollback.go:39-40`); dukungan > 2 pemain unverified.
- Simulasi sepenuhnya bisa di-replay dari input (`rollback.go:229-241`).
- Snapshot = deep clone seluruh state (`state.go`, `state_clone.go` ~1270 baris) + checksum.

## 7. Yang diadopsi / diubah / dibuang
| Konsep | Keputusan |
|---|---|
| Header StateDef + controller ber-trigger | **Adopsi** (data-driven) |
| Urutan fase per frame; push sebelum hit; hit diurutkan prioritas lalu id | **Adopsi** |
| Rantai get-hit (shake → knockback/fall → bounce → lie → getup paksa) | **Adopsi**, diperluas untuk 3D |
| Juggle budget, `movecontact`/`hitdefattr` untuk cancel, buffer beku saat hitpause, `ignorehitpause` | **Adopsi** |
| Replay dari input + checksum | **Adopsi** (replay & validasi server) |
| Clsn persegi 2D, facing ±1, guard tinggi/rendah via jongkok, batas layar | **Buang**, ganti volume 3D, yaw, guard arah |
| float32, state global, RNG global, clone manual | **Ubah**: fixed-point, instance per match, RNG per match, state berupa struct nilai |
| Gear Drop / Hero Swap | Tidak ada padanan langsung. Kait terdekat: `p2stateno` dan tag/standby (`SCF_standby`), unverified |
