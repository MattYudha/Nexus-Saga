# 17 — Hero Roster, Training Mode & Bot (DRAFT v0.1, 2026-10-24)

Disusun dari keputusan terkunci (`08`, `90`) + riset LostSaga (hero/gear) + Ikemen (state). **Desain, bukan kode.**

---

## 1. Filosofi roster
- Hero = **paket senjata + gear** di atas avatar; dipisah dari kosmetik (`08 §8`).
- Semua hero pakai **shared humanoid rig** (2 base body) → animasi & gear bisa dipertukarkan (`10 §A4`).
- Perbedaan rasa antar-hero: **defense multiplier + weight + moveset/skill**, BUKAN HP (HP milik pemain).
- Arketipe untuk sinergi 5v5: Opener/Melee, Zoner/Ranged, Support/Escape, Tank/Bruiser, Assassin/Flanker.

## 2. Daftar hero (roadmap, bukan final)
| Fase | Hero | Arketipe | Peran | Status |
|---|---|---|---|---|
| **MVP (Fase 2)** | **TITAN-01** | Grappler/Brawler | Hydraulic Gauntlets + Jet-Thruster; grab/slam | Dibuat |
| **MVP (Fase 2)** | **PULSE-X** | Zoner/Gunner | Dual Rail-Pistols + Tactical Drone; kontrol area | Dibuat |
| Fase 3 | **Support** | Pelindung | Shield, buff gerak (bukan heal saat Critical) | Direncanakan |
| Fase 3+ | Bruiser/Tank | Melee tahan | Garda depan, weight tinggi | Konsep |
| Fase 3+ | Assassin | Flanker | Mobilitas, burst, backstab (guard 180) | Konsep |
| Fase 4+ | (rotasi musiman) | variatif | konten live-ops | — |

Catatan: MVP **2 hero** cukup menguji semua state (`06 §4`). Hero baru = konten utama live-ops.

## 3. Definisi hero (ringkas; detail combat di `13`)
```
Hero {
  heroId, name, archetype
  baseBody : enum { M, F }
  stats : { defenseMult: float, weight: float, moveSpeed, dashSpeed }   // NO hp
  gearSlots : { Weapon, Armor, Helmet, Trinket -> defaultGearId }
  states, anims, hitdefs, commands  -> paket data combat (13), ber-hash
}
```
Validasi balancing di build: siluet dalam batas, box tidak kosong saat attack aktif, referensi state valid.

## 4. Training Mode
Tujuan: belajar hero, uji combo, tanpa risiko rank. Reuse Combat Core penuh.
```
TrainingSession {
  playerId
  stage          : training arena
  myHero/squad   : pilih bebas (semua hero bisa dicoba? atau yang dimiliki — lihat terbuka #1)
  dummy          : DummyConfig
  hud            : { showFrameData, showHitbox, showDamage, showInputs, comboCounter }
}
DummyConfig {
  behavior : enum { Stand, Crouch?, Jump, Walk, Guard, GuardAfterHit, CPU }
  recovery : enum { None, Random, Instant }     // bangun/air recovery
  resetOnHit : bool
  infiniteHp : bool
  playbackRecord : bool    // rekam & ulang input dummy (uji setup)
}
```
Fitur penting untuk brawler: **tampilkan frame data, hitbox, dan combo counter** (kita bikin hitbox editor + debug HUD, HANDOFF). Reset posisi cepat.

## 5. Bot / CPU (play-with-bot)
Dipakai di: Training (dummy CPU), mode latihan vs bot, dan **fallback matchmaking** (isi slot saat pemain kurang) — opsional.
```
BotProfile {
  botId, heroId
  difficulty : enum { Rookie, Normal, Hard, Nightmare }
  behaviorTree : btRef         // AI reuse Combat Core input (bot "menekan tombol" seperti pemain)
  reactionTicks : int          // delay reaksi per difficulty (fairness)
  aggression, spacing, comboChance : tuning params
}
```
Prinsip: **bot mengeluarkan INPUT** ke Combat Core yang sama (bukan jalur stat khusus). Ini menjaga determinisme & keadilan, dan AI otomatis "paham" aturan combat.
- Rookie: reaksi lambat, jarang combo.
- Nightmare: reaksi cepat, tahu punish — untuk latihan lanjutan, bukan untuk ranked.
- **Bot tidak masuk ranked/MMR** kecuali mode kasual yang ditandai jelas.

## 6. Mode latihan & onboarding
| Mode | Isi | Fase |
|---|---|---|
| Tutorial | Ajari gerak, guard, combo dasar, Critical, swap (rekaman input ala Ikemen `tutorial.rep`) | Fase 2 |
| Training Grounds | Dummy + HUD debug | Fase 2 |
| Vs Bot (kasual) | 1v1/teamvs bot berbagai difficulty | Fase 2–3 |
| Combo Trial | Tantangan combo per hero (reward kosmetik) | Fase 3 |

## 7. Keputusan terbuka
1. Di Training, apakah semua hero bisa dicoba gratis, atau hanya yang dimiliki + rotasi?
2. Bot untuk mengisi slot matchmaking saat sepi — ya/tidak? (risiko: pemain merasa "dibohongi" jika tak diberi tahu)
3. Jumlah difficulty bot & apakah Nightmare perlu "membaca input" (reaksi 0-tick) — hindari agar tetap adil/manusiawi.
4. Combo Trial reward: kosmetik saja (jaga non-P2W).

