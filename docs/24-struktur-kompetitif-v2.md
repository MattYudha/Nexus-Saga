# 24 — Struktur Kompetitif v2, Mode & Sosial (2026-10-26)

**Amandemen** atas keputusan terkunci (owner-approved). Mengubah: struktur rank, hapus Leader Duel, tambah Faction/Guild War, Survival 10 ronde, Relic lebih ramai, squad shop, chat slash-command, hapus Fashion Contest.

---

## 1. Hapus Leader Duel → Solo Tier Ladder (1v1)
- **Leader Duel DIHAPUS** (hibrida 1v1-mewakili-squad → rawan gap logika).
- **1v1 jadi ladder kompetitif pribadi** satu-satunya.

## 2. Alokasi poin per mode (model LostSaga, diadaptasi)
| Mode | Format | Poin masuk ke | Currency |
|---|---|---|---|
| **Solo Ranked** | 1v1, matchmaking otomatis | **MMR Ladder pribadi** (Bronze→Mythic) | RP |
| **Faction War (F-War)** | 3v3 / 5v5 | **Faction Board** (Orde vs Legion) | Faction Point (FP) |
| **Guild War** | 3v3 / 5v5 (satu squad) | **Guild Board** (ranking squad) | Guild Score |
| **Custom Room** | 3v3 / 5v5 (undang teman) | **Account Rank EXP** + currency | EXP + Gold (dikurangi) |

Prinsip: **rank pribadi hanya dari 1v1.** Tim menyumbang ke kolektif (faksi/guild) atau sekadar EXP akun. Menutup masalah MMR party (premade vs solo) sepenuhnya.

### Progres pribadi pemain (3 lapis, tidak bentrok)
1. **Account Rank** (dari SEMUA main) — pangkat EXP, nol efek kompetitif (kosmetik/gelar).
2. **Solo MMR Ladder** (hanya 1v1) — rank sejati, tier Bronze→Mythic.
3. **Kolektif** — Faction standing + Guild standing.

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

## 4. Guild War — Fase 3
- Squad vs squad (3v3/5v5) → Guild Score → Guild Board ("Top Squad", doc 16).
- Menggantikan sebagian peran "Squad War perebutan distrik" (doc 16): **Guild War = pertandingan terjadwal**; perebutan distrik Plaza tetap sebagai lapisan world-cosmetic opsional.

## 5. Mode Survival/Elimination — 10 ronde
- **Format: first-to-6 (best of 10).** Tidak selalu 10 ronde penuh → durasi terbatas.
- ⚠️ Pemain ter-KO menganggur: ronde dibuat **cepat**; pemain mati bisa **spectate tim**. Antar-ronde singkat.
- Berlaku untuk 1v1 Solo Ranked dan mode tim Survival.

## 6. Relic (Relix) — zona co-op ramai (DIPERLUAS)
- Dulu: PvE 1–4. **Baru: zona co-op bersama** dengan banyak pemain (nuansa LostSaga).
- ⚠️ **Bottleneck server (kritis):** combat 60 Hz otoritatif untuk banyak pemain + monster = berat, mengganggu target ≥20 match/vCPU, dan magnet bot-farming.
- **Keputusan:** cap **8–12 pemain per instance Relic**, tetap di game server + Core, encounter didesain untuk jumlah itu. Bukan open-world tanpa batas.
- Loot/chest **server-authoritative** (seperti gacha); masuk pakai Gold (standar) / Ticket (peti + pity). Anti-AFK + rate-limit drop.
- Monster = bot input ke Core (doc 17 §5); RNG per match ter-seed server.

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

## 10. Dampak & scope
| Item | Fase |
|---|---|
| Solo Ranked 1v1 (Glicko-2) | **MVP (Fase 2)** — 1v1 sudah jadi fokus arena MVP |
| TDM / Custom Room | Fase 2–3 |
| Survival first-to-6 | Fase 2–3 |
| Guild War + Squad Shop | Fase 3 |
| **Faction War (Orde vs Legion)** | **Fase 3+** (sistem besar) |
| Relic co-op ramai | Fase 3 |
| Chat slash-command | Fase 2 (dasar) → faction Fase 3 |

⚠️ **Catatan scope (solo + AI):** Faction War, Relic ramai, Squad Shop menambah scope. MVP tetap ketat: **1v1 + 2v2, 2 hero**. Sistem kolektif menyusul.

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
