# 02 — Matriks Game Referensi (DRAFT v0.1, 2026-10-24)

Prinsip: pakai metode riset **termurah yang cukup**. Reverse engineering biner hanya bila informasinya tidak tersedia secara publik/observasi.

| Komponen | Referensi | Yang diambil | Metode riset terbaik |
|---|---|---|---|
| Lobi sosial & avatar | Audition/AyoDance, LostSaga, Roblox | Struktur slot avatar (rambut, wajah, atasan, bawahan, sepatu, aksesori), emote, sinkronisasi posisi di room | Observasi + data tabel client (jika diberikan) + dokumentasi Roblox (avatar API publik) |
| Combat & state machine | LostSaga | State (Idle, Run, Dash, Attack, Airborne, Down, Faint/Stun, Bound, Frozen, Get-up invincible), transisi, hitstun/knockback, swap gear | **Ini paling berharga untuk dibedah** — tabel data/ini client + observasi frame-by-frame rekaman video |
| Matchmaking MMR | Dota 2, MLBB, LoL, Valorant | Hidden MMR vs rank points, party handling, placement, decay | **Bukan RE.** Biner server mereka tidak tersedia. Algoritmanya publik: Elo, Glicko-2, TrueSkill, **OpenSkill** (open-source, cocok tim) |
| Durasi item & gacha | LostSaga, Genshin, Roblox | Sewa 7/30 hari/permanen, pity, dupe conversion | Desain sendiri (pola `expires_at` server-side sudah standar); referensi tabel drop LostSaga untuk inspirasi angka |
| Hub & instance | Roblox, Fortnite, GTA RP | Hub kecil + instance match, server per room | Dokumentasi publik engine/backend |
| Komunitas & war | LostSaga (guild), Clash of Clans (clan war), Albion (territory) | Siklus war mingguan, reward kolektif | Wiki/komunitas + observasi |
| Rest room/minigame | Audition, Club Penguin, Animal Crossing | Ritme singkat, fishing, kuis, ruang sosial | Observasi |
| Live-ops & economy | Fortnite, Roblox, Valorant | Battle pass, shop rotation, anti-P2W | Postmortem/GDC talks publik |

## Catatan Legal / Etika
- Menganalisis client yang Anda miliki untuk **memahami desain** umumnya dapat diterima; **menyalin** kode, aset, nama, atau data tabel mentah ke game sendiri tidak. Hasil riset kita ditulis ulang sebagai spesifikasi sendiri.
- Kita tidak menyentuh server resmi, tidak membuat cheat, dan tidak mendistribusikan file hasil ekstrak.

## Template Hasil Bedah (`research/<sistem>-<game>.md`)
1. Sumber (file/path, versi, metode)
2. Temuan (struktur data, state, angka)
3. Apa yang kita adopsi / ubah / buang
4. Spesifikasi versi Nexus Saga
