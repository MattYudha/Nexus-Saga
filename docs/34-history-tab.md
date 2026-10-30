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

## DETAIL MATCH v2 (klik kartu) — komponen `mode = history | result` (gaya post-match Wild Rift, adaptasi 1v1)
Overlay **layar penuh OPAK** (di-reparent ke `profile-root` → **sembunyikan sidebar + tombol Back profil**; satu tombol saja). Dibangun sebagai komponen; **wiring ke NexusGame sebagai LAYAR HASIL (mode result) = item antrean terpisah (poin e)**.
- **Banner**: skor KAMU (kiri, `--nx-team-ally`) · "MENANG" emas 56px / "KALAH" abu-baja · skor LAWAN (kanan, `--nx-team-enemy`), semua 64px. Meta (`RANKED · tgl · durasi`) **baris sendiri** 16px — tidak overlap. (Label EndReason menyusul.)
- **Kolom pemain** (kiri KAMU biru / kanan LAWAN merah): header kolom, **potret hero netral setinggi kolom** (tinggi eksplisit, `--nx-hero-neutral`, desaturate bila kalah), nama 28px, baris tier (emblem+nama), baris hero — **masing-masing baris sendiri** (tidak bertabrakan). Badge jarak 8px (tidak menempel tepi). **Poin Ladder** (ranked): kolom kamu = bar progres + delta (mode result: isi animasi 0,8 dtk + "NAIK TIER!"); lawan = delta kecil.
- **Tab Ringkasan** = baris **tug-of-war** tinggi ±48px: label 16px tengah atas, **satu bar** (kiri biru = a/(a+b), kanan merah = sisa; **a=b=0 → abu netral**), nilai di kedua ujung 22px PUTIH (sisi lebih besar bold). **Warna ikut SISI, bukan baik/buruk. TANPA emas.**
- **Baris (1v1, tanpa cermin ganda)**: KO · Damage diberikan · Critical · Guard crush · **Gear drop (baru)** · Dodge berhasil · Serangan di-guard · Akurasi skill (`skillsUsed=0` → **"–"**) · Kill streak. **DIHAPUS**: "Damage diterima" & format K/D ganda (cermin di 1v1). Data lama/tak terdefinisi → "–".
- **Tab "Jalannya Match" DISEMBUNYIKAN** sampai data `koTimeline` ada (T2) — tanpa dummy.
- **Footer**: Match ID + Salin (kiri); satu tombol kanan — history: **KEMBALI** (sekunder, Esc) · result: **LANJUT** (oranye CTA). Semua warna dari token, teks ≥16px.

## KONSISTENSI
Riwayat & Rekaman Battle pakai `/api/matches` + aturan sama (format, Poin Ladder, badge). Lihat [[docs/32]] (stats/format), [[docs/33]] (Poin Ladder).

## REVISI 2026-10-30 (desain ulang)
- **BUG Poin Ladder terbalik DIPERBAIKI**: rating di DB BENAR (pemenang +, kalah −). Penyebab tampilan = `LadderPoints` per-tier (0–100) reset di batas tier. Sekarang pakai **`LadderPointsGlobal` = tier*100 + poin** (monotonik) untuk DELTA → pemenang selalu +, kalah selalu −. Tes backend: pemenang `ratingDelta>=0`, kalah `<=0`.
- **BUG FLAWLESS**: kini tampil di kartu DAN Detail (sisi pemenang, dari skor 5-0).
- Kartu 280×548, STRIP RINGKASAN ("N match: W Menang · L Kalah · WR% · Poin Ladder ±X"), art full-bleed + desaturate KALAH + banner nama + hero ke-2 bulat, skor 32px, K/D ikon pedang/tengkorak, durasi "–" bila kosong, nav ‹ › bulat 48px di luar jalur + scroll halus + sembunyi di ujung, hover angkat+glow+art scale.
- ~~Detail v1: dua sisi + statistik cermin~~ → **diganti Detail Match v2** (2026-10-30, lihat bagian "DETAIL MATCH v2" di atas) karena tes editor menemukan header/tier/hero bertumpuk, art hero kolaps, FLAWLESS hilang, bar bukan tug-of-war, angka kiri emas, teks <16px, dua tombol kembali + sidebar terlihat, akurasi 0% semestinya "–", dan baris cermin mubazir di 1v1.
- **DITUNDA (poin e)**: wiring Detail Match v2 sebagai **LAYAR HASIL** (mode `result`, animasi Poin Ladder + tombol LANJUT) ke NexusGame menggantikan IMGUI. Komponen sudah siap dua mode; tinggal pemicunya.
- **CATATAN T2**: tambahkan `koTimeline` ke payload sim = array maks 9 `{tick, killerSlot}` (deterministik, dibandingkan antar-klien, disimpan per match). Setelah ada → aktifkan tab **"Jalannya Match"** (grafik tangga skor kamu vs lawan terhadap waktu, Painter2D, garis biru/merah + penanda KO, strip timeline ala Wild Rift). Sampai itu, tab disembunyikan (tanpa dummy).

## STATE KHUSUS
- `legacy5v5`: tag "FORMAT LAMA", K/D "–".
- Disputed: **belum tampil** (`/api/matches` hanya `Finished`). Nanti: surface Disputed sebagai kartu abu "TIDAK DIHITUNG".

## FILE
`ProfileTabHistory.uxml`, `ProfileController.cs` (region Tab RIWAYAT), USS `.nxl-hist-*`/`.nxl-hero-*`/`.nxl-badge*`/`.nxl-detail-*` di `NexusLobby.uss`, sprite `Sprites/hero_*.png`.
