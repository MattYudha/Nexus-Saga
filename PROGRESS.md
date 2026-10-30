# PROGRESS — Nexus Saga: Chronicles

> **BACA FILE INI DULU sebelum memilih tugas apa pun** (terutama setelah conversation di-compact).
> Urutan antrean di bawah **tidak boleh diubah tanpa persetujuan user**. Kerjakan dari atas,
> lapor di akhir setiap poin. Repo: `NyxCreats` = docs/rencana, `photon-backend` = kode (backend + game Quantum).

---

## 🔢 ANTREAN PRIORITAS (dikunci user 2026-10-30)

| # | Tugas | Status |
|---|-------|--------|
| **a** | **(1)** Proteksi demosi NONAKTIF selama dev (`DemotionGraceMatches=0`, kode tetap). **(2)** Konsistensi tier: tier tampil SAMA di semua layar = tier dari **rating asli**; conservative rating HANYA untuk urutan posisi leaderboard. | ✅ 2026-10-30 |
| **b** | Konfirmasi/selesaikan koreksi deteksi akun uji: `IsTestAccount` default **false**, ditandai **eksplisit** oleh jalur tes, **tanpa tebakan awalan deviceId**. | ✅ 2026-10-30 |
| **c** | **Fitur Pilih Faksi ORDE/LEGION**: layar onboarding sebelum lobby · endpoint set faction + validasi server · label "Butuh Pejuang" + bonus utk faksi kecil · badge faksi konsisten semua layar. **Keputusan user**: terkunci satu season · Guest ikut memilih · akun lama tanpa faksi diminta memilih saat login berikutnya. | ✅ 2026-10-30 (⚠️ klien butuh compile editor) |
| **d** | **Selesaikan UI Lobby**: (1.6) Settings lengkap (Grafis/Audio/Kontrol/Antarmuka/Akun+Logout), simpan lokal + langsung diterapkan. (1.7) Lobby tidak kosong: hero terakhir di tengah (placeholder ada), panel Pengumuman/Event kecil kiri-atas. Tombol belum berfungsi (Shop, Inventory, Hero Deck, Quest, Event, Guild, Mail, HQ, Plaza) → nonaktif + "Segera Hadir". | ⬜ |
| **e** | Layar hasil pasca-match pakai layout Detail Match (ganti IMGUI lama). | ⬜ |
| **f** | UI Tab Statistik baru (ring Flawless, grid mekanik, radar). | ⬜ |
| **g** | Kartu Disputed "TIDAK DIHITUNG". | ⬜ |
| **h** | Fase 2 dst sesuai docs/31 (chat, teman, party, guild, mail). | ⬜ |

Legend: ⬜ belum · ⏳ sedang · ✅ selesai.

---

## ⏭️ SISIPAN SEBELUM POIN d (dikunci user 2026-10-30, dari laporan tes faksi)

User menyisipkan tiga TUGAS **sebelum** poin d. Urutan baru: **Tugas 1 → Tugas 2 → Tugas 3 → poin d**.
Kerjakan **berurutan, BERHENTI & LAPOR tiap tugas** sebelum lanjut. (Poin e–h tetap setelah d.)

