# 01 — Spesifikasi T2: aturan & angka (usulan, belum disetujui)

Domain: persiapan **T2** (antrean berikutnya). Keluaran dokumen; **tidak ada kode diubah**.
Tujuan: begitu CodeGen selesai, T2 bisa dieksekusi tanpa menebak angka.

Sumber: `PROGRESS.md` (T2), `docs/90` 2026-10-24 (C1/C4), `docs/32`, kode `NxCombatSystem.cs` +
`NxDamage.cs` (OBSERVED). Angka = **PROPOSED**, butuh persetujuan user.

## Ringkasan
1. **KO hanya lewat 3 Break Stock** → bleed-out (`CritTimer`, 240 tick) dihapus, bukan diperpanjang.
2. **C4 = tekanan, bukan hukuman mati**: gerak melambat bertingkat + **Overload** saat lawan mendiamkan.
3. Semua ambang dihitung **tick** dan disimpan di `NxCombat`, supaya bisa dibandingkan antar-klien.
4. Bot harus **berhenti mengabaikan target Critical** — ini akar bug 5v5.
5. **`koTimeline` maks 9 hanya benar untuk Ranked 1v1**; untuk mode lain kapasitas harus berbeda (§6).

## 1. Menghapus bleed-out (OBSERVED → PROPOSED)
| Sekarang (`NxCombatSystem.cs`) | Setelah T2 |
|---|---|
| `c->CritTimer++` tiap tick; >=240 (4 dtk) -> auto-KO | `CritTimer` **dihapus dari logika** (field boleh tetap sampai CodeGen) |
| Atribusi kill ke `LastHitBy*` | tidak ada lagi kill bleed-out |
| Invariant kills A = deaths B terjaga karena semua KO punya pembunuh | tetap, lebih sederhana |

Konsekuensi: pemain **tidak bisa** lolos dari Critical dengan kabur. Ini memperbaiki deadlock yang kamu catat.

## 2. Penalti gerak saat Critical (C4)
| Kondisi | Sisa stock | Kecepatan | Dash |
|---|---|---|---|
| Normal | 4 (di luar Critical) | 100% | bebas |
| Masuk Critical | 3 | **70%** | **dikunci** |
| Stock berkurang 1 | 2 | **50%** | boleh |
| Stock berkurang 2 | 1 | **35%** | **dikunci** |
| Stock ke-3 | 0 | — | **KO** |

Aturan: penalti **tidak** mengubah `MoveSpeed` global — hanya mengalikan saat `Critical == 1`, supaya hero
lain/tim tidak terpengaruh. Dash terkunci = `DashCd` diisi nilai besar deterministik, bukan flag baru.

## 3. Overload (anti-camping)
| Parameter | Usulan | Alasan |
|---|---|---|
| Ambang | **480 tick (8 dtk)** tanpa damage masuk saat Critical | cukup lama untuk merasa aman, cukup pendek agar tidak jadi exploit |
| Efek | **terkunci 90 tick (1,5 dtk)**: tidak bisa gerak/guard/serang | sesuai permintaan |
| Kerentanan | **TIDAK ADA pengali damage** (dihapus user) | pengali justru membuat menunggu Overload lebih untung daripada menyerang |
| Bukan KO | ya | tidak menambah jalan KO baru |
| Reset | setiap kena damage; setelah lock selesai timer mulai 0 | mencegah lock berulang tanpa interaksi |
| Indikator | ikon Overload di HUD lawan + VFX di kaki | keterbacaan |

Determinisme: 480/90/1.2 semuanya integer/FP di data, bukan `Time.time`.

## 4. Bot memprioritaskan target Critical
Sekarang: `DummyAi` memilih musuh terdekat (`NxCombatSystem.cs:280-290`). Usul skor:
```
skor = jarakKuadrat
      - 40  bila target Critical
      - 80  bila target sedang Overload-lock
      + 30 x (jumlah penyerang lain yang sudah menargetkan dia)
```
Pilih skor **terkecil**; seri -> `EntityRef.Index` terkecil. Semua integer -> deterministik.
Efek: bot berhenti menumpuk di satu target sehat sambil membiarkan target Critical berdiri.

