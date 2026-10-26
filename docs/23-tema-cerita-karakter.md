# 23 — Tema, Cerita & Desain Karakter (DRAFT v0.1, 2026-10-26)

Anchor kreatif yang selama ini kosong. **Amandemen desain** (mengisi, bukan mengubah mekanik terkunci).

---

## 1. Tema: **Hypebeast Meets Combat Exo-Gear**
Dunia **near-future urban**: budaya streetwear/hypebeast bertemu teknologi exo-suit tempur. Anak muda kota memakai **streetwear** sebagai identitas, lalu mengenakan **Exo-Gear** (modul tempur sci-fi) di atasnya untuk bertarung di arena "Nexus".

Kenapa tema ini kuat & cocok arsitektur kita:
| Lapisan game (sudah terkunci) | Jadi tema ini |
|---|---|
| Kostum avatar (kosmetik, tak pernah lepas) | **Streetwear / hypebeast** (hoodie, sneaker, cap, chain, jaket) — identitas & flex |
| Gear tempur (Helm/Armor/Trinket/Weapon, bisa rontok) | **Exo-Gear** (modul exo-tech sci-fi di atas streetwear) |
| Faction War (Orde vs Legion) | **Dua faksi jalanan** → narasi perang faksi |
| Ekonomi kosmetik non-P2W | **Street cred / flex** (sneaker langka, aura, badge) |
| Arena brawl (LostSaga) | **Sanctioned Nexus brawl** di kota |

Tone: **netral/maskulin, stylish, urban, sporty** — bukan feminin (sejalan dengan penghapusan dance & Fashion Contest).

## 2. Baseline story — Neo-Veridia & The Exo-Drop
Kota masa depan **Neo-Veridia**, berdiri di atas patahan energi tempat jatuhnya artefak berenergi tinggi: **Relic** (peristiwa "The Exo-Drop"). Warga merakit Relic jadi **Combat Exo-Gear** — perangkat tempur modular (Helm/Visor, Chest Rig, Thruster/Trinket, Weapon) yang **mengunci magnetis di luar streetwear**. Saat pengguna kena benturan melampaui batas (Critical / HP 0), kunci magnetik **overload dan Exo-Gear terpental lepas satu per satu** — ini kanon dari mekanik Gear Drop kita.

Dua kubu berebut dominasi:
- **ORDE — Aegis Directorate.** Korporasi militer taktis; ingin memonopoli & menertibkan Relic demi stabilitas kota. Estetika: **techwear bersih, Putih / Emas / Cyan**, VFX presisi geometris.
- **LEGION — Vanguard Syndicate.** Sindikat kru jalanan; meng-overclock Exo-Gear demi kebebasan distrik. Estetika: **hypebeast jalanan, Hitam Matte / Crimson / Neon Volt**, VFX listrik/grafiti/glitch.

Pemain = **Runner** yang membangun reputasi: street cred (fashion) + combat prowess (exo-gear). Cerita = pembungkus, bukan RPG naratif berat.

> Cerita hanya **pembungkus**, bukan mode story berat. Side-content naratif (quest/event) opsional di live-ops.

## 3. Desain karakter & wardrobe
### 3.1 Prinsip
- **2 base body (M/F)** + shared humanoid rig (terkunci). Proporsi stylized (semi-realistis, bukan chibi, bukan anime murni) agar streetwear & exo-gear sama-sama meyakinkan.
- **Hurtbox tetap standar untuk semua** (terkunci) — exo-gear besar hanya bulk visual, tidak mengubah hurtbox. Keterbacaan via identitas gear, bukan ukuran.
- Siluet gear per hero tetap dalam batas (terkunci).

### 3.2 Streetwear (kostum avatar — kosmetik, 13 slot)
Kategori item bernuansa hypebeast: hoodie/jaket, kaos grafis, cargo/techwear pants, **sneaker** (kategori flex utama), cap/beanie, masker, chain/aksesori, tas selempang, kacamata. Dye untuk colorway. Sneaker & jaket = "chase item" status tinggi.

### 3.3 Exo-Gear (hero/gear tempur)
4 slot = modul exo-tech:
| Slot | Wujud exo | Fungsi (terkunci) |
|---|---|---|
| Weapon | Gauntlet/blade/blaster exo | Moveset dasar |
| Helmet | Visor/helm HUD | 1 skill |
| Armor | Chest exo-rig | 1 skill |
| Trinket | Drone/pack/aura core | 1 skill |

### 3.3b Dua hero MVP (nama & rig)
| Hero | Arketipe | Exo-Rig | Weapon | Armor | Helm | Trinket |
|---|---|---|---|---|---|---|
| **TITAN-01** | Grappler/Brawler | berat, mekanis | Hydraulic Gauntlets (dua tangan) | Pelindung bahu mekanis | Tactical Holo-Visor | Jet-Thruster (grab/slam) |
| **PULSE-X** | Zoner/Gunner | ramping, taktis | Dual Rail-Pistols | Mantel taktis berpelindung energi | Target-Lock Headset | Floating Drone (ranjau/tembak) |

Support (Fase 3) = "Field/Medic rig".

### 3.4 Faksi & kosmetik
Tiap faksi punya **colorway & emblem** khas; kosmetik ber-tema faksi (badge, aura) didapat dari Faction War (kosmetik, nol stat).

## 4. Arah VFX skill — Stylized Cyber-Street FX
Gaya: garis neon tajam & bersih (ala Zenless Zone Zero / Valorant), hologram, spray-burst, shockwave bersih — bukan fantasi sihir. Prinsip terkunci: **VFX selalu kosmetik**, tidak pernah ubah hitbox/timing/keterbacaan.

**Aturan emas VFX (wajib, untuk keterbacaan 3v3/5v5):**
1. **Ground-ring indikator ancaman.** Serangan **AoE / ter-telegraph / skill** musuh wajib punya **ring/outline di lantai**: **merah = musuh**, **biru/aman = kawan**. (Pukulan dasar cepat tidak perlu ring — dibaca dari animasi, agar tidak clutter.)
2. **Zero-clutter sumbu vertikal.** Asap/ledakan **dilarang menutup siluet tubuh > 0,2 detik**. Pemain harus selalu bisa membaca animasi startup pukulan **dan** melihat saat Exo-Gear lawan rontok.
3. Hit spark / hurt flash pakai **warna standar** (bukan warna skin/faksi) — konfirmasi hit tetap jelas.
4. **Skin skill** (MiCash) mengganti tampilan VFX, bukan gameplay; hit confirm/hitpause identik.
5. Warna faksi (Orde cyan/emas, Legion crimson/volt) untuk flair, **bukan** untuk indikator gameplay.
6. Budget partikel per layar (mobile) — LOD + pooling (doc 19).

## 5. Dampak ke dokumen lain
- `01`, `11`, `README`: tambahkan tema; ganti "avatar generik" → streetwear, "gear" → exo-gear.
- `12`: **Fashion Contest dihapus** (tidak sesuai tema; lihat 24).
- `15 §6`: kategori kosmetik diberi rasa hypebeast (sneaker sebagai kategori).

## 6. Keputusan terbuka
1. Gaya visual presisi: semi-realistis stylized vs cel-shaded stylized? (menentukan pipeline aset)
2. Nama faksi final: Orde/Legion (placeholder) — pertahankan atau ganti?
3. Seberapa jauh narasi: murni pembungkus, atau ada season storyline ringan?
4. Rating 13+ vs estetika "grungy" Legion — jaga agar tidak terlalu gore.
