# IS-431 Boxing Robot — Complete Project Knowledge Brief

**Last Updated:** 2026-04-07
**Compiled By:** Antigravity (Electrical & Systems Architect Agent)
**Purpose:** Fully self-contained context handoff for any new agent. All critical knowledge is embedded here — do not assume access to any other file.

---

## 1. Project Overview

**Project ID:** IS-431 (CDE4301 Final Year Project, NUS)
**Robot Name:** BoxBunny
**Type:** 2-DOF differential-joint boxing robot — a stationary sparring partner that delivers punch strikes to a human trainee

There are 4 mechanical subsystems:
1. **Arm Actuation** — 2-DOF coaxial differential joint driven by 4× Damiao DM-J4310-2EC brushless motors
2. **Height Adjustment** — Motorised lead-screw column driven by a CHP-36GP-555 brushed DC motor via a Cytron MDDS10 H-bridge driver
3. **Base Rotation** — Rotating platform driven by a Z55BLD400-24GU 400W BLDC motor via a ZBLD C20-800LRC CAN Modbus driver
4. **Strike Sensing** — 4× MPU6050 IMUs mounted on padding zones for impact detection

**Computing stack:**
- **Jetson Orin NX** — primary computer, runs ROS 2 Humble + Python GUI
- **Teensy 4.0** — real-time motor controller (micro-ROS, CAN bus, I2C)
- **Arduino Uno R4 WiFi** — standalone base rotation controller (BLE + CAN at 125 kbps)

**Academic context:** This is a Final Year Project at NUS. The report must conform to strict academic writing standards (passive voice, no bold in body prose, no bullet lists in paragraph sections, V-Model traceability). The web report is submitted as HTML pages, not a PDF.

---

## 2. Full Hardware Specifications

### 2.1 Arm Motors — 4× Damiao DM-J4310-2EC

| Parameter | Value |
|---|---|
| Quantity | 4 (2 per arm — left arm: M1/M2, right arm: M3/M4) |
| Voltage | 24V DC |
| CAN protocol | MIT Position-Velocity mode, **1 Mbps** |
| CAN IDs | **0x101–0x104** (per motor_specifications — ⚠ HTML report pages list 0x01–0x04, discrepancy pending firmware confirmation) |
| CAN bus topology | **PARALLEL (star)** — all 4 motors share one bus wire from Teensy CAN transceiver. **NOT daisy-chain.** 120Ω termination at Teensy transceiver end; one more at the furthest physical motor. |
| Motor role naming | M1, M3 = roll motor (outer body rotation); M2, M4 = pitch motor (inner shaft) |
| Gear reduction | 3:1 helical gear (each motor drives into the coaxial differential gear stack) |
| Measured peak power (sparring) | ~33W peak / ~10W average across all 4 during a full strike cycle |
| Theoretical stall power | ~384W (16A stall × 24V) — use ONLY for fuse/wire sizing, not PSU sizing |
| Measured sparring current | <1A per motor (well below 3A firmware safety limit) |
| RegenClamp | **NOT required** — internal PID manages deceleration ramps; bus capacitors absorb gradual back-EMF |
| Safety limit | 3A firmware current watchdog; GUI has adjustable current-limit UI |

### 2.2 Height Motor — CHP-36GP-555

> ⚠ **Critical:** This motor was previously documented as "LGYMSZSS" and "MY1016Z" in all older files and log entries. Those names are **wrong**. The model was positively identified by reading the physical motor label on 2026-04-06. Always use CHP-36GP-555.

| Parameter | Value |
|---|---|
| Model | **CHP-36GP-555 GEAR BOX MOTOR** |
| Type | Brushed DC with integrated all-metal planetary gearbox |
| Supply voltage | 24V DC |
| Output shaft speed (no-load) | **440 RPM** (after 27:1 gearbox) |
| Gearbox ratio | **27:1** (i27) |
| Shaft | 8mm D-type |
| Rated current | ~2.6A |
| **Stall current** | **~21A** (critical for brake resistor sizing) |
| Winding resistance | ~1.14Ω (= 24V / 21A stall; confirmed in range) |
| Rated torque | ~14 kg·cm (1.37 N·m) |
| Stall torque | ~35–50 kg·cm |
| Speed encoder | AB phase Hall encoder — **PRESENT but UNUSED** (excluded from all documentation) |
| Driver | Cytron SmartDriveDuo-10 (MDDS10) |
| Control mode | Sign-Magnitude PWM — Teensy Pin 3 → AN1 (PWM speed); Teensy Pin 2 → DIG1 (direction) |

**MDDS10 DIP switch configuration** (Sign-Magnitude PWM, independent channels):
```
SW1=ON, SW2=OFF, SW3=ON, SW4=ON, SW5=OFF, SW6=ON
Binary array: 1 0 1 1 0 1 x x
```
> Note: Pin labels were originally transposed in documentation. The correct assignment is confirmed: **Pin 3 = AN1 (speed/PWM)** and **Pin 2 = DIG1/IN1 (direction)**. No physical rewiring required — only firmware was corrected.

**RegenClamp status:** Required — ✅ **10Ω 50W aluminium wirewound. TO PROCURE.**
Reasoning: At hard stop, unclamped regen current = ~21A (V_back-EMF / R_winding). RegenClamp limits this to 2.65A at 70W for ≤300ms.

