# 10 — Review Kritis v3: Celah yang Tersisa Sebelum Arsitektur Dikunci (2026-10-24)

Tujuan: menemukan hal yang, bila tidak diputuskan **sekarang**, akan memaksa perombakan Combat Core, format input/snapshot, atau pipeline aset nanti.

Legenda: 🔴 memengaruhi Core/format data (harus diputuskan sebelum spike) · 🟡 memengaruhi produksi · 🟢 bisa ditunda

---

## A. Koreksi atas keputusan stack

### A1. 🔴 "Bisa pindah ke Photon Quantum kapan saja tanpa merombak desain" — **tidak sepenuhnya benar**
Yang **bisa** pindah: desain (state, HitDef, data hero, aturan Critical/Swap/Gear).
Yang **harus ditulis ulang**: kode.
- Quantum punya ECS sendiri, tipe fixed-point sendiri (`FP`), physics sendiri, dan DSL komponen.
- Model jaringannya berbeda: **semua entity diprediksi** di semua client (rollback penuh), bukan "lokal diprediksi + remote diinterpolasi + lag compensation di server".

Mitigasi supaya biaya pindah kecil:
1. Tulis Core dengan gaya **data-oriented**: state = struct komponen, logika = fungsi murni `Step(state, inputs) → state`, tanpa objek berpointer.
2. Bungkus math di tipe `Fix64`/`FixVec3` milik kita dengan API mirip `FP`.
3. Transport dan netcode **di luar** Core (sudah direncanakan).
4. **Saat spike, uji juga sampel Quantum 2–3 hari** untuk perbandingan langsung, sebelum ratusan jam masuk ke netcode custom.

### A2. 🔴 Masalah "rasa" terbesar: reaksi korban **remote** datang terlambat
Model DDNet: pemain lokal diprediksi, pemain lain **diinterpolasi di masa lalu** (~1 interval snapshot + buffer).
- Di brawler juggle, saat kita memukul lawan, lawan baru terlempar **setelah konfirmasi server** (≈ 1 RTT, 100–200 ms). Combo udara terasa "lengket"/delay.
- DDNet tidak punya masalah ini karena bukan game juggle.

Usulan solusi (wajib masuk kriteria spike):
- **Predicted hit reaction.** Reaksi korban sepenuhnya ditentukan HitDef penyerang (prinsip Ikemen). Jadi client bisa langsung mensimulasikan korban masuk hitstun/knockback saat hit-confirm lokal.
- Korban yang terkena pukulan kita dipindah dari mode *interpolasi* ke mode *prediksi* sampai hitstun selesai. Kemudian dikoreksi oleh snapshot server.
- Biaya: logika handoff interpolasi ↔ prediksi per entity. Ini kompleks. Quantum mendapatkannya gratis karena memprediksi semua entity. **Ini argumen terkuat untuk Quantum**, dan kriteria lolos/gagal spike harus mengukurnya.

### A3. 🟡 Bottleneck sebenarnya untuk solo + AI adalah **konten**, bukan kode
AI mempercepat kode, tapi tidak membuat model 3D, rigging, dan animasi. Kebutuhan per hero:
- Animasi 15–30 aksi
- **Data frame + hitbox per frame**
- Gear 4 slot
- VFX/SFX

Mitigasi:
- Shared humanoid rig → bisa memakai **animasi humanoid siap pakai** (Mixamo, marketplace) lewat retarget.
- Gaya visual stylized/low-poly agar asset pack komersial bisa dipakai.
- **Hitbox editor di Unity Editor** (tool internal: scrub animasi, gambar capsule/OBB per frame, ekspor ke data Core). Tanpa tool ini, authoring hitbox tangan adalah kerja rodi. Masuk daftar pekerjaan **sebelum** hero ke-2.

### A4. 🟡 Shared rig + "2–3 body type" melipatgandakan biaya wardrobe
Setiap item kostum harus dibuat **per body type**. 3 body type = 3× biaya untuk setiap item toko.

