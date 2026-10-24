# 06 — Kamera Arena & Avatar di Arena (2026-10-24)

## 1. Kamera: koreksi keputusan sebelumnya
Keputusan "2.5D side-view (seperti LostSaga)" **keliru**: LostSaga bukan side-view murni. Karakter bergerak bebas di bidang X/Z, bisa lompat (Y), dan kamera tetap menyamping-atas.

| | Side-view murni (Brawlhalla/Elsword) | Free-roam 3D, kamera tetap (LostSaga) |
|---|---|---|
| Sumbu gerak | X + Y | X + Z + Y |
| Mengitari musuh yang guard | ❌ | ✅ |
| Knockback ke drop zone / jurang | Hanya kiri-kanan | Ke segala arah |
| Gear jatuh & dipungut | Terbatas | ✅ |
| Hitbox | Kotak 2D | Volume 3D (box/capsule) |
| Netcode | Paling ringan | Sedikit lebih berat; masih wajar untuk 5v5 server-authoritative |

**Usulan:** arena **3D free-roam dengan kamera quarter-view tetap** (tidak bisa diputar player). Alasannya: identitas LostSaga (mengitari guard, drop zone, gear rontok) ada di sumbu Z. Kamera tetap menjaga keterbacaan dan memudahkan kontrol keyboard.

Konsekuensi: Ikemen GO (2D) tetap dipakai sebagai referensi **format data state & HitDef**, bukan referensi ruang/fisika.

## 2. Avatar vs Gear di arena
**Usulan: Opsi B dengan aturan siluet.**

| Lapisan | Contoh | Bisa rontok? | Sumber |
|---|---|---|---|
| Tubuh avatar | Wajah, rambut, warna kulit | Tidak | Wardrobe |
| Kostum avatar | Baju, celana, sepatu | **Tidak pernah** | Wardrobe (Gold/MiCash) |
| Gear tempur | Senjata, armor, helm, jubah/trinket | **Ya** (kombo/hit tertentu) | Hero/Gear set |
| Skin gear | Warna, material, efek partikel gear | Ikut gear | Toko (MiCash) |

Aturan:
- Pemain selalu terlihat dengan kostumnya, termasuk saat seluruh gear rontok. Kostum tetap tampil sebagai "pamer gaya".
- **Skin gear tidak boleh mengubah siluet**: bentuk dasar dan ukuran per hero tetap standar, sehingga musuh selalu bisa membaca hero dan gear apa yang dipakai.
- Gear yang jatuh di lantai diberi outline warna tim + ikon di HUD.
- Mekanik pungut gear musuh: **perlu diverifikasi** saat membedah client LostSaga. Bila dipakai, gear pungutan tampil dalam versi default (tanpa skin pemilik).

## 3. Gold sink (pelengkap ekonomi)
Selain sewa dan rent-to-own: tiket masuk Relic, pembelian hero, ganti nama, dye/ganti warna kostum, furnitur Squad HQ, biaya daftar turnamen komunitas. Tidak ada biaya perbaikan gear, karena terasa menghukum pemain.

## 4. MVP: 2 hero
| Hero | Arketipe | State yang diuji |
|---|---|---|
| Melee Grappler | Jarak dekat, grab, lempar | Dash, Guard, Hitstun, Bound (grab), Down, Get-up i-frame, Gear rontok |
| Ranged Zoner | Proyektil, kontrol area | Airborne (launcher), Faint/Stun, Frozen, proyektil vs guard |
| Keduanya | — | Idle, Run, Jump, Gear swap, drop zone |
