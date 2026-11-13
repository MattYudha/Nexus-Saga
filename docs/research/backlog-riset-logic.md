# Backlog riset logic — apa yang dipelajari, dari mana, kapan dipakai (2026-11-13, dirapikan)

Aturan: **logic & formula boleh dipelajari lalu ditulis ulang**; **aset tidak diambil** dari game komersial.

**Status = status RISET, bukan status game.**
`riset ✅` dokumen/angka sudah ada · `riset 🟡` sebagian · `riset ⬜` belum.
Apakah fitur sudah ada di game → lihat `docs/00-ROADMAP.md` (Selesai/Sedang/Antre/Diblok).

**Kapan dipakai** (ikut antrean `PROGRESS.md`, tidak mengubahnya):
`M` = milestone aktif "Ranked 1v1 end-to-end" (T2, poin d–e, poin g) ·
`S` = setelah milestone (Fase 2–5, Street Room, Battle, Survival) ·
`A` = fase produksi aset (model, animasi, suara, VFX) ·
`R` = menjelang rilis (ekonomi, regulasi).

Sumber kunci:
`IK` = Ikemen GO v1.0.0 (MIT) · `NAK` = Nakama (Apache-2.0) · `COL` = Colyseus (MIT) ·
`EFF` = Effekseer (MIT) · `SL` = SoLoud (zlib) · `MA` = miniaudio (MIT-0) · `OD` = OpenDota (MIT) ·
`DK` = Dota 2 Wiki/Liquipedia/dev blog (dokumentasi publik, hanya untuk konsep) · `GD` = GDC/paper.
`OB` = OpenBOR — **lisensi belum diverifikasi, jangan dipakai sebagai sumber sampai dicek.**

---

## Urutan riset menurut antrean
| Urutan | Domain | Kapan | Untuk apa |
|---|---|---|---|
| 1 | §1 Combat logic | M (T2) | Critical/Overload, hitstop, juggle |
| 2 | §2 Battle & alur match | M (T2) | batas waktu, AFK forfeit (**angka diputus user**) |
| 3 | §10 Netcode/replay | M (poin g) | checksum, kartu Disputed |
| 4 | §8 Room, §9 Matchmaking | S | Street Room, party, sosial Fase 2–4 |
| 5 | §3 Hero/ability, §4 Animasi | S/A | hero ke-3+, pipeline animasi |
| 6 | §5 Map, §6 Sound, §7 VFX | A | produksi aset |
| 7 | §11 Ekonomi | R | shop, gacha, regulasi |

---

## 1. Combat logic (inti brawler) — `M`
| Kebutuhan | Sumber | Yang diambil | Artefak | Status |
|---|---|---|---|---|
| Urutan fase per tick, hit resolve | `IK` system.go:2794+ | urutan push→hit→paksa getup | `ikemen-extract/README`, state-machine | riset ✅ |
| Frame data & hitstop | `IK` HitDef | rasio startup/active/recovery, pausetime | `combat-tuning.json` | riset ✅ |
| Cancel window & combo route | `IK` state -1 | model tertutup + validator graf | `01 §4.3` | riset ✅ |
| Guard gauge, armor, counter hit | (tidak ada di IK) | desain sendiri, angka di JSON | `03` | riset 🟡 |
| Juggle budget | `IK` targetedBy | per-penyerang vs S1 | `03 §6.4` | riset 🟡 — **butuh keputusan user** |
| Hit reaction lanjutan (wall hit, bounce) | `IK` down.bounce + `GD` | kurva bounce, damage | `combat-tuning.json` | riset 🟡 |
| Priority/trade & throw tech | `IK` char.go:10706-10790 | mekanisme trade | `03 §4` | riset 🟡 |
| Readability/juice | `IK` EnvShake/hitspark | parameter, bukan seni | `02` | riset ✅ |

