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

## 2. Baseline story (ringkas, bisa diperluas)
Kota **Nexus City**, near-future. Setelah sistem lama runtuh, kekuasaan jalanan dipegang dua faksi:
- **ORDE** — disiplin, teknologi rapi, "order through strength". Estetika: clean, geometric, putih/biru-neon.
- **LEGION** — liar, improvisasi, "freedom through chaos". Estetika: grungy, tribal-tech, merah/oranye-neon.

Keduanya berebut dominasi lewat **Nexus Brawl** (arena resmi) dan perang wilayah. Pemain = seorang **Runner** yang membangun reputasi: street cred (fashion) + combat prowess (exo-gear). Tidak ada "chosen one" — ini dunia kompetitif sosial, bukan RPG naratif berat (sesuai pilar "dunia ringan").

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

Arketipe hero dibungkus tema: **Grappler** = "Bruiser rig" (exo-gauntlet berat), **Zoner** = "Tech-blaster rig" (drone + proyektil), **Support** (Fase 3) = "Medic/field rig".

### 3.4 Faksi & kosmetik
Tiap faksi punya **colorway & emblem** khas; kosmetik ber-tema faksi (badge, aura) didapat dari Faction War (kosmetik, nol stat).

## 4. Arah VFX skill
Prinsip (terkunci): **VFX selalu kosmetik**, tidak pernah ubah hitbox/timing/keterbacaan.
- Gaya: **neon-tech + street graffiti energy** (glitch, hologram, spray-burst), bukan fantasi sihir.
- Warna faksi: Orde biru/putih, Legion merah/oranye — tapi **readability gameplay tetap** (hit spark, hurt flash pakai warna standar, bukan warna skin).
- **Skin skill** (MiCash) mengganti tampilan VFX, bukan gameplay. Hit confirm/hitpause tetap identik.
- Budget partikel per layar (mobile) — LOD + pooling (doc 19).

## 5. Dampak ke dokumen lain
- `01`, `11`, `README`: tambahkan tema; ganti "avatar generik" → streetwear, "gear" → exo-gear.
- `12`: **Fashion Contest dihapus** (tidak sesuai tema; lihat 24).
- `15 §6`: kategori kosmetik diberi rasa hypebeast (sneaker sebagai kategori).

## 6. Keputusan terbuka
1. Gaya visual presisi: semi-realistis stylized vs cel-shaded stylized? (menentukan pipeline aset)
2. Nama faksi final: Orde/Legion (placeholder) — pertahankan atau ganti?
3. Seberapa jauh narasi: murni pembungkus, atau ada season storyline ringan?
4. Rating 13+ vs estetika "grungy" Legion — jaga agar tidak terlalu gore.
