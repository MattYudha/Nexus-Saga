# 26 — Setup DB + Docker (Postgres persisten via WSL2) — 2026-10-27

Status: ✅ **Jalan & terverifikasi.** Backend meta kini pakai **PostgreSQL persisten** di Docker (bukan in-memory).

## Lingkungan
- **Docker Engine di dalam WSL2 Ubuntu-22.04** (bukan Docker Desktop). systemd aktif (`/etc/wsl.conf [boot] systemd=true`) → `docker.service` + container (`restart: unless-stopped`) **auto-start saat WSL boot**.
- Proyek: Windows `C:\Users\US3R\photon-backend` = WSL `/mnt/c/Users/US3R/photon-backend`.
- Networking: **NAT default** (localhost-forwarding WSL2). API bind `127.0.0.1:5080` di dalam WSL → reachable dari **Windows `http://localhost:5080`** (aman, tak buka ke LAN).
  - ⚠️ `networkingMode=mirrored` **GAGAL** di mesin ini (`0x8007054f` → fallback "None"/no-network). Jangan dipakai; NAT sudah cukup.
  - ⚠️ Setelah WSL/container restart, **tunggu ~15–30 dtk** sampai API `healthy` sebelum Unity konek (forwarding sempat flaky saat container baru start).

## Stack (`docker-compose.yml`)
- `db`: postgres:16-alpine, volume `pgdata` (persisten), tak publish ke host.
- `api`: build `./backend`, `127.0.0.1:${API_PORT}:8080`. Migration **auto-apply saat startup** (semua: InitialCreate, Glicko2, UserAccounts, PlayerStats).
- `caddy` (profil `tls`, opsional, produksi).
- Secret di `.env` (POSTGRES_PASSWORD, JWT_SECRET, Photon secrets, `API_PORT=5080`). `.env` **gitignored** — jangan commit.

## Perintah (dari PowerShell/terminal Windows, lewat WSL)
```
# start (biasanya sudah auto-start saat WSL boot)
wsl -e bash -lc "cd /mnt/c/Users/US3R/photon-backend && docker compose up -d"
# status / health
wsl -e bash -lc "cd /mnt/c/Users/US3R/photon-backend && docker compose ps"
#   lalu buka http://localhost:5080/health  → Healthy
# log API
wsl -e bash -lc "cd /mnt/c/Users/US3R/photon-backend && docker compose logs -f api"
# stop (data tetap) / rebuild setelah ubah kode backend
wsl -e bash -lc "cd /mnt/c/Users/US3R/photon-backend && docker compose stop"
wsl -e bash -lc "cd /mnt/c/Users/US3R/photon-backend && docker compose up -d --build"
```
Dari dalam Ubuntu langsung: `cd ~/.../photon-backend && docker compose ...` (tanpa prefix `wsl`).

## ⚠️ ATURAN: SELALU pakai `docker compose` (plugin), JANGAN `docker-compose` (standalone)
- Di mesin ini ada **dua CLI**: plugin **v5.1.2** (`docker compose`) dan standalone **v2.27.0** (`docker-compose`). Keduanya menulis `config-hash`/label berbeda.
- Memakai dua-duanya pada proyek yang sama → `up` berikutnya menganggap container "beda config" lalu **recreate** (kill `signal=15` = exit 143). Itu penyebab container "mati sendiri" yang pernah terlihat — **bukan OOM, bukan WSL idle**.
- **Selalu `docker compose` (plugin).** **JANGAN uninstall `docker-compose` 2.27** — proyek lain (`corevo-aratechnology`/hris, mysql) di daemon yang sama mungkin memakainya.
- Diagnosis (2026-10-30): RAM lega (6.6Gi free), tanpa OOM, `Restarts=0`, daemon systemd enabled+active. Satu-satunya akar churn = campur versi compose.

## Gejala & catatan (localhost forwarding WSL↔Windows)
- **Cek cepat dari host**: `curl http://localhost:5080/health` → `Healthy`. Bila GAGAL tapi dari dalam WSL `curl localhost:5080/health` **berhasil** → itu **glitch forwarding WSL2**, bukan backend mati. Verifikasi fungsi dari dalam WSL; untuk playtest Unity (konek dari Windows) tunggu/retry.
- Catatan kapan gagal (isi bila terjadi): tanggal · setelah aksi apa (rebuild/restart/idle) · pulih setelah (retry / `wsl --shutdown`).
- Bila sering mengganggu playtest: pertimbangkan `.wslconfig [wsl2] vmIdleTimeout` (perlu `wsl --shutdown`) — **diputuskan/diterapkan user sendiri di akhir hari**, bukan otomatis.

## Verifikasi (sudah lulus)
- Register akun via Windows `localhost:5080` → OK (rating 1500).
- `docker compose down && up` (recreate container) → **login akun lama tetap sukses** → data **persisten** di volume `pgdata`.

## Unity
`BackendUrl = http://localhost:5080` — **tidak berubah** (dev `dotnet run` maupun Docker sama).
⚠️ Jangan jalankan dev `dotnet run` (port 5080) bersamaan dengan Docker → bentrok port.

## Reset data (kalau perlu mulai bersih)
`docker compose down -v` (hapus volume `pgdata` → semua akun/rating hilang).
