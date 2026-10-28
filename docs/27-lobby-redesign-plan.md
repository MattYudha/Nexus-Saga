# 27 — Lobby Redesign Plan (UI Toolkit, PC-first)

Rencana & aturan baku redesign UI meta Nexus Saga (lobby + auth), gaya **Mobile Legends × LostSaga**
(cerah, arcade, chunky, glossy — tapi brand & aset tetap orisinal Nexus Saga). Dokumen ini adalah
sumber kebenaran; bila ada konflik, ikuti file ini.

Kode UI: `photon-backend/game/Assets/NexusUI/` (Assembly-CSharp, UI Toolkit).
Lihat juga: [15 — skema data](15-skema-data-pemain-ekonomi.md), [24 — struktur kompetitif](24-struktur-kompetitif-v2.md).

## 1. Prinsip produk (WAJIB)
- **PC-first**, BUKAN mobile. PanelSettings `ScaleWithScreenSize`, referensi **1920×1080**, match 0.5.
  Uji di 1920×1080, 2560×1440, 1280×800, 2560×1080 (ultrawide → ruang scene melebar, tombol TIDAK melar).
- **Tidak ada data dummy.** Currency = 0, friend list = empty state, quest tersembunyi bila kosong,
  mode belum siap = terkunci "Segera Hadir" (disabled). Jangan pernah hard-code angka palsu.
- **Satu pemilih mode** (di tengah) dan **satu tombol utama** (oranye glow, fungsinya mengikuti mode terpilih).
  Create Room = tombol sekunder, hanya muncul di mode room.
- **Satu blok rank** (kiri). Bottom nav **maksimal 6**: Shop, Inventory, Hero Deck, Quest, Event, Guild.
- **GM / Dev Lounge hanya di editor / development build** (`#if UNITY_EDITOR || DEVELOPMENT_BUILD`), pojok, kecil.
- Logout + FB/TikTok masuk **Settings**, bukan panel utama.
- Friend list & chat **selalu terbuka** (bukan popup).
- Bangun **berdampingan**: toggle `useNewLobby` di Inspector; jangan hapus `NexusMetaUI.cs` lama
  sampai lobby baru terbukti jalan. Jangan hapus logic Photon/matchmaking/handler — pindahkan binding, pertahankan nama.
- Keyboard: Esc = tutup/kembali, Enter = fokus chat.
- States wajib: searching (timer + Batal), disconnect (banner + Reconnect), new player (empty states).

## 2. Design system — sprite 9-slice
Generator: `Assets/Editor/NexusSpriteGen.cs` → menu **Nexus → Generate Lobby Sprites**
(output `Assets/NexusUI/Sprites/`). Parameter: Size 48, Radius 9, Border 3, **Slice 12**.
- Tombol: gradient kontras (atas terang, bawah gelap), sheen 40% atas, inner-highlight 1px di tepi atas, bevel bawah.
- Sprite: `btn_orange/green/blue/gray/red`, `btn_mode` + `btn_mode_active`, `tab_inactive` + `tab_active`, `panel_frame`.
- `tab_active` = navy lebih terang dari inactive + garis bawah cyan (BUKAN putih).
- `panel_frame` semi-transparan alpha **0.85**.
- Scene uji: `SpriteTest.uxml` → menu **Nexus → Setup Sprite Test Scene** → Play.

## 3. Palet warna
- Panel fill `rgba(15,30,60,0.85)`.
- **Border biasa = biru redup `#2A4A7A`.** Border **cyan terang `#4FD1FF` HANYA untuk elemen aktif/terpilih.**
- Teks utama `#FFFFFF`, sekunder `#A8C4E8`, redup `#78 92 BA`.
- Aksen rank/emas `#F5C542`.
- Tombol oranye `#F28C1E` (border `#FFB347`), hijau `#3CB043` (border `#6EE07A`), merah `#D64844`, biru `#3A7BD5`.

## 3b. Hirarki visual & "menahan diri" (pelajaran dari ML)
Elegan datang dari restraint, bukan dari banyak bingkai:
- **Hanya SATU elemen paling mencolok** di layar (tombol utama oranye). Semua elemen lain mengalah.
- **Border/bevel 9-slice hanya untuk yang bisa diklik** (tombol, mode, tab). **Panel informasi**
  (friend list, chat, quest) **nyaris tanpa bingkai** — latar semi-transparan lembut, seolah melayang di atas scene.
