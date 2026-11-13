# 90 — Decision Log

| Tanggal | Keputusan | Status |
|---|---|---|
| 2026-10-24 | Nama kerja: **Nexus Saga: Chronicles** | Disepakati |
| 2026-10-24 | Belum coding; fase brainstorming + riset + dokumentasi | Disepakati |
| 2026-10-24 | Dokumentasi disimpan di `docs/` sebagai `.md` | Disepakati |
| 2026-10-24 | 3 mata uang: Gold / Ticket / MiCash, kosmetik nol stat, rent-to-own sebagai Gold sink utama | Disepakati |
| 2026-10-24 | Developer mode berbasis role di server + audit log; otorisasi tidak pernah di client | Disepakati |
| 2026-10-24 | Urutan riset: **Wardrobe AyoDance + format state Ikemen GO** dulu; state machine LostSaga setelah client tersedia | Disepakati |
| 2026-10-24 | Platform: **PC dulu**, mobile di fase berikutnya | Disepakati |
| 2026-10-24 | ~~Kamera arena: 2.5D side-view (seperti LostSaga)~~ — keliru: LostSaga bergerak bebas X/Z. Diganti: **arena 3D free-roam (gerak 8 arah X/Z + lompat Y), kamera quarter-view terkunci** (lihat 06) | Disepakati |
| 2026-10-24 | Ukuran tim maksimal: **5v5** | Disepakati |
| 2026-10-24 | Rating umur **13+**; couple/dating room **18+ dengan verifikasi umur** | Disepakati |
| 2026-10-24 | Riset AyoDance hanya **statis** (ada Xigncode); tidak menjalankan/attach game | Disepakati |
| 2026-10-24 | Avatar di arena: **lapisan kostum tidak pernah lepas; slot gear tempur (senjata/armor/helm/jubah) bisa rontok**; gear rontok saat kondisi kritis/HP 0; skin gear wajib patuh batas siluet hero | Disepakati |
| 2026-10-24 | MVP: **2 hero** (Melee Grappler + Ranged Zoner), mode 1v1 & 2v2 | Disepakati |
| 2026-10-24 | Tidak membongkar proteksi/packer client LostSaga (`lostsaga.exe`, `iopac.dll`); riset LostSaga ditunda | Disepakati |
| 2026-10-24 | Urutan kerja: **(a) state machine Ikemen GO → (d) arsitektur core combat** (+ tick/snapshot DDNet); AyoDance wardrobe setelah core combat | Disepakati |
| 2026-10-24 | Guard **busur depan 180°**; serangan dari belakang menembus | Disepakati |
| 2026-10-24 | Pickup gear lawan: **Helm/Armor/Trinket boleh** (siapa cepat dia dapat), **senjata tidak** | Disepakati |
| 2026-10-24 | **3 hero per match** (MVP aset 2 hero); cooldown swap **3 s** netral/combo, **12 s** defensive cancel | Disepakati |
| 2026-10-24 | HP 0 → **Critical**: pukulan berat merontokkan Helm → Trinket → Armor, lalu KO; ~~DropZone = KO langsung~~ (direvisi, lihat baris DropZone); **senjata tidak rontok sebelum KO** | Disepakati |
| 2026-10-24 | Patch: G1 **Lock Facing saat guard** + Pivot; G2 guard gauge; S1–S4; C1 3 Break Stock; C2 Break Meter; C4 **penalti gerak/dash + indikator posisi** (tanpa bleed-out); P1–P3 shared humanoid rig | Disepakati |
| 2026-10-24 | Stack: **Unity** + **Core C# murni deterministik** (tanpa UnityEngine, tanpa root motion) + **game server .NET UDP** + **Nakama**; content bundle ber-hash | Disepakati |
| 2026-10-24 | Tim: **solo architect + AI**; strategi spike berlapis (Core decoupled dari transport; Quantum sebagai cadangan) | Disepakati |
| 2026-10-24 | Hurtbox satu standar untuk semua pemain; tanpa HP dasar per hero | Koreksi konsistensi (lihat 10 B3/B4) |
| 2026-10-24 | B1 aim-assist ±22,5° saat startup + auto-face guard 6 m; B5 heal → shield, tanpa revive; B6 KO pemecah stock ke-3, assist 10 s, jatuh → musuh terakhir; S5 swap 3 s hanya netral/hit-confirm, whiff hanya bisa Burst 12 s; A1 Core data-oriented + uji Quantum; A2 predicted hit reaction = kriteria spike; A4 2 base body + hurtbox kapsul tunggal | Disepakati |
| 2026-10-24 | **DropZone bukan KO**: fall damage + kembali ke zona spawn tim + i-frame; HP di-clamp ke 0; saat Critical jatuh = pecah 1 stock. Satu-satunya jalan KO = 3 Break Stock | Disepakati (koreksi user) |
| 2026-10-24 | Aim-assist/auto-face dihitung client, `aimYaw` dikirim di input, divalidasi server (10 §E3) | Disepakati |
| 2026-10-24 | Respawn TDM berbasis waktu match (5 s → 10 s), bukan escalating per pemain | Disepakati |
| 2026-10-24 | Kriteria spike terukur (10 §E5); misprediksi = Hit-Confirm/Combat State Misprediction | Disepakati |
| 2026-10-24 | Mode MVP: **Survival/Elimination** per ronde 90–120 s (1v1, 3v3) + **TDM** | Disepakati |
| 2026-10-24 | DropZone: **Gear Ejection** ke `lastGroundedPos` + **Sky-Drop + Landing Stagger** 0,5–0,6 s | Disepakati |
| 2026-10-24 | Sky-Drop kembali ke titik lantai valid terakhir (±3 m ke dalam), tidak bisa diserang selama stagger (10 §F1) | Disepakati |
| 2026-10-24 | Masuk Critical = reset netral; setiap stock pecah = hard knockdown, maks 1 stock per combo (10 §F2) | Disepakati |
| 2026-10-24 | Tie-break ronde Elimination + target TTK diukur di prototipe (10 §F4) | Disepakati |
| 2026-10-24 | **Base model game dikunci** (dokumen 08–11) | Disepakati |
| 2026-10-24 | **Riset AyoDance dimajukan**: diselesaikan menyeluruh **sebelum implementasi apa pun** (menggantikan jadwal 'setelah core combat'). Prinsip: riset tuntas dulu, baru implementasi | Disepakati (permintaan user) |
| 2026-10-24 | Riset AyoDance statis **selesai** (2 dokumen di `docs/research/`) | Selesai |
| 2026-10-24 | Wardrobe: item mendaftar **set slot yang ditempati**; sistem **Dye** (color mask) menggantikan 'warna = item'; `itemId` numerik + `assetKey`; harga Gold & MiCash per item; skala per item; slot aksesori kepala terpisah | Usulan — menunggu konfirmasi |
| 2026-10-24 | Sosial/live-ops: event shell generik + modul per event; room sosial 6+30; outfit tersimpan + deal harian; tanpa slot machine/upgrade berbayar/mata uang ke-4 | Disepakati |
| 2026-10-24 | Observasi AyoDance manual selesai (`docs/research/ayodance-observasi.md`) | Selesai |
| 2026-10-24 | **Tetap 3 mata uang**; konten couple pakai token non-tradable, bukan mata uang inti | Disepakati |
| 2026-10-24 | **Tolak booster EXP/progres berbayar** (anti-P2W); MiCash hanya kosmetik + kenyamanan non-kompetitif | Disepakati |
| 2026-10-24 | Pet/Badge/Platform = kosmetik **nol stat**; Nexus Saga punya **rent-to-own** (AyoDance tidak) | Disepakati |
| 2026-10-24 | **TANPA mode dance/ritme** (copyright musik + biaya). Rest Room: **Fashion Contest** (pamer+vote), Photo Booth, fishing, kuis, Training/Target (reuse Core). Lihat 12 | Disepakati (permintaan user) |
| 2026-10-24 | Kosmetik **untradeable** antar pemain (MVP); **gifting** hanya item MiCash (anti-farming) | Disepakati |
| 2026-10-24 | **Account Level** dari bermain = kosmetik/profil saja, **nol efek kompetitif**; XP tidak bisa dibeli | Disepakati |
| 2026-10-24 | Couple ring berlevel = nol stat, hanya kosmetik + akses sosial (Love Party, efek room) | Disepakati |
| 2026-10-24 | Rest Room v2: hub pasif + Lobby Chase/Tag + Brawl Ball + Arcade **tanpa judi** + Fashion Contest. **Casino/slot/poker ditolak** (rating + regulasi). Masak buff hanya XP non-kompetitif. Mount Racing (nol stat) tunda Fase 3+. Lihat 12 | Disepakati |
| 2026-10-24 | Kategori kosmetik baru **dikonfirmasi** (nol stat): mount/kendaraan, emote duduk/hangout, efek pijakan/aura langkah. Dikerjakan **bertahap di akhir** setelah fungsi inti jalan | Disepakati |
| 2026-10-24 | Riset implementasi: combat data spec (13), backend Nakama (14), skema pemain/ekonomi (15), squad/komunitas (16), hero/training/bot (17) | Selesai (draft) |
| 2026-10-24 | Trigger combat = **enum-condition** (bukan bahasa ekspresi); hitbox 3D capsule/OBB; authoring JSON→biner (13) | Usulan — menunggu konfirmasi |
| 2026-10-24 | Rating = **OpenSkill (Plackett-Luce)**; hidden mu/sigma + RP terlihat; update hanya dari game server (idempoten) (14) | Usulan — menunggu konfirmasi |
| 2026-10-24 | Custom room = Nakama authoritative match + label queryable (listMatches); Plaza = authoritative match; combat tetap di game server .NET (14) | Usulan — menunggu konfirmasi |
| 2026-10-24 | Arsitektur teknis lengkap (18): FE/BE scope, skema 3D/anim/VFX, world building, scaling mobile tanpa rombak, pemakaian REA, flowchart. README diperbarui + flowchart | Disepakati (dokumen) |
| 2026-10-24 | Mobile-ready sejak awal: abstraksi input touch, UI resolution-independent, budget mobile, payment abstraction (18 §8) | Usulan — menunggu konfirmasi |
| 2026-10-24 | Koreksi arsitektur v2 (19): mesh-combine kostum + socket gear; collider Core **primitif proxy saja**; Warm-Pool Registry (+heartbeat/auth/alokasi atomik); UDP session token + migrasi **terverifikasi MAC**; input per-platform→1 struct Core; Relic di game server; snapshot tanpa kosmetik; AoI Plaza | Disepakati |
| 2026-10-24 | Pengaman: anti-replay (seq number di MAC) pada migrasi endpoint; non-blocking cosmetic fallback ke base body (19 A/B) | Disepakati |
| 2026-10-24 | **Desain arsitektur LOCKED** — stress-test cukup, tidak tambah sistem baru di atas kertas | Disepakati |
| 2026-10-24 | Spike Fase 1 = **pure .NET headless** (tanpa engine 3D); rencana detail S-00..S-14 di doc 20 | Disepakati |
| 2026-10-24 | Pipeline aset: **Claude + Blender headless (bpy)** untuk arena/collider/rig/LOD/retarget/export; MPFB2 untuk base body | Disepakati |
| 2026-10-24 | **AI-mesh-gen lokal (TRELLIS/Hunyuan) TIDAK layak di GTX 1650 4GB** → mesh organik dari cloud/marketplace/artist; Claude pasca-proses | Disepakati (koreksi realita) |
| 2026-10-24 | Engine client (Unity vs Godot 4 .NET) **ditunda**; bake-off awal Fase 2 fokus export mobile; Core/server tidak terpengaruh | Usulan — menunggu konfirmasi |
| 2026-10-24 | Spike S-12b: **Lightweight Debug Viewer** 2D (HTML5 Canvas/WebSocket) — kapsul, hitbox/hurtbox, prediksi vs snapshot; read-only, opsional (doc 20) | Disepakati |
| 2026-10-26 | **Tema: Hypebeast + Combat Exo-Gear**; cerita Nexus City; faksi Orde vs Legion; streetwear=kostum, exo-gear=gear; VFX neon-tech (doc 23) | Disepakati |
| 2026-10-26 | **Leader Duel DIHAPUS**; 1v1 jadi **Solo MMR Ladder** pribadi (rating **Glicko-2**, revisi dari OpenSkill) | Disepakati |
| 2026-10-26 | Alokasi poin per mode: Solo 1v1→MMR pribadi; F-War→Faction Board; Guild War→Guild Board; Custom Room→EXP+Gold (tanpa MMR) (doc 24) | Disepakati |
| 2026-10-26 | **Faction War (Orde vs Legion)** = sistem besar, **Fase 3+**; faksi orthogonal dgn guild; mode queue menentukan tujuan poin | Disepakati |
| 2026-10-26 | Survival = **first-to-6 (best of 10)**; pemain KO bisa spectate | Disepakati |
| 2026-10-26 | Relic diperluas jadi **zona co-op cap 8–12 pemain** (tetap game server+Core); loot server-authoritative; anti bot-farm | Disepakati |
| 2026-10-26 | Squad HQ + **Squad Shop** (furnitur + kosmetik emblem, Contribution Points, nol stat, anti transfer kekayaan) | Disepakati |
| 2026-10-26 | Chat: slash-command /all /f(squad) /w /b(broadcast cooldown+biaya) /faction; via hook moderasi | Disepakati |
| 2026-10-26 | **Fashion Contest DIHAPUS** (tidak sesuai tema); flex bergeser ke street cred + status cosmetic | Disepakati |
| 2026-10-26 | ⚠️ Scope: Faction War/Relic ramai/Squad Shop menambah beban → MVP tetap 1v1+2v2, 2 hero; kolektif menyusul Fase 3+ | Disepakati |
| 2026-10-26 | FINAL 4 jalur: Solo 1v1→Solo Ladder (Glicko-2, tier Rookie→Nexus Legend); **Squad War = District Conquest** (TIDAK dihapus, satu squad, perebutan distrik Plaza); Faction War (Orde/Legion); Street Room (Custom→EXP+Gold). Faksi ⊥ squad; antrean menentukan papan (doc 24) | Disepakati |
| 2026-10-26 | MVP = **Solo 1v1 Ladder + Street Room** saja; Squad War/Faction War/Relic → Fase 3 | Disepakati |
| 2026-10-26 | **Relic 2-lapis**: Excavation Zone 20–50 pemain di **Nakama** (ringan, tanpa combat 60Hz); Relic Rift boss **maks 8** di game server 60Hz. Rate-limit spawn Rift | Disepakati |
| 2026-10-26 | Survival = **Race-to-6 (Best of 10)**, 90s/ronde, transisi 3s, Ronde 11 sudden death bila 5-5, spectate rekan | Disepakati |
| 2026-10-26 | Squad HQ + Squad Shop pakai **Squad Cred** (dari Squad War+absen squad; tak bisa ditarik jadi Gold) | Disepakati |
| 2026-10-26 | Chat: lokal, /f (squad dari mana saja), /w (whisper), /b (broadcast cooldown + auto saat drop langka Relic/Gacha) | Disepakati |
| 2026-10-26 | Tema FINAL: **Neo-Veridia / The Exo-Drop**; ORDE=**Aegis Directorate** (Putih/Emas/Cyan), LEGION=**Vanguard Syndicate** (Hitam/Crimson/Neon Volt); hero MVP **TITAN-01** & **PULSE-X**; Exo-Gear magnetis lepas saat Critical | Disepakati |
| 2026-10-26 | VFX: Stylized Cyber-Street; **ground-ring merah=musuh/biru=kawan** untuk AoE/skill; asap dilarang tutup siluet >0,2s (baca startup + lihat gear rontok) | Disepakati |
| 2026-10-26 | RE **io3dengine.dll** selesai (research/io3dengine-lostsaga.md): simbol C++ lengkap. Memvalidasi shared-rig(RcSkeleton)+instance, bone=(pos,quat), **gear attach via LinkedSkeleton butuh bone-count sama** (= shared rig wajib), collision **OBB+Sphere TANPA capsule** | Selesai |
| 2026-10-26 | Collider FINAL: **hit/hurt = OBB+Sphere** (drop capsule); **pushbox = Upright Cylinder** (X-Z + tinggi Y, tak terpengaruh yaw, anti-nyangkut). Amandemen doc 13 §8 | Disepakati |
| 2026-10-26 | Analisis **photon-backend** (Quantum 3 scaffold user) → research/photon-backend-analysis.md. Plan-B netcode yang SUDAH JADI; room 5v5 via Photon Realtime cocok; backend minimal (bukan pengganti Nakama) | Selesai (analisis) |
| 2026-10-26 | **USULAN STRATEGIS:** balik urutan spike → **mulai dari Quantum 3** (bukan custom UDP). Jika lolos di 10 pemain → adopsi Quantum, buang custom UDP server (hemat besar solo). Otoritas via **replay re-sim backend** (sim DLL sama). Combat Core tetap desain Ikemen (OBB+sphere) diimplementasi sebagai Quantum systems | Usulan — menunggu konfirmasi |
| 2026-10-26 | **FINAL: Spike Quantum-first** (bukan custom UDP); **Unity dikunci** (bake-off Godot batal); **S-00 izin coding diberikan**. 3 aturan: (a) bone-attached OBB + **offline pose baking** ke FPVector3/Quat di Quantum Asset; (b) **split-session routing** (Photon hanya di Arena, Plaza=Nakama, hemat ~70% CCU); (c) anti-cheat **checksum + backend replay re-sim**. Target uji: 10 kapsul, OBB+Sphere, Guard 180, Critical/Gear Drop, lag 150ms, replay verify. Doc 20 revisi v2 | Disepakati |
| 2026-10-26 | **RE research DINYATAKAN SELESAI** (Ikemen/DDNet/AyoDance/io3dengine cukup) | Disepakati |
| 2026-10-26 | Spike Q-02/Q-03 diimplementasi ke **photon-backend** (Opsi A): Simulation/Nexus (Nexus.qtn + NxCombatSystem + NxHitSystem) + View/Nexus/NexusInput; Pong tak tersentuh. Butuh user jalankan CodeGen di Unity (blind-compile, mungkin 1-3 fix). Blueprint juga di spike/ | Dibuat |
| 2026-10-26 | Deep-dive io3dengine selesai (research doc §A–E). Adopsi: anti-clipping rambut via **visibility flag + whitelist** (bukan swap); **hitbox terikat bone + enable-flag per frame-window** (bukan bake per keyframe); event animasi **crossed-interval**; upper/lower split via **track-weight per-bone** (bukan layer); kamera **3-spring + occlusion pull-in**, **shake/hit-zoom client-only**; rope jiggle **substep 1/60 s** client-only | Disepakati |
| 2026-10-26 | ✅ **MILESTONE: Spike Quantum Q-03 JALAN** — kapsul gerak 8 arah (WASD) + pukul (J) kena dummy, deterministik di Quantum 3 (local play, photon-backend). Combat Core pertama terbukti di Quantum | Selesai |
| 2026-10-26 | ✅ **MILESTONE: Brawler mini Q-05 JALAN** (local): gerak 8 arah, lompat, dash i-frame, Guard 180 + crush/faint, attack + knockback, Critical 3 Break Stock + Gear Drop, dummy AI, KO/respawn — semua deterministik di Quantum 3. Combat feel terbukti | Selesai |
| 2026-10-26 | ✅ **MILESTONE: Netcode Quantum JALAN** — editor + build standalone connect via Photon Cloud, 2 pemain + dummy saling main deterministik (NexusGame, tanpa backend/auth). Spike netcode terbukti berfungsi. Bug render build (magenta, built-in RP strip Standard) diperbaiki: Unlit/Color + Always Included Shaders | Selesai |
| 2026-10-26 | 🎉 **SPIKE NETCODE SUKSES** — multiplayer Quantum 3 jalan penuh tanpa error (editor + build, Photon region asia). Brawler deterministik (gerak/jump/dash/guard/critical/geardrop) main bareng via jaringan. Quantum 3 TERBUKTI layak untuk Nexus Saga | Selesai |
| 2026-10-26 | 🏁 **SPIKE LULUS (GO)** — Quantum 3 stabil di 176ms ping (gerak instan, pukul nyambung, tanpa freeze/desync). **Keputusan FINAL: adopsi Photon Quantum 3; custom UDP DIBATALKAN.** Laporan: doc 22 | Disepakati |

