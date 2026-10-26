# 24 — Struktur Kompetitif v2, Mode & Sosial (2026-10-26)

**Amandemen** atas keputusan terkunci (owner-approved). Mengubah: struktur rank, hapus Leader Duel, tambah Faction/Guild War, Survival 10 ronde, Relic lebih ramai, squad shop, chat slash-command, hapus Fashion Contest.

---

## 1. Hapus Leader Duel → Solo Tier Ladder (1v1)
- **Leader Duel DIHAPUS** (hibrida 1v1-mewakili-squad → rawan gap logika).
- **1v1 jadi ladder kompetitif pribadi** satu-satunya.

## 2. Empat jalur pertandingan (FINAL — binding)
| # | Mode & format | Nama di game | Poin → Papan | Hadiah utama |
|---|---|---|---|---|
| 1 | Solo **1v1** (auto-matchmaking) | **Solo Ranked Ladder** | Solo MMR (Glicko-2) | Gelar individu, aura/border, patung Top-1 Solo di Plaza |
| 2 | Trio **3v3 / 5v5** (satu squad penuh) | **Squad War (District Conquest)** | Squad Score / District Influence + **Squad Cred** | **Perebutan distrik Plaza** (bendera, neon logo squad, patung squad, 1 minggu) |
| 3 | Trio **3v3 / 5v5** (se-faksi, lintas squad) | **Faction War (Orde vs Legion)** | Faction Point (FP) + pangkat faksi | Kubu pemenang musiman → ubah tema warna pusat Plaza + badge faksi |
| 4 | **Custom Room** 1v1–5v5 | **Street Room** (casual/latihan) | Account Rank EXP + Gold (rate-limit, anti-AFK) | Naik pangkat akun (Trainee→Major→Colonel), hangout/latihan tanpa risiko MMR |

**Aturan pemisahan (anti-bug):** antrean yang dipilih menentukan papan tujuan (antrean F-War → FP; antrean Squad War → Squad Score). **Faksi ⊥ Squad** (orthogonal): faksi = alegiansi akun level server; squad = grup. Squad War tidak peduli faksi; Faction War tidak peduli squad.

Prinsip: **rank pribadi hanya dari Solo 1v1.** Squad War = kolektif squad (distrik). Faction War = kolektif kubu. Custom = EXP akun. Menutup masalah MMR party sepenuhnya.

> **Koreksi dari v2:** "Guild War" terpisah **dihapus** — Squad War (satu squad) **adalah** perebutan distrik Plaza. Tidak ada mode guild-match terpisah.

### Progres pribadi pemain (3 lapis, tidak bentrok)
1. **Account Rank** (dari SEMUA main) — pangkat EXP (Trainee→Major→Colonel), nol efek kompetitif.
2. **Solo MMR Ladder** (hanya 1v1) — rank sejati. Tier (tema): **Rookie → Contender → Rival → Gladiator → Conqueror → Nexus Legend**.
3. **Kolektif** — Squad standing (distrik) + Faction standing.

### 🔧 Revisi algoritma rating (atas doc 14 §3)
- Ladder **1v1 → Glicko-2** (memang sistem 1v1; lebih tepat dari OpenSkill untuk solo).
- Rating tim (F-War/Guild War) **hanya untuk menyeimbangkan matchmaking**, bukan ladder: pakai rata-rata/OpenSkill sederhana. Bukan angka yang dipamerkan.

## 3. Faction War (Orde vs Legion) — Fase 3+
⚠️ **Sistem besar; bukan MVP.**
```
Faction { id: Orde|Legion, emblem, colorway, seasonPoints }
PlayerFaction { playerId, faction, factionPoints, factionRank }
```
Aturan:
- Pemain memilih faksi (alegiansi level akun). Faksi **orthogonal dengan guild** (guild = grup; faksi = kubu server).
- **Mode yang di-queue menentukan tujuan poin** (F-War → faction board; Guild War → guild board). Tidak bentrok.
- Akhir musim: faksi dengan FP terbanyak menang → reward kosmetik ber-tema faksi untuk semua anggota; pemain kontribusi tertinggi dapat pangkat faksi khusus (kosmetik, nol stat).
- Ganti faksi: cooldown panjang (mis. per season) agar tidak lompat-lompat.

## 4. Squad War = District Conquest (perebutan distrik Plaza) — Fase 3
- **Squad War adalah fitur bintang; TIDAK dihapus.** Satu squad penuh (3v3/5v5) vs squad lain → Squad Score + District Influence.
- Siklus mingguan: squad skor tertinggi di tiap distrik **menguasai distrik Plaza** selama 1 minggu (bendera, neon logo squad, patung squad).
- Reward: **Squad Cred** (belanja Squad Shop), kosmetik, Gold. Nol stat.
- ⚠️ Butuh populasi pemain cukup (squad vs squad) → wajar di **Fase 3**, bukan MVP.

## 5. Survival Elimination — 10 ronde (FINAL)
- **Format: Race-to-6 (Best of 10), 90 detik/ronde, transisi 3 detik.**
- Skor imbang **5–5 di ronde 10 → Ronde 11: Final Sudden Death.**
- Pemain ter-KO: **kamera spectate rekan setim**; tempo cepat agar tidak menganggur.
- Berlaku untuk 1v1 Solo Ranked dan mode tim Survival.

