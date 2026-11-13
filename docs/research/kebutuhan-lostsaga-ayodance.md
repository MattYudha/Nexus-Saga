# Kebutuhan dari LostSaga & AyoDance — checklist riset (2026-11-13)

Dokumen ini = **daftar periksa**, bukan keputusan baru. Tiap baris punya status dan **lokasi bukti** di repo,
supaya tidak ada klaim "sudah ada" tanpa rujukan.

Legend: ✅ ada di kode/dokumen · 🟡 separuh (desain ada, implementasi belum) · ⬜ belum ada · 🚫 ditolak kebijakan

Aturan sumber (sudah disepakati, tidak berubah):
- LostSaga/AyoDance: **hanya observasi statis & dokumentasi publik** (docs/90: "riset AyoDance hanya statis, ada Xigncode", "tidak membongkar proteksi/packer client LostSaga").
- Ikemen GO: **open source MIT**, boleh dibaca & diturunkan desainnya → hasil ekstraksi di `docs/research/ikemen-extract/`.

---

## 0. Dua koreksi terhadap tabel awal

**0.1 Netcode — baris awal salah.**
Photon Quantum **bukan** "authoritative server + reconciliation". Quantum = simulasi **deterministik**
(semua klien menjalankan frame yang sama dari input yang sama) + prediksi lokal + rollback saat input
terlambat. Server **meneruskan input** dan boleh memvalidasi lewat plugin server; server tidak
"menjalankan kebenaran lalu mengirim state". Konsekuensinya untuk desain:
- semua nilai combat **fixed-point** (sudah jadi aturan repo, `Nexus.qtn`),
- efek visual **tidak boleh** menyentuh state simulasi (lihat `ikemen-extract/02`),
- cheat terdeteksi lewat **checksum/desync**, bukan lewat "koreksi state dari server" (lihat `ikemen-extract/04`).

**0.2 Sisi ritme AyoDance = ARSIP, bukan fitur.**
docs/12 sudah memutuskan Nexus Saga **tanpa mode dance/ritme** (lisensi musik, biaya chart, identitas brawler).
Bagian §B2 di bawah tetap didaftar untuk kelengkapan riset, **tidak** mengubah keputusan. Kalau mau dibuka,
harus diputus eksplisit dulu dan dicatat di docs/90.

---

## A. LostSaga (brawler, hero-swap)

| Kebutuhan | Status | Bukti / di mana | Catatan riset |
|---|---|---|---|
| Frame data per serangan (startup/active/recovery/hitstop/pushback) | 🟡 | docs/13 §4 (tabel tuning), `kfm.cns` OBSERVED | **Angka konkret: `ikemen-extract/01`, `combat-tuning.json`** |
| Hitbox/hurtbox 3D, collider proxy, FP | 🟡 | docs/13 §3 + §8, docs/08 §5.2 | OBB+Sphere (bukan capsule) |
| Reaksi kena pukul: stagger, launch, juggle, ground bounce, wall hit, knockdown, wake-up + i-frame | 🟡 | state-machine-ikemen §3 (rantai 5000→5110→5120) | **Wall hit tidak ada di Ikemen** → desain sendiri |
| Guard, guard crush, super armor, counter hit | 🟡 | `ikemen-extract/03` (dizzy, SCF_guardbreak, MoveCountered) | Ikemen punya guard & dizzy; **super armor tidak ada** |
| Input buffer, cancel window, combo route | ⬜→🟡 | `ikemen-extract/01` | Mekanisme `time` / `buffer.time` / `state -1` + usulan skema cancel |
| Hero swap: cooldown, transisi, state terbawa | 🟡 | docs/08 §6 + `ikemen-extract/05` (TagIn, SCF_standby) | Ikemen punya **TagIn**, tidak punya cooldown/HP-share |
| Gear drop + pungut ulang | ✅ | docs/08 §7 (FINAL), `NxCombat.GearMask` | — |
| Animasi terikat ke data (bukan Animator bebas) | ⬜ | `ikemen-extract/01` (anim frame = tick), docs/13 §5 | Aturan: durasi frame dalam tick, bukan detik |
| Kamera free-roam 3D, lock-on | 🟡 | docs/06 + `ikemen-extract/06` (CameraView) | Ikemen: Fighting/Follow/Free View |
| Kontrol keyboard, gamepad, touch | ⬜ | `ikemen-extract/01` (model command), Quantum `input{}` | Quantum input = struct per tick; sentuh = mapper, bukan logika baru |

