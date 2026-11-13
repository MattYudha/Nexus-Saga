# 05 — QA pass 4: Glicko2 + StatsEndpoints (2026-11-13)

Lanjutan `04`. Baca-saja. Fokus: matematika rating & agregasi statistik (bug yang baru terlihat setelah data menumpuk).

---

## A. Glicko-2 — verifikasi matematika
Saya cocokkan `Services/Glicko2.cs` baris-per-baris dengan algoritma Glickman (paper Glicko-2):

| Langkah paper | Kode | Status |
|---|---|---|
| μ=(r−1500)/173.7178, φ=RD/173.7178 | `:27-29` | ✅ |
| g(φ)=1/√(1+3φ²/π²) | `:99` | ✅ |
| E=1/(1+e^(−g·(μ−μj))) | `:100` | ✅ |
| v=[Σg²E(1−E)]⁻¹, Δ=v·Σg(s−E) | `:33-49` | ✅ |
| f(x)=e^x(Δ²−φ²−v−e^x)/(2(φ²+v+e^x)²)−(x−a)/τ² | `:55-62` | ✅ |
| A=ln σ², B=ln(Δ²−φ²−v) atau A−kτ | `:68-80` | ✅ |
| Illinois (regula falsi, `f(A)/=2`) | `:84-94` | ✅ |
| σ′=e^(A/2) | `:95` | ✅ |
| φ*=√(φ²+σ′²), φ′=1/√(1/φ*²+1/v) | `:98-99` | ✅ |
| μ′=μ+φ′²Σg(s−E) | `:100` | ✅ |
| Simetris dari snapshot pra-match | `MatchService.cs:315-316` | ✅ |

**Kesimpulan: implementasinya benar.** Tidak ada bug matematika inti. Yang bermasalah adalah **kebijakan di sekitarnya**:

| ID | Sev | Lokasi | Temuan | Dampak |
|---|---|---|---|---|
| **Q48** | S2 | `Glicko2.cs:98-101` | RD **tidak di-clamp** ke batas bawah (paper: 30). Hanya cabang "tanpa game" yang di-clamp (`:31`) | Setelah puluhan match, RD→kecil (mis. <5): `conservative = rating − 2·RD` ≈ rating, sehingga makna "keyakinan" hilang dan urutan leaderboard praktis = rating mentah |
| **Q49** | S2 | `MatchService.cs:315` | **Tidak ada inflasi RD untuk pemain pasif.** RD hanya berubah saat bermain | Pemain lama yang kembali bertanding memakai RD basi (terlalu yakin) → perolehan/kekalahan rating tidak wajar; papan jadi "lengket" |
| **Q50** | S3 | `MatchService.cs:321,342` | `lDelta` memakai `Math.Max(0, round(Rating))` lalu `l.Rating = Math.Max(0, ...)`. Clamp ganda, dan yang pertama memotong **rating**, bukan delta | Tidak berbahaya pada rating ~1500, tapi menyesatkan pembaca; rapuh bila kelak ada rating awal rendah |
| **Q51** | S3 | `MatchService.cs:322-329` | Anti-kolusi meredam `wDelta`/`lDelta`, tapi `Rd` & `Volatility` tetap diperbarui **penuh** | Keyakinan naik seolah match dihitung penuh, sementara poin rating diredam → konservatif jadi tidak konsisten |
| **Q52** | S4 | `Glicko2.cs:17` | `Score` mendukung 0.5 (seri) tetapi jalur seri **tidak pernah** memanggil `Update` (`FinalizeDrawAsync`) | Bila kelak seri diberi rating, kode siap; sekarang hanya catatan |

## B. StatsEndpoints — agregasi

| ID | Sev | Lokasi | Temuan | Dampak |
|---|---|---|---|---|
| **Q53** | S2 | `StatsEndpoints.cs:118` | `if (r.Won && loserScore == 0) a.Flawless++;` — **FLAWLESS dihitung dari skor lawan 0**, tanpa melihat `EndReason` | Kemenangan **waktu habis 1-0** atau **WO** tercatat FLAWLESS, padahal pemain mungkin sudah kehilangan Break Stock/gear. Badge jadi tidak bermakna |
| **Q54** | S2 | `StatsEndpoints.cs:113` | `durSum += r.DurationSec` untuk **semua** match, termasuk match lama yang durasinya dari wall-clock (sebelum fix Q4) | Rata-rata durasi mencampur dua satuan waktu; angka statistik tidak bisa dibandingkan antar-era |
| **Q55** | S2 | `StatsEndpoints.cs:94-108` | Dasar perhitungan tidak seragam: K/D & MaxKill hanya dari `ranked1v1`, sedangkan Flawless/Comeback/CloseMatch menghitung **semua** format | Pemain battle 5v5 bisa mendapat FLAWLESS/COMEBACK tanpa K/D yang sah → radar & badge tidak konsisten |
| **Q56** | S3 | `StatsEndpoints.cs:161-166` | Radar memuat **seluruh** `Players` ke memori lalu memuat **seluruh** `MatchPlayers` tier tersebut per request | Biaya tumbuh linear terhadap seluruh riwayat; pada 10k match bisa detik-an per muat profil. Perlu cache/agregat tersimpan |
| **Q57** | S3 | `StatsEndpoints.cs:186-188` | Persentil menghitung **diri sendiri** dalam populasi (`tierIds.Add(playerId)`) | Nilai 100 mustahil dimiliki sendirian; skor radar sedikit bias ke atas |
| **Q58** | S3 | `StatsEndpoints.cs:148` | `ketahanan = DamageTaken / max(1, DetailedKoReceived)` | Pemain dengan 0 death → penyebut 1 → sumbu meledak; karena persentil, ia mendominasi sumbu itu |
| **Q59** | S4 | `StatsEndpoints.cs:132` | `Kda = Kills / max(1, Deaths)` | Pemain 5 kill 0 death tampil `5.00`, bukan "sempurna/–"; konsisten dengan UI? perlu keputusan tampilan |

## C. Prioritas
1. **Q53** — badge FLAWLESS salah untuk menang-waktu/WO. Butuh `EndReason` di query statistik.
2. **Q48/Q49** — RD: clamp bawah 30 + inflasi untuk pemain pasif (atau minimal dokumentasikan bahwa papan sengaja "rating-first").
3. **Q55** — seragamkan basis statistik (semua badge dari `ranked1v1`, atau tandai per-format).
4. **Q56** — cache agregat sebelum populasi tumbuh.
5. Sisanya kosmetik/konsistensi.

## D. Belum dipindai
`FactionService` (bonus ganda, race populasi) · `auth` (rate limit, enumerasi, expiry) · `LeaderboardService` (tie-break vs docs/33) · state machine UI `NexusGame`.