## 2026-10-26 — 🚀 FASE 2 dimulai: 2 hero nyata (TITAN-01 vs PULSE-X)
Langkah pertama Vertical Slice di atas Quantum (kode di `photon-backend`, terpisah dari Pong):
- **NxDamage.cs** — refactor: logika Guard 180 / Damage Gate / Critical 3 Break Stock / Gear Drop / KO jadi satu helper bersama, dipakai melee DAN projectile (satu sumber kebenaran).
- **NxProjectileSystem.cs** + component **NxProjectile** — projectile deterministik (gerak lurus, sphere-hit XZ, hancur saat kena/habis Life).
- **NxCombat** + `HeroId`, `SkillCd`, `ShotCd`.
- **TITAN-01** (grappler): J melee · K lunge gap-closer. **PULSE-X** (zoner): J tembak cepat · K charged shot. Ganti hero: **H**.
- Dummy sekarang PULSE-X → menembaki pemain (menguji projectile + dodge).
Keputusan desain: kedua hero berbagi satu pipeline damage → tidak ada divergence aturan combat antar-hero/antar-jenis-serangan. Konsisten untuk anti-cheat replay nanti.
Berikutnya: hitbox dari animasi (OBB baked) → uji 10 pemain → backend meta.

## 2026-10-26 — ✅ Uji skala 5v5 LULUS + team brawler
Fase 2 item "uji 10 pemain" (versi bot, di `photon-backend`):
- **5v5 = 10 fighter** (1 human + 9 bot, campuran TITAN/PULSE) berjalan **stabil 60 FPS, tanpa freeze**, skor per-tim jalan. Skala rollback + O(n²) hit/separation aman untuk 10 entity.
- Tambah **hero select screen** (State 0, pilihan via input `PickHero` — deterministik), **skor per-tim** (ScoreA/ScoreB by attacker team).
- Fix **respawn**: bleed-out timer (`CritTimer`) → nyangkut di Critical 4 dtk auto-KO/respawn (dulu human bisa stuck di Critical selamanya). Respawn disebar anti-numpuk.
- Tambah **NxSeparationSystem** (pushbox ringan XZ) → fighter tak menumpuk.
Catatan: netcode scale 10 pemain NYATA (10 koneksi) belum diuji — ini uji skala simulasi+rollback via bot. Cukup untuk de-risk sebelum investasi aset/hero besar.
Berikutnya: backend meta (auth→matchmaking→MMR) ATAU hitbox dari animasi (OBB baked).