**OVP incident (2026-03-11):** When height motor was stopped abruptly, back-EMF tripped the Mean Well PSU OVP (~28V threshold), causing a full system power reset. Short-term mitigation: software PWM ramp-down (6 decreasing steps over 300ms before STOP). Hardware fix (RegenClamp) still pending procurement.

### 2.3 Base Motor — Z55BLD400-24GU

| Parameter | Value |
|---|---|
| Model | Z55BLD400-24GU |
| Type | 400W BLDC motor |
| Supply voltage | 24V DC |
| Internal gearbox | **26:1** (measured via encoder; datasheet says 25:1 — **actual is 26:1**) |
| Timing belt reduction | **3.5:1** (20-tooth pinion → 70-tooth driven pulley) |
| **Total gear ratio** | **91:1** (26:1 × 3.5:1) |
| Position encoder | AS5047P 14-bit absolute magnetic encoder (mounted on motor input shaft) |
| Effective resolution | 16,384 counts × 26 = **425,984 counts per output revolution** |
| Driver | ZBLD C20-800LRC (CAN Modbus, **125 kbps**) |
| Controller | Arduino Uno R4 WiFi (separate from Teensy — independent failure domain) |
| Comms to Jetson | WiFi UDP (eliminates cable twist through rotating base joint) |
| Design output speed | 150°/s = 2,275 motor RPM (67% of 3,400 RPM maximum) |
| Position limits | ±90° base output = ±22.75 motor turns (Arduino-enforced in firmware) |
| Measured power at 150°/s | ~37W (1.6A @ 23.5V) |
| Design power allocation | 45W (20% safety margin) |
| **RegenClamp** | Required — ✅ **5Ω 100W aluminium wirewound. TO PROCURE.** |

**Base rotation PID controller (tuned, validated 2026-04-05):**

| Parameter | Value |
|---|---|
| Loop rate | 50Hz |
| Kp | 25.0 |
| Ki | 1.0 |
| Kd | 1.0 |
| Dead zone | ±1° (motor stops when within 1° of target) |
| Peak RPM cap | 1000 RPM (default; user-adjustable via `PEAK:` command) |
| Command protocol | `L:deg` (relative left), `R:deg` (relative right), `GO:deg` (absolute), `PEAK:rpm`, `PID:Kp,Ki,Kd` |

**Key PID bugs fixed:**
1. Direction inversion → positive feedback runaway. Fixed: hardcoded CAN direction mapping (positive output → dir=2 = CAN 0x0001 = encoder-positive direction).
2. Hard limit trap at ±90° blocked recovery commands. Fixed: limits only block *toward* the limit; return-to-centre always allowed.
3. `dirFlipped` flag conflicted with PID direction understanding. Fixed: flag removed; direction baked into CAN mapping.

**AS5047P Encoder — Pin 13 conflict:** Arduino R4 WiFi uses Pin 13 for CAN RX, which conflicts with hardware SPI SCK. Solution: bit-banged software SPI on Pins 4–7 (CSn=4, CLK=5, MOSI=6, MISO=7).

---

## 3. Power Architecture

### 3.1 Dual-Rail Topology (ACTIVE — as of 2026-04-03)

```
AC Mains (Standard 230V/110V)
│
├── Mean Well LRS-200-24 (24V, 8.8A, 211W)   ─── MOTOR BUS
│   │
│   ├── 20A Inline Fuse
│   ├── Mushroom-head NC Emergency Stop Switch
│   │   (cuts ALL 24V actuators; 12V logic stays live; NC = fail-safe)
│   └── 24V Distribution Busbar
│       ├── 4× DM-J4310-2EC Arm Motors (DIRECT — no RegenClamp)
│       ├── RegenClamp V0.3 (26.5V threshold) → MDDS10 → CHP-36GP-555 [Height]
│       └── RegenClamp V0.3 (PENDING install) → ZBLD C20-800LRC → Z55BLD400 [Base]
│
└── Mean Well 12V 5A PSU  ─── LOGIC BUS (galvanically isolated from motor bus)
    │
    ├── Jetson Orin NX
    │   └── USB-A to Micro-B → Teensy 4.0 (data + 5V power)
    └── HW-140 Buck Converter (12V → 5V, ≥1A)
        └── Arduino Uno R4 WiFi (0.4A / 2W via VIN pin)
```

> **Isolation rationale:** Before 2026-03-13, a 12V buck was drawing from the 24V motor bus. When the height motor caused an OVP trip, the Jetson and Teensy lost power mid-session. Now they are on a completely separate 12V PSU from AC mains — motor faults no longer reboot the computer.

### 3.2 PSU Recommendation

| Current PSU | Recommended Upgrade |
|---|---|
| LRS-200-24 (8.8A / 211W) | **LRS-350-24 (14.6A / 350W)** — same footprint, 2.5× headroom. At 55% utilisation (normal sparring ~115W), handles startup transients without OVP risk. |

### 3.3 Measured System Power Budget

