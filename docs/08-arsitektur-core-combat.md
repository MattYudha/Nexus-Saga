# 08 — Arsitektur Core Combat (DRAFT v0.1, 2026-10-24)

Dasar riset: `research/state-machine-ikemen.md` (model state) + `research/netcode-ddnet.md` (tick/snapshot).
Keputusan pengikat: arena 3D free-roam + kamera quarter-view terkunci; 5v5; server-authoritative; Opsi B + aturan siluet (06).
Dokumen ini adalah **desain**, bukan kode. Format data ditulis sebagai skema konseptual.

---

## 1. Prinsip
1. **Satu Combat Core.** Simulasi combat ditulis sekali sebagai library deterministik. Server memakainya sebagai otoritas; client memakainya untuk prediksi. Ini menghindari dua salinan kode seperti di DDNet.
2. **Server-authoritative.** Damage, KO, Gear Drop, dan Hero Swap hanya diputuskan server.
3. **Tick 60 Hz.** 1 tick = 1 frame animasi, sehingga frame data (startup, hitstun, hitpause) ditulis langsung dalam tick.
4. **State integer.** Posisi fixed-point, yaw integer, semua timer integer. Di-quantize setiap tick, sehingga delta snapshot kecil dan prediksi stabil.
5. **State berupa struct nilai** (tanpa pointer/global), sehingga snapshot, rollback, dan replay murah.
6. **Data-driven.** State, animasi, hitbox, dan skill hero ada di file data. Balancing tidak butuh build ulang.
7. **RNG per match**, di-seed server. Tidak ada RNG global.

## 2. Model ruang
| Besaran | Representasi |
|---|---|
| Posisi | int32 fixed-point, 1 unit = 1/256 meter |
| Velocity | int32 fixed-point per tick |
| Yaw | uint16 (65536 = 360°); gerak 8 arah, rotasi visual boleh halus |
| Sumbu | X/Z = lantai, Y = tinggi |
| Input arah | Relatif kamera (kamera terkunci → arah layar = arah dunia, konsisten untuk semua pemain) |

## 3. Pipeline per tick (server dan prediksi client identik)
```
T0  Kumpulkan input untuk tick N (dikunci per tick; terlambat → dipakai di tick berikutnya)
T1  Update command buffer      (dibekukan selama hitpause pemilik)
T2  Lapisan Command → ChangeState (setara state -1 Ikemen)
T3  Terapkan ChangeState tertunda; jalankan controller state aktif
    (re-run di tick yang sama maksimal 4 kali)
T4  Physics: velset/gravitasi/friksi → gerak X/Z/Y → collision arena
T5  Push resolution antar karakter (urut entity id)
T6  Hit detection: hitbox aktif vs hurtbox (3D), urut prioritas lalu entity id;
    hurtbox korban di-rewind (lag compensation, lihat §9)
T7  Hit result → antrian reaksi (diterapkan di T3 tick berikutnya, aturan eksplisit)
    + hitpause kedua pihak + damage + cek Gear Drop + cek KO
T8  Sistem loadout: Gear Drop, pickup gear, Hero Swap
T9  Timer (hitstun, i-frame, cooldown), advance frame animasi, time++ (kecuali hitpause)
T10 Quantize semua state → (server) bangun snapshot
```
Aturan penting dari riset: push sebelum hit; seluruh hit di-resolve dalam satu pass sebelum hasilnya diterapkan; urutan berdasarkan entity id. Ini menjaga hasil 10 pemain bebas dari efek urutan.

## 4. Model state
### 4.1 Header StateDef (adaptasi Ikemen)
| Field | Nilai | Catatan |
|---|---|---|
| `posture` | Stand / Air / Down | **Tanpa Crouch** (LostSaga tidak punya jongkok) |
| `moveType` | Idle / Attack / Hurt | |
| `physics` | Ground / Air / None | Ground = friksi X/Z, Air = gravitasi |
| `anim` | id animasi | |
| `ctrl` | bool | Boleh menerima command |
| `velSet` | (x, y, z) lokal terhadap yaw | |
| `juggleCost` | int | |
| `armor` | None / Super / Hyper | Super armor = tidak masuk Hurt (tetap kena damage) |
| `invuln` | none / strike / grab / all | Untuk i-frame |
| `gearSkillSlot` | Weapon / Armor / Helmet / Trinket / none | State ini butuh gear slot tertentu |

