# 19 — Koreksi Arsitektur Teknis v2 (2026-10-24)

Lima koreksi teknis (semua **diterima**) + komentar kritis & celah lanjutan yang saya temukan pada tiap koreksi. Memperbarui `18`.

Legenda: ✅ diterima · ⚠️ celah lanjutan yang WAJIB ditutup · 💡 catatan.

---

## 1. Draw call bottleneck — mesh combine untuk kostum, socket untuk gear
✅ **Diterima.** 13 slot × SkinnedMeshRenderer terpisah = ~15–17 renderer/karakter → Plaza 60 pemain ~900+ renderer → mobile drop. Solusi:
- **Kostum avatar (tak pernah copot):** **Runtime Mesh+Texture Combiner** saat spawn/selesai berdandan → 1 SkinnedMeshRenderer + 1 atlas.
- **Gear tempur (bisa copot):** tetap sub-mesh di socket agar bisa di-eject instan saat Break Stock pecah tanpa rebaking.

⚠️ **Celah lanjutan:**
1. **Dye vs atlas.** Dye pakai material color-mask per zona. Kalau semua mesh digabung ke 1 atlas, warna dye harus tetap per-item. Solusi: bake warna dye **ke dalam atlas saat combine** (di wardrobe/spawn, bukan runtime combat), atau simpan `MaterialPropertyBlock` per sub-region. Keputusan: **bake saat combine** (combat tidak pernah rebake).
2. **Crowd LOD Plaza (60 pemain).** 1 renderer/pemain pun masih 60 skinned mesh + animasi = berat di HP. Wajib: **interest management (AoI)** — hanya pemain dalam radius yang di-skinning penuh; pemain jauh pakai impostor/animated-texture atau bone-count rendah + update animasi jarang.
3. **Rebake hanya di wardrobe & spawn.** Di tengah combat **dilarang** rebake; gear eject = unparent socket (bukan rebake). Konsisten dengan koreksi Anda.
4. **GPU instancing + GPU skinning** untuk kerumunan bila memungkinkan.

💡 Ini **murni client (visual)** — tidak menyentuh Combat Core/determinisme.

## 2. Collider arena → hanya primitif proxy
✅ **Diterima.** Core fixed-point + target ≥20 match/vCPU → **tidak boleh** cek tabrakan ke MeshCollider segitiga mentah. Aturan keras Exporter: geometri fisik yang diekspor ke Core **hanya** primitif: **AABB, OBB/Box, Cylinder/Capsule, Ramp (bidang miring sederhana), DropZone trigger box**. Mesh visual boleh detail; collider Core = proxy kotak/silinder.

⚠️ **Celah lanjutan:**
1. **Dua representasi terpisah:** mesh visual (Unity, client) ≠ collider proxy (Core, deterministik, fixed-point). Exporter memvalidasi: setiap proxy = primitif, koordinat fixed-point, tidak ada mesh mentah lolos.
2. **Tangga/lereng:** pakai Ramp primitif atau **step-offset** (naik otomatis ≤ X). Desain arena sengaja "blocky" (cocok estetika LostSaga).
3. **Arena data ber-hash** masuk content bundle; client & server pakai proxy identik (prediksi tidak meleset).
4. **Anti-nyangkut:** karena primitif, resolusi tabrakan sederhana & stabil; hindari celah antar-proxy (exporter cek overlap/gap).

## 3. Orkestrasi Nakama ↔ .NET Game Server — Warm-Pool Registry (bukan K8s dulu)
✅ **Diterima.** Nakama tidak bisa menyalakan proses .NET ajaib. MVP: **Lightweight Warm-Pool Registry**:
- Tiap .NET server saat start **mendaftar** ke Nakama (IP, Port UDP, kapasitas, mis. 0/20 match) lewat endpoint internal.
- Matchmaker Nakama pilih server paling longgar → RPC internal `AllocateMatch(matchId, loadouts, secretKey)` → kirim tiket IP:Port ke client.
- (Agones/K8s = jalur scale Fase 4, sudah dicatat `09`.)

⚠️ **Celah lanjutan (penting, keamanan & keandalan):**
1. **Heartbeat + deregister.** Server kirim heartbeat berkala; Nakama **tidak boleh** alokasi ke server mati. Tanpa crash → timeout → keluarkan dari pool.
2. **Alokasi atomik (anti-race).** Dua match jangan dialokasi ke slot sama bersamaan. Alokasi + pengurangan kapasitas harus atomik (matchmaker Nakama 1 node, `14 §2` — manfaatkan itu).
3. **Autentikasi pendaftaran.** Endpoint register **wajib** pakai shared secret / jaringan internal. Tanpa ini, penyerang daftar server palsu → membajak match. **Ini celah keamanan, bukan opsional.**
4. **Graceful drain** saat update server.

## 4. Mobile: session token di header UDP + input chorded
✅ **Diterima keduanya.**
- **Seamless Endpoint Migration:** tiap paket UDP bawa `PlayerSessionToken` di header. Paket dengan token + tanda tangan sah dari IP:Port baru → server perbarui alamat tujuan tanpa putus.
- **Chorded/Modifier input:** kombinasi tombol (mis. Guard + arah/serang, atau hold/slide) agar tombol layar ringkas (maks 5–6 di kanan), bukan 10 tombol.

