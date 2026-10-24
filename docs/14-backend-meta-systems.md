# 14 — Backend & Meta Systems (Nakama, 2026-10-24)

Hasil riset Nakama (dok resmi Heroic Labs) + algoritma rating. Melengkapi `09`. **Desain, bukan kode.** Sumber di bagian akhir.

Fakta lintas-sistem (penting): Nakama **tidak punya** role/RBAC in-game, **tidak punya** mute, dan **tidak punya** "room" sebagai objek. Ketiganya kita bangun di atas storage, match label, dan RPC. Sisanya memetakan erat ke primitive Nakama.

Tiap sistem: **Nakama sediakan / Kita bangun / Rekomendasi**.

---

## 1. Auth & sesi
- **Nakama:** device/email/custom/social auth (Apple, Google, Steam), link banyak metode ke 1 akun, sesi JWT + refresh, `UsersBanId` (menandai, **tidak** memutus sesi live).
- **Kita bangun:** role in-game (player/mentor/mod/GM/dev), mute, penegakan ban.
- **Rekomendasi:**
  - Mulai device auth → dorong link email/Steam (progres selamat saat ganti device).
  - Role di **account metadata** (server-write only) atau storage write=0; **setiap RPC privileged baca ulang role di server** (sesuai "otorisasi tidak pernah di client").
  - Ban = `UsersBanId` + tulis record moderasi + `SessionLogout` + `SessionDisconnect`.
  - Mute = storage `{muted_until, scope}`; di-drop di hook chat (§7).

## 2. Matchmaking
- **Nakama:** matchmaker penuh. Ticket `addMatchmaker(query, minCount, maxCount, stringProps, numericProps, countMultiple)`; query Lucene-like (`+`=must, `-`=must-not, `^n`=boost, range `>=,<=`); party via `addMatchmakerParty`; hook `RegisterMatchmakerMatched` / `Override` (tempat plug OpenSkill) / `Processor`.
- **Kita bangun:** strategi pelebaran band, **alokasi game server .NET**, join ticket.
- **Rekomendasi:**
  - `{mode, region}` = string props; `{mmr, partySize}` = numeric. 5v5 → `minCount:10, maxCount:10` atau `countMultiple:10`.
  - **Pelebaran:** submit ticket baru dengan band MMR lebih lebar (±100 → ±200 → ±400 → region tetangga sebagai SHOULD); andalkan `max_intervals` untuk fallback ukuran.
  - **Jangan** buat authoritative match Nakama untuk pertarungan. Di `RegisterMatchmakerMatched` → panggil **Allocator** (S2S) → kirim notifikasi berisi `{matchId, ip, port, joinToken}` → client UDP ke server .NET.
  - **Backfill:** Nakama tidak punya primitive resmi (flagged) → tangani drop via toleransi ronde atau RPC top-up targeted; jauhkan dari ranked.

## 3. MMR / rating — **OpenSkill (Plackett-Luce)**
- **Perbandingan:** Elo (1v1, adaptasi tim ad-hoc), Glicko-2 (punya RD/volatility tapi fundamentalnya pairwise), **OpenSkill** (Bayesian, lisensi bebas, **native multi-tim**, ada port **.NET: OpenSkillSharp**).
- **Rekomendasi:** OpenSkill model Plackett-Luce.
  - **Hidden MMR** = `{mu, sigma}` per pemain (default mu=25, sigma≈8.33); matchmaking pakai **ordinal = mu − 3·sigma**.
  - **Rank Points (RP) terlihat** = angka terpisah → Bronze–Mythic; monoton (menang +RP, kalah −RP, skala gap MMR). Simpan RP di **leaderboard** (§5), `{mu,sigma}` di **storage**.
  - **Placement:** sigma tinggi di awal → ±10 game update besar → ungkap tier.
  - **Soft reset musiman:** `mu' = mean + (mu−mean)·k` (k≈0.5–0.7), sigma di-inflasi ulang; RP reset via jadwal leaderboard.
  - **Party:** rate tim apa adanya; premade vs solo → bias di `RegisterMatchmakerOverride`, bukan merusak mu/sigma.
  - **Decay:** job terjadwal naikkan sigma / trim RP untuk akun tier tinggi tak aktif.
- **Di mana jalan:** **hanya dari laporan game server** (bukan client). Game server .NET POST ke **RPC server-to-server** Nakama (auth runtime HTTP key, tanpa user context), **idempoten per matchId**. Math rating di Go (port Weng–Lin ~100 baris) atau layanan .NET tipis (OpenSkillSharp); paling sederhana di RPC Go.

## 4. Lobby / room
### (a) Plaza
- **Nakama:** **authoritative match** (`match_init/join_attempt/join/loop/leave/terminate`) cocok untuk hub 30–60 pemain (sudah di `09 §4.1`, 10–15 Hz, gerak client-authoritative + cek kewajaran).
- **Kita bangun:** logika handler (posisi avatar, emote, interest management), sharding saat penuh.