## 2026-10-26 — ✅ Backend Meta Slice: Solo 1v1 Ranked (Glicko-2 + MMR) TERVERIFIKASI
Fase 2 "backend meta" slice pertama (di `photon-backend/backend`, ASP.NET Core 8):
- **.NET 8 SDK** dipasang lokal (user-scope) → bisa build + `dotnet test` (DB in-memory, tanpa Docker).
- **Glicko-2** gantikan Elo (RD+Volatility, EF migration), divalidasi contoh resmi Glickman.
- **Matchmaking MMR** (singleton in-memory): join/status/leave, pasangkan rating terdekat dalam window + region.
- **Dev DB in-memory** → API jalan cukup `dotnet run`.
- **25/25 test lolos** + smoke-test runtime end-to-end (login→antre→matched→report→Glicko-2 1500→1662/1338→leaderboard).
- Klien Unity `NexusBackend.cs` (REST) ditulis.
Keputusan: reuse model 2-pemain "kedua lapor cocok" (semi anti-cheat) untuk ranked; Glicko-2 jadi algoritma rating resmi (doc 24). Lihat doc 25.
Belum: flow UI ranked di Unity + win-condition 1v1 di sim + slot-report = PlayerRef (butuh uji live).

## 2026-10-27 — ✅ Ranked flow LULUS uji live + Leaderboard UI
- Loop Solo 1v1 Ranked (login→MMR→pilih hero→5v5→hasil→Glicko-2→rating) **terverifikasi live** (editor+build).
- Perbaikan matang: device-id unik per-launch (2 instance = akun beda), matchmaking retry bersih + Cancel, UX Pilih Hero (feedback hijau + "menunggu pemain lain X/Y siap"), arena dibersihkan saat selesai.
- **Leaderboard UI** ditambah di menu (konsumsi `/api/leaderboard`).
Berikutnya: Profil & ekonomi kosmetik (backend, bisa dites) ATAU true 1v1 / aset 3D.