Controller: `{ trigger, persistent, ignoreHitPause, actions[] }`. Contoh action: ChangeState, VelSet, HitDef, SpawnProjectile, SetInvuln, PlaySfx.

### 4.2 Daftar state inti
| ID | State | posture / moveType | Catatan |
|---|---|---|---|
| 0 | Idle | Stand / Idle | |
| 10 | Run (8 arah) | Stand / Idle | |
| 20 | Dash | Stand / Idle | i-frame awal opsional per hero |
| 30 / 31 / 32 | Jump start / Airborne (kontrol) / Land | Air / Idle | |
| 40 / 41 / 42 | Guard / Guard-hit / Guard break | Stand / Idle→Hurt | Guard **busur depan 180°**; serangan dari belakang tembus (§5.3) |
| 100–499 | Serangan & skill hero | — / Attack | Dari data hero + gear |
| 500 / 501 | Grab start / Grab hold | Stand / Attack | |
| 1000 / 1001 | Hit stand (shake → slide) | Stand / Hurt | `hittime`, `slidetime` |
| 1010 | Launched (Airborne kena) | Air / Hurt | Juggle aktif |
| 1020 | Fall | Air / Hurt | |
| 1030 | Ground bounce | Air / Hurt | |
| 1040 | Down (terbaring) | Down / Hurt | Hit OTG terbatas |
| 1050 | Get-up | Stand / Idle | **i-frame penuh**; dipaksa saat `downTime` habis |
| 1060 | Air recover | Air / Idle | Input recovery di 1020 |
| 1100 | Faint / Stun | Stand / Hurt | Durasi dari HitDef; mashing mempercepat |
| 1110 | Frozen | Stand / Hurt | Animasi beku, hit berikut memecah es |
| 1120 | Bound (dipegang/diikat) | Stand / Hurt | Dikendalikan state penyerang (setara `p2stateno`) |
| 1500 | Drop-zone fall | Air / Hurt | Jatuh dari arena → 1900 |
| 1800 / 1810 | Hero Swap out / in | Stand / Idle | §6 |
| 1900 | KO | Down / Hurt | Semua gear jatuh |
| 1910 | Respawn | Stand / Idle | i-frame spawn |

### 4.3 Transisi utama
```
Idle ⇄ Run ⇄ Dash        Idle → Jump → Airborne → Land → Idle
Idle/Run → Attack(100+) → (cancel via movecontact/hitdefattr) → Attack berikut
Idle → Guard → Guard-hit → Guard (atau Guard break → Faint)

Kena hit (antrian T7 → T3 tick berikut):
  ground, fall=0            → 1000 → 1001 → Idle
  ground, fall=1 / launcher → 1010 → 1020 → (recover? 1060) → land 1030 → 1040 → 1050 → Idle
  air                       → 1010 (juggle budget berkurang)
  stun / freeze / bind      → 1100 / 1110 / 1120 → Idle
  keluar arena              → 1500 → 1900
  HP 0                      → 1900 → 1910
```
Reaksi ditentukan oleh **HitDef penyerang**, bukan kode korban (prinsip Ikemen).

