# Riset: Sistem Sosial, Lobi/Room, Rhythm & Live-ops AyoDance (2026-10-24)

Sumber: client AyoDance di `C:\Megaxus\AyoDance`, **analisis statis saja** (Xigncode). Tidak menjalankan game, tidak membongkar enkripsi/packer, tidak menyalin data mentah.

Label: **OBSERVED** (bukti langsung) · **INFERRED** (dugaan beralasan) · **UNKNOWN**.

> ⚠️ Layout UI, tabel item modern, dan data lagu versi sekarang **terenkripsi**. Detail di bawah berasal dari nama file UI, manifest teks, tabel desain lama (2004–2005), dan header file.

---

## Ringkasan temuan (ID)
| Topik | Temuan | Status |
|---|---|---|
| Format UI | 187 file `SCRIPT\*.bin` = layout UI terenkripsi (cipher blok 64-bit, satu kunci); `list.gul` = manifest teks berisi 184 root UI | OBSERVED / cipher INFERRED |
| Riwayat fitur | 53 baris terakhir `list.gul` = urutan fitur yang ditambahkan (event → AudiPass → Lumi gacha → SoulMate → tutorial baru → boss guild → piano) | INFERRED |
| Pola "Renewal" | Fitur yang didesain ulang ditambah `…Renewal` dan versi lama **tetap disimpan** (Ranking, RoomMake, Tutorial, Fashionmall, BigGame) | OBSERVED |
| Alur masuk | Server → distrik/channel → pilih lobi (utama / club / shop) | INFERRED |
| Kapasitas room | **6 pemain** (file posisi panggung 48 byte per pemain; 6 slot avatar & blokir) | OBSERVED / INFERRED |
| Mode tim | Tabel posisi punya flag solo/tim; tata letak 1on1 | OBSERVED |
| Voice chat | DLL voice dengan grup (room = grup), mute per pemain, kontrol mikrofon | OBSERVED (ekspor DLL) |
| Moderasi | Daftar blokir, ikon blokir per slot room, tabel kata kasar | OBSERVED |
| Gameplay inti | **Level N = urutan panah sepanjang N** (numpad 1–9 tanpa 5; diagonal = mode 8 arah), dikonfirmasi Space tepat di beat; tiap urutan → klip animasi dansa | OBSERVED (tabel 1.791 gerakan) |
| Data lagu | Tabel: artis, judul, file, level 0–19, BPM, flag aktif, "baru"; ada versi tabel khusus server | OBSERVED (tabel lama) |
| File musik | `ABM\` = musik + chart (`*_note.tbm`), terenkripsi/terkompresi setelah header | OBSERVED / isi UNKNOWN |
| Mode game | Normal, Beat-Up/Beat Rush, Combo, Rhythm Holic, Guitar, Piano, Couple dance, Club, minigame | INFERRED (nama suara & UI) |
| Event | **Dua lapis**: kerangka event generik (Inform/Popup/Set board, event mode, event cash) + **satu root UI khusus per event** | INFERRED |
| Exe | `Audition.exe` **Themida**; Patcher = .NET 4.7.2; shader FX dengan parameter color-mask (mendukung dye) | OBSERVED |
| Teknologi | Direct3D 9, FMOD lama, DirectInput, jsoncpp (2024), WinINet (banner/web), Lua 5.1 (tidak di import langsung) | OBSERVED |

---

## A. Peta fitur (dari 184 root UI)
| Sistem | Contoh root UI (nama) |
|---|---|
| Boot / server / channel | ServerSelect, ServerDistrict, MainLobbySelect, License, Curtain |
| Lobi / room / mode | RoomMake(+Renewal), ModifyRoomOption, InRoomRule, GameRoom (salah satu terbesar), Result, Invitation, **VIP Room/Invitation**, ShopLobby, ClubLobby, DancePracticeRoom, CameraEdit |
| Mode alternatif / minigame | BigGame, ChampionTimeBattle, TeamTitleMatch, MatchingCard, AvatarMatchGame, Rock-Paper-Scissors, PianoChallenge, SpacePang, DanceAcademy, guild boss battle, slot machine couple |
| Story / quest / bantuan | StoryBoard, StoryRank, QuestBoard, TutorialRenewal, GuideBook, Diary |
| **Guild ("Fam")** | Create, **Bank**, Board, **RollBook (absensi)**, FamilyTree, **House**, **Butler NPC**, Ranking, **Boss Battle**, **channel berbayar**, sponsor turnamen |
| **Couple / pernikahan** | CoupleRegistration, **Wedding** (+uang hadiah), DatePlanner, SoulMate, **Couple Garden** (bank book, shop, slot machine), Secret Garden, Couple Shop |
| Sosial / chat / moderasi | Messenger (terbesar), Whisper, FindFriend, **Shout (megaphone)**, BlackList, profil, MyHome, **PhotoStudio**, Sticker |
| Broadcast | BroadCastRoot (besar, diperbarui 2026) — streaming atau pengumuman: UNKNOWN |
| Toko | FashionMall: **Cart, PresentBox (hadiah), MyCodi (outfit tersimpan)**, ChoicePackage, **OneDayMarket (deal harian)**, Black/White Label, Showcase, Preview; ItemMall, MusicMall, Catalog, DressingRoom, ReSell |
| Gacha / upgrade | **ChanceHelp (UI peluang)**, LumiGacha, LumiUpgradeZone, HappyBox |
| Retensi | **AudiPass (+Renewal, 2024)**, Attendance, MaestroGradeUp, Referral |
| Pet | Mandrake pet & shop, Mascot pet & dance tour |
| Event musiman | Natal, Valentine, White Day, puzzle, bingo, kolaborasi artis, MixEvent |
| Ranking | Ranking(+Renewal), FamRanking, StoryRank |

Aktivitas update UI: 26 file diubah 2024, 17 di 2025, 22 di 2026 — live-ops berjalan terus selama ±20 tahun.

## B. Lobi, channel, room
- **INFERRED:** alur server → distrik/channel → tipe lobi (utama, club, shop); guild bisa membeli channel privat.
- **OBSERVED/INFERRED:** kapasitas **6 penari per room**; 9 tata letak panggung untuk tiap jumlah pemain 3–6; ada tata letak tim 1on1.
- **INFERRED:** siklus room: ready room → loading → main → hasil (dari nama audio).
- **OBSERVED:** voice chat grup (DLL `T3CAudio`): buat/masuk/keluar grup, mute per pemain, volume mic/speaker.
- **OBSERVED:** quick-chat makro F5–F8 (3 frasa per tombol); tabel kata kasar di client.
- **UNKNOWN:** penonton, password room, batas channel.

## C. Gameplay ritme
- **OBSERVED:** tabel gerakan dansa 1.791 baris: level 1–9; **panjang urutan tombol = level**; digit = arah numpad (2/4/6/8 dominan, 1/3/7/9 = mode 8 arah); setiap urutan memetakan ke file animasi dansa. Callout suara 1–9 tanpa 5.
- **OBSERVED:** `tutorial.rep` = rekaman input (kode tombol + milidetik) untuk demo tutorial.
- **OBSERVED:** tabel lagu: 264 lagu (lama), level 0–19, BPM ≤ 178, flag aktif & baru; tabel versi server terpisah → metadata dibagi client–server.
- **OBSERVED:** `ABM\` berisi 5.213 file musik/chart; 458 file `*_note.tbm` (**INFERRED:** chart mode gitar dipisah); prefix huruf menandai katalog/region.
- Suara gameplay: perfect, miss, combo 1–5, gauge checkpoint/max, beat rush, piano.

## D. Teknologi client
| Komponen | Temuan |
|---|---|
| `Audition.exe` | Themida (section `.themida`, `.boot`), x86, versi info T3Entertainment © 2007, butuh admin |
| Patcher | .NET 4.7.2: pemutar musik launcher, banner remote, cek MD5, ekstrak patch, kirim email error |
| Render / input / audio | Direct3D 9, DirectInput, FMOD 3.x (UPX), keyboard hook (matikan tombol Windows, timer resolusi tinggi untuk ketepatan input) |
| Shader | D3DX9 Effect terkompilasi; teknik UI & `CharacterLight…`, bloom/HDR; parameter bergaya Unity termasuk `_ColorMaskMap` (**INFERRED:** dye via color mask) |
| Launcher | Banner & iklan dari server (live-ops) |
| Lain | jsoncpp (2024), WinINet (halaman web in-game), Lua 5.1 (penggunaan UNKNOWN) |

## E. File terenkripsi / tidak terbaca (dihentikan sesuai aturan)
| Item | Status |
|---|---|
| `SCRIPT\*.bin` (187) | Terenkripsi (blok 64-bit) |
| `SCRIPT\*.loc` (4 bahasa) | Obfuskasi |
| 302 arsip `DATA\*.acv` baru | Index terenkripsi |
| `ABM\*.abm/.tbm/.amp` | Terenkripsi/terkompresi setelah header |
| `Audition.exe` | Themida |

---

## F. Pelajaran untuk Nexus Saga (adopsi / ubah / buang)
| Temuan AyoDance | Keputusan Nexus Saga | Catatan |
|---|---|---|
| Kerangka event generik + modul per event | **ADOPSI** | Event = data + modul UI kecil; cocok dengan live-ops berbasis data |
| Pola "Renewal" (versi lama tetap ada) | **UBAH** | Kita pakai feature flag server, lalu hapus versi lama setelah migrasi — mencegah utang teknis 20 tahun |
| Tabel desain spreadsheet bertipe, dibagi client–server | **ADOPSI** | Sejalan dengan content bundle ber-hash (09 §5); authoring JSON/Sheets + baris tipe/skema |
| Room 6 pemain + ready → load → main → hasil | **ADOPSI untuk Rest Room/Dance Duel**; arena tetap ≤ 10 (5v5) | |
| **Level = panjang urutan panah**, konfirmasi di beat | **ADOPSI untuk Dance Duel** | Mekanik sederhana, mudah dipahami, skala kesulitan jelas; kita pakai 4 arah dulu, 8 arah sebagai mode lanjut |
| Voice chat grup per room + mute per pemain | **ADOPSI (Fase 3)** | Wajib ada mute/report; 13+ → voice default off untuk akun di bawah umur dewasa |
| Quick-chat makro & tabel kata kasar | **ADOPSI** | Filter di **server**, bukan hanya client |
| Blokir per pemain di room | **ADOPSI** | Sudah ada di aturan keselamatan |
| Guild mendalam: bank, absensi, rumah, NPC butler, boss raid, channel berbayar | **ADOPSI sebagian** | Squad HQ + absensi + boss raid (PvE squad) cocok; channel berbayar **dibuang** (P2W sosial) |
| Couple → wedding → garden bersama | **ADOPSI sebagian (18+)** | Couple room 18+ sudah ada; wedding/garden sebagai konten sosial, tanpa slot machine |
| **Slot machine couple, gacha + upgrade (Lumi)** | **BUANG slot machine & upgrade berbayar** | Bertentangan dengan rating 13+, risiko regulasi judi, dan pilar non-P2W. Gacha kita tetap transparan + pity |
| UI peluang gacha (ChanceHelp) | **ADOPSI** | Sejalan dengan aturan gacha transparan |
| Toko: keranjang, **hadiah**, **outfit tersimpan (MyCodi)**, deal harian, preview | **ADOPSI** | Gifting + simpan outfit = fitur sosial kuat; deal harian = live-ops murah |
| AudiPass (battle pass) + absensi + referral | **ADOPSI** | Sudah sejalan dengan battle pass kosmetik |
| Photo studio, sticker, megaphone | **ADOPSI (Fase 3)** | Konten sosial murah; megaphone dengan cooldown + moderasi |
| Banyak mata uang terpisah (garden cash, SG cash, event cash) | **BUANG** | Kita tetap 3 mata uang; mata uang event = item/token event, bukan mata uang ke-4 |
| Shader color mask untuk dye | **ADOPSI** | Mengonfirmasi keputusan Dye system (lihat riset wardrobe) |
| Banner launcher dari server | **ADOPSI** | Berita/event dari server |
| Proteksi client (Themida, enkripsi data, Xigncode) | **CATAT** | Kita mengandalkan **server-authoritative**; obfuskasi client hanya lapisan tambahan, bukan keamanan utama |

## G. Belum diketahui (tidak akan dibongkar)
Opsi room, penonton, password, batas channel, isi AudiPass, mekanik Lumi, isi broadcast, data lagu modern. Jalur sah bila dibutuhkan: **observasi gameplay** dengan akun sendiri atau dokumentasi publik.
