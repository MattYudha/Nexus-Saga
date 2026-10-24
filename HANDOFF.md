# HANDOFF — Nexus Saga: Chronicles

> **Baca file ini pertama kali** jika kamu pindah device, atau kamu orang baru yang melanjutkan proyek ini.
> Terakhir diperbarui: **2026-10-24** · Status: **Fase 0 selesai (desain terkunci) → siap Fase 1 (Spike)**

---

## 0. Ringkasan 30 detik
- **Apa ini?** Game PC online: avatar sosial ala AyoDance + brawler tim ala LostSaga + ekonomi kosmetik non-P2W. Penjelasan sederhana: [`docs/11-konsep-game-bahasa-sederhana.md`](docs/11-konsep-game-bahasa-sederhana.md).
- **Sampai mana?** Semua desain game dan arsitektur sudah **dikunci**. **Belum ada satu baris kode game pun.**
- **Langkah berikutnya?** **Fase 1 — Spike netcode (2–3 minggu)**. Rencana detail langkah-demi-langkah di [`docs/20-rencana-spike-fase1.md`](docs/20-rencana-spike-fase1.md). Lihat juga §5.
- **Mulai dari mana saat lanjut?** Tugas **S-00** = izin pemilik untuk mulai coding, lalu S-01 (pasang .NET 8 SDK). Semua desain sudah LOCKED (`docs/19`), jadi tinggal eksekusi.
- **Aturan paling penting:** jangan mulai coding sebelum pemilik proyek memberi izin, dan jangan mengubah keputusan yang sudah dikunci tanpa mencatatnya di [`docs/90-decision-log.md`](docs/90-decision-log.md).

---

## 1. Aturan kerja (wajib dipatuhi)
| # | Aturan |
|---|---|
| 1 | **Belum boleh coding game** sampai pemilik proyek bilang "mulai". Tooling dokumentasi (mis. generator PDF) boleh |
| 2 | Setiap keputusan baru → baris baru di `docs/90-decision-log.md` (tanggal, keputusan, status) |
| 3 | Pertanyaan yang belum terjawab → `docs/91-open-questions.md` |
| 4 | Hasil riset game lain → `docs/research/<sistem>-<game>.md` (pisahkan observasi / inferensi / belum diketahui) |
| 5 | **Riset clean-room:** pelajari desain, jangan salin kode/aset/data game lain. Jangan bongkar proteksi/packer. Jangan jalankan game ber-anti-cheat di bawah debugger/Frida |
| 6 | **Jangan commit** file hasil ekstrak game, dump, atau evidence REA mentah (`.gitignore` sudah memblokir) |
| 7 | Proposal PDF berlabel **Rahasia** → **tidak** di-push ke GitHub (hanya skrip pembuatnya) |
| 8 | Bahasa dokumentasi: Indonesia |

---

## 2. Peta dokumen (urutan baca yang disarankan)
| Urutan | File | Isi | Wajib? |
|---|---|---|---|
| 1 | `HANDOFF.md` | File ini | ✅ |
| 2 | `docs/11-konsep-game-bahasa-sederhana.md` | Seluruh konsep game dengan bahasa sederhana | ✅ |
| 3 | `docs/90-decision-log.md` | Semua keputusan + status | ✅ |
| 4 | `docs/08-arsitektur-core-combat.md` | Spesifikasi combat: tick, state, HitDef, Critical, Gear, DropZone, netcode | ✅ untuk programmer |
| 5 | `docs/09-arsitektur-sistem.md` | Engine, backend, alur lobi → match | ✅ untuk programmer |
| 6 | `docs/10-review-kritis-v3.md` | Celah yang ditemukan & cara menutupnya; kriteria spike | ✅ untuk programmer |
| 7 | `docs/research/*.md` | Hasil bedah Ikemen GO & DDNet (dengan rujukan file:baris) | Referensi |
| 8 | `docs/01`–`07` | Sejarah brainstorming, readiness, riset awal | Referensi (beberapa bagian sudah digantikan oleh 08–11) |
| 9 | `proposal/` | Generator proposal PDF untuk atasan | Opsional |

> Bila ada konflik antar dokumen: **`90-decision-log.md` > `08`/`09`/`10` > `11` > `01`–`07`**.

---

## 3. CHECKLIST — Yang sudah selesai ✅

