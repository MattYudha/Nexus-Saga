# 09 — Arsitektur Sistem (DRAFT v0.1, 2026-10-24)

Cakupan: engine client, backend, cara berbagi Combat Core antara client dan server, dan alur Lobi → Match → kembali.
Status: **usulan, menunggu keputusan** (lihat §9).

---

## 1. Syarat yang mengikat pilihan
Diturunkan dari keputusan sebelumnya (01, 06, 08):
1. Combat Core deterministik **dijalankan di server dan di client** (prediksi). Bahasa harus sama di keduanya.
2. Server-authoritative; 10 pemain per match; 60 Hz.
3. Inti monetisasi = **avatar & wardrobe** (AyoDance), jadi pipeline karakter 3D, rangka humanoid, dan ganti kostum harus kuat.
4. PC dulu, **mobile nanti**.
5. "Update terus": balancing dan konten tanpa patch store bila memungkinkan.
6. Hub sosial 30–60 pemain per instance (Plaza), chat, party, guild, ekonomi 3 mata uang.

## 2. Engine client
| Kriteria | Unity (C#) | Godot 4 .NET (C#) | Unreal (C++) |
|---|---|---|---|
| Berbagi Core C# dengan server .NET | ✅ | ✅ | ❌ (C++; Core harus ditulis C++) |
| Pipeline avatar/wardrobe, retarget humanoid | ✅ Paling matang | ⚠️ Ada, ekosistem lebih kecil | ✅ Matang, tapi berat |
| Mobile nanti | ✅ Matang | ⚠️ C# di mobile lebih muda — cek status terkini sebelum memutuskan | ⚠️ Berat untuk mobile low-end |
| Asset store / tenaga kerja | ✅ Terbesar | ⚠️ Lebih kecil | ✅ |
| Berat di PC dev (GTX 1650, 16 GB) | OK | Sangat ringan | Berat |
| Lisensi | Proprietary (berbayar di atas ambang pendapatan) | MIT, gratis | Royalti di atas ambang |

**Rekomendasi: Unity.** Alasan utamanya adalah syarat #3 dan #4. Wardrobe dan retarget humanoid adalah jantung monetisasi, dan Godot paling lemah justru di area itu.

Godot tetap layak bila prioritasnya lisensi open-source dan tim nyaman membangun tooling avatar sendiri.

## 3. Pola berbagi Combat Core
```
NexusSaga.Core   (C# murni, netstandard2.1, TANPA referensi Unity)
 ├─ FixedMath        fixed-point, vektor, yaw
 ├─ Sim              tick pipeline, state machine, HitDef, collision sederhana
 ├─ Loadout          gear, hero swap, critical
 ├─ Data             skema data hero + loader (biner)
 └─ Net              format input/snapshot, delta, quantize

Dipakai oleh:
 ├─ Unity Client  → prediksi + render (via DLL atau package lokal)
 └─ Game Server   → .NET 8 console app (tanpa Unity!)
```
Aturan wajib supaya pola ini berhasil:
1. **Core tidak boleh menyentuh Unity API** (tidak memakai `UnityEngine`, PhysX, atau Animator). Inilah yang memungkinkan game server berupa console app .NET biasa: ringan, murah, dan bisa menampung banyak match per proses.
2. **Fisika arena dibuat sendiri** di Core: kapsul karakter, lantai/dinding/DropZone sebagai bentuk sederhana. Level designer membuat arena di Unity, lalu tool mengekspor collider-nya ke data Core.
3. **Tanpa root motion.** Gerak berasal dari Core. Unity hanya **men-sample animasi** berdasarkan (animId, frame) dari state Core, memakai Playables atau sampling manual, bukan Animator state machine.
4. Satu repo, satu set test. Test determinisme: simulasi dari input yang sama dua kali → checksum identik.

Catatan kritis — fixed-point vs float:
- Server-authoritative + koreksi snapshot **tidak menuntut** determinisme bit-exact lintas CPU (itu syarat lockstep). DDNet memakai float + quantize.
- Fixed-point tetap direkomendasikan karena memberi **replay dari input** dan **validasi ulang match di server** (anti-cheat, sengketa).
- Biayanya: tidak bisa memakai physics engine bawaan. Ini sejalan dengan aturan #2.

## 4. Backend
### 4.1 Pembagian tanggung jawab
| Layanan | Isi | Usulan |
|---|---|---|
| **Meta backend** | Akun/login, role (player/GM/dev), friends, party, guild/squad, chat, matchmaker, leaderboard, wallet 3 mata uang, inventory + `expires_at`, gacha, toko | **Nakama** (open-source, Go runtime — Go sudah terpasang) + PostgreSQL |
| **Plaza / Rest Room** | 30–60 avatar bergerak, emote, chat lokal | Nakama **authoritative match** (Go), 10–15 Hz. Gerak client-authoritative dengan cek kewajaran di server (tanpa combat) |
| **Game server** | Combat 10 pemain, 60 Hz, UDP | .NET 8 console + Core + **LiteNetLib** (UDP, MIT) |
| **Alokator server** | Memilih/menyalakan proses game server | MVP: alokator sederhana (pool proses di 1 VPS). Skala: Agones (Kubernetes) |
| **Konten (CDN)** | Data hero/balancing, bundle aset kosmetik | Addressables + CDN, versi bertanda hash |
| **Admin/GM** | Panel developer, audit log | Nakama console + RPC khusus ber-role |

### 4.2 Alternatif yang dipertimbangkan
| Opsi | Kenapa tidak (untuk sekarang) |
|---|---|
| Backend custom ASP.NET | Satu bahasa (C#), tapi friends/party/chat/matchmaker/leaderboard/wallet harus dibangun sendiri. Itu berbulan-bulan untuk fitur yang Nakama sudah punya |
| Photon Fusion untuk combat | Netcode-nya sendiri bertabrakan dengan desain tick & HitDef kita; mode server butuh Unity headless; biaya per CCU |
| **Photon Quantum** | **Alternatif serius**: engine deterministik predict-rollback yang dirancang untuk brawler. Bisa memangkas pekerjaan netcode berbulan-bulan. Minus: vendor lock-in, biaya, kontrol lebih sedikit. **Dijadikan rencana cadangan** bila spike netcode (§8) gagal |
| Combat di Nakama runtime | Runtime Nakama = Go/TS/Lua, tidak bisa menjalankan Core C# |

## 5. Data & "update terus"
Ada **konflik** yang harus diakui: client butuh data hero yang **persis sama** dengan server untuk prediksi. Mengubah balancing di server saja akan membuat prediksi client salah.

Solusi:
- Data hero/balancing = **content bundle bertanda hash**, diunduh client dari CDN saat login (bukan dikompilasi ke dalam build).
- Konfigurasi match menyertakan `dataHash`; client dengan hash berbeda wajib update sebelum join.
- Hasilnya: balancing dan hero baru bisa dirilis **tanpa update store**. Update store hanya untuk perubahan kode Core atau engine.
- Format: authoring JSON (mudah di-diff dan di-review) → dikompilasi ke biner untuk runtime. Tabel ekonomi (harga, drop rate, event) tetap di Nakama storage, server-side penuh.

## 6. Alur Lobi → Match → Kembali
```
[Login] ─► Nakama auth ─► unduh content bundle (cek hash)
   │
   ▼
[Plaza instance] (Nakama authoritative match, gaya AyoDance)
   │  avatar jalan, chat, emote, party dibentuk di sini
   │
   ├─(A) Ranked/Quick: Battle Gate → leader party masuk antrean
   │        Nakama matchmaker {mode, mmr, partySize, region}
   │
   └─(B) Custom Room (gaya LostSaga): daftar room → buat/gabung → slot tim → ready
            room = label match di Nakama
   │
   ▼
[Match terbentuk] ── hook server (Go) ──► Alokator: minta game server
   │                                     ◄── alamat IP:port + matchId
   ▼
[Pre-match / Loadout] (± 30 detik, state di Nakama)
   │  pilih 3 hero; server memvalidasi kepemilikan & sewa (expires_at) SAAT KUNCI
   │  kosmetik yang dipakai dikunci (id saja)
   ▼
[Tiket join] Nakama menerbitkan token bertanda tangan (matchId, userId, loadout, TTL pendek)
   │  client pre-load arena + bundle kosmetik 10 pemain
   ▼
[Game server] client UDP connect + tiket → server verifikasi tanda tangan
   │  match 60 Hz; status pemain di Plaza = "In Battle"
   ▼
[Akhir match] game server → Nakama (server-to-server, berautentikasi):
   │  hasil, statistik, KDA, durasi  — idempoten per matchId
   │  Nakama: update MMR/rank, Gold, statistik profil, riwayat match
   ▼
[Kembali ke Plaza] (instance baru atau sama) + layar hasil
```
Aturan keamanan:
- **Reward dan MMR hanya dari laporan game server**, tidak pernah dari client.
- Transaksi wallet di Nakama memakai ledger + idempotency key (matchId / orderId).
- Reconnect: tiket diterbitkan ulang dalam jendela mis. 60 detik; slot pemain ditahan.
- Item sewa yang habis **di tengah match** tetap dipakai sampai match selesai (dicek hanya saat kunci loadout).

Catatan kritis untuk kosmetik di match: 10 pemain × kostum + gear + skin bisa membengkakkan waktu loading dan memori, terutama untuk mobile nanti.
- Batasi jumlah layer per avatar.
- Siapkan LOD kosmetik.
- Pre-load selama fase loadout.

## 7. Topologi deployment (MVP → skala)
| Tahap | Setup |
|---|---|
| Dev lokal | Nakama + Postgres (Postgres lokal sudah jalan; Nakama via Docker atau biner), game server .NET lokal |
| Playtest tertutup | 1 VPS region Asia Tenggara (Jakarta/Singapura): Nakama + Postgres + N proses game server |
| Rilis | Nakama cluster / managed; game server fleet (Agones) multi-region; CDN konten |

## 8. Risiko terbesar & mitigasi
| Risiko | Mitigasi |
|---|---|
| **Netcode custom** adalah bagian paling sulit dan paling berisiko | **Spike 2–3 minggu** sebelum produksi: 2 kapsul saling pukul lewat jaringan, latensi simulasi 150 ms, 60 Hz, prediksi + lag compensation. Kriteria lolos ditetapkan di awal. Gagal → evaluasi Photon Quantum |
| Ukuran tim vs cakupan (Unity + Core + Nakama + server + tooling) | Vertical slice ketat (04 §D); fitur sosial memakai bawaan Nakama |
| Rangka humanoid bersama (P1/P2) membatasi desain hero | Diputuskan sejak awal; body type standar |
| Data client/server tidak sinkron | Hash konten wajib di setiap match |

## 9. Keputusan yang dibutuhkan
1. Engine client: **Unity** (usulan) atau Godot?
2. Backend meta: **Nakama** (usulan) atau custom?
3. Combat: **Core C# sendiri + spike** (usulan) atau langsung Photon Quantum?
4. Ukuran & pengalaman tim (solo / 2–5 / lebih)? Ini memengaruhi semua pilihan di atas.
5. Patch combat G1–G2, S1–S5, C1–C4, P1–P3 (`08`).
