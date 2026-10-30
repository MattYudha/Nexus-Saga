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
- 2026-10-30: **Poin c SELESAI** (docs/35). Backend faksi: `FactionService` (populasi/Butuh Pejuang/bonus), `GET /api/factions`, `POST /me/faction` (validasi+lock satu season+idempoten), bonus XP minoritas di FinalizeAsync. **67 tes hijau**, deploy live. Klien: layar onboarding `faction-screen` (NexusLobbyController+NexusGame), badge konsisten (`SetFactionBadge`: top bar + profil), Guest ikut memilih. **⚠️ Klien butuh compile+playtest di editor (tak bisa diverifikasi headless).** Backend commit `ed951f2`.
- 2026-10-30: **Poin a & b SELESAI.** Demosi dinonaktifkan (grace=0, floor dibersihkan saat startup, kode/tes tetap). Leaderboard: tier/poin dari rating asli, conservative hanya utk posisi (+2 tes). Deteksi akun uji dikonfirmasi eksplisit (tanpa deviceId guessing); docs/33 §1 + komentar tes diperbaiki. **61 tes hijau.** Deploy live. Berikutnya: poin c (Faksi).
- 2026-10-30: Antrean prioritas dikunci. Commit snapshot (backend `0a9f5a4`, docs `735404a`). Mulai poin a.
- 2026-10-30: Proteksi demosi opsi 1 diimplementasi (lalu dinonaktifkan di poin a).
- 2026-10-29/30: 1v1 ranked, leaderboard, Tab Riwayat + Detail Match. 58 tes hijau.