## 5. HitDef & hitbox 3D
### 5.1 HitDef (per serangan)
| Field | Isi |
|---|---|
| `attr` | posture target yang bisa dikenai, jenis (normal/skill/throw/projectile) |
| `priority` | angka + tipe (Hit/Miss/Dodge) untuk trade |
| `damage` / `guardDamage` | |
| `hitPause` | (penyerang, korban) dalam tick |
| `hitStun` | ground / air dalam tick (**minimal ±10**, menutup 1 RTT; riset DDNet) |
| `knockback` | (maju, naik) relatif arah serangan → menjadi vektor X/Z/Y |
| `reaction` | stand / launch / trip / stun(n) / freeze(n) / bind(stateId) |
| `fall` | bool, `bounce`, `downTime` |
| `juggleCost` | |
| `guardBreak` | nilai pengurang guard gauge |
| `gearKnock` | 0–3 (§7) |
| `hitFx` | spark/sfx (kosmetik; skin boleh mengganti, gameplay tidak) |

### 5.2 Box
- Per frame animasi: daftar **hitbox** (serang) dan **hurtbox** (badan).
- Bentuk: **capsule** (badan, tongkat) dan **OBB** (tebasan). Sphere untuk proyektil.
- Koordinat lokal terhadap yaw karakter.
- **Aturan siluet:** hurtbox ditetapkan per **hero**, bukan per kostum atau skin. Kostum dan skin gear tidak pernah mengubah box apa pun.
- Hitbox satu serangan hanya bisa mengenai target yang sama sekali, kecuali `multiHit` diset.

### 5.3 Resolusi (urutan)
1. Kumpulkan semua pasangan (hitbox aktif × hurtbox lawan, tim berbeda), tolak yang `invuln`.
2. Cek juggle budget target.
3. Trade/prioritas: prioritas lebih tinggi menang; sama → Hit-vs-Hit trade; seri throw → RNG match.
4. Guard: target dalam state Guard **dan** sudut serangan dalam busur depan **180°** → guard-hit; selain itu → hit.
   - Sudut dihitung dari yaw korban ke **posisi penyerang** (melee) atau ke **kebalikan arah velocity proyektil** (proyektil).
   - **Patch usulan G1:** selama Guard, kecepatan putar yaw dibatasi (mis. 45° per 6 tick). Tanpa ini, pemain bisa berputar instan menghadap setiap penyerang dan busur 180° efektif menjadi 360°.
   - **Patch usulan G2:** Guard gauge. Setiap guard-hit mengurangi gauge; habis → 42 Guard break → 1100 Faint. Gauge pulih saat tidak guard. Menahan turtling dari depan.
5. Kumpulkan hasil → terapkan bersamaan (T7).

## 6. Hero Swap
### 6.1 Disepakati (2026-10-24)
- Sistem mendukung **3 hero per match (squad)**. Produksi aset MVP tetap 2 hero.
- **HP milik pemain**, bukan per hero.
- Dua jenis swap:
  | Jenis | Kapan | Cooldown |
  |---|---|---|
  | Neutral/Combo Swap | Idle atau sedang menyerang (combo extension) | **3 detik** |
  | Defensive Cancel | Saat Hurt/hitstun | **12 detik** |
- Hero Swap = **state snapshot persisten** (heroId aktif + timer), bukan event transien.
- Semua angka cooldown dan durasi disimpan di data (bisa di-tuning tanpa build ulang).

### 6.2 Patch usulan (menunggu konfirmasi)
- **S1 — Juggle budget milik korban, bukan milik hero penyerang.** Budget tidak di-reset saat penyerang swap. Tanpa ini, swap tiap 3 detik bisa memperpanjang combo tanpa batas.
- **S2 — Satu cooldown bersama.** Neutral swap memasang cooldown 3 detik, defensive swap memasang 12 detik, pada timer yang sama. Tanpa ini, pemain bisa swap defensif lalu langsung swap netral.
- **S3 — Defensive Cancel harus berdaya.** Mendapat pushback ke lawan terdekat + i-frame SwapIn singkat (mis. 10 tick). Tanpa itu, ia hanya menukar hero yang tetap terkena combo.
- **S4 — Swap dikunci saat Critical** (lihat §7). Tanpa ini, pemain di HP 0 bisa swap ke hero lain untuk mendapat set gear utuh = "nyawa" tambahan.
- **S5 — Swap-cancel dari serangan hanya pada frame tertentu** (mis. setelah hit/guard terjadi, `movecontact`). Tidak dari startup, supaya swap tidak menjadi pembatal animasi universal.
- State: `1800 SwapOut` (rentan) → `1810 SwapIn`. Hero masuk di posisi yang sama dengan arah hadap yang sama.
- Keterbacaan 5v5: 10 pemain × 3 hero = 30 kit. HUD menampilkan squad tiap lawan, dan swap diberi VFX/sfx khas.