Usulan:
- **2 base body** (laki-laki/perempuan, seperti AyoDance) dengan rangka identik.
- Variasi tinggi/gempal via **bone scale + blendshape**, bukan mesh terpisah.
- Item kostum dibuat per gender (2×), bukan per body type.

## B. Celah desain yang belum punya jawaban

### B1. 🔴 Sistem facing & targeting (memengaruhi struktur input Core)
Gerak 8 arah + Lock Facing saat guard memunculkan pertanyaan yang belum dijawab:
1. **Arah hadap diambil dari mana?** Arah gerak terakhir? Jika pemain sedang lari menjauh lalu menekan guard, ia akan mengunci guard **membelakangi musuh**.
2. **Serangan diarahkan ke mana?** Murni arah hadap 8 arah (musuh di sudut 20° tidak kena), atau ada **aim-assist** (snap ±22,5° ke musuh terdekat dalam jangkauan)?
3. Apakah ada **lock-on target**? (Kebanyakan brawler 5v5 tidak memakainya.)

Usulan:
- Arah hadap = arah input terakhir.
- Saat guard/serangan dimulai **dengan input arah ditahan**, arah itu yang dipakai.
- Serangan memakai **soft aim-assist** (cone ±22,5°, jangkauan per skill, deterministik: musuh terdekat, seri dipecah dengan id).
- Tanpa lock-on.

Ini harus final sebelum spike, karena menentukan isi struct input (arah 8 vs analog, tombol).

### B2. 🔴 Aturan mode/match belum ada (memengaruhi Critical, KO, respawn)
Critical, KO, dan "kabur di 5v5" bergantung pada aturan mode yang belum didefinisikan:
- Respawn atau eliminasi? Delay respawn? Kondisi menang (skor KO, waktu, ronde)?
- Apa yang dicegah dengan menghukum pemain Critical yang kabur, jika mati tidak berarti apa-apa (respawn cepat)?

Usulan: Core punya **Mode Rules** berbasis data:
- `respawn` (on/off, delay)
- `winCondition` (KO count / last team standing / objective)
- `roundCount`, `timeLimit`
- `dropZoneEnabled`

MVP: **Team Deathmatch** (respawn 5 detik, target skor) + **Survival** (tanpa respawn, ronde).

### B3. 🔴 HP milik pemain vs perbedaan antar-hero
Jika HP milik pemain, field "HP dasar per hero" tidak bermakna (sudah dihapus dari 08 §10).
- Perbedaan ketahanan hero dibuat lewat **pengali defense** dan **berat** (knockback), bukan HP.
- Max HP = konstanta mode.

### B4. 🔴 Hurtbox vs body type
Kalau body type kecil punya hurtbox kecil, ia lebih sulit dipukul. Itu **P2W terselubung** bila body type/kostum dijual.
- Hurtbox **satu standar untuk semua pemain** (sudah dikoreksi di 08 §5.2). Body type hanya visual.

### B5. 🟡 Heal/Support vs Critical
Arketipe hero ke-3 = Support. Pertanyaannya:
- Apakah heal bisa mengeluarkan pemain dari Critical (HP > 0)?
- Bisakah memulihkan Break Stock?
- Ada revive?

Usulan:
- Heal **tidak berlaku** saat Critical (Critical hanya berakhir dengan KO).
- Support dapat memberi **shield sementara** yang menahan pengisian Break Meter.
- Tanpa revive. Keputusan ini memengaruhi desain hero Support.

### B6. 🟡 Atribusi KO & assist (untuk KDA, MMR, reward)
Critical menambah tahap: siapa yang mendapat KO? Usulan:
- **KO** = yang memecahkan Break Stock terakhir (termasuk lewat jatuh: musuh terakhir yang memukul dalam 10 detik).
- **Assist** = siapa pun yang memberi damage/break dalam 10 detik terakhir.
- Dicatat oleh game server dalam laporan akhir.

