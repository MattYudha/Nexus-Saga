# 11 — Nexus Saga: Chronicles, Dijelaskan dengan Bahasa Sederhana (2026-10-24)

> Versi "bahasa bayi" dari semua keputusan di dokumen 01–10. Kalau ada yang bertentangan, dokumen teknis (08/09/10) dan `90-decision-log.md` yang berlaku.

---

## 1. Game ini apa, dalam satu kalimat?
**Kamu punya "dirimu" di dunia game (avatar), kamu nongkrong dan berteman di sebuah kota, lalu kamu masuk arena untuk berkelahi bareng tim memakai pakaian perang dan senjata hero.**

Gabungan dari:
- **AyoDance** → avatar keren, nongkrong, dandan.
- **LostSaga** → berkelahi seru, pakaian perang bisa copot.
- **Roblox** → dunia yang terus di-update dan belanja tanpa curang.
- **Mobile Legends/Dota** → rank, MMR, statistik.

---

## 2. Kamu = Avatarmu
- Saat pertama main, kamu membuat **avatar**: pilih badan laki-laki atau perempuan, wajah, rambut, tinggi/gempal.
- Avatar itu adalah **kamu**. Dia yang jalan-jalan di kota, nongkrong, dan berkelahi di arena.
- Baju sehari-hari avatar (kaos, celana, sepatu, topi) disebut **kostum**. Kostum **tidak pernah copot**, bahkan saat berkelahi. Ini identitasmu.
- Kostum **tidak membuatmu lebih kuat**. Ia hanya membuatmu **keren**.

Contoh: kamu pakai jaket merah dan sepatu putih. Di kota, di rest room, dan di arena, kamu tetap terlihat dengan jaket merah itu.

---

## 3. Kota (Plaza)
- Begitu login, kamu muncul di **kota kecil**. Isinya 30–60 pemain lain sekaligus.
- Kamu bisa jalan, lompat, joget (emote), dan ngobrol.
- Di kota ada beberapa "pintu":
  | Pintu | Untuk apa |
  |---|---|
  | **Battle Gate** | Masuk antrean berkelahi (ranked/cepat) atau bikin room sendiri |
  | **Relic Gate** | Masuk dungeon untuk farming |
  | **Rest Room** | Tempat santai & minigame |
  | **Shop / Gacha / Wardrobe** | Belanja & dandan |
  | **Squad HQ** | Markas geng (squad) kamu |
- Kota **berubah** sesuai hasil perang antar-squad: bendera dan warna distrik berganti, dan ada patung pemain terbaik minggu ini.

---

## 4. Rest Room & Minigame (tempat santai)
- Kalau capek berkelahi, kamu bisa ke **Rest Room**: ngobrol, kenalan, berteman.
- Ada minigame untuk mendapat Gold kecil-kecilan:
  - **Fashion Contest**: pamer kostum di panggung, pemain lain memberi vote, pemenang dapat Gold.
  - **Photo Booth**: berpose dengan avatar untuk disimpan/dibagikan.
  - **Mancing**.
  - **Kuis**.
> Catatan: **tidak ada mode dance/menari** di Nexus Saga (menghindari copyright musik). Lihat `12-rest-room-tanpa-dance.md`.

- **Couple room** (kenalan/dating) hanya untuk umur **18+** yang sudah verifikasi. Ada tombol block, report, dan mute. Game ini sendiri untuk umur 13+.

---

## 5. Hero & Gear (pakaian perang)
Bayangkan **hero = paket pakaian perang + senjata** yang kamu pakai **di atas** kostummu.

Satu hero punya 4 bagian:
| Bagian | Bisa copot saat berkelahi? | Fungsi |
|---|---|---|
| **Senjata** | ❌ Tidak pernah (sebelum KO) | Menentukan gaya bertarung dasar (pukulan, combo) |
| **Helm** | ✅ | Memberi 1 skill |
| **Armor** | ✅ | Memberi 1 skill |
| **Trinket** (jubah/aksesori) | ✅ | Memberi 1 skill |

- Semua hero memakai **kerangka tubuh yang sama**. Jadi helm hero A bisa dipakai hero B, dan baju avatar cocok untuk semua hero.
- Contoh hero untuk awal (MVP):
  - **Pegulat** (jarak dekat, banting, pegang lawan).
  - **Penembak/Zoner** (jarak jauh, kontrol area).
  - Nanti ditambah **Support** (pelindung, bantu teman).
