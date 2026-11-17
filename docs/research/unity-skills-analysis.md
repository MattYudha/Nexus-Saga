# Analisis: Unity-Skills (Besty0728) & Unity-Technologies/skills (2026-11-17)

Dua repo yang di-clone user. **Keduanya bukan konten/aset/netcode game** — tidak ada yang "diambil" ke
runtime Nexus Saga. Keduanya = **skill otomasi Unity Editor untuk AI agent**. Relevansinya bukan ke gameplay,
tapi ke **workflow** (menutup keterbatasan Claude: tak bisa lihat/compile/screenshot Unity).

## A. Besty0728/Unity-Skills — **TINGGI (dev tool)**
- Apa: **REST API di dalam Unity Editor** (localhost:8090–8100), 873 skill. MIT. Unity 2022.3+. Dukung Claude Code resmi.
- Kemampuan relevan (dari `SkillsForUnity/Editor/Skills/`):
  - `ConsoleSkills` / `ConsoleLogHistoryService` / `CompilationResultService` → **baca error compile & Console** (tak perlu user tempel error lagi).
  - `debug_force_recompile` → paksa recompile.
  - `PlayCaptureService` / `CameraSkills` → **screenshot Game/Scene view** (menutup "aku tak bisa screenshot").
  - `BuildPlayerService`, play mode, batch, asset/komponen ops.
- Kenapa penting: **menghapus bottleneck #1 kita.** Kalau paket ini dipasang di project Nexus + server ON,
  Claude bisa `curl localhost:8090/...` untuk: recompile → baca error sendiri, enter play, screenshot lobby.
  Loop "edit → user screenshot → ulang" (redesign lobby B) jadi jauh lebih cepat.
- Sifat: **editor-only package** (assembly Editor) → TIDAK ikut ter-build ke game. Tak ada isu lisensi/clean-room untuk game.
- Risiko: server HTTP lokal yang bisa mengubah project. Hanya jalankan di mesin tepercaya; ada permission system
  selaras mode Claude Code. Pihak ketiga (bukan Unity resmi), tapi aktif & MIT.

## B. Unity-Technologies/skills — **SEDANG (referensi workflow resmi)**
- Apa: skill resmi Unity untuk agent (Claude Code dll), jalan via **Unity CLI**. Bukan REST; panduan + otomasi CLI.
- Skill yang relevan untuk Nexus Saga:
  - `ui-uitk` → **lobby kita UITK** — panduan API benar (kurangi salah UXML/USS/C#9 milikku).
  - `localize-unity-project` → lokalisasi **ID/EN** (ada di backlog docs/C).
  - `implement-in-app-purchases` → monetisasi (fase nanti).
  - `project-auditor-fixes`, `optimize-text-mesh-pro`, `build-multiplayer-game`, `unity-cli`, `migrate-birp-to-urp`.
- Nilai: memperbaiki **akurasi** kerja Unity-ku (API benar), bukan menambah fitur game. Butuh Unity CLI terpasang.

## Verdict
1. **Pasang Besty Unity-Skills ke project Nexus** sebagai jembatan editor Claude ⇄ Unity. Ini leverage tertinggi:
   menyelesaikan "tak bisa screenshot/compile/baca error" yang jadi friksi tiap sesi.
2. **Rujuk** beberapa Unity-Tech skills (`ui-uitk`, `localize`, `project-auditor`) saat kerja terkait.
3. **Jangan** anggap keduanya sumber kode/aset game — tidak ada yang dipakai di runtime.

## Langkah pakai Besty (agar Claude bisa drive Unity besok)
1. Copy `SkillsForUnity/` → `photon-backend/game/Packages/` (atau install via package manager lokal).
2. Unity → `Window > UnitySkills` → nyalakan **Server** (port 8090). Set permission sesuai kenyamanan.
3. Tes dari Claude: `curl -s http://localhost:8090/<health/skills>` → kalau jawab, Claude bisa recompile,
   baca error, dan screenshot sendiri → verifikasi A1–A3 & redesign lobby B jadi mandiri.

**Status:** analisis saja, tidak ada kode diubah. Keputusan pasang/tidak = user. Masuk INBOX (NX-IN-TOOL).