| Component | Rail | Measured Current | Measured Power |
|---|---|---|---|
| 4× Arm Motors (sparring) | 24V | <1A total across 4 | ~33W peak / ~10W avg |
| CHP-36GP-555 Height Motor | 24V | ~1.6A | ~38W |
| Z55BLD400 Base Motor @ 150°/s | 24V | ~1.6A | ~37W |
| Jetson Orin NX | 12V | ~2A | ~25W |
| Teensy 4.0 | 5V USB | 0.1A | 0.5W |
| Arduino Uno R4 WiFi | 5V buck | 0.4A | ~2W |
| **Normal sparring total** | — | — | **~115W** |

### 3.4 Brake Resistor Sizing (Complete)

| Motor | Brake Resistor | Brake Current | Peak Power | Pulse Duration | Status |
|---|---|---|---|---|---|
| CHP-36GP-555 (Height) | **10Ω 50W aluminium wirewound** | 2.65A (26.5V/10Ω) | 70W | ≤300ms | **TO PROCURE** |
| Z55BLD400 (Base) | **5Ω 100W aluminium wirewound** | 5.3A (26.5V/5Ω) | 140W | ≤800ms | **TO PROCURE** |
| DM-J4310-2EC (Arms) | None | — | — | — | Exempt |

**RegenClamp V0.3 specs:** 26.5V clamping threshold, 800W dissipation capability. One unit installed on height; one unit pending installation on base.

### 3.5 Wire & Connector Specification

| Segment | Wire | Connector | Rationale |
|---|---|---|---|
| AC Mains → PSUs | IEC C13, 3×1.5mm² | IEC inlet | Standard instrument cord |
| PSU → Fuse | 12AWG silicone | XT60 | High-current, quick-disconnect |
| Fuse → E-Stop → Busbar | 12AWG silicone | Ring terminals | 20A continuous |
| Busbar → ZBLD/MDDS10 | 14AWG silicone | XT30 | 15A branch rating |
| MDDS10/RegenClamp → Motors | 18AWG silicone | Screw terminal | <2A operating |
| Damiao arms (from busbar) | 18AWG silicone | JST-XH 2P | <1A measured |
| 12V PSU → Jetson | 16AWG silicone | Barrel jack | Jetson standard |
| 12V PSU → Buck Converter | 18AWG silicone | Screw terminal | Module input |
| Buck → Arduino | 22AWG dupont | VIN pin header | 0.4A |
| Jetson → Teensy | USB-A to Micro-B | USB cable | Data + 5V |

---

## 4. Signal / Data Architecture

### 4.1 Control Flow

```
Jetson Orin NX (ROS 2 Humble)
  │
  ├── USB serial (micro-ROS) ──────────────────────────────────┐
  │                                                             ▼
  │                                                   Teensy 4.0 (200Hz unified loop)
  │                                                     │
  │                                                     ├── CAN Bus (1 Mbps, PARALLEL/STAR)
  │                                                     │    └── 4× DM-J4310-2EC (0x101–0x104)
  │                                                     ├── PWM/DIR → MDDS10 → CHP-36GP-555
  │                                                     └── I2C 400kHz (dual bus)
  │                                                          ├── Wire  (pins 18/19): 0x68, 0x69
  │                                                          └── Wire1 (pins 17/16): 0x68, 0x69
  │
  └── WiFi UDP ─────────────────────────────────────────────────┐
                                                                ▼
                                                      Arduino Uno R4 WiFi
                                                        └── CAN (125 kbps)
                                                             └── ZBLD → Z55BLD400
```

### 4.2 Teensy Firmware V4 — 200Hz Unified Loop Budget (5ms)

| Task | Time Used |
|---|---|
| CAN motor commands (4× Damiao) | ~1.2ms |
| CAN motor feedback read | ~0.8ms |
| I2C IMU polling (4× MPU6050) | ~1.5ms |
| micro-ROS publish/subscribe | ~0.3ms |
| **Total** | **~3.8ms** (1.2ms headroom) |

**Micro-ROS disconnect recovery:** If the ROS agent fails 3 consecutive pings (1.5 seconds), Teensy executes a hardware silicon reset (`SCB_AIRCR = 0x05FA0004`). This restores a clean memory state regardless of WSL/USB driver state, ensuring the Teensy re-handshakes cleanly when the agent returns.

**CAN command strategy (arms):** Edge-trigger — only re-send if target position changed by >0.01 rad, OR a 100ms keep-alive pulse regardless. This prevents the Damiao firmware's "trajectory reset bug" where continuous 50Hz commands restart the internal trapezoidal planner every 20ms, causing severe stuttering.

**Current feedback parsing fix (critical):** Damiao CAN telemetry packages torque as a **12-bit** integer, not a 16-bit float. Earlier firmware misread this and consumed the adjacent temperature byte, causing phantom 8–9A idle current readings. Fixed by explicitly extracting the 12-bit MIT torque field.

### 4.3 ROS 2 Topic Interface (7 topics)

**Subscribers (commands → robot):**

| Topic | Message Type | Payload |
|---|---|---|
| `/motor_commands` | Float64MultiArray | [pos×4, speed×4, enable_flag] |
| `/robot/height_cmd` | String | `UP:pwm`, `DOWN:pwm`, `STOP`, `REVERSE:0/1` |
| `/robot/strike_command` | String (JSON) | `{"slot": 1, "duration": 3.0, "speed": 15.0}` |
| `/robot/punch_slots` | String (JSON) | `{"1": {"arm": "left", "strike": "Jab"}, ...}` |
| `/robot/system_enable` | String | `"enable"` / `"disable"` |

