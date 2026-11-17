# Pipeline aset = main core (keputusan 2026-11-17)

User mengarahkan: jika berguna, jadikan **main core pembuatan aset**. Verdict: **BERGUNA — adopsi.**
Ini jalur aset **legal & orisinal** (bikin sendiri), kebalikan dari rip LostSaga. Aman clean-room.

## Komponen (semua MIT/ open, `uv`+Python 3.11 sudah terpasang)
| Alat | Peran | Cara aktif |
|---|---|---|
| **Blender MCP** (`mcp-for-blender`, ex ahujasid/blender-mcp) | **Buat/edit model 3D** (hero, props, environment) via Blender | `uvx mcp-for-blender setup` → pasang addon + config Claude; buka Blender (addon start server) |
| **unity-mcp** (CoplayDev, v10, MCP-native, 50 tool) | **Core otomasi Unity**: import aset, prefab, material, scene, edit skrip, run test, build, **v10 asset generation**. Tool group: vfx/animation/ui/testing | Unity → Package Manager → git URL `https://github.com/CoplayDev/unity-mcp.git?path=/MCPForUnity#v10.0.0` → `Window → MCP for Unity → Configure All Detected Clients` (auto-tulis config Claude Code) |
| Besty Unity-Skills (REST) | **Cadangan** editor-bridge (screenshot/console) bila unity-mcp kurang | hanya bila perlu; JANGAN jalan bareng unity-mcp (hindari konflik kontrol) |
| Tripo3D MCP (opsional, nanti) | text/image→3D cepat untuk draft model | fase modeling |

## Alur kerja aset (target)
```
ide hero/prop → Blender MCP (model+UV+rig dasar) → export → unity-mcp (import, material URP, prefab, pasang ke scene)
→ unity-mcp (edit skrip/komponen, run test) → commit ke mine
```
Menggantikan fase "placeholder sprite" (memory nexus-modeling-pipeline) dengan aset 3D nyata, bertahap.

## Pilihan: unity-mcp > Besty untuk Unity
- unity-mcp **MCP-native** → jadi tool langsung di Claude (bukan curl), MIT, dirawat (v10 2026-10), self-config, run test/build.
- Besty = REST (perlu curl), 873 skill, kelebihan screenshot. Simpan sebagai cadangan, bukan core.
- **Jangan dua-duanya aktif** sebagai bridge Unity bersamaan.

## Batas jujur
1. **MCP baru jadi tool setelah: setup + app (Blender/Unity) terbuka + Claude Code di-restart.** Sesi ini belum bisa memakainya.
2. Blender MCP hebat untuk blockout/props/environment & aset sederhana; **model karakter berkualitas tetap butuh iterasi/seni** — bukan sekali-klik.
3. Semua ini **tooling/editor-only** → tidak ikut ter-build ke game; aset yang DIBUAT = milikmu (orisinal), tak ada isu lisensi.
4. Tetap hormati C#9 Unity (memory nexus-csharp9-unity) untuk skrip yang dihasilkan.

## Langkah aktif (user, lalu restart Claude)
1. Blender: `uvx mcp-for-blender setup` → pilih Claude Code → install addon → buka Blender.
2. Unity: Package Manager add git URL unity-mcp → `Window → MCP for Unity → Configure All Detected Clients`.
3. **Quit & buka ulang Claude Code** (biar MCP ter-load) → Claude tes: "buat cube + Rigidbody" (unity-mcp), "buat kubus" di Blender (blender-mcp).
4. Setelah tools muncul, Claude bisa bantu pipeline aset + (bonus) baca error compile & drive editor → menutup friksi "tak bisa lihat Unity".

Status: analisis + keputusan. Tak ada kode/config diubah otomatis (installer resmi masing-masing yang menulis config, simpan `.bak`). INBOX: NX-IN-TOOL (diperluas).
