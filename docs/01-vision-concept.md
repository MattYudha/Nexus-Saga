# 01 — Visi & Konsep (DRAFT v0.1, 2026-10-24)

## Genre
Social-Competitive Action RPG Hybrid. "Avatar = diri player" (Audition/AyoDance, GTA RP) + brawler skill-based (LostSaga) + kompetitif MMR/Tier + live-ops kosmetik non-P2W (Roblox/Fortnite).

## 5 Pilar Desain
1. **Avatar adalah identitas.** Avatar yang sama dipakai di lobi, rest room, dan arena. Uang dibelanjakan untuk *tampil*, bukan *menang*.
2. **Skill > dompet.** Semua yang memengaruhi kemenangan bisa didapat lewat bermain (Gold). Cash hanya mempercepat atau mengubah tampilan.
3. **Dunia yang hidup tapi ringan.** Hub kecil (plaza/kota) + instance terpisah untuk match. Bukan MMO open-world berat.
4. **Komunitas sebagai konten.** Squad/guild, rest room, event komunitas, perebutan wilayah — player menjadi konten satu sama lain.
5. **Update terus tanpa patch berat.** Konten (item, hero balance, event, drop rate) digerakkan oleh *data tables* di server, bukan hard-code.

## Struktur Dunia
```
[Login] → [Plaza Hub (kota, 30–60 player/instance)]
              ├─ Battle Gate  → Lobby Room (gaya LostSaga) → Arena Match
              ├─ Relic Gate   → PvE Relic Dungeon (farming)
              ├─ Rest Room    → Social rooms + minigames
              ├─ Shop / Gacha / Wardrobe
              └─ Squad HQ     → Squad War (mingguan)
```
- **Pemisahan penting:** *Avatar* (tubuh/kostum, kosmetik) ≠ *Hero/Gear Set* (kit tempur). Seperti LostSaga: kostum terpisah dari "mercenary". Ini kunci agar kosmetik tidak menyentuh stat.

## Mode Permainan
| Mode | Format | Tujuan |
|---|---|---|
| Casual Battle | 1v1, 2v2, 3v3, 5v5, FFA | Latihan, Gold |
| Ranked | Solo/Duo/Trio/Full party 5 | MMR & Tier |
| Leader Duel | Leader 1v1 mewakili squad | Gengsi, momen tontonan |
| Squad War | Squad vs squad, mingguan | Wilayah di Plaza → bonus komunitas |
| Relic (PvE) | 1–4 player | Farming material/avatar/relic |
| Rest Room | Bebas | Ngobrol, kenalan, minigame, Gold kecil |

## Kompetitif
- **Tier:** Bronze → Silver → Gold → Platinum → Diamond → Mythic (+ Mythic Leaderboard Top 100). Masing-masing 3–5 divisi.
- **Dua angka berbeda:** *Hidden MMR* (untuk matchmaking, rating Bayesian tim) dan *Rank Points* yang terlihat (untuk progres & emosi). Ini standar industri dan mencegah frustrasi.
- **Profil:** win rate, KDA, hero terfavorit, stat per hero, riwayat match, peak tier per season, badge.
- **Party fairness:** party 5 hanya melawan party ≥3; bonus/penalti MMR berdasarkan ukuran party.

## Ekonomi (3 mata uang)
| Mata uang | Sumber | Kegunaan |
|---|---|---|
| **Gold** | Match, Relic, minigame, quest harian | Hero (harga grinding wajar), sewa kosmetik 7/30 hari, masuk Relic biasa |
| **Ticket** | Quest, event, battle pass, pembelian | Gacha |
| **MiCash** | Uang asli | Kosmetik permanen, skin/efek skill, battle pass premium, hero (alternatif cepat) |

### Aturan anti-P2W (wajib)
- Hero yang dijual MiCash **juga** bisa dibeli Gold (mis. setelah 2 minggu rilis).
- Kosmetik **nol stat**. Efek skill skin tidak mengubah hitbox/timing/kejelasan visual.
- Ranked: hero hanya perlu dimiliki (atau gratis via rotasi mingguan); tidak ada "level gear" yang dibeli.
- Durasi item (7/30 hari/permanen) **hanya** untuk kosmetik dan hero trial, tidak untuk stat.

### Gacha & Relic berbayar — catatan
- Drop rate **wajib dipublikasikan** di dalam game (aturan App Store/Google Play, dan tren regulasi loot box).
- **Pity system** (jaminan item langka setelah N tarikan) + duplikat dikonversi jadi currency/shard.
- Selalu ada jalur Gold/farming untuk item yang sama atau setara (item cash-only boleh, tapi kosmetik saja).

## Developer Mode
- Bukan "backdoor di biner client." Flag `is_developer` di client bisa di-patch cheater dalam hitungan menit (justru inilah yang biasa dilakukan pada game seperti LostSaga).
- Desain yang benar: **role di server** (Player / Moderator / GM / Developer). Client hanya *menampilkan* panel jika server mengizinkan; setiap perintah (spawn item, ubah cuaca, ban, set MMR) divalidasi server dan **dicatat ke audit log**.
- Developer-only area (mis. "Dev Lounge") di Plaza hanya bisa dimasuki akun dengan role tersebut.

## Rest Room & Komunitas
- Room publik/privat, emote/pose, **Fashion Contest** (pamer outfit + voting penonton), Photo Booth, fishing, kuis, "couple room" / social matching. **Tanpa mode dance/ritme** (lihat 12).
- **Keselamatan wajib** untuk fitur kenalan/dating: verifikasi umur & age-gating, block/report/mute, filter chat, moderator. Ini bukan opsional — tanpa ini store bisa menolak game.
- Komunitas: squad (guild) dengan HQ, papan pengumuman, event dibuat komunitas, leaderboard squad.

## Live-ops (supaya "update terus")
- Season 8–10 minggu: reset soft MMR, battle pass kosmetik, hero/skin baru.
- Event mingguan rotasi (double Gold, Relic khusus, Leader Duel cup).
- Semua angka (harga, drop rate, stat hero, jadwal event) di **tabel data server** → bisa diubah tanpa update client.