## 2026-10-27 — ✅ Sistem Akun & Profil (backend 30/30 test + UI Unity)
Fondasi akun sebelum ekonomi/kosmetik (atas permintaan user, mumpung build ranked):
- Register/Login username+password (hash PasswordHasher), Player += Username/PasswordHash/Faction (migration AddUserAccounts).
- `/me` diperluas: username, faction, rating, **rank tier** (Rookie→Nexus Legend), W/L, matches, win-rate. Endpoint set-faction (ORDE/LEGION).
- Guest login tetap (device per-launch) untuk quick play.
- **30/30 test lolos** + smoke-test runtime (register→me rank Silver→faction ORDE).
- UI Unity: layar Login/Register/Guest, panel profil di menu (rank/rating/W-L/win-rate/faction + picker), leaderboard. Ranked kini pakai akun login (bukan device hack) → rating permanen.
- Repo BE diperbarui di github.com/MattYudha/be-Nexus-saga-.
Berikutnya: uji live UI akun → lalu ekonomi kosmetik (currency/shop/inventory) di atas fondasi ini.

## 2026-10-27 — ✅ Profil & Statistik sesuai schema riset (31 test)
Dibangun DARI riset (doc 15 §3 PlayerProfile + doc 24 §2.3 progres 3 lapis), bukan karangan:
- **Tier ladder diperbaiki** ke tema riset: Rookie→Contender→Rival→Gladiator→Conqueror→Nexus Legend (sebelumnya salah pakai Bronze/Silver).
- **Account Rank** Trainee→Colonel dari accountXp/level (nol efek kompetitif).
- **Statistik**: kills/deaths/assists/KDA, wins/losses/win-rate, matches. Sim melacak Kills per-pemain (kredit killer di NxDamage.Ko) + deaths (termasuk bleed-out); klien lapor saat State=Over.
- `/me` profil penuh; match-report terima kills/deaths/assists + akumulasi + award XP (menang+100/kalah+60).
- **UI Unity: halaman Profil sendiri** (Page.Profile) — 3 lapis rank, statistik, riwayat match, faction picker. + layar Login/Register/Guest, leaderboard.
- 31/31 test + smoke-test (profil: tier Rival, Account Rank Trainee, KDA). BE di-push.
Note: butuh CodeGen (field Kills di .qtn) + rebuild .exe untuk uji live.
Berikutnya: uji live → lalu ekonomi kosmetik di atas fondasi akun/profil ini.