**Publishers (robot → status):**

| Topic | Message Type | Payload |
|---|---|---|
| `/motor_feedback` | Float64MultiArray | [pos×4, current×4, CAN_count, IMU_accel×12] = **21 doubles** |
| `/robot/strike_feedback` | String (JSON) | `{slot, strike, status, duration_allowed, duration_actual}` |
| `/robot/strike_detected` | String (JSON) | `{pad_index, pad_name, peak_accel, calibrated_peak, relative_power}` |

> ⚠ **Topic name inconsistency (open bug):** `padding/electrical-integration.html` uses `/strike_events`, `firmware-software.html` uses `/robot/strike_detected` (with prefix), and `motor_specifications.md` uses `/strike_detected` (no prefix). The authoritative topic is `/robot/strike_detected` as implemented in the active GUI V3 code.

### 4.4 IMU Configuration

- **Hardware:** 4× InvenSense MPU6050 ICs
- **Buses:** Wire (Teensy pins 18/19) and Wire1 (Teensy pins 17/16), both at 400 kHz
- **Addressing:** Two addresses per bus — 0x68 (AD0=GND) and 0x69 (AD0=VCC)
- **Mapping:** Centre Body (Wire/0x68), Left Body (Wire/0x69), Right Body (Wire1/0x68), Reserved (Wire1/0x69)
- **I2C protocol fix:** Must use Hard STOP (`endTransmission(true)`) before reading. Long wires to chassis padding cause high capacitance that hangs the bus with Repeated Start at 400kHz.
- **Polling rate:** 200Hz (unified with motor loop) — some older documentation incorrectly states 500Hz. ⏳ PENDING firmware source confirmation.

---

## 5. Arm Mechanism — Kinematics & Design

### 5.1 Mechanical Design

- **Joint type:** Coaxial differential (outer housing = roll axis, inner shaft = pitch axis)
- **Gear chain:** Each Damiao motor drives a 3:1 helical gear, which drives the coaxial differential gear stack
- **Bevel gear coupling:** When the outer housing (roll) rotates, the inner bevel gear "walks," coupling roll into pitch displacement
- **Motor-to-joint naming:** M1/M3 = roll motor (outer body); M2/M4 = pitch motor (inner shaft)
- **Total arm reach:** 0.80m from rotation axis (arm + pool noodle padding)
- **Shoulder offset from body centre:** ±0.2414m (symmetric arms)

### 5.2 Validated Forward Kinematics (validated on hardware 2026-04-02)

Old incorrect model treated roll as a global Z-tilt. Physically, **rolling rotates the pitch swing plane** (via bevel gear walking). The correct model:

$$\vec{d} = [s_x \cos(p),\quad \sin(p)\cos(r),\quad \sin(p)\sin(r)]$$

Where `p` = joint pitch angle, `r` = joint roll angle. The Z-component is `sin(p)sin(r)` — coupled between pitch and roll. Both CW and CCW body rotation cause the arm to tilt **upward** because the bevel walking direction reverses with roll direction.

### 5.3 Motor ↔ Joint Space Conversion

$$m_r = s_r \cdot r + \text{roll\_offset}$$
$$m_p = s_p \cdot p + c \cdot s_p \cdot m_r + \text{pitch\_offset}$$

Where:
- `s_r` = roll motor direction sign
- `s_p` = pitch motor direction sign
- `c` = bevel gear coupling direction (±1)

**Validated calibration results (physical hardware):**

| Parameter | Left Arm (M1/M2) | Right Arm (M3/M4) |
|---|---|---|
| pitch_sign (sₚ) | **-1** | **+1** |
| roll_sign (sᵣ) | **+1** | **-1** |
| coupling (c) | **-1** | **-1** |

Both arms share coupling = -1 (same bevel gear arrangement). Signs are mirrored (symmetric geometry).

### 5.4 Joint Limits

| Axis | Physical Hard Stop | Recommended Software Zone | Notes |
|---|---|---|---|
| Pitch | ±1.57 rad (±90°) | ±1.0 rad | 3D-printed plastic stops on inner shaft |
| Roll | None | Cable-wrap dependent (~±2–3 full turns) | Free-spinning outer housing |

**Joint-space pitch clamping (active in GUI):** Before motor commands are sent, slider values are converted to joint space, pitch is clamped to `[pitch_lower, pitch_upper]`, then converted back with coupling compensation. This prevents walking the pitch axis into hard stops via roll-only commands.

### 5.5 Kinematic History (for academic thesis context)

| Approach | Date | Status | Failure Reason |
|---|---|---|---|
| Joint-space firmware endstops (`apply_dynamic_endstops`) | 2026-03-11 | **Abandoned** | "Jump-Back" defect: activating the clamp required sudden counter-commands to uncommanded motor, causing visible arm bounce |
| Automated sensorless homing (current sweep against hard stops) | 2026-03-11 | **Abandoned** | False termination: current spike from hard stop indistinguishable from motor fault spike; Motor 2 resonance torque aborted sequence |
| Raw motor space + manual calibration + dI/dt impact detection | 2026-03-11 | **Active (legacy GUI V3)** | Working but requires operator calibration session |
| Joint-space pitch clamping in Python GUI | 2026-04-02 | **Active (GUI V4)** | Resolved decoupling dilemma |

