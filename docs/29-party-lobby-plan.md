# 29 — Ruang Tim (Party Lobby) Plan

Fitur: **RUANG TIM** — semua mode wajib lewat sini sebelum matchmaking. Design system `NexusLobby.uss`.
Lihat [27 — lobby](27-lobby-redesign-plan.md).

## ALUR
Lobby → pilih mode (slider) → **MAIN** → **Ruang Tim** → **MULAI** → matchmaking (overlay "Mencari lawan" + timer + Batal) → match.
Kembali/Esc di Ruang Tim = keluar party, balik ke lobby. **Klik MAIN tidak lagi langsung matchmaking** — membuka Ruang Tim.

## UKURAN TIM PER MODE (config SATU tempat — `NexusPartyConfig` saat implementasi)
Usulan awal (sesuaikan saat tim modes nyata ada; matchmaking backend saat ini hanya 1v1/2 pemain):
- **Ranked (Solo 1v1): 1 slot**
- **Battle: 3 slot** (3v3 target; sementara MULAI tetap panggil Quick Match 1v1 yang ada)
- **Faction War: 5 slot** — tetap "Segera Hadir"
- **Nexus Cup: 5 slot** — tetap "Segera Hadir"
Slot di luar ukuran mode tidak ditampilkan.

## TAMPILAN (1920×1080)
- Judul kiri atas: "RUANG TIM" + nama mode (mis "RANKED - SOLO 1v1"), tombol **Kembali** kiri.
- Deretan **kartu slot vertikal** di tengah (banner 9-slice):
  - Terisi: avatar, nama, level, emblem rank (khusus ranked), ping (ms), mahkota kecil utk ketua.
  - Kosong: tombol **"+ Undang"** (bukan tanda tanya).
- Tombol **MULAI** besar (oranye) bawah-tengah; **Enter** = MULAI. Hanya ketua yang bisa; anggota lihat "Menunggu ketua..." atau tombol **SIAP**.
- Bawah kiri: **Party chat** kecil. Kanan: panel undang (tab Teman & Kode Party).

## TAHAP
## ATURAN RANK & PLACEMENT (temuan backend — PENTING)
`backend/.../Services/Ranks.cs` → `TierFor(rating)`: **tier langsung dari rating Glicko-2, TANPA sistem placement.**
- Pemain baru rating **1500** (center) → langsung **"Rival"** (1400–1600). Menang → rating naik → bisa "Gladiator" (1600–1800).
- Band: Rookie<1200 · Contender<1400 · Rival<1600 · Gladiator<1800 · Conqueror<2000 · Nexus Legend≥2000.
- **Tidak ada "5 placement"** di backend → teks "Selesaikan 5 placement" DIHAPUS dari UI. UI kini selalu tampilkan tier asli.
- `NexusRankConfig` disamakan dengan `TierFor` (nama + batas) + `TierForRating()`. `/leaderboard` kirim rating → tier dihitung client (MMR mentah tetap disembunyikan).
- **Opsi backend (kalau mau placement sungguhan)**: tahan tier jadi "UNRANKED" sampai N match → perlu tambah field `placementCount`/aturan di `/me`. Belum dikerjakan.

## RUANG LADDER v2 (revisi — jendela penuh + grafik)
- **Jendela penuh**: margin 48px (~1824×984), flex kolom: header 56 → identitas 72 → **baris utama flex-grow** (kartu + tab mengisi tinggi, ikon 128px) → bawah 200. Tak ada ruang kosong sisa.
- **Bawah grid tegas**: kolom chat 58% + kolom (info+MULAI) sisa, gap 16px. Input chat flex-grow, **KIRIM selalu terlihat** (tak lagi tertutup MULAI). Area pesan chat mengisi tinggi.
- **Kontras**: label kartu 16px `#A8C4E8`; detail (Menang/Kalah, K/D/A) 18px putih.
- **GRAFIK RANKING (dibuat, Painter2D)**: rating kronologis dihitung dari `/api/matches` (rating sekarang − akumulasi `ratingDelta` mundur). Line cyan + titik per match, titik terakhir besar + "Saat Ini". **Pita tier horizontal** (Contender/Rival/Gladiator/Conqueror dari `NexusRankConfig`) + label tier kiri; **sumbu Y tanpa angka MMR**; sumbu X tanggal singkat. <2 match → "Grafik muncul setelah 2 pertandingan ranked". **Tab default = Grafik**.
- **Nama konsisten**: satu sumber `NexusLobbyController.PlayerName` = **displayName** (fallback username) dipakai di lobby/profil/ladder/Top100/rekaman/chat.

## RUANG LADDER (Ranked Solo 1v1) — JENDELA TERPUSAT (gaya Lost Saga)
Satu jendela `panel_frame` **1440×760 di tengah** (bukan full-screen), di atas vignette.
- Header jendela (56px): kiri `FAKSI | RANKED SOLO`, kanan **Keluar** (= Esc). Header luar party disembunyikan di mode solo.
- Identitas: avatar 48 + nama + tier.
- Kiri 55%: 3 kartu **tinggi tetap 360** (tak direntangkan): **RANK** (emblem crest + "Ladder Rank" + tier + progress + Menang/Kalah), **WIN RATE** (ikon piala + % 44px + W·L), **KDA** (ikon pedang silang + KDA + K/D/A). Ikon: `ic_crest/ic_trophy/ic_swords`.
- Kanan 45%: tab Grafik/Top 100/Rekaman Battle (tinggi = kartu). **Top 100**: baris 40px, kolom peringkat/nama/tier/W-L, **baris sendiri di-highlight** (bg cyan + border); di luar 100 → baris sendiri di bawah "100+" (peringkat asli perlu endpoint).
- Bawah: chat (55%) kiri · info "Mode: Ranked Solo · Peta: Acak" + MULAI (isi sisa) kanan.
- Konsistensi: kartu & baris Top 100 sama-sama dari DB (W/L cocok).
- **Butuh backend**: peringkat global pemain (untuk "100+"), Grafik rank/waktu, profil lawan saat VS.