## 2. Battle & alur match — `M`
| Kebutuhan | Sumber | Yang diambil | Status |
|---|---|---|---|
| Statemachine match (countdown→playing→over) | `IK` roundState | 4 fase lifecycle | riset ✅ `battle-flow/01 §1` |
| Batas waktu match + sudden death | `IK`, docs/24 | aturan waktu habis + draw | riset 🟡 `battle-flow/01 §3` |
| AFK/forfeit | `DK`, `GD` | grace→forfeit, tanpa bot di ranked | riset 🟡 `battle-flow/01 §4` (T2 = deteksi) |
| Skor & kondisi menang | docs/24, docs/32 | per-mode + sebab menang (`winTrigger`) | riset ✅ `battle-flow/01 §2` |
| Rematch/alur antrean | `NAK`/`OM` docs | ranked tidak, casual boleh | riset 🟡 `battle-flow/01 §4` |

## 3. Hero & ability (dipangkas untuk brawler) — `S`
Hanya konsep yang relevan untuk brawler 1v1–3v3. **Sistem khas MOBA** (tipe damage physical/magical/pure,
rumus armor, kategori dispel, modifier stacking kompleks) **tidak diriset** sampai ada hero yang
benar-benar membutuhkannya — risiko scope.

| Kebutuhan | Sumber | Yang diambil | Status |
|---|---|---|---|
| Skill data-driven (cast point, backswing, cooldown, cost) | `DK` (konsep) + `IK` HitDef | skema field + angka acuan | riset ⬜ |
| Cancel animasi skill | `DK`, `IK` | jendela cancel, tradeoff | riset ⬜ (sebagian di §1) |
| Turn rate & facing | `DK` | konsekuensi gerak/aim di 3D | riset ⬜ |
| Status effect sederhana (stun, slow, armor) | `IK` | daftar minimal, durasi deterministik | riset ⬜ |
| Arketipe kit hero (grappler/zoner) | docs/17 | komposisi kit, bukan hero | riset 🟡 |
| Bot AI (utility / behavior tree) | `GD` (GDC AI talks) | pola keputusan sederhana | riset ⬜ (prioritas Critical = T2) |

## 4. Animation — `S`/`A`
| Kebutuhan | Sumber | Yang diambil | Status |
|---|---|---|---|
| Animasi data-driven (tick, bukan klip) | `IK` `.air`/ANIM | struktur frame + trigger | riset ✅ (`01 §4.5`) |
| Hit reaction (flinch, launch, getup) | `IK` common states | daftar state wajib | riset 🟡 |
| Blending & additive layer | Unity docs, `GD` | aturan layer, bobot | riset ⬜ |
| Root motion dilarang → in-place + data | docs/10 | aturan | riset ✅ |
| Animasi mocap legal | Mixamo, Rokoko, Move.ai | sumber aset | riset 🟡 (docs/21) — `A` |
| Kompresi animasi | `GD` ACL (MIT) | teknik | riset ⬜ — `A` |

## 5. Map / stage — `A`
| Kebutuhan | Sumber | Yang diambil | Status |
|---|---|---|---|
| Layout arena (batas, tinggi, hazard) | `GD` map design talks, `IK` stage | prinsip layout | riset ⬜ |
| Batas kamera bergantung zoom | `IK` camera.Reset | rumus | riset ✅ (`06`) |
| Modul map (kit-bash) | Kenney/Quaternius/Synty | aset berlisensi | riset ⬜ |
| Lighting/HDR | Poly Haven (CC0) | HDRI | riset ⬜ |
| Rotasi map/hazard | — | desain sendiri | riset ⬜ |

## 6. Sound — `A`
| Kebutuhan | Sumber | Yang diambil | Status |
|---|---|---|---|
| Layering (whoosh/impact/voice) | `IK` hitspark+SFX, `GD` | aturan prioritas | riset ✅ (`02 §7`) |
| Ducking & bus (SFX vs VO vs musik) | FMOD/Wwise docs, Unity Audio Mixer | snapshot/bus | riset ⬜ |
| Announcer & VO | lisensi/komisi | aset | riset ⬜ |
| ~~Audio DSP presisi + kalibrasi latensi perangkat~~ | `SL`, `MA` | — | **ARSIP** — kebutuhan mode ritme (docs/12) |

## 7. VFX — `A`
| Kebutuhan | Sumber | Yang diambil | Status |
|---|---|---|---|
| Hit spark & guard spark | `IK` | parameter & posisi kontak | riset ✅ (`02 §4`) |
| Pooling & VFX event-driven (di luar sim) | Quantum docs | pola | riset ✅ (`02 §1`) |
| Telegraph (awalan skill terbaca) | `GD` readability | prinsip | riset ⬜ |
| Runtime VFX: VFX Graph/Particle System bawaan **vs** Effekseer | Unity docs, `EFF` | perbandingan | riset ⬜ — **Effekseer = plugin baru → keputusan user** |
| Trail/impact berlisensi | Unity Asset Store | aset | riset ⬜ |

