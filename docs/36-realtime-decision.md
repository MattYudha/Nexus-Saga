# 36 — Keputusan Realtime Fase 2 (Chat / Teman / Party)

> **Status: USULAN — menunggu approve user.** Tanpa implementasi. Dibandingkan: **Photon Chat**, **SignalR**, **Nakama**.
> Nakama dicatat sebagai keputusan meta-backend lama (docs/90, 2026-10-24/26) → **wajib dibandingkan ulang atau dicabut resmi** di sini.

## 1. KEBUTUHAN FASE 2 (docs/31 §2)
Presence (online/offline), **teman** (add/accept/list), **party/undangan**, **chat** (lobby/world + party; guild menyusul Fase 3). Realtime, hemat, cocok dengan stack saat ini: **ASP.NET Core (PhotonBackend.Api) + Photon Quantum/Realtime (arena)**.

## 2. KONTEKS: apa yang SUDAH ada
- Match/arena = **Photon** (Quantum 3 + Realtime room). Sudah jalan.
- Meta (auth, profil, match result, rating, leaderboard, stats, **faksi**) = **PhotonBackend.Api (ASP.NET + Postgres)**. Sudah tumbuh jauh melampaui "Pong-spesifik".
- Keputusan lama (docs/90): meta sosial (party/guild/chat/shop/wallet) = **Nakama**. **Belum** diimplementasi; ASP.NET sudah mengambil alih sebagian (auth/leaderboard/stats).

## 3. OPSI

### A. Photon Chat
- **Apa**: layanan pub/sub chat SaaS, vendor sama dengan Quantum/Realtime.
- **+**: setup cepat, SDK Unity sudah ada, presence & channel bawaan, skala ditangani vendor, satu vendor dengan arena.
- **−**: **hanya chat/presence** — teman & party TETAP harus di backend sendiri (ASP.NET). Biaya per-CCU terpisah dari Realtime. Riwayat chat terbatas (bukan sumber kebenaran; harus persist sendiri bila perlu). Lock-in vendor.
- **Cocok untuk**: chat + presence cepat; sisanya (teman/party) tetap di ASP.NET.

### B. SignalR (di PhotonBackend.Api)
- **Apa**: hub realtime WebSocket di ASP.NET yang SUDAH ada.
- **+**: **satu backend, satu auth (JWT yang sudah ada), satu DB** → teman/party/chat jadi satu sistem konsisten; kendali penuh (riwayat, moderasi, rate-limit); tanpa vendor/biaya tambahan; reuse TokenService + EF Core.
- **−**: kita yang urus **scale-out** (butuh backplane mis. Redis bila >1 replika), presence manual, reconnect/transport sendiri. Beban ops & kode lebih banyak.
- **Cocok untuk**: integrasi paling rapat dengan sistem akun/faksi yang sudah dibangun; skala awal–menengah.

### C. Nakama (keputusan lama)
- **Apa**: server sosial open-source lengkap — chat, teman, party, presence, storage, matchmaking, (wallet/inventory).
- **+**: fitur sosial **paling lengkap out-of-the-box**; satu sistem untuk teman+party+chat+guild; skala teruji.
- **−**: **server terpisah** (ops: deploy, DB sendiri, upgrade) → **dua sumber identitas** (Nakama vs ASP.NET yang sudah pegang akun/rating/faksi) → perlu sinkronisasi/menyatukan auth. Sebagian perannya **sudah diambil** ASP.NET → tumpang tindih. Kurva belajar (runtime Lua/Go).
- **Status**: karena ASP.NET sudah jadi sumber kebenaran akun/kompetitif, mengadopsi Nakama sekarang = **duplikasi identitas**. Pilihan jujur: **cabut Nakama** untuk meta sosial inti, ATAU pakai Nakama HANYA untuk lapisan dunia besar (Plaza/Excavation 20–50 pemain, docs/90 2026-10-26) dan BUKAN untuk auth/teman.

## 4. RINGKAS BANDING
| | Photon Chat | SignalR | Nakama |
|---|---|---|---|
| Cakupan fitur | chat+presence | semua (kita bangun) | semua (bawaan) |
| Satu auth/DB dgn akun+faksi | tidak | **ya** | tidak (sinkron) |
| Beban ops | rendah (SaaS) | sedang | tinggi (server+DB) |
| Biaya | per-CCU vendor | infra sendiri | infra sendiri |
| Lock-in | vendor | rendah | rendah |
| Kontrol (riwayat/moderasi) | terbatas | **penuh** | penuh |

## 5. ARAH (usulan, belum dieksekusi)
- **Condong ke SignalR** untuk teman+party+chat Fase 2: menyatu dengan akun/JWT/faksi yang sudah ada, tanpa vendor/identitas kedua; tambah Redis backplane saat perlu scale-out. Photon Chat = alternatif bila ingin presence/chat instan tanpa bangun hub.
- **Nakama**: untuk meta sosial inti **dicabut** (digantikan ASP.NET). Dipertahankan hanya sebagai kandidat lapisan **dunia besar non-combat** (Plaza/Excavation) bila/ketika fitur itu digarap — keputusan terpisah, bukan Fase 2.

## 6. KEPUTUSAN
_Menunggu pilihan user._ Setelah dipilih → update docs/90 (cabut/leksikografi Nakama) + mulai spike kecil. **Tanpa kode sampai disetujui.**