### 3.1 Desain game (dikunci)
- [x] Visi, 5 pilar desain, target pemain, core loop (`01`, `11`)
- [x] Struktur dunia: Plaza, Battle/Relic Gate, Rest Room, Shop, Squad HQ, Dev Lounge (`01`, `04`)
- [x] Avatar ≠ Hero; kostum tidak pernah lepas; aturan siluet (`06`, `08 §8`)
- [x] Hero = Senjata + Helm + Armor + Trinket; shared humanoid rig; 2 base body; hurtbox kapsul tunggal (`08`, `10 §A4`)
- [x] Kamera: arena 3D free-roam 8 arah, quarter-view terkunci; maks 5v5 (`06`)
- [x] Guard depan 180° + Lock Facing + Pivot + Auto-Face 6 m + Guard Gauge (`08 §5.3`, `10 §E`)
- [x] Aim-assist ±22,5°; `aimYaw` dihitung client, divalidasi server (`10 §E3`)
- [x] Nyawa: Damage Gate → Critical → 3 Break Stock → KO; stock pecah = hard knockdown (`08 §7.2`)
- [x] Gear drop & pickup siapa cepat (kecuali senjata); milik match saja (`08 §7.3`)
- [x] DropZone bukan KO; gear ejection; Sky-Drop + stagger (`08 §7.4`)
- [x] Hero Swap: 3 hero, HP bersama, swap 3 s / Burst 12 s, timer bersama, terkunci saat Critical (`08 §6`)
- [x] Mode MVP: Survival (ronde 90–120 s + tie-break) dan TDM (respawn berbasis waktu match) (`10 §E2`, `§F4`)
- [x] KO & assist; heal → shield saat Critical; tanpa revive (`10 §D`)
- [x] Ekonomi: Gold/Ticket/MiCash, nol stat, sewa 7/30/permanen, rent-to-own, gacha transparan + pity (`01`, `11`)
- [x] Developer mode berbasis role server + audit log (`01`)
- [x] Rating 13+, couple room 18+ dengan verifikasi umur (`90`)

### 3.2 Arsitektur teknis (dikunci)
- [x] Stack: **Unity** (client) + **Combat Core C# murni** + **game server .NET 8 UDP** + **Nakama** (`09`)
- [x] Core data-oriented (struct + fungsi murni), fixed-point, tanpa UnityEngine, tanpa root motion (`09 §3`, `10 §A1`)
- [x] Pipeline tick 60 Hz T0–T10 (`08 §3`)
- [x] Netcode: input per tick redundan, snapshot delta 30–60 Hz, prediksi rollback, predicted hit reaction, lag compensation ≤ 150 ms (`08 §9`, `10 §A2`)
- [x] Content bundle ber-hash untuk balancing tanpa update store (`09 §5`)
- [x] Alur Lobi → Match 8 langkah + aturan keamanan (`09 §6`)
- [x] Kriteria lulus spike yang terukur (`10 §E5`, `§F7`)
- [x] Rencana cadangan: Photon Quantum bila spike gagal

### 3.3 Riset
- [x] Ikemen GO v1.0.0 — state machine, HitDef, juggle, cancel, rollback (`docs/research/state-machine-ikemen.md`)
- [x] DDNet 20.1.1 — tick, snapshot delta, prediksi, quantize (`docs/research/netcode-ddnet.md`)
- [x] LostSaga (LSRebirth) — temuan statis awal: exe & iopac.dll terproteksi → **tidak dibongkar** (`07 §E`)
- [x] AyoDance — wardrobe, sosial, lobi/room, rhythm, live-ops (`docs/research/ayodance-*.md`)

### 3.4 Tooling & infrastruktur
- [x] Repo GitHub: https://github.com/MattYudha/Nexus-Saga (branch `main`)
- [x] `.gitignore` memblokir file ekstrak game, dump, evidence REA, `.env`
- [x] REA MCP (rea-agents 6.7.0) terhubung ke Claude Code + Ghidra 12.1.4
- [x] Proposal PDF 21 halaman untuk atasan (`proposal/`, PDF lokal saja)

---

## 4. CHECKLIST — Yang BELUM ⏳

### 4.1 Belum diimplementasikan (kode)
- [ ] **Semua kode game.** Belum ada: Combat Core, game server, client Unity, backend Nakama.

