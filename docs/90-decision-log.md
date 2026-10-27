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