### 5.6 Material Selection for 3D-Printed Parts

| Component | Material | Reason |
|---|---|---|
| Gear teeth | **PLA** | Higher stiffness (3.5 GPa vs 2.0 GPa for PETG); brittleness acceptable because 3A current-limit watchdog stops the motor before gear tooth fracture |
| Structural housing | **PETG** | Better impact ductility, 20°C higher glass transition than PLA (important for chassis near motors) |
| Rejected material | **PETG-CF** | Physical testing: short chopped carbon fibres act as stress concentrators → crack initiation; also reduces inter-layer adhesion → unexpected brittle fracture. **Do not use for gear components.** |

**Structural failures (documented for thesis):** During a project showcase, 3D-printed shaft components fractured under load. Post-failure revisions: 6mm stainless D-shaft, 2mm Delrin pin, M2 screw reinforcement.

---

## 6. Software Architecture

### 6.1 Active File Versions

| Component | File/Location | Version | Status |
|---|---|---|---|
| Teensy Firmware | `teensy_firmware_V4/teensy_firmware_V4.ino` | V4 | ✅ VALIDATED |
| GUI (primary production) | `ros2_ws/unified_GUI_V3.py` | V3, ~2278 lines, PyQt5/PyQtGraph | ✅ VALIDATED |
| GUI (V4 modular build) | `ros2_ws/unified_v4/build_v4.py` + tab modules | V4 | In development |
| Base Controller Firmware | `base_motor_control/ble_control/ble_control.ino` | V2+PID | ✅ Validated |
| Web Bluetooth UI | `base_motor_control/ble_control/controller.html` | — | ✅ Validated |
| Test Validation GUI | `testing/test_validation_GUI.py` | — | ~1346 lines, standalone |

**Deprecated/archived (do NOT modify):** `unified_GUI.py` (Tkinter V1), `unified_GUI_V2.py` (PyQt5 V2, archived).

### 6.2 GUI Tab Architecture (V3)

| Tab # | Class | Purpose |
|---|---|---|
| 1 | `ManualTab` | Slider-based 4-motor positioning; record sequences to JSON |
| 2 | `CalibrationTab` | Per-motor homing via current spikes; safety current threshold; encoder offset editor |
| 3 | `StrikeLibraryTab` | 2-point strike library (Windup+Apex); Teach Pendant from live encoders; Load/Save unified JSON |
| 4 | `AnalyticsTab` | Real-time current/position plots; live power telemetry; CSV export |
| 5 | `HeightTab` | MDDS10 lead-screw control (hold-to-move, PWM slider, direction reverse, ramp-down stop) |
| 6 | `IMUDiagnosticsTab` | Strike detection with Butterworth LPF; live FFT; Punch Calibration Wizard |
| 7 | `DynamicSparringTab` | FSM combat engine — IMU-triggered pad-based sparring with all FSM features |
| 8 | `RosControlTab` | ROS 2 front-end interface — 6 strike slots; dynamic speed adaptation; auto-return |

### 6.3 Dynamic Sparring FSM (Hardware-Validated 2026-03-27)

```
Strike Triggered
  │
  ├── Compute alignment angle θ
  │     Strike vector:   V_strike  = apex - windup          (intended approach direction)
  │     Approach vector: V_approach = apex - current_pos     (actual approach if windup skipped)
  │     θ = arccos( V_strike · V_approach / |V_strike| |V_approach| )
  │
  ├── θ < threshold (default 30°)?
  │     YES → Skip Windup — approach is aligned; go directly to Apex
  │
  └── θ ≥ threshold?
        YES → Windup Required
              ├── Find all other strike windups whose M1 falls between M1_start and M1_target
              ├── Sort by M1 in travel direction (perimeter orbit — avoids sweeping through centre/face zone)
              ├── Execute transit waypoints → target Windup → Apex
              └── Snap-back: recovery = apex - snap_factor × (apex - windup)
  │
  └── Synchronized arrival: spd_M1 = base × (ΔM1 / max(ΔM1, ΔM2)), and vice versa
                             (ensures both motors arrive at target simultaneously = straight-line trajectory)
```

### 6.4 Strike Library Format (V4 Joint-Space Storage)

Strikes stored in joint space (survive motor recalibration), converted to motor space at execution via `strike_to_motor()`:

```json
{
  "left": {
    "Jab":         { "windup": [roll, pitch], "apex": [roll, pitch], "space": "joint" },
    "Left Hook":   { "windup": [roll, pitch], "apex": [roll, pitch], "space": "joint" },
    "Left Uppercut": { "windup": [roll, pitch], "apex": [roll, pitch], "space": "joint" }
  },
  "right": {
    "Cross":         { "windup": [roll, pitch], "apex": [roll, pitch], "space": "joint" },
    "Right Hook":    { "windup": [roll, pitch], "apex": [roll, pitch], "space": "joint" },
    "Right Uppercut":{ "windup": [roll, pitch], "apex": [roll, pitch], "space": "joint" }
  }
}
```

### 6.5 IMU Strike Detection Pipeline

