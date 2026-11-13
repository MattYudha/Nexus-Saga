# 06 — Kamera: 3 mode Ikemen → quarter-view 3D Nexus Saga

Menutup 🟡 "kamera free-roam 3D, lock-on".

## 1. OBSERVED
`type Camera struct` (`camera.go:88-101`) dengan tiga mode (`camera.go:80-86`):
`Fighting_View` (auto-frame dua petarung), `Follow_View` (ikuti satu `FollowChar`), `Free_View` (lepas).
Field: `Pos`, `ScreenPos`, `Offset`, `XMin/XMax`, `Scale`, `MinScale`, `boundL/R/H/Lo`, `zoff`, `halfWidth`,
`FollowChar`, `LegacyZoomMin/Max`. Default `LegacyZoomMin = 5.0/8.0` (= 0.625), `Max = 1` (`camera.go:103-109`).

`Reset()` (`camera.go:111-135`) menghitung batas dunia dari `boundleft/right` + `zoomout`, lalu
`XMin = boundL - halfWidth/BaseScale()`. Artinya: **batas kamera bergantung pada zoom** — kalau zoom out,
kamera boleh bergerak lebih jauh. Ini trik yang berguna untuk arena besar.

## 2. PROPOSED (docs/06 sudah memutuskan quarter-view; ini detail teknisnya)
| Aspek | Aturan |
|---|---|
| Sudut | quarter-view tetap (yaw kamera tidak dirotasi pemain); tinggi & jarak boleh berubah |
| Follow | kamera mengikuti **titik berat tim**, bukan satu pemain, supaya 5v5 tidak memotong layar |
| Lock-on | hanya memutar **yaw hero** ke target, **bukan** memutar kamera (kamera berputar = mual + sulit aim) |
| Bounds | clamp ke batas arena; saat zoom-out, batas melebar (adopsi rumus Ikemen) |
| Zoom | `MinScale = 0.625`, `MaxScale = 1.0` (angka Ikemen dipakai sebagai titik awal) |
| Shake | offset presentasi di View, **tidak** masuk `Camera.Pos` sim |
| KO/Critical | zoom-in ringan + sedikit turun (dramatis), durasi ≤ 45 tick, kembali smooth |
| Mobile | FOV lebih lebar 10–15°, karena layar sempit |

## 3. Yang harus dihindari
- Kamera mengikuti vektor kecepatan (bikin goyang saat strafe).
- Auto-rotate kamera ke lawan terdekat (di 5v5 target berpindah terus).
- Kamera yang ikut hitstop secara tidak konsisten (presentasi, jadi boleh; sim jangan).
- Menyimpan posisi kamera di state simulasi — kamera **tidak** memengaruhi gameplay, jadi tidak perlu ikut
  snapshot (kecuali untuk replay visual: simpan sebagai event, bukan state).
