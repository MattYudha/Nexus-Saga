# 01 — Input buffer, command, & jendela cancel

Menutup ⬜ "input buffer, cancel window, combo route" dan "animasi terikat ke data".

## 1. Model command (OBSERVED)

Satu command = daftar **langkah** (`steps[]`) + 4 timer. Field-nya di `Command` (`input.go:2014`):
`maxtime`, `curtime`, `maxbuftime`, `curbuftime`, `maxsteptime`, `stepTimers[]`, `completed[]`.
Diisi dari INI/tabel (`input.go:2651-2657`): `time`→`maxtime`, `buffer.time`→`maxbuftime`,
`step.time`→`maxsteptime`, plus `buffer.hitpause`, `buffer.pauseend`.

Default dari KFM (`chars/kfm/kfm.cmd:142-146`): `command.time = 15`, `command.buffer.time = 1`.
Artinya jendela input bawaan = **15 tick (250 ms @60 Hz)** dan buffer **1 tick**.

Simbol langkah (kfm.cmd:38-64, parser `ReadCommandSymbols`):
`~` rilis · `/` tahan · `$` salah satu dari 3 arah (D/DB/DF) · `+` bersamaan · `>` langkah ketat (tanpa slack) ·
prefix angka `~30a` = tahan minimal 30 tick lalu lepas.

## 2. Alur timer (OBSERVED)

`Command.Step()` (`input.go:2433-2475`), urutan penting:
1. `hpbuf` / `pausebuf` dimatikan kalau `buffer.hitpause` / `buffer.pauseend` = false (`:2442-2452`).
2. `curbuftime--` **hanya** kalau tidak sedang hitpause/pause (`:2448-2451`) → **buffer membeku saat hitpause**.
3. Langkah yang `completed` menaikkan `stepTimers[i]`; kalau lewat `maxsteptime` → langkah dibatalkan (`:2462-2470`).
4. `curtime++` hanya kalau ada langkah yang sudah selesai; kalau tidak, command **reset** (`:2472-2475`).

Saat sequence selesai: `curbuftime = Max(curbuftime, maxbuftime + extratime)` (`:2599`). Command tetap
"tersedia" sampai dikonsumsi `Assert()` (`:2585-2602`) atau timer habis. `extratime` = tambahan dari frame
pause/hitpause (`char.go:13286-13300`) — satu-satunya alasan special yang ditekan saat hitpause tetap menyala.

> Konsekuensi desain: buffer **tidak** berarti "tombol diingat bebas". Yang diingat adalah **command utuh**
> yang sudah selesai, selama slot buffer-nya. Ini yang membuat combo 1-tick-link terasa adil.

## 3. Cancel & combo route (OBSERVED)

Tidak ada sistem cancel khusus. Semua cancel adalah **trigger biasa di state -1** (`char.go:11922-12045`,
`kfm.cmd:379-400`). Predikat yang dipakai di praktik (KFM 95%):
`stateno`, `time>N`, `ctrl`, `movecontact` / `movehit` / `moveguarded`, `hitdefattr = SC,NA,SA,HA`, `command=`.
`movecontact` dihitung dari `mctime` (`char.go:5639-5665`) — yaitu **sudah pernah menyentuh** (kena ATAU
di-guard) di state ini, bukan "kena sekarang".

Route combo = graf state yang boleh dicapai dari state X selama predikat benar. Karena bebas, **tidak ada
validasi** — char bisa combo tak berujung kalau datanya salah. Itu kelemahan yang tidak kita tiru.

## 4. PROPOSED untuk Nexus (Quantum)

### 4.1 Input history di dalam frame state (deterministik)
Quantum sudah punya `input { MoveDir, Buttons, AimYaw }` per tick. Tambahkan **kondisi turunan** di komponen
(bukan di View, bukan di `MonoBehaviour`):

```
component NxCmd {
    byte  Motion;        // bit: 1 QCF, 2 QCB, 4 DP, 8 Charge, 16 DoubleTapFwd
    byte  MotionAge;     // tick sejak motion terakhir selesai (0..15)
    byte[6] BtnPressAge; // umur tekan per tombol; 255 = tidak pernah (di-reset saat konsumsi)
    byte  ConsumeMask;   // bit tombol yang baru dipakai frame ini (untuk buffer 1 slot)
}
```
Alasan: semua isinya integer, ikut tersimpan di rollback, tidak butuh alokasi dinamis.

### 4.2 Angka usulan (tick @60 Hz)
| Parameter | Nilai | Padanan Ikemen |
|---|---|---|
| Jendela gesture (QCF/DP) | 15 | `command.time = 15` |
| Buffer tombol | **4** | `buffer.time = 1` (kita lebih longgar, netcode punya jitter) |
| Buffer gesture | **6** | — |
| Freeze buffer saat hitstop | ya | `buffer.hitpause=false` (default) |
| Panjang langkah max | 6 | `step.time` |
| Tekan di dalam hitstop ikut dihitung | **ya** (maks 1 frame ekstra) | `extratime` |

Kenapa 4 dan bukan 1: di 60 Hz dengan RTT 60–100 ms, buffer 1 tick = pemain harus menekan di frame yang
"benar" menurut simulasi, bukan menurut layar. 4 tick (~66 ms) menutup satu RTT tanpa membuat input "basi".

### 4.3 Cancel window eksplisit (bukan trigger bebas)
```json
"cancels": [
  { "from": "light_1", "to": "light_2",
    "openTick": 6, "closeTick": 20,        // relatif ke state time
    "require": "contact",                   // none | contact | hitOnly | guardOnly
    "cost": 0, "maxChain": 4 }
]
```
- `require: contact` = padanan `movecontact` — lebih permisif dari `hitOnly`, dan **disengaja**: on-block
  cancel membuat tekanan guard terasa hidup.
- `openTick` = startup aktif pertama (padanan `time>N`), `closeTick` = akhir recovery.
- `maxChain` mencegah loop; validator build menolak siklus `from→…→from` tanpa kenaikan state-time.

### 4.4 Combo route & scaling
Simpan di data, bukan kode:
```
comboScaling[hit] = { 1.00, 0.90, 0.80, 0.70, 0.60, 0.50 min 0.40 }
```
Dihitung dari **jumlah hit dalam satu combo** (counter yang di-reset saat victim keluar dari hitstun ≥ 6 tick).
Ini deterministik karena hit counter tersimpan di `NxCombat`.

### 4.5 Animasi terikat data
Ikemen: animasi = daftar frame dengan durasi **tick**, dan `AnimElem`/`AnimTime` jadi trigger logika
(`char.go:5245-5249`). Kita ikuti: klip Unity **tidak** menentukan timing logika. Data frame = sumber waktu,
klip hanya visual; View melakukan `animFrame = data.frameAt(tick)`.
Konsekuensi: animasi tidak boleh pakai Animator state machine / root motion (sudah aturan docs/10).

### 4.6 Kontrol perangkat
Satu model command, tiga mapper (keyboard, gamepad, touch). Touch = tombol virtual yang memetakan ke
`MoveDir` 8 arah + 6 tombol; **tidak ada** logika game khusus mobile. Ini yang membuat mobile tidak
menggandakan sistem combat.