## 7. Gear Drop (Opsi B)
### 7.1 Model loadout (terpisah dari state badan)
```
Player
 ├─ AvatarCosmetic   (tidak pernah lepas; nol efek gameplay)
 └─ ActiveHero
     └─ GearSlots[4] = Weapon, Armor, Helmet, Trinket
          - tiap slot memberi skill (state 100–499 yang memerlukan slot itu)
          - status: Equipped / Dropped
```
Gear Drop **bukan state badan**. Ia perubahan komponen loadout yang diproses di T8, bersamaan dengan reaksi hit biasa. Korban tetap masuk 1000/1010/… sesuai HitDef, ditambah animasi overlay "gear terlepas".

### 7.2 Aturan rontok — Disepakati (2026-10-24)
- Gear **tidak** rontok selama HP > 0.
- **HP 0 → state Critical (Zero HP Vulnerability).** Pemain belum KO.
  - Pukulan berat/knockdown merontokkan 1 gear, urutan **Helm → Trinket → Armor**.
  - Pukulan berat saat ketiganya sudah lepas → **KO**.
  - DropZone → KO langsung.
- **Senjata tidak pernah rontok sebelum KO.** Saat KO hanya terpental secara visual, tidak bisa dipungut. Tidak ada state unarmed.
- Slot yang rontok: skill slot itu hilang dan visual gear hilang. **Kostum avatar tetap tampil.**

### 7.3 Patch usulan untuk Critical (menunggu konfirmasi)
- **C1 — Pisahkan "lapisan nyawa" dari gear fisik.** Critical memberi **3 Break Stock tetap** per nyawa. Setiap stock yang pecah menjatuhkan gear berikutnya jika masih ada.
  - Masalahnya bila jumlah gear = jumlah nyawa: pemain yang memungut gear lawan saat Critical **menambah nyawa sendiri**. Sebaliknya, pemain yang gear-nya sudah dicuri sebelum Critical langsung KO.
  - Dengan C1, gear hanya memberi skill, sedangkan daya tahan Critical selalu adil (3).
- **C2 — Pukulan ringan juga berarti di Critical.** Pukulan ringan mengisi Break meter; penuh = 1 stock pecah. Pukulan berat memecahkan 1 stock langsung.
  - Masalahnya bila hanya pukulan berat yang dihitung: hero zoner yang serangannya ringan tidak bisa menuntaskan lawan, dan pemain Critical kebal terhadap pukulan ringan.
- **C3 — Critical sangat terlihat** (aura, ikon, suara) dan **tidak bisa swap** (S4). Tidak ada regenerasi HP di Critical.
- **C4 — Batas waktu Critical** (mis. 15 detik tanpa terkena pukulan → kembali ke HP kecil, mis. 10%). Opsional; mencegah pemain Critical bersembunyi di 5v5. Perlu diuji.

### 7.4 Gear di lantai — Disepakati (2026-10-24)
- Entity `DroppedGear` di snapshot (persisten): pemilik, heroId, slot, posisi, sisa umur (mis. 10 detik).
- **Siapa cepat dia dapat**, termasuk lawan, untuk **Helm, Armor, Trinket**. Senjata tidak bisa dipungut.
- Gear pungutan tampil versi default (tanpa skin pemilik), atau aura/ikon saja di fase MVP.
- Pickup = input "interact", diputuskan server.