1. IMU streams accel at 200Hz via `/motor_feedback` topic (21-double payload, last 12 entries)
2. `IMUDiagnosticsTab` applies Butterworth LPF, computes `|a| = √(x²+y²+z²)` vector magnitude
3. **Nyquist blind-spot fix:** GUI refreshes at 20Hz but firmware at 200Hz. Fix: use `np.max(buffer[-n_scan:])` to search all samples acquired since last GUI tick — not just the last sample
4. Punch Calibration Wizard sets detection threshold as a user-specified percentage of measured baseline peak
5. On threshold breach → publish to `/robot/strike_detected`
6. `DynamicSparringTab` maps `pad_index` to pre-assigned strike slot and executes the strike

---

## 7. Strike Speed Performance (Validated 2026-04-03, 43 Tests)

### 7.1 Key Finding — Partially Meets Requirement

| Metric | Requirement | Status |
|---|---|---|
| Peak arm joint angular velocity | 90° in ≤0.25s at constant velocity | ✅ MET — 113 joint RPM sustained = 90° in 0.13s theoretically |
| End-to-end strike time (WU → AP) | ≤0.25s | ❌ NOT YET — measured ~0.64s at 30 rad/s |
| Root cause | PID accel/decel overhead ~0.45s constant regardless of speed | Diminishing returns above 20 rad/s |
| Path to compliance | Damiao PID tuning (higher Kp) or MIT mode (direct torque control) | **DEFERRED — no spare motors** |

Current 0.64s strike cycle provides realistic boxing tempo for sparring purposes.

### 7.2 Per-Strike Timing (25 rad/s, 3 reps each)

| Strike | Arm | WU→AP (s) | Total (s) | Peak Motor RPM | Peak Current |
|---|---|---|---|---|---|
| Jab | Left | 0.66 | 1.24 | 239 | <0.7A |
| Left Hook | Left | 0.67 | 1.25 | 300 | <0.7A |
| Left Uppercut | Left | 0.55 | 1.09 | 218 | <0.7A |
| Cross | Right | 0.61 | 1.18 | 285 | <0.7A |
| Right Hook | Right | 0.62 | 1.20 | 207 | <0.7A |
| Right Uppercut | Right | 0.57 | 1.07 | 238 | <0.7A |

### 7.3 Why Measured Power (33W) Is Much Lower Than Theoretical (384W)

1. **Short travel distance:** A punch is ~1.57 rad at joint = ~4.71 rad at motor. At 25 rad/s, the required transit time is 0.19s — the motor never reaches steady-state velocity before deceleration begins (triangle velocity profile, not trapezoid).
2. **PID overhead:** ~0.45s constant accel/decel regardless of speed. Execution time plateaus near 0.64s.
3. **Torque ∝ current, not speed:** 16A stall current only occurs when motor is mechanically locked. During a free-air punch with lightweight pool noodle (~200g): <1A per motor.

**Both figures are needed in the thesis:** 33W (measured, for PSU sizing + efficiency analysis) and 384W (theoretical stall, for fuse, wire gauge, and safety analysis).

---

## 8. Web Report — IS-431 HTML Pages

### 8.1 Page Structure

The report lives at `documents/IS431/pages/robot-mechanism/` with these sub-pages:

| Folder | Pages Inside |
|---|---|
| `arm-actuation/` | `electrical-integration.html`, `firmware-software.html`, `design-ideation.html`, `mechanical-design.html`, `testing-evaluation.html` |
| `height-adjustment/` | `electrical-control.html` |
| `padding/` | `electrical-integration.html`, `mechanical-design.html`, `testing-evaluation.html`, `troubleshooting.html` |
| `rotation/` | `electrical-control.html` |

**Shared components:** `documents/IS431/components/lightbox/lightbox.js` — click-to-zoom for all architecture diagram images.

Architecture diagrams are referenced as PNG files from `System_architecture/` folder (rendered from D2 source files using `d2 --layout=elk`).

### 8.2 Academic Writing Standards (Summary)

The report must comply with strict academic standards (reference: `documents/academic_writing_skills.md`):

- **No bold in body text:** `<strong>` and `<b>` are only permitted in headings, table headers, and figure captions — never in `<p>` body paragraphs
- **No lists in prose sections:** `<ul>` and `<ol>` are forbidden inside body paragraph sections; use prose with commas/semicolons instead
- **Passive voice** preferred for methods and design sections
- **V-Model traceability:** Each page must reference the relevant requirements (RM-1 through RM-7); tests must link back to requirements
- **Section numbering:** Comment markers in HTML must match visible heading numbering; no jumping from §2 to §4
- **Cited measurements:** Every quantitative claim (current, speed, timing) requires evidence — test data reference, or cite which sensor/measurement method

### 8.3 Content Audit Status — validation_report_2.md

22 findings total. Status legend: ✅ CLOSED (no action needed), ⏳ PENDING (needs another agent/firmware confirmation), open (must fix).

**Closed findings:**
| # | Finding | Resolution |
|---|---|---|
| 2 | Single 120Ω CAN terminator stated (should be two for parallel bus) | CLOSED — engineer confirmed single transceiver resistor is functional; system validated in operation |
| 10 | Height motor model uncertainty | CLOSED — CHP-36GP-555 positively confirmed from motor label |