## 8. Room & sosial — `S`
Nakama/Colyseus dipelajari **polanya saja** — bukan pilihan stack. Stack realtime menunggu **K-11 (docs/36)**.

| Kebutuhan | Sumber | Yang diambil | Status |
|---|---|---|---|
| Model room (owner, slot, ready, kick) | `NAK`, `COL` docs | state machine room | riset ⬜ |
| Chat channel & moderasi | `NAK` docs, docs/36 | mute/block, filter | riset 🟡 (K-11) |
| Party/lobby & invite | `NAK` | alur | riset 🟡 |
| Emote/pose & photo mode | docs/12 | desain | riset 🟡 |
| Room browser (Street Room 1v1–3v3) | docs/00-ROADMAP, docs/24 §10a | filter, kapasitas | riset 🟡 |

## 9. Matchmaking — `S`
Antrean tetap di backend ASP.NET yang sudah jalan. **Open Match tidak dipakai** (butuh Kubernetes, kebesaran
untuk skala kita); dokumentasinya boleh dibaca untuk konsep perluasan window.

| Kebutuhan | Sumber | Yang diambil | Status |
|---|---|---|---|
| Rating (Glicko-2) | paper Glicko-2 | formula, RD, placement | riset ✅ — **sudah di game** (docs/33) |
| Leaderboard & tie-break | docs/33 | urutan tier-first | riset ✅ — **sudah di game** |
| Perluasan window, party MMR | `DK` dev blog | aturan | riset ⬜ |
| Isi bot saat sepi | docs/00-ROADMAP | kebijakan | riset 🟡 |
| Behavior/abandon score | `DK` dev blog | indikator + penalti | riset ⬜ |
| Anti-abuse (smurf, win-trade) | `OD` (pola data), `DK` | heuristik | riset ⬜ — `R` |

## 10. Netcode, replay, anti-cheat — `M` (poin g) / `S`
| Kebutuhan | Sumber | Yang diambil | Status |
|---|---|---|---|
| Determinisme & rollback | `IK` rollback.go, Quantum | urutan frame, input log | riset ✅ (`04`) |
| Checksum/desync | `IK` LiveChecksum, Quantum checksum | CRC state ringkas | riset ✅ — `M` |
| Validasi hasil di server | Quantum plugin docs | arsitektur | riset 🟡 — `M` |
| Kartu Disputed | docs/32 | alur UX+backend | riset 🟡 — `M` (poin g) |
| Spectator & killcam | `IK` replay | delay & rewind | riset ✅ — `S` (belum ada di game) |

## 11. Ekonomi & telemetri — `R`
| Kebutuhan | Sumber | Status |
|---|---|---|
| Currency sink/source, rent-to-own | docs/15 | riset 🟡 |
| Gacha & tampilan peluang (IGRS, aturan Indonesia) | regulasi + docs/15 | riset ⬜ |
| Telemetri combat (heatmap, durasi match) | `OD` (pola data), docs/32 | riset ⬜ |

---

## Aturan main penggarapan
1. **Ikuti urutan di atas**; domain `S`/`A`/`R` baru diriset saat antrean PROGRESS sampai ke sana.
2. Satu sesi = satu domain. Jangan campur combat dan matchmaking.
3. Tiap tabel diisi **angka** + sumber berlabel (OBSERVED/DERIVED/PROPOSED); tabel tanpa angka = belum selesai.
4. Butuh sesuatu yang hanya ada di client komersial → tulis "buat sendiri" + estimasi biaya, jangan cari jalan pintas.
5. Hasil riset masuk `docs/research/<domain>/` dan dirujuk dari `docs/90`. **Riset tidak menyentuh kode**;
   kode masuk lewat item antrean (mis. T2), dan field `.qtn` baru ditambah hanya bila ada sistem yang memakainya.
6. Keputusan yang muncul dari riset (juggle, Effekseer, angka AFK) **tidak diputus sendiri** — catat sebagai
   pertanyaan untuk user.