### B7. 🟡 S5 belum dijawab
Swap-cancel dari serangan: kapan saja, atau hanya setelah serangan mengenai/di-guard (`movecontact`)?
- Jika kapan saja, swap jadi pembatal animasi universal setiap 3 detik: recovery serangan berisiko bisa dihapus.
- Usulan: hanya setelah contact.

### B8. 🟢 Indikator posisi pemain Critical
Server tetap mengirim posisi semua pemain (10 pemain = snapshot penuh). Jika nanti ada culling/fog per penonton, pemain Critical **dikecualikan** dari culling.

### B9. 🟢 Pickup gear: durasi
Disebutkan "akses skill sampai durasinya habis atau rontok lagi". Durasi gear pungutan perlu angka (usulan: sampai rontok atau KO, tanpa timer — lebih sederhana).

## C. Hal yang sudah divalidasi aman
| Keputusan | Kenapa aman |
|---|---|
| Lock Facing saat guard (G1 revisi) | Lebih responsif daripada batas putar; deterministik; membuka cross-up. Bergantung pada B1 |
| Shared cooldown S2 | Satu timer = satu field di snapshot |
| S4 kunci swap saat Critical | Menutup eksploit "nyawa dari hero lain" |
| C1 Break Stock terpisah dari gear | Menutup eksploit pickup gear = nyawa |
| C4 revisi (penalti gerak + indikator) | Menjaga clutch; mencegah sembunyi |
| Core C# murni + server .NET + Nakama | Cocok untuk solo: meta-fitur bawaan, satu bahasa untuk combat |
| Content bundle ber-hash | Balancing tanpa patch store |

## D. Keputusan yang dibutuhkan sebelum spike
| # | Topik | Usulan |
|---|---|---|
| 1 | B1 Facing & aim-assist | Arah input terakhir + soft aim-assist ±22,5°, tanpa lock-on |
| 2 | B2 Mode MVP | Team Deathmatch + Survival |
| 3 | B5 Heal vs Critical | Heal tidak berlaku saat Critical; tanpa revive |
| 4 | B6 KO/assist | Pemecah stock terakhir / jendela 10 detik |
| 5 | B7 (S5) | Swap-cancel hanya setelah contact |
| 6 | A2 Kriteria spike | Wajib mengukur predicted hit reaction pada korban remote |
| 7 | A1 | Uji sampel Quantum 2–3 hari selama spike |
| 8 | A4 | 2 base body (L/P) + bone scale/blendshape |

---

## E. Hasil review babak 4 (2026-10-24)

### E1. Koreksi user: DropZone bukan KO langsung — ✅ diterima
- Jatuh = **fall damage + kembali ke zona spawn tim + i-frame**. Saat Critical, jatuh = pecah 1 Break Stock.
- **Semua damage HP di-clamp di 0.** Tidak ada "overkill". Satu-satunya jalan KO = 3 Break Stock pecah.
- Detail di 08 §7.6.
- Catatan: perilaku asli LostSaga soal jatuh **belum diverifikasi**. Cek dengan observasi (rekam match di LSRebirth). Aturan ini tetap berdiri sendiri sebagai keputusan desain kita.

Celah yang harus ditutup dari aturan ini:
| Risiko | Penutup |
|---|---|
| Jatuh dipakai sebagai **teleport kabur** (mis. sedang dikepung) | Titik kembali = zona spawn tim (jauh dari pertarungan) + biaya HP/stock. Mundur paksa yang mahal |
| Jatuh untuk menghindari pemberian KO ke lawan | Atribusi tetap ke musuh terakhir yang memukul dalam 10 detik |
| Edge-guard jadi tidak bernilai | Tetap bernilai: damage + lawan tersingkir dari area ±beberapa detik + stock pecah saat Critical |

### E2. Mode MVP
| Mode | Aturan |
|---|---|
| **Survival / Elimination** (1v1, 3v3, ronde) | KO (setelah 3 stock pecah) = tereliminasi untuk ronde itu. **Tidak ada lagi KO instan dari jurang** |
| **Team Deathmatch** | Respawn; skor tim |