- Badan semua pemain punya **"kotak kena pukul" yang sama ukurannya**. Avatar kecil atau besar sama-sama gampang dipukul. Adil.

---

## 6. Cara berkelahi
- Arena dilihat dari **atas-samping, kamera diam** (seperti LostSaga). Kamu bisa jalan **8 arah**, lompat, dan lari.
- Tombol dasar: **pukul**, **skill**, **lompat**, **dash** (lari cepat menghindar), **guard** (menangkis).
- **Combo**: pukulan bisa disambung ke pukulan lain kalau kena. Lawan bisa dilempar ke udara lalu dipukul lagi (**juggle**). Tapi tiap lawan punya batas juggle, jadi tidak ada combo tak terbatas.
- **Aim-assist kecil**: kalau musuh sedikit miring dari arah pukulanmu (sampai 22,5°), karaktermu otomatis berputar sedikit ke arahnya.
- **Guard (menangkis) hanya dari depan.**
  - Saat menahan guard, arah badanmu terkunci.
  - Kalau dipukul dari belakang, tetap kena. Jadi menyerang dari belakang dan kerja sama tim sangat berguna.
  - Kalau kamu menekan guard tanpa memilih arah, badanmu otomatis menghadap musuh terdekat.
  - Guard punya **meter**. Kalau terlalu lama ditangkis terus, guard-nya **pecah** dan kamu pusing sebentar (Faint).
- Status kena pukul yang bisa terjadi:
  - terlempar ke udara (Airborne)
  - jatuh terbaring (Down)
  - pusing (Faint)
  - membeku (Frozen)
  - dipegang/diikat (Bound)

  Saat bangun dari jatuh, kamu kebal sebentar.

---

## 7. Darah & Nyawa (bagian paling penting)
Bayangkan nyawamu punya **dua lapis**:

**Lapis 1 — Darah (HP)**
- Kamu dipukul, darah turun.
- Sekeras apa pun pukulannya, darah **berhenti di 0**. Kamu **tidak langsung mati**.

**Lapis 2 — Kondisi Kritis (Critical)**
Begitu darah 0:
1. Kamu terpental dan jatuh sebentar (kebal waktu bangun). Kesempatan napas.
2. Kamu punya **3 "Break Stock"** = 3 lapis pertahanan terakhir.
3. Setiap 1 stock pecah:
   - satu pakaian perang copot dan jatuh ke lantai, urutannya **Helm → Trinket → Armor**;
   - kamu jatuh terbanting (kebal waktu bangun).
4. Pukulan **berat** langsung memecahkan 1 stock. Pukulan **ringan** mengisi meter; kalau penuh, 1 stock pecah.
5. Stock ke-3 pecah → **KO**. Senjatamu terpental (cuma efek visual).

Saat Kritis:
- tidak bisa ganti hero;
- tidak bisa disembuhkan (teman Support hanya bisa memberi perisai);
- lari sedikit lebih lambat;
- posisimu terlihat lawan, jadi tidak bisa sembunyi.

Tapi kamu **masih bisa melawan** sampai titik terakhir. Comeback tetap mungkin.

**Kenapa begini?** Supaya tidak ada yang mati konyol dalam sekejap, dan momen terakhir selalu menegangkan.

---

## 8. Jurang (DropZone)
- Arena punya pinggiran/jurang. Kalau kamu didorong (atau jatuh) ke jurang:
  | Kondisimu | Akibat |
  |---|---|
  | Darah masih ada | Darah berkurang (mis. 15%). Kalau sisa darah lebih kecil, darah jadi 0 → Kritis (tidak mati) |
  | Sudah Kritis | 1 Break Stock pecah |
- Pakaian perang yang copot karena jatuh **tidak hilang di jurang**. Ia terlempar ke tepi tempat kamu jatuh, jadi lawan bisa memungutnya.
- Kamu **jatuh dari langit kembali ke dekat tempat kamu jatuh** (bukan ke markas), lalu terduduk sebentar ±0,6 detik. Selama itu kamu tidak bisa dipukul dan tidak bisa memukul.
- Jadi jurang **tidak bisa dipakai untuk kabur**, dan lawan yang mendorongmu tetap untung.
- Kalau kamu sengaja lompat ke jurang, poinnya tetap untuk musuh terakhir yang memukulmu.