| # | Tugas | Status |
|---|-------|--------|
| **T1** ✅ (⚠️ verifikasi editor) | **Kunci semantik warna UI** (tanpa ubah backend). Token baru di `NexusTokens.uss` (`--nx-team-ally/-enemy`, `--nx-result-win`=alias rank, `--nx-result-loss`, `--nx-gain`, `--nx-online`, `--nx-faction-orde/legion-bg/-fg`, `--nx-hero-neutral` + varian `-dim`). **Aturan keras**: token faksi HANYA badge/emblem/layar pilih faksi/header ladder. Terapkan di `.nxl-facbadge`, faction-screen, header ladder, `.nxl-detail-*` (kamu=ally, lawan=enemy), `.nxl-hist-*` (**KALAH=loss abu-baja, BUKAN merah**), delta Poin Ladder (+gain/−loss), titik online, placeholder hero. SpriteGen: `emblem_orde` (perisai) + `emblem_legion` (chevron); regen `hero_titan/pulse` → netral+ikon kelas. Swatch volt/hijau/emas di navy & onyx + sim buta warna (screenshot). Grep semua hex/rgb di luar NexusTokens.uss. Update docs/34 (hapus "ORANYE (lawan)", KALAH=abu-baja), docs/35, docs/90. Usulan nilai: gain/online ~`#34D399`, volt `#C6FF3D`. **Lapor: file diubah, hasil grep, swatch, layar yang user cek manual.** | ⬜ |
| **T2** ⛔ DIBLOK (tunggu tes editor user) | **Pulihkan C4: KO HANYA lewat 3 Break Stock** (hapus bleed-out sbg jalan KO). Hapus KO dari `CritTimer/CritBleedTicks`. Penalti gerak C4 bertingkat (70%→50%→35%, dash dikunci) + indikator posisi Critical utk lawan. **Overload**: tak tersentuh 8 dtk → terkunci 1,5 dtk, rentan, BUKAN KO, reset tiap kena pukul. **AI bot prioritaskan target Critical** (akar bug 5v5). Jaring pengaman: batas waktu match + AFK (tanpa input N dtk → kalah WO/forfeit, bukan KO) — **usulkan nilai, tanya user dulu**. Hapus atribusi kill bleed-out; invariant 1v1 tetap hijau; tes baru (Critical 30 dtk tak tersentuh → tak KO, Overload terpicu, skor tetap). Jangan ubah data lama. Update docs/32, docs/90. CodeGen bila `.qtn` berubah. Nilai di config, bukan hardcode. | ⬜ |
| **T3** | **Audit docs 13–36/90/91 → buat `docs/00-ROADMAP.md`**. Keputusan baru dicatat di docs/90: Solo Ladder≠Survival (docs/24); leaderboard urut tier tampil→conservative→WR→match (sinkron docs/31&33); Nakama di docs/36 (✅ sudah); **"Guild"→"Squad"** semua docs/UI/channel; slider lobby = ANTREAN saja (Ranked + Battle 3v3 bot + teaser), **Street Room = room browser tombol sendiri** samping HQ/Plaza, 2v2 dicabut; **layar faksi SETELAH hasil match pertama** (bukan sebelum lobby; layar+backend dipakai ulang, ubah pemicu); **pindah faksi gratis 1× sampai 5 placement ranked** (backend `FactionSwitchUsed` + validasi di `/api/me/faction` + tes); demosi NONAKTIF (perbaiki docs/31 yg masih tulis grace=3). Milestone aktif: "Ranked 1v1 end-to-end". Tabel "Konflik ditemukan" (A vs B/resolusi/status); konflik baru **jangan** diputus sendiri → tanya user. **Lapor: perubahan per dokumen, konflik butuh keputusan, kode (faksi-pemicu + leaderboard) + hasil tes.** | ⬜ |

**4 concern desain (dasar tugas di atas, dari user):**
1. **Bleed-out = deadlock state, bukan posisi.** Pemain diam di Critical karena tak dipukul (bot 5v5 tak prioritaskan Critical). "Pindah ke posisi aman" = menghadiahi kabur → SALAH. Solusi = T2 (Critical tanpa batas waktu & tanpa auto-KO; penalti gerak + Overload + bot prioritas + AFK forfeit).
2. **Ukuran tim**: 2v2 dicabut (ganti Solo Ladder + Street Room, kpts 10-26). Battle (mode=1) sudah di kode tapi hilang dari slider → kembalikan ke slider (antrean). Street Room = room browser (tombol sendiri). Survival 1v1/3v3 menyusul; Faction War/Nexus Cup 5v5 Fase 3+.
3. **Jendela pindah faksi gratis**: karena layar faksi pindah ke SETELAH match pertama, "sebelum ranked pertama" bisa nol → pakai **1× sampai 5 placement ranked** (sejalan syarat leaderboard).
4. **Warna faksi = terang-gelap, bukan hue**: Volt (~75°) terjepit antara emas (~44°) & hijau (~158°); deuteranopia → volt≈hijau. ORDE terang (ivory/teks gelap), LEGION gelap (onyx/garis+teks volt) + bentuk emblem beda. **Delta negatif Poin Ladder = abu-baja, bukan merah.** (Create Room hijau = keputusan user; bila ramai → outline netral.)

---

## 📌 CATATAN PENTING YANG BERLAKU

- **Proteksi demosi NONAKTIF** (`Game:DemotionGraceMatches=0`) selama development. Kode, kolom DB,
  dan tes dipertahankan. **Aktifkan kembali (nilai 3) sebelum rilis publik.** (docs/33)