### 4.2 Belum didesain detail (perlu sesi desain sebelum fasenya)
| Item | Dibutuhkan sebelum | Catatan |
|---|---|---|
| Art direction (chibi / anime / low-poly / stylized) | Fase 2 | Menentukan asset pack & pipeline |
| Daftar skill & frame data 2 hero MVP (Pegulat, Zoner) | Fase 2 | Format HitDef sudah ada di `08 §5` |
| Desain Relic (PvE): monster, loot table, peluang | Fase 3 | |
| Angka ekonomi: harga, rate gacha, pity, rent-to-own % | Fase 2 (toko Gold) / Fase 3 (gacha) | Harus disimpan sebagai data server |
| Formula MMR & Rank Points (OpenSkill) | Fase 2 | |
| Minigame (Dance Duel, mancing, kuis) | Fase 3 | |
| Squad War: aturan wilayah & hadiah | Fase 3 | |
| UI/UX flow (login, Plaza, loadout, hasil match) | Fase 2 | |
| Tutorial / onboarding | Fase 2 | |
| Audio | Fase 2–3 | |

### 4.3 Riset tertunda
- [x] **AyoDance (statis) — selesai 2026-10-24**: wardrobe + sosial/lobi/rhythm/live-ops (statis) + **observasi manual** (`docs/research/ayodance-*.md`, termasuk `ayodance-observasi.md`). 13 slot, sewa 7/30/permanen, 3 mata uang, room 6+30 terkonfirmasi
- [ ] **Observasi video LostSaga** (rekam match di LSRebirth): perilaku jatuh ke jurang, guard, gear — untuk validasi, bukan penentu
- [ ] Format arsip `.iop` LostSaga (opsional; jangan bongkar proteksi)

### 4.4 Non-teknis
- [ ] Persetujuan atasan atas proposal (PDF di `proposal/`)
- [ ] Verifikasi regulasi: klasifikasi gim (IGRS) & PSE Komdigi; aturan gacha
- [ ] Lisensi Unity sesuai ketentuan
- [ ] Pilihan payment gateway MiCash (fase akhir)
- [ ] 1 VPS uji region Asia Tenggara (untuk spike tahap akhir)

---

## 5. NEXT — Fase 1: Spike Netcode (2–3 minggu)

> **Rencana eksekusi rinci (struktur .NET, kontrak data, tiap langkah + "selesai bila") ada di [`docs/20-rencana-spike-fase1.md`](docs/20-rencana-spike-fase1.md).** Ringkasan di bawah.

**Tujuan:** membuktikan Combat Core custom + netcode terasa responsif pada lag nyata, **sebelum** produksi. Gagal → evaluasi Photon Quantum. **Spike = pure .NET headless, tanpa engine 3D** (plus Debug Viewer 2D opsional di akhir).

**Kondisi uji:** ping 150 ms, jitter 20 ms, packet loss 2%.

**Kriteria lulus** (`10 §E5`):
| # | Metrik | Target |
|---|---|---|
| 1 | Reaksi korban di layar penyerang | ≤ 1 frame setelah hit-confirm lokal |
| 2 | Hit-confirm / combat state misprediction | < 5% (koreksi gerak biasa tidak dihitung) |
| 3 | Koreksi posisi korban | < 0,5 m pada 95% kasus, dihaluskan ≤ 6 frame |
| 4 | Kapasitas server | ≥ 20 match × 10 pemain per 1 vCPU |
| 5 | Bandwidth | < 64 kbps per pemain |