---

## 9. Memungut pakaian perang lawan
- Helm, Armor, dan Trinket yang jatuh di lantai bisa dipungut **siapa saja yang paling cepat**, termasuk lawan.
- Kalau kamu memungut helm lawan, kamu dapat **skill helm itu** sampai helm itu copot lagi atau kamu KO.
- Senjata **tidak bisa** dipungut.
- Ini hanya berlaku **di dalam pertandingan**. Barang di tas (inventory) pemiliknya tidak pernah hilang.
- Memungut gear **tidak menambah nyawa** (Break Stock selalu 3).

---

## 10. Ganti Hero di tengah pertandingan (Hero Swap)
- Sebelum bertanding kamu memilih **3 hero** (squad pribadi).
- Darahmu **satu** untuk ketiganya (milik kamu, bukan milik hero).
- Dua cara ganti:
  | Cara | Kapan | Jeda (cooldown) |
  |---|---|---|
  | **Swap biasa** | Saat santai, atau tepat setelah pukulanmu kena/ditangkis (untuk menyambung combo) | 3 detik |
  | **Burst Swap** | Saat kamu sedang dipukuli, atau untuk membatalkan pukulanmu yang meleset | 12 detik; mendorong lawan + kebal sebentar |
- Jeda dua cara itu **satu timer bersama**, jadi tidak bisa disambung beruntun.
- Saat Kritis, ganti hero **dikunci**.

---

## 11. Mode Pertandingan
| Mode | Cara main | Mati itu artinya… |
|---|---|---|
| **Survival / Elimination** (1v1, 3v3) | Ronde 90–120 detik | KO = keluar sampai ronde berikutnya. Kalau waktu habis: tim dengan anggota hidup lebih banyak → stock lebih banyak → darah lebih banyak → sudden death |
| **Team Deathmatch** (sampai 5v5) | Kumpulkan skor KO tim | Hidup lagi setelah 5 detik (awal match) sampai 10 detik (akhir match), sama untuk semua orang |
- Main bareng teman: **duo, trio, atau party 5**.
- Ada dua cara masuk:
  - **Antrean ranked/cepat**: dipasangkan otomatis.
  - **Custom room** ala LostSaga: bikin room, atur tim, ready.

---

## 12. Rank, MMR, dan Statistik
- Ada **nilai tersembunyi (MMR)** untuk mencari lawan yang seimbang, dan **Rank Points yang terlihat**.
- Tingkatan: **Bronze → Silver → Gold → Platinum → Diamond → Mythic** (+ Top 100).
- Profilmu menampilkan:
  - win rate
  - KDA (Kill/Death/Assist)
  - hero favorit
  - statistik per hero
  - riwayat pertandingan
  - rank tertinggi per season
- **KO** dihitung untuk yang memecahkan stock terakhir. **Assist** untuk yang ikut memukul dalam 10 detik terakhir.

---

## 13. Squad (geng), Squad War, Leader Duel
- Kamu bisa bergabung dengan **squad**, yang punya markas sendiri (**Squad HQ**) dan bisa dihias dengan furnitur.
- **Squad War** mingguan: squad memperebutkan distrik di kota. Pemenangnya membuat distrik itu berwarna/berbendera squad mereka selama seminggu.
- **Leader Duel**: ketua squad duel 1 lawan 1, ditayangkan di layar besar kota.
- **Mentor**: pemain Diamond ke atas membimbing pemula. Dua-duanya dapat hadiah kalau si pemula naik rank.

---

## 14. Relic (dungeon untuk farming)
- Mode lawan monster (1–4 pemain) untuk mencari bahan, avatar item, dan relic.
- Masuk pakai **Gold** → hadiah standar.
- Masuk pakai **Ticket** → peti spesial. Peluang dapatnya **ditulis jelas**, dan ada **jaminan (pity)** setelah sekian kali.

---

## 15. Uang di dalam game (tanpa pay-to-win)
| Mata uang | Didapat dari | Dipakai untuk |
|---|---|---|
| **Gold** | Main, minigame, quest | Beli hero, sewa kostum 7/30 hari, masuk Relic |
| **Ticket** | Quest, event, battle pass | Gacha |
| **MiCash** | Uang asli | Kostum permanen, skin, efek keren, battle pass premium |