### A2. Rasa pukulan ("juice") — semua ⬜
| Item | Status | Bukti |
|---|---|---|
| Hit spark | ⬜→🟡 | `ikemen-extract/02` (sparkno/sparkxy/sparkangle/sparkscale) |
| Screen shake | ⬜→🟡 | `ikemen-extract/02` (EnvShake: time/freq/ampl/phase/mul/dir/decay) |
| Slow-mo KO | ⬜→🟡 | `ikemen-extract/02` (slow_time=60, slow_fade=45, slow_speed=0.25) |
| Suara berlapis (whoosh/impact/voice) + announcer | ⬜ | belum ada spesifikasi |
| Damage number + indikator Critical | ⬜ | indikator Critical = T2 |

### A3. Konten / kompetitif
| Kebutuhan | Status | Bukti |
|---|---|---|
| Roster hero + kit data-driven | 🟡 | docs/17 |
| Arena: hazard, ketinggian, rotasi map | ⬜ | belum ada |
| Bot AI | ✅ dasar / 🟡 prioritas Critical | T2 (queue) |
| Training mode & tutorial | 🟡 | docs/12 (Training Grounds = reuse Core), docs/17 |
| Replay, spectator, killcam | ⬜→🟡 | `ikemen-extract/04` (input log + checksum) |
| Ranked Glicko-2, ladder, leaderboard | ✅ | docs/33, 00-ROADMAP |
| Party/Squad/Squad War | 🟡 | K-09 menunggu keputusan |
| Anti-cheat (checksum desync, validasi server, kartu Disputed) | 🟡 | docs/32 + `ikemen-extract/04` |

---

## B. AyoDance

### B1. Sisi sosial (diadopsi)
| Kebutuhan | Status | Bukti |
|---|---|---|
| Slot avatar (rambut/wajah/atas/bawah/sepatu/aksesori/pet/aura) | 🟡 | docs/15, research/ayodance-avatar-wardrobe.md |
| Ganti kostum: skinned mesh swap, mesh combining, tint | ⬜ | riset wardrobe (statis) |
| Fisika rambut & kain | ⬜ | belum ada |
| 2 base body rangka identik | 🟡 | docs/10 |
| Fitting room + preview shop | ⬜ | — |
| Room publik/privat, emote, Photo Booth | 🟡 | docs/12 |
| Chat channel, /f squad, megaphone | 🟡 | docs/24, K-11 |
| Teman, mail, hadiah, couple | 🟡 | docs/31 Fase 2–5 |

### B2. Sisi ritme — 🚫 ARSIP (docs/12)
Audio DSP presisi, judgement window, format chart + editor, musik original, mocap tari, mode solo/tim/couple/battle.
**Tidak dikerjakan.** Disimpan hanya sebagai catatan kalau docs/12 dibuka lagi.

---

## C. Yang sering terlupa (keduanya)

**Teknis/ops:** Addressables+bundle hash (docs/18) · CDN & patcher · remote config/balancing tanpa build ulang ·
analytics & crash reporting · region Photon (SG) & biaya CCU · anti-cheat klien + report/ban · lokalisasi ID/EN.

**Legal Indonesia:** PSE Kominfo/Komdigi · IGRS · UU PDP · payment gateway (Midtrans/Xendit/Mayar) + voucher ·
aturan gacha (tampilkan peluang, tanpa P2W) · ToS/privacy + cek merek "Nexus Saga" · log clean-room tiap angka.

**Produksi:** 3D artist, animator, VFX, sound, komposer (pipeline docs/21) · QA/playtest · live-ops & moderator.

---

## D. "Ambil langsung dari mereka" — keputusan tetap

| Opsi | Status | Alasan |
|---|---|---|
| Pakai engine/source LostSaga (termasuk bocoran) | 🚫 | Mencemari seluruh kode; docs/90 |
| Ekstrak model/tekstur/suara/musik dari client | 🚫 | Hak cipta; boleh dilihat gaya, tidak boleh dipakai |
| Private server / emulator | 🚫 | — |
| Jalankan AyoDance di bawah debugger/Frida | 🚫 | Xigncode; docs/90 "riset statis saja" |
| Pelajari desain → tulis ulang (clean-room) | ✅ | Jalur yang dipakai di repo ini |
| Lisensi resmi IP/engine | 🟡 | Mahal, perlu negosiasi |
| Aset legal (Asset Store, Mixamo, Synty, sound lib) | ✅ | Prototipe cepat |
| **Baca source open source (Ikemen GO, MIT)** | ✅ | **Dasar `ikemen-extract/`** |

---

## E. Yang sudah ditutup oleh riset terbaru
Lihat `docs/research/ikemen-extract/` — 6 dokumen + 1 file tuning JSON:
input buffer & cancel · juice (hitstop/shake/KO slow/superpause) · guard-dizzy-counter-juggle ·
replay/spectator/anti-desync · hero swap (TagIn/standby) · kamera.
