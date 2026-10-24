# 15 — Skema Data Pemain & Ekonomi (DRAFT v0.1, 2026-10-24)

Disusun dari keputusan terkunci (`90-decision-log.md`) + riset AyoDance/LostSaga. **Desain data, bukan kode.** Skema ditulis konseptual (field + tipe); storage final menyesuaikan Nakama (lihat `14`).

Prinsip pengikat:
- Server-authoritative: semua saldo, kepemilikan, dan hasil hanya diubah server.
- Anti-P2W: kosmetik & hero tidak memberi stat tempur; MiCash tidak mempercepat progres kompetitif.
- Avatar (kosmetik) terpisah dari Hero/Gear (kit tempur).
- Semua angka (harga, durasi) = **data server**, bukan hard-code (content bundle ber-hash).

---

## 1. Player (akun)
```
Player {
  playerId            : uuid (PK)
  username            : string (unik, bisa ganti nama berbayar)
  role               : enum { Player, Mentor, Moderator, GM, Developer }   // dicek SERVER
  createdAt          : timestamp
  region             : enum { SEA, ... }
  ageVerified        : bool            // gate couple room 18+
  accountLevel       : int             // dari XP bermain — NOL efek kompetitif
  accountXp          : int             // tidak bisa dibeli
  status             : enum { Online, InPlaza, InRoom, InBattle, Offline }
  banState           : { banned:bool, until:timestamp, reason:string }   // audit
}
```
Catatan: `accountLevel` hanya membuka kosmetik/gelar/slot profil. Tidak pernah memengaruhi combat/MMR/Gold kompetitif.

## 2. Wallet & ledger
```
Wallet {
  playerId : uuid
  gold     : int      // soft; dari match/minigame/quest
  ticket   : int      // gacha
  micash   : int      // hard; dari top-up uang asli
}
LedgerEntry {           // setiap perubahan saldo tercatat (audit + anti-dobel)
  entryId, playerId, currency, delta, reason, refId (matchId/orderId), ts
  idempotencyKey : string (unik)   // cegah transaksi ganda
}
```
- 3 mata uang final (tanpa mata uang ke-4). Konten couple pakai **token relasional non-tradable** (lihat `16`), bukan currency inti.

## 3. Profil & statistik (kompetitif)
```
PlayerProfile {
  playerId
  mmr            : { [mode]: float }      // hidden, per mode (lihat 14)
  rankPoints     : { [mode]: int }        // terlihat
  tier           : enum { Bronze..Mythic } + division
  peakTier       : { [season]: tier }
  stats          : {
     wins, losses, winRate,
     kills, deaths, assists, kda,
     favoriteHeroId,
     perHero : { [heroId]: { games, wins, kda } }
  }
  matchHistory   : [ matchId... ]  (ringkas; detail di match record)
  badges         : [ badgeId... ]  // kosmetik/gelar
}
```

## 4. Hero (katalog & kepemilikan)
### 4.1 Katalog (data server, sama untuk semua)
```
HeroDef {
  heroId        : int (PK)
  name, archetype : enum { Grappler, Zoner, Support, ... }
  dataHash      : string           // combat data hero (lihat 13); wajib cocok client-server
  baseBodyType  : enum { M, F }    // shared humanoid rig
  priceGold     : int | null       // null = tidak dijual Gold
  priceMiCash   : int | null
  goldUnlockAfter : days           // hero MiCash juga bisa Gold setelah N hari (anti-P2W)
  rotationFree  : bool             // masuk rotasi gratis mingguan?
  releaseSeason : int
}
```
### 4.2 Kepemilikan
```
PlayerHero {
  playerId, heroId
  acquiredAt
  source        : enum { Gold, MiCash, Event, Rotation }
  masteryLevel  : int              // membuka KOSMETIK (border/emote/skin), bukan stat
  masteryXp     : int
}
```
- Ranked: hero cukup dimiliki ATAU sedang rotasi gratis. Tidak ada "upgrade hero" berbayar.

## 5. Gear (katalog & kepemilikan)
Gear = komponen hero (Weapon/Armor/Helmet/Trinket) yang memberi **skill**, bukan stat pasif. Lihat `08 §7`.
```
GearDef {
  gearId     : int (PK)
  heroId     : int            // gear terikat hero (shared rig untuk pickup)
  slot       : enum { Weapon, Armor, Helmet, Trinket }
  skillStateId : int          // state skill yang dibuka (data combat)
  priceGold, priceMiCash
}
PlayerGear {
  playerId, gearId, acquiredAt, source
}
```
- Dalam match: gear bisa rontok & dipungut (match-only, tidak mengubah kepemilikan — `08 §7.3`).

