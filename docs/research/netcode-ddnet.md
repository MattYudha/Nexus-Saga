# Riset: Netcode DDNet 20.1.1 (2026-10-24)

Sumber: source DDNet 20.1.1 (open-source), di-clone ke `C:\Users\US3R\Nexus_Lab\src\ddnet` (di luar repo). Hanya dibaca. Path di bawah relatif ke folder itu. "unverified" = belum dikonfirmasi dari kode.

## Ringkasan (ID)
- Server: **50 Hz fixed tick**, loop catch-up, input dikunci per tick. Input terlambat **digeser maju**, tidak pernah di-rewind.
- Snapshot: **25 Hz** (tiap 2 tick). Dibuat per penonton, **delta terhadap snapshot terakhir yang di-ack**. Ack dibawa di paket input. Ada CRC + fallback resync penuh.
- Client: **rollback & replay penuh** dari snapshot server terbaru di setiap tick prediksi. Pemain remote diinterpolasi antar dua snapshot.
- Determinisme: physics float, tapi **di-Quantize ke integer setiap tick** di client dan server.
- Hit: **tanpa lag compensation**. Efek hit diprediksi lalu di-dedup dengan event server.
- Transport: UDP, paket 1400 B, chunk "vital" (reliable) vs non-vital, Huffman statis.

## Rekomendasi untuk Nexus Saga
1. Tiru: fixed tick + input per tick (unreliable, kirim 2–3 input terakhir redundan), umpan balik input-timing untuk sinkron jam, delta snapshot vs ack, state integer + quantize tiap tick, kode simulasi **satu library** untuk client & server, rollback-replay, dedup event prediksi.
2. Ubah:
   - **Sim 60 Hz** (frame animasi = tick), snapshot 30–60 Hz. 10 pemain ≈ < 1 KB/snapshot.
   - **Lag compensation melee**: histori hurtbox 200–300 ms di server, rewind dibatasi ±150 ms.
   - Client boleh memprediksi hit-confirm/hitpause/spark milik **penyerang**. Damage, knockdown, dan **Gear Drop** hanya dari server.
   - Hitstun ≥ ~10 frame supaya keterlambatan 1 RTT di sisi korban tertutup blend animasi.
   - **Hero Swap, Gear Drop pickup, KO** = pesan reliable atau state snapshot persisten, bukan event transien.
3. Jebakan: float tanpa quantize, urutan proses beda client/server, snapshot > 1 MTU, prediksi tak dibatasi.

---

## Laporan lengkap (EN)

### 1. Tick model
- `SERVER_TICK_SPEED = 50` (`src/engine/shared/protocol.h:81`), i.e. a fixed 50 Hz / 20 ms sim. `MAX_INPUT_SIZE = 128` ints (`protocol.h:106`).
- Server loop: a while-loop catches up one iteration per elapsed tick (`src/engine/server/server.cpp:3547-3597`). Each player's input is looked up by exact tick (`:3579-3589`); `nullptr` means "no new input" and the last input is kept. A snapshot is built once per loop that advanced at least one tick (`:3600-3602`). The world tick runs every entity's `Tick()`, then every entity's `TickDeferred()` (`src/game/server/gameworld.cpp:229,238`).
- Input: `CNetObj_PlayerInput` (`datasrc/network.py:113-127`): direction, target X/Y, jump, fire, hook, flags, weapon fields.
- Client `SendInput` (`src/engine/client/client.cpp:350-407`): packs the last acked snap tick, then the predicted tick, then the input. It keeps a 200-entry ring and sends unreliable with `MSGFLAG_FLUSH` (`:399`). The server drops vital inputs (`server.cpp:1862-1865`).
- Server input handling (`server.cpp:1860-1933`): stores the ack, measures latency, and replies `NETMSG_INPUTTIMING(IntendedTick, TimeLeft)` (`:1910-1918`). Late input is clamped with `IntendedTick = max(IntendedTick, Tick()+1)` (`:1921`).
- Prediction clock: `m_PredictedTime.Update` uses TimeLeft (`client.cpp:2084-2108`). `cl_prediction_margin` defaults to 10 ms (`config_variables.h:27`). The predicted time resets beyond `MaxLatencyTicks` (`client.cpp:5429-5432`, `:2950-2954`). Optional `sv_preinput` (`server.cpp:1934-1947`).

