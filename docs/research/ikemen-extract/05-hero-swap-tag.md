# 05 — Hero swap: apa yang bisa dipinjam dari TagIn, apa yang harus dibuat sendiri

Menutup 🟡 "hero swap: cooldown, transisi, state yang terbawa".

## 1. OBSERVED — sistem tag Ikemen
Controller `TagIn` (`bytecode.go:5260-5345`) parameternya:
`stateno` (state hero yang masuk), `partnerstateno` (state hero yang keluar), `memberno` (urutan tag),
`self` / `partner` (flag standby), `ctrl` / `partnerctrl`, `leader`.
Terkait: `changeTagOrder`, `changeTagLeader`, `partnerTag(n)`.

`SCF_standby` = partner yang "di belakang panggung". Perilakunya (yang penting untuk kita):
| Aspek | Perilaku | Bukti |
|---|---|---|
| Kontrol | `ctrl()` false → tidak bisa digerakkan | `char.go:5423` |
| Tetap disimulasi | ya (posisi/HP/anim tetap dihitung) | — |
| Hit detection | **dilewati** — tidak bisa dipukul | `char.go:10464` |
| Kamera | tidak di-track | `char.go:10035` |
| State | diset via `setSCF(SCF_standby)` saat keluar | `char.go:3646` |

Tidak ada di Ikemen: cooldown swap, HP bersama, gear yang terbawa, swap saat hitstun, biaya swap.

## 2. Keputusan kita (docs/08 §6.1 — jangan diubah di sini)
3 hero per match, **HP milik pemain** (bukan per hero), neutral swap **3 dtk**, defensive cancel **12 dtk**,
swap = snapshot persisten, bukan event transien. Patch S1–S5 masih **menunggu konfirmasi user**.

## 3. PROPOSED — pemetaan ke Quantum
```
component NxSwap {
    byte   ActiveHero;      // 0..2
    ushort SwapCd;          // satu timer bersama (S2)
    byte   SwapKind;        // 0 none, 1 neutral, 2 defensive
    ushort SwapLock;        // >0 = swap dikunci (startup attack, hitstun, Critical)
}
```
Alur (semua di `NxCombatSystem`, deterministik):
1. Baca `Buttons & Swap` → cek `SwapCd == 0`, `SwapLock == 0`, bukan `Posture = Down`, bukan `Critical` (S4).
2. Tentukan jenis: `HitStun > 0` → defensive (12 dtk) · `require contact` untuk cancel dari serangan (S5) ·
   selain itu neutral (3 dtk).
3. Hero keluar → state `1800 SwapOut` (rerentan, 18 tick); hero masuk → `1810 SwapIn` (i-frame 10 tick, S3).
4. **State yang terbawa**: HP (milik pemain), `GuardGauge` (milik pemain), posisi & `Yaw`, status gear
   (`GearMask`) per hero, cooldown skill **per hero** (tidak di-reset), buff/debuff sisa tick, `HitStun` **tidak**
   dibawa (swap-in selalu bersih — kalau tidak, defensive cancel jadi tak berguna).
5. Buff yang tidak boleh ikut: apa pun yang menempel pada animasi hero lama (mis. "hyper armor 20 tick")
   → di-clear saat swap-out, dengan pengecualian yang ditulis eksplisit di data hero.

## 4. Satu konflik yang perlu dicatat (jangan diputus sendiri)
- Ikemen: **juggle budget per penyerang** (`targetedBy[id]`, `char.go:1232-1236`). Efeknya: penyerang baru
  punya jatah sendiri — combo tag tetap bisa lanjut.
- docs/08 S1: **budget milik korban**, tidak reset saat penyerang swap. Efeknya: total juggle dibatasi
  lintas hero.

Dua-duanya sah, hasilnya berbeda: S1 lebih ketat (combo tag tidak memperpanjang juggle), Ikemen lebih bebas.
Rekomendasi riset: **pakai S1 (satu pool milik korban)** karena match kita 5v5 dan swap murah (3 dtk).
Tapi ini **keputusan desain**, bukan temuan teknis → masuk daftar tanya user, bukan diubah diam-diam.

## 5. Biaya & risiko teknis
- Hero non-aktif **tidak** perlu disimulasikan penuh (beda dari Ikemen yang tetap mensimulasi partner).
  Di Quantum, cukup simpan datanya di komponen; entity hero lain tidak dibuat. Lebih murah untuk 5v5.
- Animasi hero masuk harus punya hurtbox yang sudah benar sejak frame 1 (jangan warisi posisi hero lama).
- Gear Drop saat swap: kalau gear rontok bersamaan dengan swap, urutan resolusi harus tetap
  (hit → gear drop → swap), kalau tidak, hasil antar-klien bisa berbeda.
