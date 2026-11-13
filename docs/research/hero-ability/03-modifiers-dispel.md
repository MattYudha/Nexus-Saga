# 03 — Model modifier (buff/debuff), stacking, dispel, immunity

> ## ⚠️ ARSIP PASCA-MVP (2026-11-13)
> Sistem modifier **tidak dibangun untuk MVP**. `Faint` tetap field biasa (sudah jalan & teruji).
> Dokumen ini disimpan sebagai rancangan fase berikutnya.

## 1. Konsep yang dipelajari (OBSERVED/`DK`, ditulis ulang)
| Konsep | Isi | Padanan kita |
|---|---|---|
| **Modifier** | efek berdurasi yang menempel pada unit | `NxModifier` (slot tetap) |
| **Basic dispel** | hapus sebagian besar buff/debuff | `DispelBasic` |
| **Strong dispel** | hapus juga stun/disable | `DispelStrong` |
| **Debuff immunity** | kebal debuff, buff tetap | tag `ImmuneDebuff` |
| **Stacking rule** | refresh / stack / independen / unik | `stackRule` |
| **Status resistance** | memperpendek durasi saat **diterapkan** | dihitung sekali, bukan per tick |

`DERIVED`: aturan paling penting bukan daftar buff, tapi **kapan** durasi dihitung dan **bagaimana**
dua sumber efek yang sama bertemu. Itu sumber bug dan sumber desync.

## 2. PROPOSED — struktur data (slot tetap, deterministik)
```
component NxModifier {
    byte  Count;
    byte[8] Id;         // id modifier (0 = kosong)
    ushort[8] Ticks;    // sisa durasi
    byte[8] Stacks;     // 1..N
    byte[8] Source;     // slot pemain pemberi (255 = sistem)
}
```
Kenapa array tetap: tidak ada alokasi, urutan iterasi **indeks**, snapshot murah.
Kalau array di `.qtn` merepotkan, alternatifnya bit-pack + 4 slot (lihat catatan di `01 §5`).

## 3. Stacking rules (PROPOSED)
| Rule | Perilaku | Contoh |
|---|---|---|
| `Refresh` | durasi di-reset ke maksimum, stack tetap | slow dari hero sama |
| `Stack` | `stacks++` (max di data), durasi refresh | bleed/poison, damage per stack |
| `Independent` | instance baru menempati slot baru | dua hero berbeda memberi slow |
| `Unique` | diabaikan bila sudah ada | aura pasif |

Urutan saat slot penuh: **buang slot dengan `Ticks` terkecil**, seri → indeks terbesar. Aturan ini
harus sama di semua klien; jangan pakai "yang terakhir masuk" tanpa tie-break.

## 4. Aplikasi & dispel
```
Apply(mod):
  1. kalau korban punya ImmuneDebuff dan mod bertag Debuff → tolak
  2. cari slot (stack rule)
  3. Ticks = floor(durasi × Π(1 − SR)) , min 1
  4. kalau perlu, buang slot (aturan §3)
```
| Dispel | Menghapus | Tidak menghapus |
|---|---|---|
| `DispelBasic` | buff/debuff biasa (slow, armor, bleed) | stun, faint, ultimate mark |
| `DispelStrong` | semua di atas + stun/faint | mark "tidak bisa didispel" (`Undispellable`) |
| Mati/respawn | **semua** | — |

Tag modifier minimum: `Buff | Debuff | Undispellable | ImmuneDebuff | OnHit | Aura | Stun`.

## 5. Kontribusi statistik — hindari urutan yang berubah
Jangan menyimpan `ArmorTotal` sebagai nilai tunggal yang ditambah/dikurangi sembarangan.
Hitung **setiap kali dibutuhkan** dari base + semua modifier, dengan urutan indeks slot:
```
armor = base; foreach slot: armor += mod.armorAdd;  armorMult = Π(1 + mod.armorPct)
```
`PROPOSED`: sum aditif untuk angka tetap, perkalian untuk persentase. Hasilnya identik di semua klien
dan tidak bergantung pada urutan pemasangan.

## 6. Interaksi dengan sistem yang sudah ada
| Sistem | Aturan |
|---|---|
| Counter hit | tidak membuat modifier, hanya amp sekali-pakai (`02 §8`) |
| Guard crush / `Faint` | `Faint` boleh diperlakukan sebagai modifier `Stun` ber-tag `Undispellable` |
| Gear Armor | `block` flat (`02 §7`), bukan modifier — supaya rontoknya gear langsung terasa |
| Critical | **bukan** modifier; state nyawa (docs/08 §7) — jangan dicampur |
| Hero swap | modifier ber-tag `HeroBound` dihapus saat swap-out |

## 7. Yang belum diputuskan
1. Jumlah slot: 8 cukup? (5v5 + gear + skill = bisa 6–10 efek serentak pada satu target)
2. Apakah `Faint` dipindah menjadi modifier (lebih bersih) atau tetap field khusus (lebih cepat)?
3. Aura: dihitung per tick atau saat masuk/keluar radius? (per tick lebih sederhana, lebih mahal)
