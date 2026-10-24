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
- **KO** = yang memecahkan Break Stock terakhir (atau yang terakhir memukul sebelum DropZone, jendela 5 detik).
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