- Tier tampil = **rating asli** di mana pun. Conservative (`rating − 2·RD`) hanya untuk **posisi** leaderboard.
- MMR mentah TIDAK PERNAH ditampilkan (hanya tier + Poin Ladder 0–100).
- Tanpa data dummy. Tombol tampil = berfungsi, atau nonaktif + "Segera Hadir".
- Nama = `displayName` konsisten di semua layar. Design system: NexusTokens/NexusLobby.uss, 9-slice, Chakra Petch/Exo 2.

## 🗂️ Sumber kebenaran per fitur
- docs/31 = rencana penyelesaian fungsional (status fase). docs/32 = stats/mekanik. docs/33 = leaderboard + demosi. docs/34 = riwayat.
- Deploy backend: `wsl -e sh -c 'cd /mnt/c/Users/US3R/photon-backend && docker compose up -d --build api'` (bukan dotnet build).

---

## 📝 LOG RINGKAS (terbaru di atas)
- 2026-10-30: **⛔ MENUNGGU TES EDITOR USER (putaran ke-3 ditunda).** Kode klien belum terverifikasi editor menumpuk: onboarding faksi, badge, palet, token semantik, badge chip, grafik, sprite hero. **JANGAN tambah pekerjaan apa pun** sampai tes masuk. Tes satu sesi (~20–30 mnt): A) faksi 1–9; B) 10 badge chip (terutama di kartu KALAH desaturate), 11 delta Poin (+hijau/−abu-baja), 12 grafik (garis biru/titik fokus cyan/band tier emas redup), 13 placeholder hero netral+ikon kelas, 14 screenshot swatch. **Percabangan pasca-tes:** ada yang gagal → **perbaiki dulu, lapor, baru T2**; semua aman → **lanjut T2** (C4: KO hanya 3 Break Stock, penalti gerak bertingkat, Overload, bot prioritas Critical; **usulkan nilai AFK forfeit lalu TANYA user sebelum angka final**). **Ikon per-badge = YA tapi dikerjakan bersama T2** (diuji di sesi tes T2), bukan sekarang.
- 2026-10-30: **T1 SELESAI (kode+docs; verifikasi editor menyusul) + keputusan user diterapkan.** Badge prestasi → **chip netral** steel-dim (`--nx-badge-bg/-fg`), FLAWLESS garis emas; COMEBACK bukan hijau, FIRST BLOOD bukan merah. Grafik Painter2D (`Profile`+`Lobby`): garis data=biru ally, band tier=emas redup, titik fokus=cyan saja. `NexusMetaUI.cs` dibuat **inert** (`LegacyEnabled=false`→OnEnable self-disable) + dikecualikan grep (komentar legacy, dihapus poin e). **Sprite hero diregen netral+ikon kelas** (titan=kepalan/Grappler, pulse=crosshair/Zoner, unknown="?", nama samar) via System.Drawing; bidang `--nx-hero-neutral` di `.nxl-hist-art`/`.nxl-dt-hero`. docs/26 (aturan: SELALU plugin `docker compose`, jangan uninstall 2.27; gejala forwarding), docs/34 (badge+grafik), docs/90 (keputusan). WSL: diputus—SELALU plugin compose, `.wslconfig` ditunda (user terapkan sendiri). **T2 TUNGGU hasil tes editor user** (butuh CodeGen). Commit menyusul.
- 2026-10-30: **Diagnosis WSL + T1 (sebagian).** Diagnosis: WSL1 distro Ubuntu-22.04, Docker 29.1.3 via systemd (enabled+active), 7.7Gi RAM/6.6Gi free, **tanpa OOM** (api/db Exit=0 OOM=false Restarts=0). Penyebab "SIGTERM 143" = **recreate churn 2 versi compose** (2.27.0 lama vs 5.1.2 baru pada 1 proyek → `up` membunuh container versi lain; event `kill signal=15`) + transien WSL↔host localhost-forwarding; BUKAN OOM/kode. `networkingMode=mirrored` **sudah pernah gagal di mesin ini** (docs/90, 0x8007054f) → jangan diusulkan. **Tabel `FactionAdminAudits` TERVERIFIKASI live di Postgres** (6 kolom+3 index, migrasi di `__EFMigrationsHistory`). Proyek kedua `corevo-aratechnology` (hris/mysql) berbagi daemon (noise). **T1 done:** token semantik di `NexusTokens.uss` (ally/enemy/result-win/-loss/gain/online/hero-neutral +dim +komentar aturan); terapkan KALAH→abu-baja (`ladder/hist-*--loss`, head tint), −Poin `pts-dn`→abu-baja, detail `accent/bar` you→ally/opp→enemy; docs/34 (KALAH abu-baja, hapus "ORANYE (lawan)"→MERAH, hero placeholder netral), docs/90 (kunci semantik). **T1 pending:** regen sprite hero netral+ikon kelas; swatch screenshot (editor); warna AMBIGU butuh keputusan user (badge COMEBACK hijau/FIRST BLOOD merah-oranye, garis grafik cyan, NexusMetaUI legacy). **Perbaikan .wslconfig vmIdleTimeout = tunggu persetujuan** (butuh `wsl --shutdown`).
- 2026-10-30: **Perbaikan 1–2 pra-tes faksi (user pilih (a)).** (1) Endpoint admin: validasi 0|1|2 (sudah), secret **constant-time** (`SecretsEqual` SHA256+FixedTimeEquals, dikonfirmasi), **audit WAJIB** → entity `FactionAdminAudit` + tabel (migrasi `AddFactionAdminAudit`) + DbSet; endpoint catat sumber(`adminSource@ip`)/playerId/lama→baro/waktu + log `AdminFaction`, respons `previous`; TODO reset pindah-gratis saat field ada (T3); docs/35+docs/91 "UTANG RILIS: X-Admin-Secret → admin berbasis role (docs/90)". (2) Deskripsi faksi **diseimbangkan** (ORDE "Pelindung Neo-Veridia…", LEGION "Kru jalanan merdeka…") di UXML+docs/35; docs/23 disinkron (ORDE "memonopoli"→"mengamankan"+sisi keras; LEGION +sisi keras). (3) docs/36 TIDAK diimplementasi (user baca dulu). **68 tes hijau** (tes admin diperluas: cek baris audit lama→baru+sumber). Backend deploy sempat healthy (health=Healthy, /api/factions live); verif live tabel terganjal WSL labil (container ber-SIGTERM) — bukan isu kode. **BERHENTI & LAPOR** sesuai instruksi; sisipan T1→T2→T3 lalu poin d dicatat di atas.
- 2026-10-30: **Revisi poin c (3 isu kritis user).** (1) Warna faksi → **PALET 4 "Terang vs Gelap"** (ORDE ivory/platinum+perisai, LEGION onyx/volt+chevron; TANPA biru/merah tim & TANPA emas rank); sprite crest `fac_orde/legion.png`; deskripsi kartu dari lore docs/23; halaman uji swatch + simulasi buta warna (temuan: Volt≠hijau +Poin, beda kecerahan). (2) Belum ada season → kunci permanen; **endpoint admin `POST /api/admin/faction`** (X-Admin-Secret) utk reset. (3) docs/35=faksi; **docs/36-realtime-decision** dibuat (Photon Chat/SignalR/Nakama), docs/31 §2.1 → docs/36. **68 tes hijau**, deploy live. Swatch: artifact NoNoBj5SE6NbvcsN6XNrN2.
- 2026-10-30: **Poin c SELESAI** (docs/35). Backend faksi: `FactionService` (populasi/Butuh Pejuang/bonus), `GET /api/factions`, `POST /me/faction` (validasi+lock satu season+idempoten), bonus XP minoritas di FinalizeAsync. **67 tes hijau**, deploy live. Klien: layar onboarding `faction-screen` (NexusLobbyController+NexusGame), badge konsisten (`SetFactionBadge`: top bar + profil), Guest ikut memilih. **⚠️ Klien butuh compile+playtest di editor (tak bisa diverifikasi headless).** Backend commit `ed951f2`.
- 2026-10-30: **Poin a & b SELESAI.** Demosi dinonaktifkan (grace=0, floor dibersihkan saat startup, kode/tes tetap). Leaderboard: tier/poin dari rating asli, conservative hanya utk posisi (+2 tes). Deteksi akun uji dikonfirmasi eksplisit (tanpa deviceId guessing); docs/33 §1 + komentar tes diperbaiki. **61 tes hijau.** Deploy live. Berikutnya: poin c (Faksi).
- 2026-10-30: Antrean prioritas dikunci. Commit snapshot (backend `0a9f5a4`, docs `735404a`). Mulai poin a.
- 2026-10-30: Proteksi demosi opsi 1 diimplementasi (lalu dinonaktifkan di poin a).
- 2026-10-29/30: 1v1 ranked, leaderboard, Tab Riwayat + Detail Match. 58 tes hijau.
