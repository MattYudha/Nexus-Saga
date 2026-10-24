# 03 — Arah Teknis (DRAFT, belum diputuskan)

> Belum ada kode. Ini hanya opsi untuk didiskusikan.

## Kenapa tidak "langsung seperti Roblox"
Roblox memberi multiplayer, avatar, dan ekonomi gratis — tapi kita terikat Robux, aturan platform, dan tidak punya currency sendiri. Kita ingin MiCash/Gold/Ticket sendiri → butuh stack sendiri yang meniru *pola* Roblox: **Hub server + instance server + backend layanan**.

## Opsi Stack
| Lapisan | Opsi A (direkomendasikan awal) | Opsi B |
|---|---|---|
| Client | Unity (URP, low-poly/stylized) | Godot 4 |
| Netcode combat | Photon Fusion / Fish-Net (server-authoritative + client prediction) | Custom UDP |
| Backend (akun, wallet, inventory, matchmaker, leaderboard, chat, guild) | **Nakama** (open-source, sudah punya semua fitur ini) | Colyseus (TS) + Postgres custom |
| Data tables | Google Sheets / CSV → JSON di server (live-config) | DB admin panel |
| Rating | OpenSkill (tim) | Glicko-2 |

## Prinsip Arsitektur
- **Server-authoritative** untuk combat, wallet, inventory, gacha roll, MMR. Client tidak pernah dipercaya.
- Item durasi: `inventory(item_id, acquired_at, expires_at NULL=permanen)`, validasi saat dipakai + job pembersih.
- Role-based admin (lihat Developer Mode di `01`).

## Yang bergantung pada keputusan state machine
Desain state machine (frame data, hitstun, i-frames) menentukan model netcode (prediksi vs rollback), tick rate, dan format data skill. Karena itu state machine perlu dirumuskan **sebelum** memilih netcode final.