### (lama) layout menyebar — digantikan jendela di atas.
Mode Ranked (solo) pakai **ruang ladder layar penuh**, BUKAN banner. Mode tim tetap banner.
- Header: Back + "RANKED" + "Solo 1v1 · Ladder".
- **Kiri 55%**: 3 kartu statistik (9-slice): **RANK** (emblem + tier + progress `NexusRankConfig` + Menang/Kalah/Win Ratio; unranked = "Selesaikan 5 placement"), **WIN RATE** (angka 48px + W/L), **KDA** (angka + K/D/A). (Win Streak belum ada di backend → pakai KDA.)
- **Kanan 45%**: tab **Rekaman Battle** (dari `/api/matches`, empty state), **Top 100** (dari `/api/leaderboard`, baris sendiri di-highlight, **MMR mentah disembunyikan** → tampil W/L), **Grafik Ranking** = "Segera Hadir".
- **Kiri bawah**: Lobby Chat (echo lokal). **Kanan bawah**: info read-only "Mode: Ranked Solo · Peta: Acak" + **MULAI** 360×72 (Enter). Tanpa Auto Kick/Setara/pilih peta (belum ada backend).
- **Transisi VS**: MULAI → "MENCARI LAWAN mm:ss" + BATAL → **lawan ketemu → layar VS ~1.8s** (kartu kamu · VS · kartu lawan) → match. (`NexusGame.OpponentFound` + `Task.Delay`.)
- **Butuh backend (dicatat)**: **Grafik Ranking** = riwayat rank per waktu (belum ada endpoint). Info **lawan** (nama/level/rank) saat VS (sekarang hanya "LAWAN · Ditemukan").

## TAMPILAN TIM (banner vertikal ML)
- Kartu = **banner vertikal 280×440** (sprite `banner_player.png`/`banner_dim.png`, ujung bawah lancip) + **platform glow** di bawah + **glow panggung** di belakang stage. Isi: chip KETUA, avatar 128, nama 22px, Level, (ranked) emblem+tier. **Ping**: nilai asli Photon RTT — DISEMBUNYIKAN di room (belum terhubung); tampil hanya saat terhubung.
- **Solo (1 slot)**: banner pemain · **VS** emas 72px · banner lawan ("?" + "Menunggu lawan", pulse saat mencari). **Tim (3/5)**: deretan banner sejajar; slot kosong "+ Undang" (disabled "Segera Hadir").
- **Undang & Party Chat hanya mode tim** (solo disembunyikan).
- Header: judul mode besar + subjudul ("Solo 1v1 · Kompetitif" / "Ruang Tim · N Pemain"). Back 44px + hover.
- **MULAI** 360×72 bawah-tengah (sama lobby), **Enter** = MULAI.
- **State mencari**: MULAI → "MENCARI LAWAN mm:ss" (disabled) + **BATAL** sekunder; Back nonaktif; lawan "?" pulse. **Esc** 1× batalkan pencarian, Esc lagi keluar ke lobby.
- **Belum**: reveal profil lawan 1.5s (backend tak kirim nama/level/rank lawan) → langsung ke match; ping real (perlu koneksi di room). Dicatat utk Tahap berikut.

- **Tahap 1 (SELESAI):** `party-screen` inline di `LobbyMain.uxml` + logika di `NexusLobbyController` (`_inParty`/`_partyMode`, `OpenParty/StartParty/LeaveParty/ApplyParty/BuildSlots`). MAIN lobby → **buka Ruang Tim** (semua mode, tak lagi langsung matchmaking). Slot dari `NexusPartyConfig.ForMode` (Ranked 1/Battle 3/Faction·Nexus 5); slot 1 = diri sendiri (avatar/nama/Lv/tier bila ranked/ping "— ms"/chip KETUA), slot lain = "+ Undang · Segera Hadir" (disabled). **MULAI** (Enter) → panggil handler matchmaking mode (`UiRanked/UiQuickMatch`); Faction/Nexus → MULAI disabled gray "SEGERA HADIR". **Create Room** (Battle) pindah ke Ruang Tim. **Kembali/Esc** → keluar party ke lobby. Cancel saat mencari → kembali ke Ruang Tim. Chat party & panel undang = stub "Segera Hadir".
- **Tahap 2 (rencana):** undang via kode party / ID pemain; buat/gabung/keluar/kick/pindah ketua/status siap.
- **Tahap 3 (rencana):** undang dari friend list (setelah sistem pertemanan backend).
- **Tahap 4 (rencana):** matchmaking party (anggota 1 tim, lawan seimbang); edge case: anggota disconnect saat mencari, ketua keluar (pindah otomatis), anggota keluar saat matchmaking (batalkan antrean).

## Integrasi teknis (rencana)
- Screen baru di controller lobby (mis. `party-screen` inline di `LobbyMain`) atau UIDocument sendiri + `PartyController`.
- `NexusGame`: state party sebelum Connecting; `btn-primary` (MAIN) → buka party; MULAI → `UiRanked/UiQuickMatch/UiCreateRoom` sesuai mode.
- Faction War/Nexus Cup: party tampil tapi MULAI disabled "Segera Hadir".