- **Bottom nav** = ikon + teks di atas strip gradient tipis, BUKAN deretan tombol berbingkai.
- **Scene 3D tengah** diberi ruang paling luas = bintang utama. Jangan penuhi dengan kotak.
- Hindari kesan "kotak-kotak": jangan setiap elemen diberi border tegas.

## 3c. Dunia & keputusan font (FINAL)
Dunia NEXUS SAGA = **near-future urban / cyber-street** ("Hypebeast Meets Combat Exo-Gear", kota Neo-Veridia),
**bukan fantasi/mitologi** (lihat [23](23-tema-cerita-karakter.md)). "Mythic" hanya nama tier rank, "Relic" = artefak teknologi, bukan sihir.
→ Font serif klasik (Cinzel) ditolak: salah tempat di dunia urban sci-fi.
**KEPUTUSAN:** font tunggal **Chakra Petch Bold** (geometric-techno, cyber-street) untuk **logo, nama rank, judul, tombol, tab**;
**Exo 2** untuk teks kecil/deskripsi. Cinzel/Saira/Rajdhani sudah dihapus dari project.

## 4. Tipografi (Google Fonts, OFL)
File: `Assets/NexusUI/Fonts/` — `ChakraPetch-Bold.ttf` + `Exo2-Variable.ttf` (+ lisensi `OFL-*.txt`).
- **Logo, nama rank, judul, tombol, tab, mode-title → Chakra Petch Bold** (`--nxl-font-title` = `--nxl-font-head`).
- **Teks kecil / deskripsi → Exo 2** (`--nxl-font-body`).
- Didaftarkan sebagai variabel USS (`-unity-font-definition: var(--nxl-font-*)`).
- Ukuran (acuan 1920×1080): deskripsi/kecil **≥16px**, tombol sekunder **18px**, tombol utama **22px**,
  judul panel **24px**, judul besar **28px+**.
- Teks tombol berwarna: `text-shadow` gelap + `-unity-text-outline-width` tipis untuk kontras.

## 4b. Revisi layout (iterasi terbaru)
- **Top bar**: kartu profil (avatar+nama+Level+XP) pindah KE DALAM top bar sebaris kiri, sejajar currency+Mail/Settings di kanan. **Logo NEXUS SAGA/CHRONICLES DIHAPUS** dari top bar (tengah kosong). Logo besar hanya di layar login.
- **Garis pemisah** top bar & bottom nav DIHAPUS → cukup strip gradient yang memudar ke transparan.
- **Blok rank permanen di kolom kiri DIHAPUS**. Info rank jadi **kontekstual di tengah**, tepat di atas tombol MAIN: mode Ranked → emblem+tier+progress (atau "UNRANKED — Selesaikan 5 placement"); mode lain → deskripsi mode.
- **Kolom kiri** sekarang hanya **Lobby Chat** (float kiri-bawah). Tengah dikosongkan untuk scene.
- **Slider mode (tengah)** = mode pertandingan saja, urut: **Ranked, Battle, Faction War, Nexus Cup** + **dots indikator** + **panah keyboard ←/→**. Ranked→antre ranked; Battle→Quick Join + tombol Create Room; Faction War & Nexus Cup→"Segera Hadir", MAIN disabled (belum ada backend).
- **HQ** (Squad HQ) & **Plaza** = tombol akses terpisah 72×72 di kiri panel mode (BUKAN bagian slider). **Market** → digabung ke **Shop** di bottom nav (tak ada item Market terpisah).
- File: `CenterCTA.uxml` (slider+dots+HQ/Plaza+rank kontekstual), `TopBar.uxml` (profil+currency), controller `NexusLobbyController` (mode 4 + disabled + dots + panah).