## 2026-10-27 — ✅ DB + Docker (Postgres persisten via WSL2)
- Backend meta kini pakai **PostgreSQL persisten** (Docker-in-WSL2 Ubuntu, systemd auto-start — bukan Docker Desktop). doc 26 = runbook.
- `.env` dibuat (secret acak, gitignored), `docker compose up -d --build` → Postgres 16 + API, migration auto-apply (4 migration), API di `localhost:5080` dari Windows (NAT forwarding, compose tetap bind 127.0.0.1 aman).
- **Persistensi terbukti**: register akun → `docker compose down && up` → login akun lama tetap sukses.
- Catatan: networkingMode=mirrored GAGAL di mesin ini (0x8007054f → fallback no-network, sudah di-revert). NAT + settle 15-30s cukup. Unity BackendUrl tetap localhost:5080.
Berikutnya: uji live UI akun+profil di Unity → lalu ekonomi kosmetik.

## 2026-10-27 — 📋 RINGKASAN HARIAN (yang diimplementasi & terverifikasi)
1. **Ranked flow LULUS uji live** (login→MMR→pilih hero→5v5→hasil→Glicko-2→rating) + fixes: device-id unik per-launch, matchmaking retry bersih + Cancel, UX pilih-hero (feedback hijau + "menunggu pemain lain X/Y"), arena dibersihkan saat selesai.
2. **Leaderboard UI** (menu).
3. **Sistem Akun**: register/login (username+password, hash PasswordHasher) + guest.
4. **Profil & Statistik** (schema dari riset doc 15 §3 + doc 24 §2.3, bukan karang): 3 lapis — Account Rank (Trainee→Colonel), Solo tier (Rookie→Contender→Rival→Gladiator→Conqueror→Nexus Legend), Faction (ORDE/LEGION) + K/D/A/KDA/win-rate/XP. **Halaman Profil sendiri** di Unity.
5. **Sim**: lacak Kills per-pemain (kredit killer) + deaths (termasuk bleed-out).
6. **Backend: 31/31 test lolos.**
7. **DB + Docker (doc 26)**: PostgreSQL **persisten** via Docker-in-WSL2, migration auto-apply, reachable dari Windows `localhost:5080`, **persistensi terbukti** (data bertahan lintas recreate).
8. **Auto-start (systemd service)**: ✅ **TERVERIFIKASI — buka terminal Ubuntu → Docker + Postgres langsung running sendiri** (tanpa `docker compose up` manual, ~10-15 dtk sampai healthy). Login/register/profil diuji live ke DB persisten (2+ akun tersimpan).
9. **Push**: docs → Nexus-Saga; backend + unit auto-start → be-Nexus-saga-.

## 2026-10-30 — 🎨 KUNCI SEMANTIK WARNA UI (T1)
Palet **navy gelap** dikonfirmasi (gaya lobby Mobile Legends); pengaruh Lost Saga = **struktur** (ruang ladder, alur room), bukan palet. **Satu warna = satu arti:**
- **biru** = tim kamu/kawan · **merah** = lawan/musuh (**satu-satunya** arti merah)
- **emas** = rank + MENANG · **abu-baja** = KALAH + delta negatif (+ art desaturate)
- **hijau** = perolehan positif (+Poin) + status online + tombol sekunder Create Room
- **oranye** = tombol utama · **cyan** = aktif/fokus
- **ORDE** = badge TERANG (ivory/platinum, teks gelap) + emblem **perisai** · **LEGION** = badge GELAP (onyx, garis+teks volt) + emblem **chevron**
- placeholder hero = **netral + ikon kelas**
- Warna lore (ORDE putih/emas/cyan, LEGION hitam/crimson/volt) hanya utk **art karakter**, BUKAN token UI.

**Token** (`NexusTokens.uss`): `--nx-team-ally/-enemy`, `--nx-result-win`(=emas)/`-loss`(abu-baja), `--nx-gain`, `--nx-online`, `--nx-hero-neutral`, `--nx-badge-bg/-fg` (+ `-dim`). **Aturan keras**: token faksi HANYA badge/emblem/layar pilih faksi/header ladder — jangan utk tim/hasil/delta/state. Diterapkan di `.nxl-ladder-row--loss`, `.nxl-hist-*--loss`, `.nxl-pts-dn` (abu-baja, bukan merah), `.nxl-dt-accent/-bar` (you=ally, opp=enemy). Lihat docs/34 (KALAH abu-baja) & docs/35 (warna+emblem faksi).

Keputusan warna ambigu (diputus user 2026-10-30):
- **Badge prestasi** (FLAWLESS/COMEBACK/FIRST BLOOD) = **satu chip netral** (steel-dim + teks putih), dibedakan **ikon+label**. FIRST BLOOD **tidak** kemerahan; COMEBACK **tidak** pakai `--nx-gain`. Pengecualian: **FLAWLESS** garis emas tipis.
- **Grafik Painter2D**: garis data = `--nx-team-ally` (biru); **cyan HANYA titik fokus/hover**; band tier = **emas redup** (-dim). Berlaku di `ProfileController` + `NexusLobbyController`.
- **`NexusMetaUI.cs`** (legacy IMGUI): dibuat **inert** (`LegacyEnabled=false` → `OnEnable` self-disable), **dikecualikan** dari audit grep warna (komentar "legacy, dihapus di poin e"). Dihapus di **poin e**.
- **Sprite hero placeholder**: regen **netral + ikon kelas** — `hero_titan`=Grappler (kepalan), `hero_pulse`=Zoner (crosshair), bidang `--nx-hero-neutral`, nama samar (TITAN/PULSE). `hero_unknown` = "?".

**Pending (editor, user)**: tes faksi 1–9 (+teks kartu baru +KALAH abu-baja) · tampilan badge & grafik baru · screenshot swatch — dalam SATU sesi. T2 (CodeGen) **tunggu hasil tes**.
→ **2026-11-13: tes editor user AMAN semua** (faksi, T1, Detail Match v2 terverifikasi).