Aturan emas:
- **Yang dijual uang asli hanya membuat KEREN, tidak membuat KUAT.**
- Hero yang dijual pakai MiCash **juga bisa dibeli pakai Gold**.
- **Sewa vs permanen**: barang bisa disewa 7 hari, 30 hari, atau dibeli permanen.
- **Rent-to-own**: uang sewa jadi potongan harga kalau nanti membeli permanen. Sewa tidak terasa hangus.
- **Gacha jujur**: peluang ditulis, ada pity, dan barang dobel bisa ditukar.

---

## 16. Mode Developer
- Akun dengan peran **Developer/GM** punya panel tambahan:
  - memunculkan item
  - mengubah cuaca kota
  - ban cheater
  - mengatur MMR untuk testing
- Ada ruangan khusus developer (**Dev Lounge**).
- Pengecekannya di **server**, bukan di aplikasi pemain. Jadi tidak bisa dibobol dengan meng-hack aplikasi. Semua aksi developer **dicatat** (audit log).

---

## 17. "Update terus"
- **Season** 8–10 minggu: rank di-reset sebagian, battle pass baru, hero/skin baru.
- **Event mingguan**: double Gold, Relic spesial, turnamen Leader Duel.
- Angka-angka (harga, peluang gacha, kekuatan hero) disimpan di server sebagai **data**. Developer bisa menyeimbangkan game **tanpa** pemain harus update aplikasi dari store. Aplikasi cukup mengunduh data baru saat login.

---

## 18. Di balik layar (teknis, versi bayi)
- **Unity** = "kamera dan kuas". Ia menggambar dunia, avatar, dan animasi di layarmu.
- **Combat Core** = "otak pertarungan". Ia program kecil yang menghitung siapa kena pukul, siapa terpental, dan darah berapa.
  - **Otak yang sama persis** dipasang di HP/PC kamu dan di server.
  - Server = **wasit**. Keputusannya yang dipakai.
  - Otak di PC kamu **menebak duluan** supaya pukulan terasa instan. Kalau tebakannya salah, wasit membetulkan.
- **Server pertandingan** = wasit yang menghitung 60 kali per detik untuk 10 pemain.
- **Nakama** = "kantor administrasi":
  - akun, teman, party, chat, squad
  - pencari lawan (matchmaker)
  - dompet Gold/Ticket/MiCash, tas barang (termasuk masa sewa)
  - leaderboard
  - mengatur kota (Plaza)
- Alur dari kota ke arena:
  1. Kamu di kota.
  2. Tekan Battle Gate / masuk room.
  3. Kantor (Nakama) mencarikan lawan.
  4. Pilih 3 hero (kantor mengecek kamu memang punya hero itu / sewanya belum habis).
  5. Kantor memberi **tiket masuk** bertanda tangan.
  6. Kamu masuk ke server pertandingan.
  7. Selesai: wasit melapor **langsung** ke kantor (bukan lewat HP kamu) untuk menambah Gold, mengubah rank, dan menyimpan statistik.
  8. Kamu kembali ke kota.

---

## 19. Urutan membuatnya
1. **Spike (2–3 minggu)**: dua kapsul saling pukul lewat internet dengan lag buatan 150 ms. Diuji juga Photon Quantum 2–3 hari sebagai pembanding.
   - Lulus kalau:
     - pukulan terasa instan (≤ 1 frame);
     - salah tebak pukulan < 5%;
     - koreksi posisi < 0,5 m;
     - 1 CPU bisa ≥ 20 pertandingan;
     - internet < 64 kbps per pemain.
   - Gagal → pindah ke Photon Quantum.
2. **Vertical slice (MVP)**:
   - Login + peran
   - Kota 1 distrik + chat + emote
   - Wardrobe 5 slot + toko Gold (sewa/permanen)
   - Arena 1v1 & 2v2, 2 hero (Pegulat + Zoner)
   - Rank + profil sederhana
   - Panel developer
3. **Fase 2–3**:
   - Squad War
   - Relic
   - Rest Room & minigame
   - Gacha
   - Battle pass
   - Hero ke-3
   - 5v5 penuh

