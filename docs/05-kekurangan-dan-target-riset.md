# 05 — Daftar Kekurangan & Target Riset Tambahan (2026-10-24)

## A. Kondisi PC saat ini
| Item | Nilai | Catatan |
|---|---|---|
| Disk C: kosong | **50 GB** dari 477 GB | ⚠️ Sempit. AyoDance saja ~22 GB. Ekstrak arsip game bisa 2–3× ukuran asli |
| RAM | 16 GB | Cukup untuk Ghidra (alokasikan 6–8 GB) |
| GPU | GTX 1650 + UHD 730 | Cukup untuk Unity/Godot 2.5D |

## B. Checklist kekurangan

### Wajib
| # | Kekurangan | Untuk apa | Cara |
|---|---|---|---|
| 1 | **Client LostSaga** | Sumber utama state machine combat, hero swap, Relic, sewa item | Unduh client resmi yang masih beroperasi di region mana pun; cukup terinstal, tidak perlu login/main |
| 2 | **JDK 21 + Ghidra 12.1.x** | Dekompilasi `.exe/.dll` native (C++) lewat REA | Temurin JDK 21 → ekstrak Ghidra → `setx GHIDRA_INSTALL_DIR "C:\Tools\ghidra_12.1.x_PUBLIC"` → restart terminal |
| 3 | **Ruang disk** | Ekstrak arsip game | Kosongkan ≥100 GB atau pakai disk eksternal, folder kerja mis. `D:\RE-Lab\` |
| 4 | **Repo git khusus proyek** | Saat ini repo git berakar di `C:\Users\US3R` (berisiko) | `git init` di `NyxCreats` |

### Sangat disarankan (melengkapi REA)
REA kuat untuk biner, .NET, arsip standar, SQLite. Untuk format **khusus game** perlu alat bantu:

| Alat | Fungsi | Kapan dipakai |
|---|---|---|
| **ImHex** | Hex editor + pattern language untuk memetakan format file tak dikenal | `.acv`/`.tbm` AyoDance, file data LostSaga |
| **QuickBMS** | Ekstraktor arsip game generik berbasis skrip | Arsip `.pak/.acv` yang formatnya sudah pernah dipetakan komunitas |
| **AssetRipper** | Ekstrak scene, prefab, animasi, ScriptableObject dari game Unity | Semua target Unity |
| **Cpp2IL** atau **Il2CppDumper** | Memulihkan nama class/method dari game Unity IL2CPP | Game Unity modern (mobile/PC) |
| **UnityPy** (Python) | Membaca asset Unity lewat skrip | Ekstrak tabel data massal |
| **JPEXS FFDec** | Dekompilasi Flash/AIR (SWF) | Game berbasis Adobe AIR |
| **OBS + mpv** (frame-step) | Rekam & analisis frame-by-frame | Mengukur durasi startup/hitstun/i-frame dari video |

### Non-teknis
| # | Kekurangan | Catatan |
|---|---|---|
| 5 | Regulasi game Indonesia | Klasifikasi gim (IGRS) & pendaftaran PSE perlu dicek ulang ke sumber resmi Komdigi sebelum rilis; berpengaruh ke rating 13+ dan gacha |
| 6 | Art direction | Belum ada: gaya visual (chibi/anime/low-poly), referensi moodboard |
| 7 | Payment MiCash | Gateway top-up (mis. Mayar yang sudah tersambung, Midtrans, Xendit) — fase akhir |

## C. Prinsip memilih target riset (urut dari termudah)
1. **Open-source / terdokumentasi** → baca langsung, tanpa RE, 100% legal untuk dipelajari.
2. **Unity Mono** (`*_Data\Managed\Assembly-CSharp.dll` ada) → REA `inspect_managed_artifact` langsung jalan **tanpa Ghidra**.
3. **Unity IL2CPP** (ada `GameAssembly.dll` + `global-metadata.dat`) → butuh Cpp2IL/Il2CppDumper dulu.
4. **Native C++** (LostSaga, AyoDance) → butuh Ghidra; paling lama.
5. **Hindari** menjalankan/attach game ber-anti-cheat kernel (Vanguard, EAC, BattlEye, Xigncode, nProtect). Analisis file di disk saja.
6. **Jangan pakai source code bocoran / private server** (melanggar hak cipta dan mencemari kode kita).

## D. Target riset per sistem

### 1. Combat 2.5D & State Machine (sistem #7)
| Target | Jenis | Kenapa berguna |
|---|---|---|
| **LostSaga** | Native C++ | Referensi utama: state, swap gear, rasa combat |
| **Ikemen GO** (engine MUGEN open-source) | Open-source (Go) | Format state MUGEN (`StateDef`, `HitDef`, statetype Stand/Crouch/Air/Lying, hitstun, juggle) adalah **model state machine fighting game paling terdokumentasi** di dunia — bisa dijadikan blueprint format data skill kita |
| **DDNet** (Teeworlds) | Open-source (C++) | Multiplayer **2D side-view** dengan client prediction, server browser, ranking, **skin kosmetik nol stat** — contoh netcode yang relevan |
| **Brawlhalla** | Gratis, Steam | Platform fighter 2D online, ranked tier, ekonomi kosmetik non-P2W. Observasi + video frame-by-frame |
| **Unity "Boss Room"** sample | Open-source (Unity) | Sistem Action/Ability + lobby + character select dengan Netcode for GameObjects — template arsitektur |

### 2. Avatar, Wardrobe, Lobi Sosial (sistem #2, #3, #4)
| Target | Jenis | Kenapa berguna |
|---|---|---|
| **AyoDance** | Sudah ada (native) | Slot kostum, Plaza/room, ritme |
| **Firestorm Viewer / OpenSimulator** (Second Life) | Open-source | Sistem avatar berlapis (wearables), inventory, region/instance, chat lokal — sangat matang & terdokumentasi |
| **Luanti (Minetest)** | Open-source (C++/Lua) | Model "Roblox-lite": dunia ringan, mod Lua, server multiplayer |
| **Roblox** | Dokumentasi publik | Avatar API, layered clothing, economy/marketplace — **pelajari dari docs**, jangan RE client (ada anti-cheat & ToS ketat) |

### 3. Matchmaking, MMR, Profil (sistem #5, #6, #9)
| Target | Jenis | Kenapa berguna |
|---|---|---|
| **OpenSkill** | Library open-source | Rating tim, langsung pakai |
| **Open Match** (Google) | Open-source | Arsitektur matchmaker (ticket, pool, director) |
| **Nakama** | Open-source | Matchmaker, leaderboard, party, guild, wallet sudah jadi |
| **DDNet ranks** | Open-source | Contoh database statistik & ranking komunitas |

### 4. Ekonomi, Gacha, Sewa, Live-ops (sistem #11, #12, #13)
| Target | Jenis | Kenapa berguna |
|---|---|---|
| **LostSaga** | Native | Tabel durasi & gacha (gear present) |
| **Unturned** | Gratis, Unity | Sistem item cosmetic + crafting/inventory berbasis **file `.dat` teks terbuka** — contoh data-driven content yang bagus. Ada BattlEye → statis saja |
| **Brawlhalla / DDNet** | Lihat atas | Ekonomi kosmetik murni |
| Dokumen rate gacha publik (Genshin, MLBB) | Publik | Angka pity & rate referensi — tidak perlu RE |

## E. Rekomendasi urutan unduhan (hemat disk)
1. **Ikemen GO + DDNet** (kecil, < 1 GB, open-source) → riset state machine & netcode 2D bisa mulai **hari ini tanpa Ghidra**.
2. **LostSaga** client.
3. **JDK 21 + Ghidra**.
4. **Unity Boss Room** (repo GitHub) → template arsitektur.
5. Opsional: Brawlhalla, Unturned, Firestorm/OpenSim.

## F. Format serah-terima ke REA
Setelah unduh, cukup kirim path folder, contoh: `D:\RE-Lab\LostSaga\`. Claude akan:
1. Inventaris file (jenis engine, arsip, tabel data).
2. Pilih tool REA yang sesuai (managed / PE resource / arsip / native).
3. Tulis hasil ke `docs/research/<sistem>-<game>.md` dengan pemisahan **observasi / inferensi / belum diketahui**.