### (b) Custom room ala LostSaga
- **Nakama:** authoritative match punya **label** string yang **queryable** via `listMatches(limit, authoritative, label, minSize, maxSize, query)`. Inilah mekanisme daftar room — tanpa entitas "room" terpisah. `match_join_attempt` = tempat cek password/kapasitas/sudah-mulai.
- **Rekomendasi:** 1 custom room = 1 authoritative match. Label (queryable) berisi field yang bisa di-browse; password hash di state privat (bukan di label).
```
label(JSON): { name, mode, size, hasPassword, state:"waiting|starting|in_battle", players, region }
state privat: { passwordHash, teams, ready, leaderUid }
browse: listMatches(authoritative=true, query="+label.mode:survival +label.state:waiting")
random-join: listMatches state:waiting + slot kosong → pilih satu
```
### (c) Room ↔ game server
Match Nakama (plaza/room) = **lapisan koordinasi saja**. Saat match terbentuk / leader tekan Start → Nakama panggil **Allocator** (S2S) → `ip:port` fleet .NET → join ticket → pemain pindah dari lobby Nakama ke server dedicated. Combat tidak pernah di Nakama.

## 5. Leaderboard
- **Nakama:** leaderboard & tournament first-class. Create (server): id, authoritative, sort DESC/ASC, operator set/best/incr, **reset CRON**, metadata (immutable setelah dibuat). Owner record bisa **user ID ATAU group ID** (→ board squad). List: by score (cursor), by owner IDs (friends/squad), **around-owner**. Reset callback = tempat grant reward musiman. Tournaments/Leagues = promosi/degradasi tier (cocok Bronze→Mythic).
- **Rekomendasi:**
  - Ranked ladder: authoritative, DESC, operator **set** (RP dihitung ulang tiap game), reset CRON per season.
  - Per-mode board: `rank_survival_s1`, `rank_tdm_s1`.
  - **Top Squad:** leaderboard owner = **group/guild id**; tulis skor agregat squad dari job terjadwal.
  - "Your rank" UI = around-owner.

## 6. Sosial
- **Nakama:** Friends (state 0=teman, 1=terkirim, 2=diterima, 3=blokir), block (diam-diam), DM persisten, Notifications (`code>0` untuk kita, persistent/transient), Parties (`CreateParty`, maxSize s/d 256, auto-promote).
- **Kita bangun:** notifikasi undangan party (custom code), kebijakan whisper non-teman, enrich presence friends.
- **Rekomendasi:** Friends+block dari Nakama; presence via status stream (tulis "plaza"/"battle"/"room:<id>" saat ganti state); undangan party = notifikasi `code>0` persisten berisi `partyId`.

## 7. Chat
- **Nakama:** 3 tipe channel: **1=Room** (publik, by name), **2=DirectMessage** (pair privat), **3=Group** (anggota, by group id); `persistence` (history), `listChannelMessages`. **Hook moderasi `ChannelMessageSend`** (before-RT) bisa **tolak/sanitasi**; dok sarankan library **go-away** untuk filter kata kasar.
- **Kita bangun:** taksonomi channel, filter kata kasar server, rate limit, penegakan mute.
- **Rekomendasi — pemetaan channel:**
  - Room → global (`global`), plaza-local (`plaza:<shard>`), custom-room (`room:<matchId>`)
  - Party → `SendPartyData` atau Room `party:<id>`
  - Guild → Group channel (type 3)
  - Whisper/DM → DirectMessage (type 2)
  - Semua filter + rate limit + mute di **satu hook** `ChannelMessageSend` (cek mute §1 → token-bucket rate limit → go-away → cek block). RPC GM role-gated untuk mute/kick + audit log.

---

## Peta ke sistem yang diminta user
| Permintaan user | Jawaban |
|---|---|
| matchmaking | §2 (Nakama matchmaker + widening + allocator) |
| multiplayer system | §4 Plaza/room (Nakama) + game server .NET (`08/09`) |
| mmr system | §3 (OpenSkill) |
| lobby system / random lobby / room ala LostSaga | §4b (match label + listMatches) |
| leaderboard | §5 |
| player profile | `15 §3` |
| player hero / gear | `15 §4–5` |
| shop schema | `15 §8` |
| quest | `15 §10` |
| chat / friends / messenger | §6, §7 |
| guild war / squad list / top squad / community lobby | `16` |
| list hero / training / bot | `17` |

## Keputusan terbuka
1. Rating di Go (port Weng–Lin) atau layanan .NET (OpenSkillSharp)? (rekomendasi: Go, satu sumber kebenaran)
2. Pakai Tournaments/Leagues bawaan untuk tier, atau leaderboard + mapping tier sendiri?
3. Strategi backfill final (toleransi ronde vs top-up RPC).
4. Self-host Nakama (Docker) vs Heroic Cloud (biaya).

## Sumber (dok resmi)
Nakama: Matchmaker, Query Syntax, Authentication, Friends, Chat, Notifications, Parties, Leaderboards, Tournaments, Server-to-Server RPC (heroiclabs.com/docs). Rating: OpenSkill (JOSS paper), OpenSkill README, OpenSkillSharp (NuGet).

### Catatan ketidakpastian (dari agen)
- Backfill: tak ada primitive resmi → verifikasi per versi.
- Field presence di friend list tak terdokumentasi → baca via status stream.
- Aturan code notifikasi kontradiktif di dok → pakai `>0` untuk aman.
- Party invite: tak ada fungsi bawaan → custom notifikasi.
- Query tipe numerik di label → konfirmasi indexing saat implement.
- Angka akurasi OpenSkill = benchmark self-reported; dipilih karena dukungan multi-tim, bukan kemenangan benchmark atas Glicko-2.