## 5. Layout target (ringkas)
- **Top bar**: kiri kartu profil (avatar→Profile+Back, nama, level, XP) + ikon sosial/Settings; tengah logo NEXUS SAGA + "CHRONICLES"; kanan currency (Gold/Ticket/Diamond, tombol "+") + Mail + Live.
- **Kiri**: blok RANK (emblem + nama tier) lalu daftar mode vertikal (ikon + judul 2 baris + badge).
- **Tengah**: panel mode (panah ganti mode, emblem, progress) di atas scene; QUICK JOIN + CREATE ROOM; tombol besar RANKED MATCHMAKING; LOBBY CHAT + input.
- **Kanan**: online count; Quest Notification (closable); Friend List (tab LOBBY/BUDDY/GUILD); Add Friend + Settings.
- **Bottom nav**: 6 item (lihat §1).

## 6. Mapping ke fitur yang sudah ada
- QUICK JOIN → Quick Match · CREATE ROOM → Create Room · RANKED MATCHMAKING → Ranked (handler sudah ada, pertahankan).
- Profil card → Profile Page (+Back, riwayat match). Logout → Settings.
- Faction/Plaza/Relic/Squad/Tourney, Friend, Quest, Currency, Mail → **placeholder** (backend Fase 3 / belum ada).

## 7. Tahapan
1. **Tahap 1 (selesai):** sprite 9-slice + USS design system + PanelSettings + SpriteTest + tipografi (Chakra Petch + Exo 2).
2. **Tahap 2 (selesai, layout+skala direvisi):** komponen UXML `TopBar` (logo tengah+currency kanan, 88px), `ProfileCard`+`RankBlock` (kolom kiri menyatu 300), `FriendPanel` (kanan 340, margin 24, teks wrap), `CenterCTA` (float bawah-tengah: pemilih mode + SATU tombol utama 360×72), `ChatPanel` (float kiri-bawah 420×200), `BottomNav` (96px, ikon 40+label 16, tersebar). Depth: `lobby_vignette` + `strip_top`/`strip_bottom` (generate ulang sprite). Preview: menu **Nexus → Setup New Lobby (Preview)**. Data 0/empty, nav borderless, GM dikecualikan.
3. **Tahap 3 (SELESAI):** `NexusLobbyController.cs` (Assembly-CSharp, UITK) + API publik di `NexusGame` (`UseNewLobby`, `Ui*` wrappers termasuk `UiLogin/UiRegister/UiGuest`, `Backend`, `Is*`, `AuthMsg/AuthBusy`, `LastError`). Binding OnEnable; mode picker prev/next; `btn-primary` ikut mode (RANKED→UiRanked, QUICK→UiQuickMatch, ROOM→UiQuickMatch + Create Room sekunder→UiCreateRoom); Logout di Settings overlay; nama/level/rank dari `NexusBackend` (currency tetap 0, tanpa dummy); state searching (timer+Batal→UiCancel) + banner disconnect. Matchmaking + IMGUI lama **tetap jalan** (toggle `UseNewLobby`). Dipasang di scene online via `Nexus → Create Online Scene` (GO `NexusLobbyUI`).
   - **Login = LAYAR SENDIRI** (`auth-screen`, bukan popup): sebelum login `lobby-body` disembunyikan total; background vignette + logo NEXUS SAGA besar. Login sukses → lobby fade-in ~0.3s; Logout → kembali ke layar login. Form: label di atas input (44px/16px), password mask + tombol ikon mata show/hide, Tab Username→Password, Enter=submit, area pesan error, tombol LOGIN jadi "MASUK..." + disabled saat proses, "Daftar" = link teks, Guest = tombol sekunder. Overlay penuh-layar HARUS anak langsung `nxl-root`/`lobby-body` (bukan `<ui:Instance>` template — pembungkus template tinggi 0 → `inset:0` kolaps).
4. **Tahap 4:** FriendList + LobbyChat + QuestNotif + empty states.
5. **Tahap 5:** states (searching/disconnect/new player) + hover/animasi.

Modular UXML: TopBar / RankBlock / ModePanel / CenterPanel / QuestNotif / FriendList / LobbyChat / BottomNav
dirakit di `LobbyMain.uxml`. Semua style di USS (jangan inline), C# hanya logic/binding by name.

## 8. Aset art yang masih perlu disiapkan user
Background scene lobby (`lobby_bg.png` 1920×1080), emblem rank, ikon mode (6), ikon currency (3),
ikon bottom-nav (6), avatar frame, ikon sosial. Sementara pakai placeholder kotak+teks bernama jelas.