### 2. Snapshots
- `CServer::DoSnapshot` (`server.cpp:1022-1179`) builds per client: `Init`, then `OnSnap(i, ...)`, then `Finish` (`:1063-1070`). Limits: `MAX_ITEMS=1024`, `MAX_SIZE=64KB` (`snapshot.h:48-50`).
- `IsGlobalSnap = m_SvHighBandwidth || tick%2==0` (`server.cpp:1024`), i.e. 25 Hz (50 Hz on LAN). Recovery and init modes are throttled (`:1051-1056`, `:1111-1113`).
- Delta: history is purged to `max(now-3s, lastAcked)` (`:1087-1090`), with the base being the last acked snap or an empty snap (`:1093-1115`). `CSnapshotDelta::CreateDelta` (`snapshot.cpp:302-379`) sends deleted keys, a per-int wrapping diff (`:239`) with unchanged items omitted (`:356`), and new items in full. The result is varint-packed (`server.cpp:1128`), split into ≤900 B parts (`protocol.h:107`), and an unchanged snap becomes `NETMSG_SNAPEMPTY`. A CRC is included (`:1145-1149`).
- Client storage (`client.cpp:2110-2358`): reassembles parts, uses the delta base (a missing base sets ack -1 for a resync), checks the CRC (>10 errors forces a resync), purges, and sets the ack.

### 3. Prediction & reconciliation
- `UpdatePrediction` (`gameclient.cpp:3519-3648`): advances the confirmed world, then overwrites it from the snapshot.
- `OnPredict` (`gameclient.cpp:2612-2886`): `CopyWorld`, then replays inputs from server tick+1 to the predicted tick (`:2647-2719`). Remote players are dead-reckoned with their last input. A 200-entry predicted-position ring is kept, and mispredictions are checked in debug.
- Smoothing: the local player uses `PredIntraGameTick`; remote players use `IntraGameTick` = mix(prev, cur) (`players.cpp:216,500,602`). `cl_antiping_smooth` blends errors, capped at 700 ms (`gameclient.cpp:2787-2846`).

### 4. Determinism
- Float `vec2` physics runs in shared `CCharacterCore` (`gamecore.cpp:195-607`), with a separate client entity copy in `src/game/client/prediction/entities/character.cpp`.
- `Quantize()` is a Write→Read round-trip (`gamecore.cpp:702-707`). Position is an int and velocity is ×256 (`:611-621`). It is called after Move on the server (`server/entities/character.cpp:876-878`) and in the client prediction (`prediction/entities/character.cpp:655`).
- Bit-identical floats across CPUs are not guaranteed (unverified). The next snapshot corrects drift.
- Fixed ordering: hook order (`gameclient.cpp:3549-3576`), and player collision by client id (`gamecore.cpp:584`).

### 5. Hits
- Server hammer (`server/entities/character.cpp:514-566`): `FindEntities` at current positions, then `TakeDamage`, then the hit event and reload ticks. **No rewind** (grep for `rewind|lag.?compensat|history` in `src/game/server` found nothing).
- Predicted weapons (`prediction/entities/character.cpp:313-370`): `m_PredictedEvents` are deduped by (type, pos, id, tick) (`prediction/gameworld.cpp:818-836`) and played once (`gameclient.cpp:3851-3897`).
- Server events are snap items on global snaps (`gamecontext.cpp:4617-4630`). The client skips one if a predicted match exists, matching on tick ≤ (`gameclient.cpp:1474-1477`). A predicted event the server never confirms is not rolled back; it expires after 3 s.

### 6. Transport
- UDP, `NET_MAX_PACKETSIZE=1400`, 3 B packet header, up to 255 chunks per packet (`network.h:69,78,83`).
- Chunk header is 2 B, or 3 B with VITAL (10-bit sequence) (`network.cpp:443-456`, `network.h:82,94`). There is a 32 KB resend buffer (`network.h:103,262`) with rate-limited resends (`network_conn.cpp:221-245`).
- Snapshots and inputs are non-vital (`server.cpp:1150,1162,1171`; `client.cpp:399`).
- Static Huffman, used only if smaller (`network.cpp:225-244`).

### 7. Recommendations
See the Indonesian summary above. The full original report is in this session's transcript; the main points are recorded here.
