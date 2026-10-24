# 90 — Decision Log

| Tanggal | Keputusan | Status |
|---|---|---|
| 2026-10-24 | Nama kerja: **Nexus Saga: Chronicles** | Disepakati |
| 2026-10-24 | Belum coding; fase brainstorming + riset + dokumentasi | Disepakati |
| 2026-10-24 | Dokumentasi disimpan di `docs/` sebagai `.md` | Disepakati |
| 2026-10-24 | 3 mata uang: Gold / Ticket / MiCash, kosmetik nol stat, rent-to-own sebagai Gold sink utama | Disepakati |
| 2026-10-24 | Developer mode berbasis role di server + audit log; otorisasi tidak pernah di client | Disepakati |
| 2026-10-24 | Urutan riset: **Wardrobe AyoDance + format state Ikemen GO** dulu; state machine LostSaga setelah client tersedia | Disepakati |
| 2026-10-24 | Platform: **PC dulu**, mobile di fase berikutnya | Disepakati |
| 2026-10-24 | ~~Kamera arena: 2.5D side-view (seperti LostSaga)~~ — keliru: LostSaga bergerak bebas X/Z. Diganti: **arena 3D free-roam (gerak 8 arah X/Z + lompat Y), kamera quarter-view terkunci** (lihat 06) | Disepakati |
| 2026-10-24 | Ukuran tim maksimal: **5v5** | Disepakati |
| 2026-10-24 | Rating umur **13+**; couple/dating room **18+ dengan verifikasi umur** | Disepakati |
| 2026-10-24 | Riset AyoDance hanya **statis** (ada Xigncode); tidak menjalankan/attach game | Disepakati |
| 2026-10-24 | Avatar di arena: **lapisan kostum tidak pernah lepas; slot gear tempur (senjata/armor/helm/jubah) bisa rontok**; gear rontok saat kondisi kritis/HP 0; skin gear wajib patuh batas siluet hero | Disepakati |
| 2026-10-24 | MVP: **2 hero** (Melee Grappler + Ranged Zoner), mode 1v1 & 2v2 | Disepakati |
| 2026-10-24 | Tidak membongkar proteksi/packer client LostSaga (`lostsaga.exe`, `iopac.dll`); riset LostSaga ditunda | Disepakati |
| 2026-10-24 | Urutan kerja: **(a) state machine Ikemen GO → (d) arsitektur core combat** (+ tick/snapshot DDNet); AyoDance wardrobe setelah core combat | Disepakati |
| 2026-10-24 | Guard **busur depan 180°**; serangan dari belakang menembus | Disepakati |
| 2026-10-24 | Pickup gear lawan: **Helm/Armor/Trinket boleh** (siapa cepat dia dapat), **senjata tidak** | Disepakati |
| 2026-10-24 | **3 hero per match** (MVP aset 2 hero); cooldown swap **3 s** netral/combo, **12 s** defensive cancel | Disepakati |
| 2026-10-24 | HP 0 → **Critical**: pukulan berat merontokkan Helm → Trinket → Armor, lalu KO; DropZone = KO langsung; **senjata tidak rontok sebelum KO** | Disepakati |
| 2026-10-24 | Patch G1–G2, S1–S5, C1–C4, P1–P3 (lihat 08) | Usulan — menunggu konfirmasi |
| 2026-10-24 | Arsitektur sistem: Unity + Core C# murni + game server .NET + Nakama (lihat 09) | Usulan — menunggu konfirmasi |

