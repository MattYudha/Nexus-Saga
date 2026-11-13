// Penjaga fokus: cetak blok 🎯 FOKUS dari BOARD.md ke konteks Claude di setiap prompt
// (hook UserPromptSubmit + SessionStart di .claude/settings.json). Stdout hook = konteks model.
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = process.env.CLAUDE_PROJECT_DIR || join(dirname(fileURLToPath(import.meta.url)), "..");
let board;
try {
  board = readFileSync(join(root, "BOARD.md"), "utf8");
} catch {
  process.exit(0); // tanpa BOARD.md: diam, jangan ganggu prompt
}

const m = board.match(/<!-- FOCUS:START -->([\s\S]*?)<!-- FOCUS:END -->/);
if (!m) process.exit(0);

console.log(`[BOARD.md — GATE FOKUS]
${m[1].trim()}
Aturan: kerjakan HANYA tiket di FOKUS. Permintaan di luar epic M1 → catat ke INBOX di BOARD.md
dan beri tahu user bahwa itu masuk antrean (kecuali user menulis OVERRIDE). Riset/ide baru tidak
boleh menggeser tiket mandatori. Setelah tiket selesai: centang di BOARD.md, pindahkan FOKUS.`);