## 6. Kosmetik / Wardrobe (inti monetisasi)
### 6.1 Katalog item
```
CosmeticDef {
  itemId       : int (PK)            // ID numerik stabil (BUKAN nama file — pelajaran AyoDance)
  assetKey     : string              // kunci aset terpisah
  slot         : enum {              // 13 slot (riset AyoDance) + kategori baru
                  Hair, Face, Top, Bottom, Shoes, Set,
                  HandL, HandR, Back, FaceAcc, HeadAcc, Pet,
                  BadgeRing, Aura, Mount, SitEmote, FootstepFx }
  occupiesSlots : [slot...]          // Set -> [Top,Bottom]; aturan "menempati slot"
  bodyType     : enum { M, F, Unisex }
  scale        : float               // koreksi skala per item (pelajaran AyoDance)
  dyeable      : bool                // sistem Dye (color mask) — divergensi dari AyoDance
  dyeZones     : int                 // jumlah zona warna
  rarity       : enum
  giftable     : bool                // hanya item MiCash giftable (anti-farming)
  tradable     : false               // untradeable (MVP)
  prices       : [ PriceOption... ]  // lihat 6.2
  effectRef    : fxId | null         // partikel/aura (nol stat)
}
```
### 6.2 Harga & durasi (sewa + rent-to-own)
```
PriceOption {
  currency : enum { Gold, MiCash }
  duration : enum { D7, D30, Permanent }
  amount   : int
  rentToOwnCredit : int   // porsi harga sewa yang jadi kredit beli permanen (fitur pembeda)
}
```
### 6.3 Inventory pemain (dengan durasi)
```
PlayerCosmetic {
  playerId, itemId
  acquiredAt
  expiresAt : timestamp | null       // null = permanen
  dyeState  : [colorPerZone...]
  rentToOwnProgress : int            // akumulasi kredit menuju permanen
  equipped  : bool
}
```
- Validasi pakai: saat **kunci loadout** pre-match; item yang habis di tengah match tetap dipakai sampai selesai (`09 §6`).
- Job pembersih: tandai `expiresAt` lewat → unequip, bukan hapus (bisa di-recover/di-rent ulang).

## 7. Loadout (yang dibawa ke match)
```
Loadout {
  playerId
  avatar   : { [slot]: itemId }      // kostum (nol stat)
  squad    : [heroId x3]             // 3 hero (lihat 08 §6), MVP produksi 2
  gearPerHero : { [heroId]: { Weapon, Armor, Helmet, Trinket : gearId } }
}
```
Server memvalidasi kepemilikan + masa aktif semua referensi saat kunci.

## 8. Shop
```
ShopListing {
  listingId
  itemRef    : cosmeticId | heroId | gearId | ticketBundle
  prices     : [ PriceOption... ]
  category   : enum { Featured, Daily, Hero, Gear, Cosmetic, Bundle }
  rotation   : { type: enum{Permanent, Daily, Weekly, Seasonal}, until }
  giftable   : bool
}
PurchaseFlow:
  client -> RPC buy(listingId, option, [giftTargetId]) ->
  server: cek saldo -> ledger debit (idempotencyKey) -> grant item (durasi) -> catat
```
- **Gifting:** hanya `giftable` (item MiCash) → masuk "PresentBox" penerima (pelajaran AyoDance).
- **Deal harian (OneDayMarket)** = `rotation=Daily`.
- **Jual-balik ke sistem** (opsional, refund Gold kecil) seperti `DenItemReSell` — keputusan terbuka.

## 9. Gacha
```
GachaBanner {
  bannerId, name, costCurrency: Ticket|MiCash, costPerPull
  pool : [ { itemId, rarity, weight } ]
  pity : { hardPityAt: int, softPityFrom: int }     // JAMINAN (divergensi dari AyoDance)
  dupeConversion : { toCurrency: Shard, amount }
  ratesPublished : true                             // WAJIB tampil (regulasi loot box)
}
PlayerGachaState { playerId, bannerId, pullsSinceRare }
```
- Semua roll di server; rate & pity ditampilkan di UI. Tanpa slot machine.

## 10. Quest
```
QuestDef {
  questId, type: enum { Daily, Weekly, Season, Event, Achievement }
  objective : { metric: enum{ PlayMatches, WinMatches, DealDamage, UseHero, Minigame, ... }, target:int }
  reward    : [ { currency|itemId, amount, duration } ]
  resetCycle : enum { Daily, Weekly, Season, None }
  prereq    : [questId...] | null
}
PlayerQuest { playerId, questId, progress, state: enum{Active, Completed, Claimed}, cycleId }
```
- Progres divalidasi server dari event match/aktivitas (bukan lapor client).
- Battle pass (AudiPass-style) = track quest season + reward kosmetik (Fase 3).

## 11. Match record (sumber kebenaran hasil)
```
MatchRecord {
  matchId, mode, startTs, endTs, region, dataHash
  teams : [ { players:[{playerId, heroesUsed, kills, deaths, assists, koList}], score } ]
  result : { winnerTeam, mmrDelta: {playerId: delta}, rewards: {playerId: {gold, xp}} }
  reportedBy : gameServerId   // server-to-server, idempoten per matchId
}
```
- Game server (.NET) melapor ke Nakama. Client tidak pernah melapor hasil.

## 12. Keputusan terbuka
1. Jual-balik item ke sistem (refund Gold) — ada/tidak?
2. Dupe gacha → shard: shard ditukar apa (item pilihan / currency)?
3. Mastery hero kosmetik — daftar reward per level.
4. Apakah avatar kosmetik bisa tradable suatu saat (butuh market, `14`).
5. Format `dataHash` & versioning hero/gear vs content bundle.