### 7.5 Patch usulan untuk pickup (menunggu konfirmasi)
- **P1 — Skill gear harus "generik".** Alasan Anda menolak pickup senjata (moveset terikat rangka hero) **berlaku juga untuk Helm/Armor/Trinket** jika skill-nya memakai animasi khusus hero tertentu. Pilihan:
  - (a) Semua hero memakai **satu rangka humanoid bersama** dan skill gear dianimasikan untuk rangka itu. Usulan, karena sejalan dengan wardrobe avatar yang juga butuh rangka bersama.
  - (b) Gear pungutan hanya memberi efek pasif.
- **P2 — Mesh gear harus pas di semua hero.** Konsekuensi (a): proporsi tubuh hero dibatasi beberapa body type standar.
- **P3 — Satu slot hanya satu gear.** Memungut helm saat helm sendiri masih terpasang = ditolak atau menukar (helm lama jatuh). Usulan: menukar.

## 8. Avatar di arena (render)
Urutan lapisan: tubuh avatar → kostum (wardrobe) → gear tempur (bisa rontok) → efek skin gear. Lapisan gameplay (hurtbox, hitbox, siluet hero) **tidak bergantung** pada kostum atau skin.

## 9. Netcode (adaptasi DDNet)
| Aspek | Desain |
|---|---|
| Sim | 60 Hz fixed tick, loop catch-up |
| Input | Struct ukuran tetap per tick, dikirim unreliable, **3 input terakhir dikirim redundan**. Membawa tick yang diprediksi + tick snapshot terakhir yang di-ack |
| Sinkron jam | Server membalas "input datang X ms lebih awal"; client mengatur jam prediksinya ke margin 10–20 ms |
| Snapshot | Per penonton, **30 Hz** (60 Hz jika bandwidth cukup), delta vs snapshot ter-ack, CRC + resync penuh. Target < 1 KB untuk 10 pemain |
| Isi snapshot | Posisi, yaw, stateId, stateTime, hitstun/hitpause tersisa, HP, guard gauge, heroId, status 4 gear, DroppedGear, cooldown |
| Prediksi client | Rollback-replay pemain lokal dari snapshot terakhir; prediksi dibatasi mis. 15 tick |
| Pemain lain | Interpolasi antar 2 snapshot; error dihaluskan **hanya di transform visual** |
| Event prediksi | Spark/sfx/hitpause penyerang diprediksi lalu di-dedup dengan konfirmasi server |
| Lag compensation | Histori hurtbox 300 ms; serangan di-resolve terhadap posisi korban di tick yang dilihat penyerang; **rewind maks 150 ms** |
| Reliable | KO, Hero Swap, Gear Drop/pickup, akhir match = state persisten di snapshot atau pesan reliable |
| Transport | UDP; paket ≤ 1200 B (aman MTU); chunk reliable/unreliable |

## 10. Data hero (pipeline konten)
Satu paket data per hero:
- `states`: daftar StateDef + controller
- `anims`: frame, durasi, box per frame
- `hitdefs`: dirujuk dari state
- `commands`: input → state, beserta buffer
- `gear`: 4 slot → skill state yang dibuka masing-masing
- `stats`: HP dasar, kecepatan, berat (pengaruh knockback)

Di build/server ada validasi data: referensi state valid, box tidak kosong saat attack aktif, siluet dalam batas.

## 11. Status keputusan
| # | Topik | Status |
|---|---|---|
| 1 | Guard busur depan 180° | ✅ Disepakati; patch G1 (batas putar) & G2 (guard gauge) menunggu |
| 2 | Pickup gear lawan (kecuali senjata) | ✅ Disepakati; patch P1–P3 menunggu |
| 3 | 3 hero/match, cooldown 3 s / 12 s | ✅ Disepakati; patch S1–S5 menunggu |
| 4 | Critical di HP 0, senjata tidak rontok | ✅ Disepakati; patch C1–C4 menunggu |
| 5 | Snapshot 30 Hz atau 60 Hz | ⏳ Uji bandwidth di prototipe |
| 6 | Format data hero | → `09-arsitektur-sistem.md` |
| 7 | Engine & backend | → `09-arsitektur-sistem.md` |
