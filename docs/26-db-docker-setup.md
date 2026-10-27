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

## Verifikasi (sudah lulus)
- Register akun via Windows `localhost:5080` → OK (rating 1500).
- `docker compose down && up` (recreate container) → **login akun lama tetap sukses** → data **persisten** di volume `pgdata`.

## Unity
`BackendUrl = http://localhost:5080` — **tidak berubah** (dev `dotnet run` maupun Docker sama).
⚠️ Jangan jalankan dev `dotnet run` (port 5080) bersamaan dengan Docker → bentrok port.

## Reset data (kalau perlu mulai bersih)
`docker compose down -v` (hapus volume `pgdata` → semua akun/rating hilang).