## 6. Relic (Relix) — 2 LAPIS (solusi beban server, FINAL)
Koreksi: "banyak orang di 1 lokasi ala LostSaga" = **zona pencarian ramai yang ringan**, bukan combat PvE 60 Hz untuk puluhan orang.

| Lapis | Isi | Kapasitas | Arsitektur |
|---|---|---|---|
| **A. Relic Excavation Zone** | Berkumpul ramai, pakai radar/scanner, gali titik Relic Core bersama, ngobrol, pamer outfit, broadcast saat ada drop langka | **20–50 pemain** | **Plaza/Nakama** (ringan, TANPA combat 60 Hz) |
| **B. Relic Rift / Boss** | Saat penggalian memicu Boss/Gate, pemain di sekitar masuk bersama melawan bos | **maks 8 pemain** | **.NET Game Server + Core** (60 Hz) |

Aturan:
- Excavation Zone = seperti Plaza authoritative match; gerak client-authoritative + cek kewajaran; **tanpa physics combat**. Beban ringan.
- Loot/dig **server-authoritative** (anti bot); drop langka → auto `/b` Server Broadcast (satu zona heboh).
- Rift memakai **warm-pool allocator** (doc 19) seperti match biasa.
- ⚠️ **Catatan kritis saya:** batasi **rate spawn Rift** (cooldown + cap instance) agar 50 pemain tidak memicu puluhan Rift sekaligus dan membebani fleet .NET.

## 7. Squad HQ + Squad Shop
- Squad HQ bisa didekorasi (doc 16) + **Squad Shop otomatis**.
- Squad Shop jual: **furnitur HQ** + **kosmetik ber-emblem squad** (banner, aura squad).
- Dibeli pakai **Contribution Points** (hasil aktivitas anggota) atau kas squad **khusus furnitur** — **tidak** bisa ditarik ke wallet pribadi (anti transfer kekayaan).
- Semua **nol stat**.

## 8. Chat (perluasan doc 14 §7) + slash-command
| Channel | Slash | Catatan |
|---|---|---|
| Global/server | `/all <msg>` | Rate-limit |
| Squad | `/f <msg>` | Kirim ke squad dari mana saja (ala AyoDance) |
| Whisper/private | `/w <nick> <msg>` | DM, persisten |
| Broadcast/megaphone | `/b <msg>` | **Cooldown + biaya** (item/Gold), anti-spam |
| Faction | `/faction <msg>` | Fase 3 (saat F-War ada) |
| Lokal (Plaza/room) | default | AoI |
Semua lewat hook moderasi (filter server, mute, anti-spam) — doc 14.

## 9. Hapus Fashion Contest
- ❌ **Dihapus** (tidak sesuai tema hypebeast/combat; terkesan feminin).
- Pendorong "pamer avatar" bergeser ke: **street cred** (tampil keren sambil menang), kehadiran di hub/lounge, dan **status cosmetic** (sneaker langka, mount, aura, badge faksi). Monetisasi tetap jalan, lebih netral.
- Kapasitas room 6+30 tetap berguna untuk spectate & hangout.

## 10. Dampak & scope (binding)
MVP = **fondasi Solo 1v1 Ladder + Street Room (Custom)**. Sistem kolektif menyusul.
| Item | Fase |
|---|---|
| **Solo Ranked 1v1 (Glicko-2)** | **MVP (Fase 2)** — 1v1 = fokus arena MVP |
| **Street Room (Custom 1v1–5v5 casual)** | **MVP (Fase 2)** |
| Survival Race-to-6 | Fase 2–3 |
| Chat slash-command (lokal, /f, /w) | Fase 2; /b + /faction Fase 3 |
| **Squad War (District Conquest) + Squad Shop** | Fase 3 |
| **Faction War (Orde vs Legion)** | Fase 3 |
| Relic (Excavation Zone + Rift) | Fase 3 |

⚠️ **Scope (solo + AI):** Squad War distrik, Faction War, Relic menambah beban. MVP tetap ketat: **Solo 1v1 + Custom Room, 2 hero (TITAN-01, PULSE-X)**. Tech arena mendukung 2v2 untuk custom.

## 11. Dokumen yang diperbarui
- `14 §3`: rating 1v1 = Glicko-2; tim = balancing saja.
- `12`: Fashion Contest dihapus.
- `16`: Guild War + Squad Shop; Squad War distrik jadi opsional/world-cosmetic.
- `08`/mode: Survival first-to-6; Leader Duel dihapus.
- `17`: Relic cap 8–12.

## 12. Keputusan terbuka
1. Ladder solo: tier LostSaga-style (Gladiator/Rival/Conqueror) atau tetap Bronze→Mythic? (usul: tetap Bronze→Mythic untuk konsistensi, nama tier bisa di-reskin tema)
2. First-to-6 vs angka lain (uji TTK).
3. Cap Relic final (8/10/12).
4. Faksi: pilih bebas atau di-assign seimbang?
5. Apakah Squad War distrik Plaza tetap ada, atau sepenuhnya diganti Guild War?
