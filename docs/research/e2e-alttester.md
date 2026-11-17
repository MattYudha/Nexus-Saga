# E2E otomatis = AltTester (keputusan 2026-11-17)

User ingin tes otomatis (anti tes manual): suntik WASD/J/H + klik UI, cari objek 3D & UI, jalankan
seluruh alur **Lobby→Practice→Tembak→Result** via **pytest**. **Verdict: AltTester = tool yang tepat, ADOPSI.**

## Kenapa cocok (terverifikasi di SDK yang di-clone)
- **Driver Python/pytest**: `Bindings~/python/alttester/altdriver.py` + `pyproject.toml` + tests. Claude bisa `run` pytest via Bash → E2E otomatis penuh.
- **Cari objek**: 3D GameObject **dan UITK** (`AltGetVisualElementProperty`, `AltWaitForVisualElementProperty`, `UIDocument`, `AltObject` UIToolkit) — lobby kita UITK, jadi tombol PRACTICE dll bisa diklik.
- **Injeksi input**: `AltPressKeys`, `AltKeysDown/Up`, `AltMoveMouse`, tap/click → WASD/J/H + klik tombol.
- **Legacy Input didukung**: SDK punya `Runtime/Input/Input.cs` (pengganti `UnityEngine.Input`) + `AltInputAxesProcessor`. Game kita pakai `UnityEngine.Input.GetKey/GetAxisRaw` (legacy) → instrumentation AltTester menukarnya ke AltTester.Input saat build/instrument, jadi key suntikan terbaca `NexusInput`.

## Peran tiap tool (saling lengkap, tak bentrok)
| Tool | Peran |
|---|---|
| **AltTester** | **E2E runtime**: pytest suntik input + cek UI/3D/sim → verifikasi A otomatis + regresi semua fitur |
| **unity-mcp** | editor: baca console, edit objek/skrip, compile, run unit test, screenshot |
| **Blender MCP** | buat aset 3D |
| Besty Unity-Skills | cadangan editor-bridge |

AltTester drive game yang BERJALAN via TCP (port 13000); unity-mcp drive editor. Beda lapisan → aman bersamaan.

## Setup (prasyarat, sekali; ~1–2 jam)
1. Pasang **AltTester SDK** ke project Unity (`game`): import package `Assets/AltTester` (atau UPM/.unitypackage dari repo clone).
2. Tambah **AltTesterPrefab** ke scene `NexusOnline` (+ `NexusLocal` bila perlu), set port 13000.
3. Aktifkan **instrumentation** (ganti `UnityEngine.Input`→AltTester.Input) via setting AltTester / build define `ALTTESTER`.
4. Jalankan game: **editor Play** dengan AltTester server ON, atau **Development Build** ter-instrument.
5. Python: `uv pip install AltTester-Driver` (atau dari `Bindings~/python`).
6. Tulis pytest E2E (object name sudah banyak diketahui dari kode: tombol lobby, hero select, dll).

## Alur E2E pertama (practice — single instance, tak perlu 2 klien)
```
launch → AltDriver connect(13000)
→ find & tap tombol mode PRACTICE → tap hero (TITAN/PULSE)
→ PressKeys W/A/S/D gerak, J tembak, H ganti hero
→ assert: proyektil mengarah ke bot (aim-assist A1), skor/KO konsisten (A2)
→ tunggu State=Result → assert layar Result practice (elemen ada, tier/ladder hilang)
```
Covers A1/A2 otomatis. Ranked no-bot (A3) butuh 2 instance — tahap lanjut.

## Batas jujur
- Setup awal tidak sepele (package+prefab+instrument+build+driver). Setelah jadi, **tes jalan sekali klik** & Claude bisa menjalankannya.
- Instrumentation legacy-Input harus benar; kalau NexusInput tak ikut ter-swap, key tak terbaca → perlu cek saat setup.
- Aset AltTester = tooling/test, **jangan** ikut build rilis (pakai define/stripping).

Status: analisis + keputusan. INBOX: NX-IN-E2E. Belum ada setup dijalankan (tunggu aba-aba user).
