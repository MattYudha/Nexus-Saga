# 16 — Squad / Guild, Guild War & Komunitas (DRAFT v0.1, 2026-10-24)

Disusun dari keputusan terkunci + riset AyoDance (guild "Fam" mendalam) + LostSaga (guild/war). **Desain data, bukan kode.** Storage menyesuaikan Nakama groups (lihat `14`).

Prinsip: fitur sosial = retensi; semua reward kolektif **nol stat kompetitif** (kosmetik, Gold, akses); moderasi & anti-abuse sejak awal.

---

## 1. Squad (guild)
> Istilah: **Squad** = guild/clan. (Menghindari bentrok dengan "party" = tim match sementara.)
```
Squad {
  squadId      : uuid (PK)
  name, tag    : string (tag pendek, unik)
  emblem       : { icon, colorPrimary, colorSecondary }   // kosmetik
  level        : int            // dari aktivitas anggota (nol efek tempur)
  xp           : int
  createdAt, ownerId
  description, recruitMessage
  memberCap    : int            // naik seiring level squad
  joinPolicy   : enum { Open, Request, InviteOnly }
  regionTag    : enum
  bank         : { gold:int }   // kas squad (opsional)
}
SquadMember {
  squadId, playerId
  rank : enum { Owner, Officer, Veteran, Member, Recruit }
  joinedAt, contributionPoints
}
```
Peran & izin: Owner/Officer kelola anggota, mulai war, atur HQ. (Tiru struktur "Fam" AyoDance tapi **tanpa channel berbayar** — itu P2W sosial.)

## 2. Squad HQ (markas)
```
SquadHQ {
  squadId
  layoutId
  furniture : [ { itemId, pos, rot } ]   // dekorasi kosmetik (Roblox-lite), nol stat
  trophies  : [ warTrophyId... ]         // hasil war mingguan
}
```
- Furnitur dibeli pakai Gold/kas squad; kosmetik murni.
- Absensi (roll book, pelajaran AyoDance): check-in harian anggota → contribution points + Gold kecil.

## 3. Squad War (mingguan)
Tujuan: memperebutkan distrik di Plaza; pemenang mengubah tampilan distrik + bonus komunitas (`01`, `04`).
```
WarSeason { warId, weekOf, state: enum{ Signup, Active, Settled } }
WarDistrict {
  districtId, name
  controllingSquadId : uuid | null
  cosmeticState : { flag, color, statue }   // berubah sesuai pemenang
}
WarMatch {
  warId, districtId, squadA, squadB, scheduledTs
  format : enum { Squad5v5, Relay, Leader Duel }
  result : { winnerSquadId, score, mvpPlayerId }
}
WarReward {
  perWinningMember : { gold, warToken, cosmeticChance }
  squad : { xp, trophy, districtControlDays }
}
```
Aturan penting:
- Reward war = Gold + token kosmetik + badge. **Tidak ada stat tempur.**
- Kontrol distrik memberi **diskon toko / bonus Gold** untuk anggota (ekonomi, bukan power).
- Matchmaking war berdasarkan level/rating squad agar adil.
- **Leader Duel**: ketua vs ketua, ditayangkan di layar Plaza (momen tontonan).

## 4. Leaderboard squad ("Top Squad")
```
SquadLeaderboard (per season) {
  metric : enum { WarWins, DistrictDays, TotalContribution, SquadLevel }
  entries: [ { rank, squadId, score } ]
  reset  : seasonal (soft)
}
```
- Ditampilkan di Community Lobby + papan di Plaza.
- Pakai Nakama leaderboard/tournament (lihat `14 §5`).

## 5. Community Lobby
Ruang komunitas skala besar (bukan arena): papan Top Squad, pengumuman, event aktif, rekrutmen squad, spectate Leader Duel/war final di layar besar.
```
CommunityBoard {
  topSquads     : [leaderboard entries]
  featuredEvents: [eventId...]
  recruitingSquads : [squadId...]  // squad membuka rekrutmen
  liveSpectate  : [ { warMatchId / duelId } ]
}
```

## 6. Mentor system
```
MentorLink { mentorId (Diamond+), menteeId, startedAt, menteeStartTier }
MentorReward { triggeredBy: menteeTierUp, mentorReward, menteeReward }   // kosmetik/Gold
```
- Membangun komunitas & onboarding (pelajaran: AyoDance punya banyak retensi sosial).

## 7. Couple / relasi (18+ untuk romantis, umum untuk friend)
Dari riset AyoDance: couple ring **nol stat**, progres relasional → kosmetik + akses sosial.
```
RelationLink {
  type : enum { Friend, Couple }       // Couple butuh keduanya ageVerified 18+
  memberA, memberB, level, relToken : int   // token non-tradable (BUKAN currency inti)
}
```
- Couple: ring berlevel (ikon makin mewah), akses Couple room/garden kosmetik, efek room. **Nol stat.**
- Wajib: block/report/mute, filter chat, dapat diputus sepihak.

## 8. Moderasi & anti-abuse (lintas sistem)
| Risiko | Penutup |
|---|---|
| Squad "farming" reward war dengan akun boneka | Matchmaking war + batas reward per akun; deteksi pola |
| Transfer kekayaan via kas squad | Kas hanya untuk furnitur HQ; tidak bisa ditarik ke wallet pribadi |
| Abuse couple/friend untuk reward | Token relasi non-tradable; cooldown ganti pasangan |
| Toxic di community/chat | Filter server + report + audit (lihat `14 §7`) |

## 9. Fase
- **Fase 3:** Squad dasar + HQ + Squad War + Top Squad + Community Lobby + Mentor.
- **Fase 3–4:** Couple/garden, absensi, boss raid squad (PvE).
- Semua butuh Nakama groups/leaderboard (`14`) + game server untuk war match.

## 10. Keputusan terbuka
1. Format war: 5v5 murni, relay (bergantian), atau campuran?
2. Berapa distrik di Plaza & berapa lama kontrol (1 minggu?).
3. Boss raid squad (PvE) — masuk Fase 3 atau 4?
4. Kas squad: aktif atau dihapus (hindari penyalahgunaan)?