**Pending findings (require firmware confirmation):**
| # | Finding | Discrepancy |
|---|---|---|
| 1 | CAN Motor IDs | HTML report: 0x01–0x04; motor_specifications.md: 0x101–0x104. Must be confirmed from firmware source |
| 15 | IMU polling rate | HTML pages state 200Hz; motor_specifications.md §9 states 500Hz. Must be confirmed from firmware |

**High-severity open findings (sample):**
| # | File | Issue |
|---|---|---|
| 3 | arm-actuation/electrical-integration.html | PSU rated "8.3A" in text; LRS-200-24 is actually 8.8A |
| 4 | arm-actuation/electrical-integration.html | IMU described as "I2C chain" — should be "parallel dual-bus" (chain implies daisy-chain) |
| 7 | rotation/electrical-control.html | Power table shows "Total from PSU: 5V rail" — Arduino R4 WiFi is actually powered from 6V VIN via buck, not 5V |
| 11 | height-adjustment/electrical-control.html | Unclosed `</div>` — structural HTML nesting error |
| 16 | padding/electrical-integration.html | Strike event ROS topic name: 3 different names across 3 pages (`/strike_events`, `/robot/strike_detected`, `/strike_detected`) |
| 18 | arm-actuation/design-ideation.html | IK equations duplicated with inconsistent numbering (Eq.1–2 in design-ideation vs Eq.3–4 in mechanical-design) |

**Medium-severity open findings (sample):**
| # | File | Issue |
|---|---|---|
| 5 | arm-actuation/electrical-integration.html | "~10W average" arm power not source-verified (actual measured: ~10W — close but needs citation) |
| 8 | rotation/electrical-control.html | Section comment numbers out of order in DOM (§2, §4, §3) |
| 9 | rotation/electrical-control.html | `<ol>` list inside body prose "Design Rationale" section — lists prohibited in body prose |
| 13 | height-adjustment/electrical-control.html | Visible heading section numbers don't match comment markers (§2, §3, §4 mislabelled) |
| 17 | padding/electrical-integration.html | `<strong>InvenSense MPU6050</strong>` inside body `<p>` — bold prohibited in body text |

---

## 9. Key Engineering Decisions & Rationale

| Decision | Rationale |
|---|---|
| Parallel CAN bus (not daisy-chain) for arm motors | Simpler wiring; all motors share one bus pulled from Teensy transceiver. Requires only 2 termination resistors. |
| Arduino R4 WiFi for base rotation (separate from Teensy) | CAN baud mismatch (125 kbps vs 1 Mbps); WiFi eliminates cable twist through rotating base joint; independent failure domain |
| 12V PSU isolated from 24V motor bus | After OVP incident (2026-03-11) proved motor bus faults reset the Jetson and Teensy, complete galvanic isolation was implemented |
| Arms exempt from RegenClamp | Damiao internal PID controls decel ramp — back-EMF is gradual, within bus capacitor tolerance. Tested over 43 strike cycles with no OVP events |
| dI/dt detection vs static current threshold for impact | Static 1.33A limit tripped during legitimate acceleration (~8–10A momentarily). dI/dt (rate of current change) distinguishes acceleration from collision. Default sensitivity: 40 A/s with 0.6s grace period |
| Joint-space pitch clamping (not firmware endstops) | Firmware joint-space endstops caused "Jump-Back" defect. Python-side clamping converts motor targets to joint space before sending — no sudden counter-commands to uncommanded motors |
| PETG-CF rejected for gear components | Physical testing: short CF fibres act as stress concentrators (crack initiation) and inter-layer bonding barriers. Gear teeth deflect under load AND fracture without warning |
| PID tuning deferred for arm speed | Only one set of 4 Damiao motors — no spares. Aggressive PID tuning risks current spikes damaging 3D-printed gears or causing mechanical resonance. 0.64s strike cycle is acceptable for sparring. |
| Speed encoder excluded from height motor documentation | The CHP-36GP-555 has an AB phase Hall encoder, but it is not connected to any control system. It plays no role in the design. |

---

## 10. Startup Procedure (For Reference)

**Prerequisites:** ROS 2 Humble (Ubuntu/Jetson), micro-ROS agent, Python packages (`PyQt5 pyqtgraph numpy scipy pandas`), Teensy flashed with V4 firmware.

```bash
# Step 1: Start micro-ROS agent
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0
# Wait for "participant created" and "subscriber" confirmation

# Step 2: Kill any ghost GUI processes (prevents ROS ghost node boomerang effect)
killall -9 python3

# Step 3: Launch GUI V3
cd ~/boxing_robot/ros2_ws
python3 unified_GUI_V3.py
```

1. Header shows **CONNECTED** (green) within 1 second
2. Verify IMU Diagnostics tab shows live raw IMU values
3. Click **SYSTEM ENABLE** in header bar — motors hold current position
4. (Optional) Load strike library JSON → test individual strikes
5. (Optional) Enable sparring mode in Dynamic Sparring tab

**Shutdown:** Click **SAFE SHUTDOWN (HOME)** — arms return to [0,0,0,0] over 2 seconds. If micro-ROS agent killed, Teensy automatically SCB_AIRCR resets within 1.5 seconds.

---

## 11. Integration Log Summary (Key Dates)