## 2026-11-13 — 🗺️ T3: AUDIT DOCS + KEPUTUSAN (peta penuh: `docs/00-ROADMAP.md`)
| # | Keputusan | Menggantikan | Status |
|---|---|---|---|
| T3-1 | **Solo Ladder ≠ Survival.** Solo Ladder = Ranked 1v1, **first-to-5 KO, tanpa ronde**. Survival = Race-to-6, ronde 90 dtk, sudden death, **1v1/3v3 menyusul**. (docs/24 §5a) | docs/24 §5 "berlaku utk 1v1 Solo Ranked" | Disepakati |
| T3-2 | **Leaderboard**: urut **tier tampil ↓ → conservative (`rating−2·RD`) di dalam tier → WR → match**. Kode + tes (Gladiator RD tinggi tak di bawah Rival). (docs/33) | urut conservative murni | ✅ Implementasi |
| T3-3 | **Nakama** = opsi ke-3 di docs/36 (bersama Photon Chat & SignalR). Belum implementasi. | — | Menunggu user (docs/36) |
| T3-4 | **"Guild" → "Squad"** di semua docs, UI (BottomNav, FriendPanel), channel chat (**SQUAD**). "Guild War/Board" → Squad War/Board. | baris 2026-10-26 "Guild War→Guild Board", "orthogonal dgn guild" (nama saja) | ✅ Diterapkan |
| T3-5 | **Mode**: slider lobby = **ANTREAN saja** → Ranked + **Battle** (3v3 santai, bot isi slot) + 1 kartu teaser "Segera Hadir" (Faction War, Nexus Cup). **Street Room = room browser** 1v1–3v3 tanpa MMR, tombol sendiri samping HQ/Plaza. **2v2 dicabut dari MVP.** Survival 1v1/3v3 menyusul; Faction War/Nexus Cup 5v5 Fase 3+. *[UBAH bila user koreksi]* | 2026-10-24 "MVP mode 1v1 & 2v2"; 2026-10-24 "Mode MVP Survival/Elimination + TDM"; 2026-10-26 "MVP tetap 1v1+2v2"; docs/24 Street Room 1v1–5v5 | Disepakati (klien = poin d) |
| T3-6 | **Faksi**: layar pilih **SETELAH hasil match pertama** (bukan sebelum lobby; pemicu saja yg pindah). **Pindah gratis 1×** selama placement <5 (`FactionSwitchUsed`, validasi `POST /me/faction`, admin reset mengembalikan jatah). Guest→akun: faksi terbawa → **tidak mungkin saat ini (K-10)**. | docs/35 "terkunci satu season", `FactionLocked`; docs/24 "cooldown per season" | Backend ✅ · pemicu klien Antre (poin e) · guest K-10 menunggu |
| T3-7 | **Proteksi demosi** status resmi = **NONAKTIF (grace=0)**; docs/31 dikoreksi. | docs/31 "grace=3" | ✅ Diterapkan |

**Konflik BARU yang menunggu keputusan user** (tidak diputus sendiri): **K-09** format Squad War (distrik vs match) · **K-10** guest→akun (faksi/progres tak terbawa) · **K-11** Nakama vs ASP.NET (via docs/36) · **K-12** papan poin Survival belum ditentukan. Rincian di `docs/00-ROADMAP.md`.

TODO besok: (a) tombol Back di Profile, (b) rebuild SELURUH UI on-theme (fondasi design system) — lihat memory nexus-ui-rebuild-tasks.

## 2026-11-13 — 🔬 RISET COMBAT: ekstraksi mekanik Ikemen GO → `docs/research/ikemen-extract/`
Tujuan: menutup baris ⬜ di tabel kebutuhan LostSaga/AyoDance **tanpa** menyentuh client komersial.
Sumber tunggal: Ikemen GO **v1.0.0, MIT** (`Nexus_Lab/src/Ikemen-GO`), dibaca statis, tidak dijalankan.

| Hasil | Isi |
|---|---|
| `ikemen-extract/01-input-buffer-cancel.md` | `time`/`buffer.time`/`step.time`, buffer **membeku saat hitstop**, cancel = state -1 + `movecontact`; usulan `NxCmd` + skema `cancels[]` |
| `ikemen-extract/02-juice-hit-feedback.md` | EnvShake default (freq 60, ampl -4), hit spark, SuperPause (30 tick, darken 0.5), KO slow-mo **60 tick / 0.25× / ramp 45**, corner push (guard ×1.3) |
| `ikemen-extract/03-guard-dizzy-counter-juggle.md` | dizzy = 1000 poin dari damage; guard break Ikemen = flag, bukan gauge; **counter hit bonus TIDAK ada di Ikemen** → kita desain; juggle per-penyerang |
| `ikemen-extract/04-replay-spectator.md` | replay = input log (~60 KB/match), `LiveChecksum` CRC32, killcam, kartu Disputed + batas jujurnya |
| `ikemen-extract/05-hero-swap-tag.md` | TagIn/`SCF_standby` (tidak bisa dipukul, tidak dikontrol), pemetaan ke `NxSwap` |
| `ikemen-extract/06-camera-views.md` | 3 CameraView, batas kamera bergantung zoom (0.625–1.0) |
| `ikemen-extract/combat-tuning.json` | angka usulan siap config (belum dipakai kode) |
| `kebutuhan-lostsaga-ayodance.md` | checklist status ✅/🟡/⬜/🚫 + rujukan bukti |

**Koreksi teknis yang dicatat:** Photon Quantum = simulasi **deterministik + prediksi + rollback**, server
meneruskan input & memvalidasi (plugin), **bukan** authoritative-server + reconciliation. Konsekuensi:
efek visual dipisah dari state sim; anti-cheat lewat checksum/desync; replay dari input, bukan dari posisi.

**Kebijakan tidak berubah** (baris 2026-10-24 tetap berlaku): riset AyoDance statis, tidak membongkar
proteksi/packer LostSaga, tidak mengekstrak aset dari client. Mode dance tetap **arsip** (docs/12).

**Pertanyaan baru untuk user (belum diputus):** model juggle — **S1 satu pool milik korban** (docs/08,
lebih ketat, combo tag tidak memperpanjang juggle) vs **per-penyerang** seperti Ikemen (lebih bebas).
Rekomendasi riset: S1. Tidak diubah sebelum user memutus.

### 2026-11-13 (lanjutan) — PATCH `.qtn` diterapkan (aditif, belum aktif)
`Nexus.qtn` +36 baris, **tanpa** field lama yang diubah dan **tanpa** komponen baru:
`NxCombat` += `DirHistory`, `BtnHistory`, `MotionMask`, `MotionAge`, `StateId`, `StateTime`,
`FrameIndex`, `MoveType`, `Juggle`, `AttackId`, `CancelMask`, `ArmorTier`, `ArmorTicks`, `CounterHit`,
`JuiceSeq/Kind/Power/Ticks/Pos`; `global` += `KoSlowTicks`, `SuperFreezeTicks`, `SuperFreezeSlot`.
Belum ada sistem yang membacanya → perilaku game **tidak berubah**. Butuh **CodeGen** di Unity.
Spesifikasi & urutan update per tick: `docs/research/ikemen-extract/07-patch-qtn.md`.
**T2 tidak disentuh** (tetap berikutnya).

### 2026-11-13 (lanjutan 2) — SISTEM PERTAMA: `NxInputSystem`
File baru `Simulation/Nexus/NxInputSystem.cs` (data-only) + registrasi di `Editor/NexusSetup.cs`
(sebelum `NxCombatSystem`, jalur Local & Online). Mengisi histori input, `MotionMask`, `StateTime`,
`MoveType`, decay `JuiceTicks`. **Tidak mengubah** gerak/hit/KO → perilaku game tetap.
Gesture = rotasi mentah (bukan "QCF") supaya pemetaan skill tetap di data. Butuh CodeGen + jalankan ulang
menu scene (sistem disimpan di asset `NexusSystemsConfig`, bukan di kode).

