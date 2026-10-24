# Nexus Saga: Chronicles — Design Docs

Folder ini adalah "memori" proyek. Setiap kesepakatan brainstorming dan hasil analisis disimpan di sini.

## Ground Rules
- **Belum ada coding** (Unity/C#/TypeScript) sampai diperintahkan.
- Setiap analisis game referensi → ringkasan di `research/`.
- Setiap keputusan final → dicatat di `90-decision-log.md`.
- Pertanyaan yang belum terjawab → `91-open-questions.md`.
- Riset game referensi bersifat **clean-room**: kita mempelajari *desain & perilaku* (cara kerja, struktur data, angka balancing), lalu menulis implementasi sendiri. Tidak menyalin kode, aset, atau data milik developer lain.

## Isi
| File | Isi |
|---|---|
| `01-vision-concept.md` | Visi, pilar desain, loop gameplay, mode, ekonomi |
| `02-reference-matrix.md` | Game referensi → apa yang diambil → cara risetnya |
| `03-tech-direction.md` | Arah teknis awal (engine, backend, netcode) — draft |
| `04-brainstorm-v2-system-map.md` | Readiness check, peta 14 sistem, ide v2, scope MVP, kendala |
| `05-kekurangan-dan-target-riset.md` | Checklist tool/bahan yang kurang + daftar game target riset per sistem |
| `06-camera-dan-avatar-arena.md` | Koreksi kamera (free-roam 3D), lapisan kostum vs gear, gold sink, 2 hero MVP |
| `07-readiness-checklist.md` | Status bahan riset, tooling RE, kesiapan arsitektur & implementasi |
| `08-arsitektur-core-combat.md` | Arsitektur core combat: pipeline tick, state 3D, HitDef/hitbox, Hero Swap, Gear Drop, netcode |
| `09-arsitektur-sistem.md` | Engine, backend, berbagi Combat Core, alur Lobi → Match, risiko |
| `research/state-machine-ikemen.md`, `research/netcode-ddnet.md` | Hasil bedah Ikemen GO & DDNet |
| `90-decision-log.md` | Keputusan yang sudah disepakati |
| `91-open-questions.md` | Pertanyaan terbuka untuk sesi berikutnya |
| `research/` | Hasil bedah per sistem/game (diisi bertahap) |

## Status Tooling
- 2026-10-24: Server MCP **REA belum terdaftar** di Claude Code (tidak muncul di `claude mcp list`). Lihat `91-open-questions.md` #1.
- 2026-10-24 (cek ulang): REA terpasang hanya sebagai **skill** di `~/.agents/skills/reverse-engineer-anything` (v42). MCP server belum terdaftar, CLI `rea` tidak ada di PATH, Terminal 2 Termul idle (tidak ada proses REA). Java/Ghidra tidak terdeteksi di PATH (dibutuhkan untuk dekompilasi .exe/.dll native). Node v24.22.0 tersedia.
- 2026-10-24: `rea setup --client claude_code --yes` → registrasi Claude Code **aligned** di `~/.claude.json` (`cmd /d /c npx -y rea-agents@6.7.0 mcp`), skill v42 aligned. Butuh restart Claude Code. Provider analisis: **belum ada** (Ghidra/IDA/JADX/Kuna tidak dikonfigurasi) → dekompilasi .exe/.dll native belum bisa; untuk itu perlu Ghidra 12.1.x + `GHIDRA_INSTALL_DIR`.
- 2026-10-24: ✅ **REA TERHUBUNG** ke Claude Code (rea-agents 6.7.0, 207 tools, client claude-code 2.1.310). Tersedia tanpa engine: `inspect_pe_resources`, `inspect_managed_artifact` (.NET), `inspect_sqlite_database`, `open_binary` (inventaris arsip), compare_*, Frida. Masih menunggu Ghidra: dekompilasi native (`analyze_function`, `batch_decompile`, pseudo code, xrefs).
  Langkah aktivasi: `npx -y rea-agents@6.7.0 doctor --client claude_code --json` → `setup --client claude_code --dry-run --json` → `setup --client claude_code --yes` → restart Claude Code.


