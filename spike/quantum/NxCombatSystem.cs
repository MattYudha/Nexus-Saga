using Photon.Deterministic;

namespace Quantum
{
    /// <summary>
    /// Nexus Saga combat — deterministic Quantum system (SPIKE skeleton).
    /// Tick pipeline (doc 08 §3), 60 Hz. NO floats, NO non-seeded RNG.
    /// Blueprint: drop into the Quantum project (QuantumUser/Simulation/Nexus).
    /// Not all branches implemented — this is the Q-03/Q-05 scaffold to flesh out in-engine.
    /// </summary>
    public unsafe class NxCombatSystem : SystemMainThreadFilter<NxCombatSystem.Filter>, ISignalOnPlayerAdded
    {
        public struct Filter
        {
            public EntityRef Entity;
            public NxCombat* C;
        }

        // ---- tuning (fixed-point; titik awal dari doc 13 §4, di-reskin tema Exo-Gear) ----
        private static readonly FP MoveSpeed   = 5;             // unit/detik
        private static readonly FP Gravity     = (FP)44 / 10;   // 0.44 * 10 (contoh)
        private static readonly FP MaxHp       = 100;
        private const int   GuardArcDeg        = 180;           // busur depan (doc 08 §5.3)
        private const int   StartBreakStock    = 3;             // Critical (doc 08 §7.2)
        private const ushort YawQuarter        = 16384;         // 90° (65536/4) → cone aim ±22.5° = 4096

        public override void Update(Frame f, ref Filter filter)
        {
            if (f.Global->State != 1) return; // Playing only
            var c = filter.C;

            // T1–T2: input → arah/aim (hitstun/hitpause membekukan aksi)
            var input = f.GetPlayerInput((int)c->Player);
            bool frozen = c->HitPause > 0;

            if (!frozen && c->HitStun == 0)
            {
                ApplyMovement(f, c, input);
                ApplyGuard(c, input);
                // TODO Q-03/Q-05: state machine (attack/skill), swap, dash — dari data hero
            }

            // T4: physics (gravitasi + integrasi); collision arena (upright cylinder) → TODO
            ApplyPhysics(f, c);

            // T9: timer
            TickTimers(c);
        }

        // Hit resolution (T5–T8) dijalankan sekali per frame di sistem terpisah (NxHitSystem)
        // yang mengumpulkan pasangan OBB attack × OBB/Sphere hurt (beda team), urut prioritas lalu id,
        // lalu menerapkan Damage Gate + Break Stock + Gear Drop serentak. (Q-03)

        private static void ApplyMovement(Frame f, NxCombat* c, Input* input)
        {
            if (input == null || input->MoveDir == 0) { c->Vel.X = 0; c->Vel.Z = 0; return; }
            // 8 arah → vektor satuan fixed-point (tabel konstan deterministik)
            FPVector2 dir = Dir8(input->MoveDir);
            c->Vel.X = dir.X * MoveSpeed;
            c->Vel.Z = dir.Y * MoveSpeed;
            // arah hadap = arah gerak (kecuali sedang guard: lock facing)
            if (c->Guarding == 0) c->Yaw = YawFromDir(dir);
        }

        private static void ApplyGuard(NxCombat* c, Input* input)
        {
            bool holdGuard = input != null && (input->Buttons & 16) != 0;
            if (holdGuard && c->Guarding == 0) { c->Guarding = 1; c->GuardYaw = c->Yaw; } // lock facing (G1)
            else if (!holdGuard && c->Guarding == 1) { c->Guarding = 0; }
        }

        private static void ApplyPhysics(Frame f, NxCombat* c)
        {
            if (c->Posture == (byte)Posture.Air) c->Vel.Y -= Gravity * f.DeltaTime;
            c->Pos += c->Vel * f.DeltaTime;
            if (c->Pos.Y <= 0) { c->Pos.Y = 0; c->Vel.Y = 0; if (c->Posture == (byte)Posture.Air) c->Posture = (byte)Posture.Stand; }
            // TODO: collision pushbox (upright cylinder X-Z), DropZone kill-plane (doc 13 §8, doc 08 §7.4)
        }

        private static void TickTimers(NxCombat* c)
        {
            if (c->HitPause > 0) { c->HitPause--; return; } // hitpause membekukan semua, termasuk state time
            if (c->HitStun > 0) c->HitStun--;
            if (c->SwapCooldown > 0) c->SwapCooldown--;
            if (c->Guarding == 0 && c->GuardGauge < 100) c->GuardGauge++; // regen guard
            c->StateTime++;
        }

        // ---- helpers deterministik ----
        private static FPVector2 Dir8(byte d)
        {
            // 1=N..8=NW, searah jarum jam; komponen fixed-point (diagonal = 0.7071 ≈ 46341/65536)
            FP s = FP.FromRaw(46341L << (FPLut.PRECISION - 16)); // ~0.70710678
            switch (d)
            {
                case 1: return new FPVector2(0, 1);
                case 2: return new FPVector2(s, s);
                case 3: return new FPVector2(1, 0);
                case 4: return new FPVector2(s, -s);
                case 5: return new FPVector2(0, -1);
                case 6: return new FPVector2(-s, -s);
                case 7: return new FPVector2(-1, 0);
                case 8: return new FPVector2(-s, s);
                default: return default;
            }
        }

        private static ushort YawFromDir(FPVector2 dir)
        {
            // FPMath.Atan2 → 0..2π dipetakan ke 0..65535. (deterministik Quantum)
            FP a = FPMath.Atan2(dir.X, dir.Y); // sesuaikan konvensi sumbu nanti
            if (a < 0) a += FP.PiTimes2;
            return (ushort)((a / FP.PiTimes2 * 65536).AsInt & 0xFFFF);
        }

        public void OnPlayerAdded(Frame f, PlayerRef player, bool firstTime)
        {
            // Spawn entity combat untuk pemain (Q-03): set Hp=MaxHp, BreakStock saat Critical, GearMask penuh.
            // Detail spawn (prototype entity + posisi awal per team) diisi di engine.
        }
    }
}
