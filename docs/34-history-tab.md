# 34 — Tab Riwayat (History) + Detail Match

Kartu match gaya Mobile Legends, diadaptasi NEXUS SAGA. Sumber: `/api/matches` (sama dengan Rekaman Battle lobby).

## KARTU (240×420, scroll horizontal)
- Header MENANG (emas) / KALAH (**abu-baja**, bukan merah — merah hanya utk lawan) + label mode (RANKED/BATTLE/LATIHAN) + badge PARTY (partySize>1).
- Gambar hero besar = hero dominan (`heroId`); hero lain (ganti hero) = ikon kecil. Placeholder **netral + ikon kelas** (grappler/zoner) — token `--nx-hero-neutral`; `hero_titan/pulse/unknown.png` akan diregen netral (T1, sprite menyusul). **Ganti dengan art asli kapan saja.**
- Rank (ranked saja): emblem tier sebelum→sesudah + **Poin Ladder** Δ (bukan MMR). Naik tier → "NAIK TIER!" emas; turun → redup. Pakai `ratingBefore` + `ratingDelta` → `NexusRankConfig.LadderPoints`.
- K·D·A (assist disembunyikan di 1v1). **K/D "–" untuk non-`ranked1v1`**.
- Badge: FLAWLESS (menang 5-0), COMEBACK (`maxDeficit≥3`), FIRST BLOOD. Tanpa MVP di 1v1.
  - **Warna (T1, docs/90)**: badge = **satu chip netral** (bidang steel-dim `--nx-badge-bg`, teks putih), dibedakan **ikon + label** — **tanpa merah** (merah=lawan) & **tanpa hijau** (hijau=perolehan). Pengecualian: **FLAWLESS** garis emas tipis (prestise menang). (Ikon per-badge menyusul.)
- Tag "FORMAT LAMA" untuk `legacy5v5`. Footer: tanggal + durasi. TANPA baris item.
- **Grafik rank/WR (T1)**: garis data = **biru `--nx-team-ally`** (kamu); **band tier = emas redup** (-dim); **titik fokus/sekarang = cyan** (cyan HANYA utk fokus). Placeholder hero = **netral + ikon kelas** (Grappler=kepalan, Zoner=crosshair), nama samar (TITAN/PULSE).

## INTERAKSI
Filter Semua/Ranked/Battle (kanan atas). Scroll horizontal + panah ‹ › di sisi. Hover: kartu terangkat + glow.
(Belum: lazy-load 20+auto, drag, roda mouse — UI Toolkit ScrollView sudah dukung roda; drag/lazy menyusul.)

## DETAIL (klik kartu) — juga LAYAR HASIL pasca-match
Header MENANG/KALAH (KALAH=abu-baja) + skor + durasi. Dua sisi: BIRU (kamu) vs MERAH (lawan) — nama, tier, hero (+waktu/hero), K/D/A, Poin Ladder Δ. Statistik mekanik untuk `ranked1v1`: damage diberikan/diterima, guard crush, critical, dodge, serangan di-guard, akurasi skill (`skillsHit/skillsUsed`), kill streak, first blood. Data lama → "–". Match ID + Salin, tombol KEMBALI (Esc).

## KONSISTENSI
Riwayat & Rekaman Battle pakai `/api/matches` + aturan sama (format, Poin Ladder, badge). Lihat [[docs/32]] (stats/format), [[docs/33]] (Poin Ladder).

## REVISI 2026-10-30 (desain ulang)
- **BUG Poin Ladder terbalik DIPERBAIKI**: rating di DB BENAR (pemenang +, kalah −). Penyebab tampilan = `LadderPoints` per-tier (0–100) reset di batas tier. Sekarang pakai **`LadderPointsGlobal` = tier*100 + poin** (monotonik) untuk DELTA → pemenang selalu +, kalah selalu −. Tes backend: pemenang `ratingDelta>=0`, kalah `<=0`.
- **BUG FLAWLESS**: kini tampil di kartu DAN Detail (sisi pemenang, dari skor 5-0).
- Kartu 280×548, STRIP RINGKASAN ("N match: W Menang · L Kalah · WR% · Poin Ladder ±X"), art full-bleed + desaturate KALAH + banner nama + hero ke-2 bulat, skor 32px, K/D ikon pedang/tengkorak, durasi "–" bila kosong, nav ‹ › bulat 48px di luar jalur + scroll halus + sembunyi di ujung, hover angkat+glow+art scale.
- Detail: full OPAK, header MENANG/KALAH 48px + skor 56px diapit nama, dua sisi (biru/merah) hero besar + tier + hero/waktu/% + Poin Ladder + badge, **statistik cermin tug-of-war** (K/D, damage, guard crush, critical, dodge, blocked, akurasi skill, kill streak), footer Match ID+Salin / KEMBALI.
- **DITUNDA**: layout Detail sebagai LAYAR HASIL pasca-match (butuh wiring NexusGame → UITK; sekarang hasil masih IMGUI). Placeholder art hero di-regen bergaya (ikon kelas TITAN fist / PULSE crosshair + nama samar).

## STATE KHUSUS
- `legacy5v5`: tag "FORMAT LAMA", K/D "–".
- Disputed: **belum tampil** (`/api/matches` hanya `Finished`). Nanti: surface Disputed sebagai kartu abu "TIDAK DIHITUNG".

## FILE
`ProfileTabHistory.uxml`, `ProfileController.cs` (region Tab RIWAYAT), USS `.nxl-hist-*`/`.nxl-hero-*`/`.nxl-badge*`/`.nxl-detail-*` di `NexusLobby.uss`, sprite `Sprites/hero_*.png`.