### 2026-11-13 (lanjutan 3) — PROMPT RISET + BACKLOG (docs saja)
Dibuat `docs/research/PROMPT-riset-legal.md` (prompt inisiator: peran, aturan label OBSERVED/DERIVED/PROPOSED,
sumber izin vs larang, format keluaran, "jangan implement") dan `docs/research/backlog-riset-logic.md`
(11 domain: combat, battle, hero/ability, animasi, map, sound, VFX, room, matchmaking, netcode, ekonomi).
Sumber: open source (Ikemen GO MIT, Nakama, Open Match, Colyseus, Effekseer, SoLoud, miniaudio, OpenDota),
dokumentasi publik Dota 2 (Wiki/Liquipedia/dev blog/paper), aset berlisensi/CC0.
**Batas tetap:** tidak mengekstrak aset client komersial, tidak membongkar anti-cheat, tidak memakai source bocor.
Tidak ada kode/aset yang diubah di sesi ini.

### 2026-11-13 (lanjutan 4) — RISET DOMAIN 1: hero/ability → `docs/research/hero-ability/`
| File | Hasil |
|---|---|
| `01-ability-data.md` | skema ability (cast point/backswing/channel/charge/target/phases), urutan eksekusi, aturan cancel & buffer, validator |
| `02-formulas.md` | pipeline damage, **armor `1−0.06A/(1+0.06|A|)`**, MR & SR & CDR multiplikatif, evasion, block, aturan pembulatan FP |
| `03-modifiers-dispel.md` | model modifier slot tetap, 4 stacking rule, `DispelBasic`/`DispelStrong`, debuff immunity, aturan buang-slot deterministik |
| `04-kit-titan-pulse.md` | kit TITAN-01 & PULSE-X + combo route + anggaran cooldown (angka dekat spike) |

Sumber: dokumentasi publik Dota 2 (`DK`) + Ikemen GO (MIT). **Formula ditulis ulang**, tidak ada teks/aset
yang disalin. Status backlog domain hero/ability: ⬜ → 🟡 (artefak ada, implementasi belum).
**Tidak ada kode/`.qtn` yang diubah.** Angka di `04` = PROPOSED, belum masuk `combat-tuning.json`.
Menunggu user: angka kit, slot ultimate MVP, resource (cooldown murni vs energy), jumlah slot modifier.

### 2026-11-13 (lanjutan 5) — REA DIPAKAI + PATCH DITAHAN + RISET battle-flow
**1. `rea` dibangun & dipakai.** `npm ci` (400 paket) + `npm run build:cached` (3 task, 13 s) sukses.
Dipakai pada **kode kita sendiri** (legal): `inspect-managed-members` → `PhotonBackend.Api.dll`,
provider `rea-dotnet-static`, sha256 `f6e35d6a…f0f6d3`, evidence `ev_abe8dcae…beed3`.
Catatan: `analyze` (native) **tidak** tersedia di mesin ini (Hopper unsupported di win32, Ghidra Windows
native addon belum dibangun, IDA belum dikonfigurasi) → untuk .NET pakai perintah `inspect-managed-*`.
rea **tidak** dipakai pada client komersial mana pun.

**2. Patch `.qtn` + `NxInputSystem.cs` DITAHAN (di-revert).** Alasan diterima: deteksi rotasi & double-tap
salah, komentar `.qtn` tak sinkron dengan kode, `StateTime` tak pernah reset, ~20 field mengunci desain
sebelum diputuskan, dan melanggar aturan "jangan menumpuk kode belum terverifikasi" + "T2 berikutnya".
**Aturan baru: field `.qtn` hanya ditambah lewat T2, dan hanya bila ada sistem yang memakainya.**
`git checkout` pada `Nexus.qtn` + `NexusSetup.cs`, file `NxInputSystem.cs` dihapus. Working tree bersih.

**3. Koreksi `hero-ability/`.** `04` ditulis ulang: charge TITAN = **Invuln 15** (bukan armor), **tidak ada
chip damage** saat guard (hanya gauge 34/hit), Jab 11/Heavy 18 + combo route = **desain baru**, satu tipe
damage, ultimate **ditunda**, resource **cooldown murni**, `pulse_overcharge` keluar dari MVP.
`02` (formula damage) & `03` (modifier/dispel) diberi label **ARSIP PASCA-MVP**; yang tetap relevan dari
`02` hanya aturan pembulatan & urutan pipeline.

**4. Riset domain berikutnya: battle/match flow** → `docs/research/battle-flow/01-match-lifecycle.md`.
Temuan: model ronde Ikemen tidak cocok (Ranked first-to-5 tanpa ronde); yang belum ada = timer, aturan
waktu habis, draw, pause, disconnect, rematch. Menunggu user 5 keputusan (§6): timer Ranked, hasil saat
seri, durasi grace disconnect, pause casual, rematch.

### 2026-11-13 (lanjutan 6) — `docs/00-CHECKLIST.md`
Dibuat checklist master (11 item selesai, 26 belum) supaya urutan kerja tidak berantakan:
A antrean terkunci (a–h, T1–T3 dengan sub-item T2) · B riset selesai · C riset belum (R1–R5) ·
D keputusan menunggu (K-09..K-12, T2-AFK, BF-1..5, HA-1) · E utang rilis · F larangan.
Aturan kerja ditulis di §G: satu item → bukti → centang; item yang butuh keputusan dipindah ke D, bukan dikerjakan setengah.