The full integration log (`integration_log_copy.md` in this folder) is 3,035 lines covering 2026-03-11 through 2026-04-06. Find key events by searching these dates:

| Date Range | Major Events |
|---|---|
| 2026-03-11 | Initial firmware V3; 3:1 gear kinematics documented; sensorless homing attempt and failure; dynamic endstops "Jump-Back" defect; MDDS10 integration; pin transposition bugfix; PSU OVP incident; academic thesis R1–R3 |
| 2026-03-13 | 12V logic rail isolated to separate PSU; RegenClamp V0.3 specified |
| 2026-03-16 | 100Hz CAN feedback; speed multiplier raised to 10×; dI/dt impact detection |
| 2026-03-25 | Standalone IMU DAQ rig (500Hz); Peak Punch vector methodology; Quad-IMU scaling; merged into Firmware V4 + GUI V2; I2C bus hang fix; Nyquist blind-spot fix |
| 2026-03-27 | Dynamic Sparring FSM: vector alignment, perimeter transit routing, synced motor speeds, snap-back — all hardware-validated |
| 2026-03-29 | GUI V3 validated (8 tabs); unified strike library; ROS Control Tab; Jupyter launch notebook |
| 2026-03-31 | D2 architecture diagrams created (power + data split); 3D model explode viewer; report sync |
| 2026-04-01 | Base motor control folder (Z55BLD400 + ZBLD via CAN); AS5047P encoder (actual 26:1 ratio discovered); Digital Twin homing tab |
| 2026-04-02 | FK model validated on hardware; joint-space pitch clamping implemented; Strike Designer added |
| 2026-04-03 | GUI V4 (joint-space strike storage); 43-test speed baseline (all 6 strikes); base architecture decision (WiFi UDP); E-stop added; wire/connector spec; BLE base controller V2+PID |
| 2026-04-06 | CHP-36GP-555 height motor positively identified (replaced LGYMSZSS/MY1016Z); brake resistors sized (10Ω/5Ω); D2 diagrams restructured to 6 focused files; CAN topology corrected to parallel; PETG-CF rejected; content validation audit (22 findings) |

---

## 12. Prompt Template for Collecting Agent Summaries

> **For any agent that has worked on this boxing robot project:**
>
> 1. Consult `integration_log_copy.md` to identify your original role and the specific dates/tasks you contributed to.
> 2. Read `agent_knowledge/PROJECT_KNOWLEDGE_BRIEF.md` for the current project state.
> 3. Contribute your domain knowledge to this folder as a new file named `<your_role>_summary.md` (e.g. `mechanical_agent_summary.md`, `software_agent_summary.md`).
>
> **Critical writing rule — your summary must be fully self-contained.** A new agent reading your file will have no access to any other file in the repository. Do not write "see `motor_specifications.md` for details" or "refer to `data_architecture.md`". Instead, **copy or paraphrase the actual content inline**. Imagine the file is the only document the next agent will ever read about your domain.
>
> Structure your summary around these five sections:
>
> **1. Agent Role**
> State your agent role and the domain you are responsible for (e.g. Electrical & Systems Architect, Mechanical & Kinematics Engineer, Lead Systems Integrator, Academic Technical Writer).
>
> **2. Key Decisions Made — With Full Rationale**
> For every significant design decision in your domain, embed both the decision AND the reason. Do not just name the decision. Example format:
> - *Decision:* CAN bus uses parallel/star topology (not daisy-chain). *Reason:* Simpler wiring from the Teensy CAN transceiver; all motors share one wire run. Requires 120Ω termination at Teensy transceiver and at the furthest physical motor only.
>
> **3. Current State of Your Domain (embed actual specs/values)**
> Embed all critical specifications, parameters, and current values inline — motor specs, resistor values, PID gains, ROS topic names, GPIO pin assignments, DIP switch settings, anything relevant. Do not reference a file; write the values directly.
>
> **4. Open Action Items**
> List everything in your domain that is incomplete, pending procurement, or pending verification. State clearly what is blocked and what the next step is.
>
> **5. Known Inconsistencies or Warnings**
> List any known discrepancies between documents, unresolved cross-agent conflicts, or things that are easy to get wrong. State the correct value and the incorrect value that may appear in older files.
>
> **File naming:** Save as `agent_knowledge/<your_role>_summary.md`, e.g.:
> - `agent_knowledge/mechanical_agent_summary.md`
> - `agent_knowledge/software_agent_summary.md`
> - `agent_knowledge/academic_writer_summary.md`

> [!IMPORTANT]
> **Step 0 — Identify your original role from the integration log before writing anything.**
>
> Open `agent_knowledge/integration_log_copy.md` and search for your earliest log entries. Each entry ends with a line like `*Logged by Agent N: Role Name*`. Find the first entry you authored to confirm your agent number and role title. Use that role as your identity in Section 1 and as your filename (e.g. `mechanical_agent_summary.md`).
>
> Your summary must consolidate **everything you have done across all sessions and conversations**, not just the most recent one. Use the integration log as the authoritative chronological record — cross-reference it to ensure no decisions, bugfixes, or spec updates from earlier sessions are missing.

---

*This document is self-contained. All critical project knowledge is embedded above. See `integration_log_copy.md` for full chronological history.*
