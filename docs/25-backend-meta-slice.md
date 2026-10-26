# 25 — Backend Meta Slice: Solo 1v1 Ranked (2026-10-26)

Status: ✅ **Backend terverifikasi** (25/25 unit/integration test lolos + smoke-test runtime end-to-end). Kode di `photon-backend/backend` (ASP.NET Core 8, repo privat).

## Yang dibangun (di atas kerangka backend yang sudah ada)
Kerangka lama (Pong) sudah punya: guest auth (device→JWT), `/me`, leaderboard, match 2-pemain + report-result "kedua pemain lapor, harus cocok" (sim deterministik → semi anti-cheat), Photon custom-auth + webhook. Ditambah/diubah untuk Nexus:

1. **Glicko-2** (`Services/Glicko2.cs`) — pengganti Elo. Rating + RD + Volatility. Divalidasi dengan contoh resmi paper Glickman `(1500,200,0.06)→(1464.05,151.52,0.05999)`.
   - `Player` dapat kolom `Rd`, `Volatility` (EF migration `AddGlicko2RdVolatility`).
   - `MatchService.FinalizeAsync` pakai Glicko-2 (kedua pemain dihitung dari rating lawan PRA-match).
   - Pemain baru: rating 1500, RD 350, vol 0.06, τ 0.5 (configurable di `Game`).
2. **Matchmaking MMR** (`Services/MatchmakingService.cs`, singleton in-memory) — pasangkan rating terdekat dalam `MatchmakingWindow` (default 400), region sama; beri `gameId` (room Photon) + slot.
   - Endpoint: `POST /api/matchmaking/join {region}`, `GET /api/matchmaking/status`, `POST /api/matchmaking/leave`.
3. **Dev fallback DB in-memory** — `Database:UseInMemory=true` (default di `appsettings.Development.json`) → API jalan **cukup `dotnet run`, tanpa Postgres/Docker**.

## Cara jalankan & uji (lokal, hanya SDK .NET 8)
```
cd photon-backend/backend
dotnet test                                   # 25 test
dotnet run --project src/PhotonBackend.Api --urls http://localhost:5080   # Development → DB in-memory
```
Smoke-test (terbukti): login 2 pemain → join/status matched (gameId + slot 0/1) → report 5-2 → Finished → Glicko-2 `1500→1662 / 1500→1338` → leaderboard terurut.

Produksi: `docker compose up -d --build` (Postgres + API), isi `.env` (JWT_SECRET, Photon secrets).

## Klien Unity
`game/Assets/QuantumUser/View/Nexus/NexusBackend.cs` — REST client (HttpClient async): `GuestLoginAsync`, `JoinQueueAsync`, `QueueStatusAsync`, `ReportResultAsync`, `RefreshMeAsync`.

## Flow ranked di Unity — ✅ TERSAMBUNG (pending uji live)
`NexusGame` kini punya tombol **Ranked Match (MMR)**: login tamu (device-id per-install via PlayerPrefs → editor & build = 2 akun) → `JoinQueue("asia")` → poll status → connect room Photon = `gameId` → main → saat `State=2` (match selesai) klien lapor skor + slot ke backend → Glicko-2 → tampilkan rating.
- **Win-condition** di sim: tim pertama capai `KoTarget` (=backend `WinScore`=5) KO → `State=2 Over`. Hanya aktif bila ≥2 manusia (practice 1 pemain tetap tak berujung).
- **Tim**: tiap tim diisi 4 bot + 1 slot human → 2 human (1 per tim) = 5v5.
- **Slot report = PlayerRef in-game** (0=BIRU/team0, 1=ORANYE/team1) → pemenang benar di Glicko-2.
- Skor di-clamp ke hasil legal (pemenang=target, kalah<target) sebelum lapor.

**Uji**: jalankan backend (`dotnet run ... --urls http://localhost:5080`), buka **editor + 1 build**, klik Ranked di keduanya. (Kode Unity ini ditulis tanpa bisa di-compile dari sisi asisten → mungkin ada iterasi kecil.)

## Berikutnya
- Uji live flow ranked (editor+build) → perbaiki bila ada error compile/runtime.
- Nanti: true 1v1 (tanpa bot), profil/ekonomi kosmetik, anti-cheat backend replay re-sim.