## 2026-11-13 — NX-11: keputusan untuk T2 (alur match Ranked)
| Topik | Keputusan | Status |
|---|---|---|
| AFK / disconnect | **20 dtk** tanpa input atau terputus → **forfeit** (satu ambang untuk keduanya) | Diputus user |
| Timer Ranked 1v1 | **100 dtk** (match cepat). Catatan: ~20 dtk/KO → banyak match akan berakhir oleh waktu. Nilai di config | Diputus user |
| Waktu habis, skor KO seri | Tie-break: gear rontok terbanyak kalah → darah tersisa paling sedikit kalah → masih sama = DRAW tanpa rating | **Diputus user** (dikonfirmasi 2026-11-13) |
| Mode Deathmatch (ala LostSaga) | Waktu habis → darah semua jadi 0, lalu tiap pukulan merontokkan gear satu per satu; gear habis duluan = kalah (koreksi user, bukan sekali-pukul-mati) | **INBOX NX-IN-05** (mode baru, di luar milestone) |
Menggantikan usulan riset battle-flow §6 (#1 timer 300 dtk, #2 DRAW langsung, #3 grace 20 dtk).

### 2026-11-13 (lanjutan 7) — R1: SPESIFIKASI T2
`docs/research/t2-spec/01-rules-and-numbers.md` — angka & aturan T2 sebelum eksekusi:
bleed-out dihapus; penalti gerak 70/50/35 dengan dash terkunci di stock 1; Overload 480 tick -> lock 90 tick
(damage x1.2, bukan KO); skor target bot (Critical -40, Overload -80, penumpukan tumpukan +30, tie-break index);
AFK 8 dtk peringatan / 30 dtk forfeit akumulatif (bot tidak menggantikan di Ranked); `koTimeline`.
**Temuan penting:** permintaan `koTimeline` maks 9 entri hanya benar untuk Ranked 1v1; Battle 3v3 butuh sampai 19,
5v5 sampai 29 -> usul opsi (c) 9 KO terakhir + `TotalKos`. 8 tes/invariant + 4 angka disiapkan untuk persetujuan.
Tidak ada kode diubah.

### 2026-11-13 — Upaya cek aturan waktu-habis LostSaga dengan REA: DIHENTIKAN
`rs.iop` = arsip ZIP dengan header diacak; **isi entri terenkripsi** (pola XOR berulang). Logika match ada di
`lostsaga.exe` (Themida). Membuka keduanya = membongkar proteksi → dilarang (keputusan 2026-10-24). Ekstrak
sementara dihapus, sesi REA ditutup. Klaim aturan LostSaga dari sumber luar (prioritas jumlah pemain bertahan →
skor ronde → DRAW bila skor 0) **tidak terverifikasi**; hanya boleh dipakai sebagai inspirasi desain, bukan fakta.

### 2026-11-13 (lanjutan 8) — T2 DIIMPLEMENTASI (kode), MENUNGGU CODEGEN
Angka final disetujui user: **AFK 15 dtk peringatan / 30 dtk forfeit akumulatif**, reset oleh
gerak/lompat/guard/dash/serang/skill (tukar hero & mouse tidak dihitung); **Overload 480 tick -> lock 90 tick,
TANPA pengali damage** (alasan user: pengali membuat menunggu lebih untung daripada menyerang);
**penalti gerak 70% sejak masuk Critical, 50% di stock 2, 35% di stock 1, dash terkunci sejak Critical**;
**`koTimeline` kapasitas per mode** (9/19/29, fallback tetap 29) — implementasi ditunda sampai sintaks array
`.qtn` terbukti.

Kode: `NxTuning.cs` (baru, semua ambang), `NxCombatSystem.cs` (bleed-out dihapus, `TrackActivity`,
`UpdateCriticalPressure`, `CritSpeedMul`, `BestTarget`, dash lock), `NxDamage.cs` (reset Overload saat kena/guard,
`KoTotal`, respawn bersih), `Nexus.qtn` (+`IdleTicks`/`OverloadCharge`/`OverloadLock`, global +`KoTotal`/`Forfeit`).
**Tidak dikerjakan:** HUD indicator (View), `koTimeline` (blokir sintaks), tes. Menunggu CodeGen + tes editor user.

### 2026-11-13 (lanjutan 9) — KODE T2 DIPERTAHANKAN, RISET DIAUDIT ULANG
User memutuskan kode T2 **tidak dihapus**; perbaikan diserahkan ke reviewer (Claude user).
Sesi ini kembali ke mode riset murni: `docs/research/t2-spec/02-audit-kode-t2.md` (peta kode + 8 temuan
perilaku + 4 risiko kompilasi + 4 pertanyaan reviewer + keselarasan `AddMatchEndReason`).
**Aturan ditegaskan ulang: riset tidak mengubah kode.** Temuan tertinggi: (B1) forfeit memaksa skor =
`KoTarget` sehingga skor nyata hilang; (B2) AFK ikut berjalan saat pemain di-combo; (B3) lock Overload
tidak mematikan guard sehingga tidak benar-benar rentan.

### 2026-11-13 (lanjutan 10) — PERAN BERGANTI: TESTER, QA PASS PERTAMA
User mengganti peran menjadi **tester**. Hasil: `docs/qa/01-laporan-tester-2026-11-13.md` (20 temuan, tanpa ubah kode).
Temuan tertinggi (**S1**): klien **memalsukan skor** ke 5-4 di `NexusGame.cs:370` padahal `NxMatch` tidak memalsukan;
`EndReason`/`WinnerSlot`/`KoTimeline` **tidak dikirim**; seri dihitung menang; durasi dari wall-clock;
`KoLog` dikunci 9 sementara backend menuntut jumlah = skor (Battle/Survival butuh 19/29); timeline dibandingkan
sebagai string JSON mentah; draw 255 vs -1. **S2**: Overload tidak mematikan guard; AFK berjalan saat pemain
di-combo; AFK 10/20 dtk (keputusan 15/30); timer 100 dtk belum diputus; timer berjalan saat hitpause;
KO dan timer di tick yang sama dimenangkan timer. 8 item dimasukkan ke checklist §C2.

## 2026-11-13 — T2 (NX-12) SELESAI DI KODE: C4 dipulihkan + akhir match
- **KO hanya lewat 3 Break Stock** — bleed-out dihapus (K-03 ditutup, menunggu tes editor). Field `CritTimer`/`LastHitBy*` dibuang.
- Critical: penalti gerak 70/50/35%, **dash & lunge TITAN dikunci** (lunge = dash; tambahan saya, mudah dibalik), Overload 8 dtk → lock 1,5 dtk (guard lepas, bukan KO), bot prioritas Critical/Overload.
- Akhir match (`NxMatch.cs`): KO 5 · waktu habis 100 dtk (skor → gear rontok → darah → seri) · forfeit AFK/disconnect **20 dtk berturut-turut** (bukan 30 dtk akumulatif versi sesi DeepSeek — digantikan keputusan user). Skor tidak pernah dipalsukan.
- `koTimeline` (≤9) dilaporkan, wajib sama antar-klien, disimpan per match; tab "Jalannya Match" aktif. Seri = rating/W/L tidak berubah, statistik menghitung seri terpisah. Warna SERI = token baru `--nx-result-draw` (netral terang).
- Proses: kode simulasi awal dari sesi DeepSeek (`--bare`, tanpa gate BOARD) dilanjutkan sesi ini; 5 bug diperbaiki (forfeit memalsukan skor → Disputed; respawn mereset AFK; Overload saat guard tetap menangkis; bot menghitung diri sendiri; label "akumulatif" ≠ kode).
- Verifikasi tanpa Unity: CodeGen headless (`Quantum.CodeGen.Qtn.dll`) menghasilkan file **identik byte** dengan `Generated/` di repo, lalu `Quantum.Simulation`, `Quantum.Unity`, Assembly-CSharp ter-compile terhadap Unity 2022.3.62f1 (menemukan & memperbaiki 1 error di HUD). Backend 84 tes, deploy live, 9 match lama tak berubah.

## 2026-11-13 — K-10 diputus: guest → akun lewat upgrade (opsi a)
`POST /api/auth/upgrade` (butuh token guest): username+password dipasang ke Player yang sama → faksi, rating, riwayat,
statistik terbawa. **DeviceId dilepas** setelah upgrade (keamanan: akun berpassword tak boleh dibuka hanya dengan deviceId;
perangkat itu berikutnya login pakai username). Akun yang sudah terdaftar → 409. Backend live, 2 tes (90 hijau).
UI menyusul di Settings › Akun (poin d). Juga hari ini: QA pass 3 (Q42 TTL 180 dtk, Q43 retry laporan, Q44 separation).