⚠️ **Celah lanjutan:**
1. **Migrasi WAJIB terotentikasi, bukan cuma cocok token.** Kalau server pindah endpoint hanya karena token cocok, penyerang yang tahu token bisa membajak sesi. **Setiap paket harus lolos MAC/tanda tangan**; migrasi hanya terjadi bila paket terverifikasi. (Mirip Connection ID QUIC.) Ini **keamanan kritis**.
2. **Migrasi (detik) vs reconnect (lebih lama).** Endpoint migration menangani ganti IP sesaat. Kalau HP ter-background/putus total > N detik → jalur **reconnect** dengan tiket diterbitkan ulang (jendela ±60 detik, `09 §6`). Dua mekanisme, satu desain.
3. **Chorded input = trade-off.** Di PC, pemain kompetitif ingin tombol **diskrit** (rasa fighting game). Di mobile perlu chorded. Solusi: **layout input per-platform**, keduanya memetakan ke **struct input Core yang sama & diskrit**. Core tidak berubah; hanya layer presentasi.
4. **Aim di mobile.** `aimYaw` (`13 §6`) susah di layar sentuh → mobile lebih bergantung **aim-assist ±22,5°** (sudah ada) + auto-face. Pertimbangkan aim-assist sedikit lebih kuat di mobile (tetap divalidasi server).
5. Chorded harus **deterministik**: kombinasi → satu input diskrit yang sama tiap kali.

## 5. Relic (PvE) di Game Server + Core, bukan client
✅ **Diterima.** Relic (PvE 1–4) **wajib** jalan di .NET Game Server + Combat Core yang sama. Monster = entitas AI berbasis state table **di dalam Core**. Mencegah cheat instant-kill untuk menambang Gold/Relic.

⚠️ **Celah lanjutan:**
1. **Monster = bot yang mengeluarkan input ke Core** (konsisten `17 §5`). Bukan jalur stat khusus → determinisme & keadilan terjaga.
2. **RNG monster/loot = RNG per match ter-seed server** (`08 §1`). Client tidak pernah roll.
3. **Loot/chest grant server-authoritative** (seperti gacha, `15 §9`): hasil Relic dilaporkan game server → Nakama (idempoten). Client hanya menampilkan.
4. **Kapasitas:** Relic 1–4 pemain → murah; tetap 60 Hz untuk konsistensi Core. Masuk accounting warm-pool (#3).

---

## Komentar: bottleneck/gap tambahan yang saya temukan (di luar 5 koreksi)

### G1. Snapshot JANGAN bawa data kosmetik per-tick
Kosmetik (13 slot) & loadout dikirim **sekali saat join match**, bukan tiap tick. Snapshot per-tick hanya **state gameplay** (pos, yaw, stateId, HP, Break Stock, status 4 gear on/off, dropped gear). Kalau kosmetik ikut per-tick, bandwidth jebol. (Perjelas di `08 §9`.)

### G2. Plaza O(n²) broadcast
60 pemain saling broadcast = 60×60. **Wajib AoI grid**: pemain hanya terima update pemain dalam radius. Tanpa ini Plaza tidak scale, apalagi mobile. (Perjelas `14 §4a`, `18 §2.1`.)

### G3. Dropped gear = entitas gameplay + visual terpisah
Gear eject: (a) **entitas DroppedGear** di snapshot (gameplay, bisa dipungut) + (b) **visual** mesh jatuh (client). Jangan campur; visual mengikuti entitas, bukan sebaliknya.

### G4. Build mobile store = masalah ukuran APK
Ratusan aset kosmetik tidak boleh masuk APK. **Wajib Addressables + CDN** (sudah diputuskan) + Play Asset Delivery. APK inti kecil; kosmetik diunduh. Tanpa ini, store menolak/ukuran jebol.

### G5. Input Core harus 1 definisi lintas platform
Keyboard/gamepad/touch/chorded → semua menghasilkan **struct input Core yang identik & diskrit**. Ini yang menjaga "mobile tanpa rombak" benar-benar terjadi. Tulis layer input abstraction sebagai kontrak tetap sejak S-02 (spike).

---

## Pengaman tambahan (dikunci 2026-10-24)
- **A. Anti-replay pada migrasi endpoint (#4).** HMAC/AEAD tiap paket **menyertakan `PacketSequenceNumber`**. Server mengizinkan pindah IP:Port **hanya** bila paket lolos MAC **dan** `SequenceNumber > HighestAuthenticatedSequence`. Mencegah serangan replay membajak sesi di Wi-Fi publik.
- **B. Non-blocking cosmetic fallback (#1, G4).** Gagal/lambat unduh bundle kosmetik dari CDN **tidak pernah** menahan masuk Arena. Kostum pemain lain yang belum siap di cache → render **Base Body default** dulu; swap ke kostum asli saat bundle tiba. Pertarungan selalu mulai tepat waktu. (Hurtbox tetap standar, jadi fallback tidak memengaruhi gameplay.)

## STATUS: Desain arsitektur **LOCKED** (2026-10-24)
Stress-test desain cukup. Tidak menambah sistem baru di atas kertas. Fokus berikutnya = eksekusi Spike Fase 1 (`20`) + pipeline aset (`21`).

## Ringkasan keputusan (untuk decision log)
1. Kostum = mesh combine (1 renderer+atlas, dye di-bake saat combine); gear = socket terpisah (eject instan). Combat tanpa rebake.
2. Crowd LOD + AoI untuk Plaza; GPU instancing bila bisa.
3. Collider Core = **hanya primitif proxy** fixed-point; exporter validasi; arena blocky + ramp/step-offset.
4. Warm-Pool Registry (register+heartbeat+alokasi atomik+**auth pendaftaran**); Agones = Fase 4.
5. UDP session token + **migrasi hanya setelah paket terverifikasi (MAC)**; reconnect ±60s untuk putus total.
6. Input per-platform → satu struct Core diskrit; mobile andalkan aim-assist.
7. Relic di Game Server+Core; monster=bot input; loot server-authoritative.
8. Snapshot tanpa kosmetik per-tick; dropped gear = entitas+visual.