🔴 **Bantahan untuk escalating respawn timer per pemain** (5 → 7 → 9 → 12 detik):
- Pemain/tim yang sedang kalah lebih sering mati → respawn makin lama → makin kalah. Ini **snowball**, padahal alasan C4 dan aturan gear sebelumnya justru untuk mencegah snowball.
- Usulan: respawn naik berdasarkan **waktu match** (mis. 5 detik di awal → 10 detik di menit akhir), sama untuk semua pemain.
- Hukuman untuk mati tetap terasa lewat **skor lawan bertambah + kehilangan posisi**.

Pertanyaan terbuka: keberatan user di bagian Survival hanya soal jurang, atau juga konsep eliminasi per ronde itu sendiri?

### E3. 🔴 Bug determinisme pada aim-assist & auto-face
Keputusan B1: aim-assist ±22,5° dan auto-face guard ke musuh terdekat.
- **Masalah:** client melihat musuh di posisi **interpolasi (masa lalu)**, server di posisi **sekarang**. Keduanya bisa memilih target atau sudut berbeda. Client memprediksi serangan ke arah A, server mengeksekusi ke arah B → misprediksi, serangan "berbelok" sendiri.
- **Solusi:** client yang menghitung yaw akhir (aim-assist/auto-face) dan **mengirim yaw terkuantisasi di struct input**. Server **memvalidasi**: yaw harus berada dalam cone ±22,5° dari arah input mentah (atau, tanpa input arah, dalam radius 6 m ke musuh mana pun pada posisi ter-rewind).
- Pola yang sama dengan game tembak: aim dipercaya dalam batas, hasil hit tetap server.
- Dampak ke Core: struct input berisi `moveDir (8 arah + netral)`, `buttons`, **`aimYaw (uint16)`**.

### E4. Swap/Burst — definisi diperjelas
Keputusan B7: whiff recovery hanya bisa dibatalkan Burst 12 detik. Akibatnya Burst berubah dari "Defensive Cancel saat hitstun" menjadi **Burst Swap universal**:
- Boleh dipakai saat hitstun **atau** saat recovery serangan sendiri.
- Tidak boleh saat Critical (S4).
- Cooldown 12 detik di timer bersama (S2).

Neutral/Hit-Confirm Swap (3 detik): dari Idle/Run/Jump, atau setelah `movecontact` (kena/di-guard).

### E5. Kriteria spike harus terukur
"Rasa pukulan masih lengket" terlalu subjektif untuk keputusan go/no-go. Kriteria usulan pada simulasi RTT 150 ms + jitter 20 ms + packet loss 2%:
1. Penyerang melihat reaksi korban (hitstun/knockback) **≤ 1 frame** setelah hit-confirm lokal.
2. Misprediksi hit (diprediksi kena, server bilang tidak) **< 5%** dalam skenario combo standar.
3. Koreksi posisi korban setelah rollback **< 0,5 m** pada 95% kasus, dan dihaluskan ≤ 6 frame.
4. Server 1 proses menjalankan **≥ 20 match** 10 pemain di 60 Hz pada 1 vCPU (target biaya).
5. Bandwidth per client **< 64 kbps** turun.

Gagal di 1–3 → evaluasi Quantum. Gagal di 4–5 → optimasi, bukan ganti stack.

### E6. Sisanya — divalidasi
| Keputusan | Status |
|---|---|
| Heal → shield/buff saat Critical, tanpa revive | ✅ Konsisten dengan clamp HP & stock |
| KO = pemecah stock ke-3; assist 10 detik; jatuh → musuh terakhir | ✅ |
| Core data-oriented (struct + fungsi statis murni) | ✅ |
| 2 base body + hurtbox kapsul tunggal; beda hero lewat defense & weight | ✅ Catatan: weight membuat combo berbeda per hero korban (seperti Smash) — wajib diuji per hero |