## 5. AFK / forfeit (angka usul — ini yang kamu minta diputus)
| Parameter | Usulan | Alasan |
|---|---|---|
| Peringatan HUD | **15 dtk** tanpa input | diputus user: 8 dtk terlalu cepat |
| Ambang forfeit | **30 dtk** akumulatif (tidak harus berurutan) | menangkap pemain yang spam disentuh sebentar |
| Reset | gerak **atau** lompat **atau** guard **atau** dash **atau** serang **atau** skill. Tukar hero & mouse TIDAK dihitung | pemain yang murni bertahan tidak boleh dianggap AFK |
| Konsekuensi | match berakhir, **lawan menang**; skor dibekukan; rating dihitung normal | lebih jelas daripada match batal |
| Penalti berulang | 3 match beruntun kena forfeit -> 30 mnt tidak bisa antre Ranked | konservatif, bisa diperketat |
| Bot menggantikan | **tidak** di Ranked; ya di Battle casual | mencegah farming rating |

T2 hanya mendeteksi & mengakhiri; hukuman beruntun boleh ditunda (butuh backend).

## 6. `koTimeline` — masalah kapasitas (TEMUAN)
Permintaan awal: array maks **9** entri. Itu cukup **hanya** untuk Ranked 1v1 first-to-5 (maks 5+4 = 9 KO).
Mode lain: Battle 3v3 target 10 -> sampai 19; Faction War 5v5 -> 29.

| Opsi | Konsekuensi |
|---|---|
| (a) kapasitas per mode: 9 / 21 / 29 | paling benar, ukuran komponen naik |
| (b) tetap 9 + `TotalKos` terpisah | entri tertua dibuang; tab Jalannya Match tidak lengkap |
| (c) simpan 9 KO **terakhir** + `TotalKos` | cukup untuk killcam/ringkasan, aman semua mode |

Usul: **(c)** untuk MVP, naik ke (a) bila tab Jalannya Match ingin lengkap.
Skema: `{ ushort Tick; byte KillerSlot; }` x 9 + `ushort TotalKos`, disimpan di `global`.

## 7. Tes & invariant yang harus hijau
| # | Tes | Harapan |
|---|---|---|
| 1 | Critical 30 dtk tanpa disentuh | tidak KO; Overload terpicu; skor tidak berubah |
| 2 | Kena pukul saat Overload | timer reset, lock berhenti |
| 3 | Sisa stock 2 / 1 | kecepatan 50% / 35%, dash sudah terkunci sejak Critical |
| 4 | KO ketiga | match selesai, pemenang benar, tidak ada KO tambahan |
| 5 | Bot vs 1 sehat + 1 Critical | bot memilih yang Critical |
| 6 | `koTimeline` | panjang = `TotalKos`, tick monoton naik, killer valid |
| 7 | Invariant 1v1 | kills A = deaths B, selalu |
| 8 | Dua sim klien | `koTimeline` + skor identik (desync = 0) |

## 8. Yang TIDAK diubah T2
- `docs/32` sengaja tetap menggambarkan kode sekarang (bleed-out) sampai T2 mendarat — jangan diperbaiki dulu.
- Guard/crush (`Faint` 90 tick, gauge 34/hit) tidak disentuh.
- Tidak ada sistem modifier, armor, atau tipe damage (arsip pasca-MVP).
- `.qtn`: hanya field yang **dipakai** T2 (`IdleTicks`, `KoSlowTicks` bila dipakai, `TotalKos`/`KoTick[]`).

## 9. KEPUTUSAN FINAL (disetujui user 2026-11-13)
1. ~~AFK: 15 dtk peringatan / 30 dtk forfeit akumulatif~~ → **DIGANTIKAN 2026-11-13 (user, NX-11): 10 dtk peringatan / 20 dtk berturut-turut → forfeit**; guard/gerak/dash/serang/skill dihitung aktif. Lihat docs/90.
2. Overload: **8 dtk -> lock 1,5 dtk, TANPA pengali damage**. ✅
3. `koTimeline`: **kapasitas per mode** (9 / 19 / 29) + `TotalKos`; fallback satu kapasitas tetap 29 bila array merepotkan. ✅
   **Implementasi ditunda**: sintaks array di `.qtn` belum terverifikasi di proyek ini (lihat laporan).
4. Penalti gerak: **70% sejak masuk Critical**, 50% (stock 2), 35% (stock 1), **dash terkunci sejak masuk Critical**. ✅