### Daftar tugas spike (urut)
| ID | Tugas | Hasil (deliverable) | Selesai bila |
|---|---|---|---|
| S-00 | **Izin mulai coding** dari pemilik proyek | — | Dicatat di decision log |
| S-01 | Pasang tool: **.NET 8 SDK** (saat ini hanya runtime), Unity Hub + Unity LTS, IDE (Rider/VS/VS Code + C# Dev Kit) | Environment siap | `dotnet --list-sdks` menampilkan 8.x |
| S-02 | Struktur repo: `core/` (NexusSaga.Core, netstandard2.1), `server/` (.NET 8 console), `client/` (Unity), `tests/`, `tools/` | Solusi .NET bisa di-build | `dotnet build` & `dotnet test` hijau |
| S-03 | `FixedMath`: Fix64, FixVec3, yaw uint16, sqrt/trig deterministik | Library + unit test | Test determinisme lulus |
| S-04 | Core minimal: 2 kapsul, gerak 8 arah, lompat/gravitasi, lantai + kill-plane, `lastGroundedPos` | `Step(state, inputs) → state` | Replay input yang sama 2× → checksum identik |
| S-05 | State machine minimal: Idle, Run, Attack(1), Hit, Launched, Down, GetUp + HitDef minimal + hitbox kapsul | Data-driven (JSON) | Test transisi state lulus |
| S-06 | Format input (`moveDir`, `buttons`, `aimYaw`) & snapshot + delta + quantize | Serializer + test | Round-trip test lulus |
| S-07 | Game server: loop 60 Hz catch-up, LiteNetLib UDP, input per tick, umpan balik input-timing | Server console | 2 client terhubung |
| S-08 | Client uji (boleh console/Unity sederhana): prediksi rollback-replay lokal, interpolasi remote | Client bisa main | Gerak lokal terasa instan |
| S-09 | **Predicted hit reaction** (korban remote masuk mode prediksi saat dipukul) | Fitur | Metrik #1 tercapai |
| S-10 | Lag compensation: histori hurtbox 300 ms, rewind ≤ 150 ms | Fitur | Test hit pada lag lulus |
| S-11 | Simulasi jaringan (latency/jitter/loss) + instrumentasi 5 metrik + bot headless | Laporan angka | Semua metrik terukur |
| S-12 | Uji kapasitas: N match bot di 1 vCPU | Angka match/vCPU | Metrik #4 terukur |
| S-13 | **Uji Photon Quantum 2–3 hari** (sampel brawler) sebagai pembanding | Catatan perbandingan | Ada rekomendasi |
| S-14 | **Laporan spike** + keputusan Go/No-Go | `docs/12-laporan-spike.md` | Dicatat di decision log |

---

## 6. Jadwal setelah spike (gerbang keputusan)
Kolom "Dokumen acuan" = spesifikasi yang dibaca sebelum mengerjakan tiap fitur.

| Fase | Isi | Dokumen acuan | Gerbang masuk |
|---|---|---|---|
| **Fase 1 — Spike netcode** | Combat Core minimal + netcode (lihat §5, S-00..S-14) | `08`, `13`, `research/netcode-ddnet.md`, `research/state-machine-ikemen.md` | — |
| **Fase 2 — Vertical slice (MVP)** | Login + role; Plaza 1 distrik + chat + emote; wardrobe (13 slot, MVP subset) + toko Gold (sewa/permanen); arena 1v1 & 2v2, 2 hero; Critical/Gear Drop/DropZone/Hero Swap; MMR + tier + profil; panel developer + audit log; **hitbox editor Unity**; **abstraksi input (touch-ready)** | `13` combat · `14` auth/matchmaking/MMR/lobby · `15` player/hero/gear/shop · `17` hero/training · `18` FE/BE/3D/anim/VFX | Spike lulus |
| **Fase 3 — Konten & sosial** | Squad + Squad War + Top Squad + Community Lobby; Relic; Rest Room minigame (Chase/Tag, Brawl Ball, Target, Fashion Contest, Fishing, Photo Booth, Arcade non-judi); gacha + pity; battle pass; quest; hero ke-3 (Support); 5v5 penuh; chat/friends/messenger penuh | `16` squad/komunitas · `14 §5–7` leaderboard/sosial/chat · `15 §9–10` gacha/quest · `12` rest room · `17` bot | MVP playtest lulus |
| **Fase 4 — Live-ops, mobile & kosmetik lanjutan** | Season, event mingguan, content bundle CDN; **build mobile (Android/iOS, IAP)**; **backlog kosmetik** (bawah); Mount Racing | `18 §8` scaling mobile · `14` · `15` | Siap rilis |

Durasi Fase 2+ **belum ditetapkan** — diestimasi dari data hasil spike.

### Peta dokumen → sistem (untuk yang melanjutkan)
| Sistem | Dokumen |
|---|---|
| Arsitektur besar, FE/BE scope, 3D/animasi/VFX, world, scaling mobile, flowchart | **`18`** |
| Combat core & data combat | `08`, `13` |
| Backend meta (Nakama): auth, matchmaking, MMR, lobby/room, leaderboard, sosial, chat | `14` |
| Player/profile/hero/gear/shop/gacha/quest | `15` |
| Squad/guild/war/top-squad/community/couple | `16` |
| Hero roster/training/bot | `17` |
| Rest Room (tanpa dance) | `12` |

### Backlog kosmetik "pamer avatar" (dikerjakan BERTAHAP di akhir, setelah fungsi inti jalan)
Semua **nol stat** (keputusan 2026-10-24). Tidak menghalangi jalur utama; dikerjakan setelah combat + wardrobe dasar + sosial inti terbukti.
| Kategori | Isi | Prasyarat | Fase |
|---|---|---|---|
| Emote duduk / hangout | Variasi gaya nongkrong untuk campfire/arcade | Hub pasif + sistem emote | akhir Fase 3 |
| Efek pijakan / aura langkah | Jejak visual saat lari/lompat (pengganti DJ Booth) | Rest Room Chase/Brawl Ball jalan | akhir Fase 3 |
| Mount / kendaraan ringan | Skateboard/hoverboard/rollerblade (nol stat); + Mount Racing | Kategori wardrobe mount + kontrol kendaraan | Fase 4 |

Catatan: MVP (Fase 2) cukup **hub pasif + emote dasar**. Sisa Rest Room & backlog kosmetik menyusul.

---

## 7. Setup di device baru

### 7.1 Ambil repo
```
git clone https://github.com/MattYudha/Nexus-Saga.git NyxCreats
```

### 7.2 Tool yang dibutuhkan
| Tool | Untuk | Status di device lama (2026-10-24) |
|---|---|---|
| Git | Repo | ✅ 2.47 |
| **.NET 8 SDK** | Core & server | ❌ **Belum** (hanya runtime) |
| Unity Hub + Unity LTS | Client | ❌ Belum |
| Python 3.11 + `reportlab`, `pypdf`, `pypdfium2` | Generator proposal PDF | ✅ |
| Node.js 24 | REA (via npx) | ✅ |
| Go 1.25 | Modul runtime Nakama | ✅ |
| Docker Desktop | Nakama + Postgres lokal | ❌ Belum (Postgres lokal tersedia sebagai alternatif) |
| JDK 21 atau 25 + **Ghidra 12.1.x** | REA dekompilasi (riset saja) | ✅ (REA 6.7.0 **hanya** menerima Ghidra 12.1.x, bukan 12.2) |

### 7.3 Bahan riset (TIDAK ada di repo — lokal saja)
| Bahan | Lokasi di device lama | Cara mendapatkan di device baru |
|---|---|---|
| Source Ikemen GO v1.0.0 | `C:\Users\US3R\Nexus_Lab\src\Ikemen-GO` | `git clone --depth 1 --branch v1.0.0 https://github.com/ikemen-engine/Ikemen-GO.git` |
| Source DDNet 20.1.1 | `C:\Users\US3R\Nexus_Lab\src\ddnet` | `git clone --depth 1 --branch 20.1.1 https://github.com/ddnet/ddnet.git` |
| Ikemen GO rilis (data `kfm`, `common1.cns.zss`) | `C:\Users\US3R\Nexus_Lab\Ikemen_Go-v1.0.0` | Unduh rilis v1.0.0 |
| AyoDance client | `C:\Megaxus\AyoDance` | Installer resmi |
| LostSaga client | `C:\Program Files (x86)\LSRebirth` | Installer |
| Proposal PDF | `NyxCreats\proposal\` (untracked) | `python proposal/build_proposal.py <output.pdf>` (butuh font Segoe UI → Windows) |

### 7.4 REA (opsional, hanya untuk riset biner)
Registrasi MCP di Claude Code (pakai `MSYS_NO_PATHCONV=1` jika lewat Git Bash, karena `/d /c` bisa berubah jadi `D:/ C:/`):
```
claude mcp add rea -s user -e GHIDRA_INSTALL_DIR=<path ghidra_12.1.x> -e JAVA_HOME=<path JDK> -- cmd /d /c npx -y rea-agents@6.7.0 mcp
```
Lalu restart Claude Code.

---

## 8. Melanjutkan dengan Claude Code
Buka sesi baru di folder repo, lalu katakan:
> "Baca HANDOFF.md, docs/11, dan docs/90-decision-log.md. Kita lanjut Fase 1 mulai dari tugas S-00."

Claude akan memakai dokumen ini sebagai sumber kebenaran.

---

## 9. Kontak & kepemilikan
- Pemilik proyek / solo architect: pemilik repo `MattYudha/Nexus-Saga`
- Keputusan desain hanya sah bila tercatat di `docs/90-decision-log.md`



