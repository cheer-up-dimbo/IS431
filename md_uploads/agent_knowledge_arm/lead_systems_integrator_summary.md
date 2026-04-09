# Lead Systems Integrator & Software Developer — Domain Summary

**Agent Role:** Lead Systems Integrator & Software Developer (also contributed Electrical & Systems Architecture validation)
**First Confirmed Contributions:** 2026-03-11 (firmware integration, GUI-Teensy wiring), 2026-03-25 (Firmware V4 + GUI V2 merge), 2026-04-05 (PID base controller), 2026-04-06 (IMU ±16g firmware fix, validation audit)
**Summary Compiled:** 2026-04-07

> **Self-contained by design.** All values, specs, and rationale are embedded inline.
> A new agent reading this file needs no other document to understand the systems integration domain.

---

## 1. Agent Role

**Primary:** Lead Systems Integrator & Software Developer — responsible for the full firmware-GUI integration stack: evolving the Teensy firmware across versions, rewriting the GUI from Tkinter to PyQt5 across four major versions, diagnosing and fixing all cross-layer communication bugs between the Teensy and Jetson, and integrating the standalone IMU rig into the main control system.

**Secondary (this conversation):** Electrical & Systems Architecture validation — confirming electrical specs (CAN IDs, IMU polling rate, PSU current, topic names) against firmware source, fixing the IMU accelerometer range firmware bug, debugging the base rotation PID controller, and auditing the IS-431 HTML documentation against source truth.

---

## 2. Key Decisions Made — With Full Rationale

### Decision: Sparse Edge-Trigger CAN Command Strategy
**Reason:** Damiao DM-J4310-2EC motors in MIT Position-Speed mode run an internal trapezoidal trajectory planner. Continuous 50Hz CAN commands reset this planner every 20ms, preventing smooth trajectory computation and causing violent stuttering. Fix: only re-transmit a CAN frame if the target position changed by >0.01 rad, OR every 100ms as a keep-alive heartbeat. This reduced bus utilisation from ~80% to ~15% during normal sparring and eliminated stuttering without losing telemetry continuity.

### Decision: 100Hz GUI Heartbeat, 200Hz Firmware Unified Loop
**Reason:** Early firmware ran at 50Hz (20ms). Upgraded to 100Hz (10ms) for smoother trajectories, then the IMU integration required a 200Hz (5ms) loop to poll all 4 MPU6050 sensors within the same tick as CAN motor control. The GUI heartbeat (`time.sleep(0.01)` = 100Hz) publishes motor commands at 100Hz via micro-ROS — fast enough to not starve the 200Hz firmware loop.

### Decision: GUI Rewrite from Tkinter to PyQt5/PyQtGraph (V1 → V2)
**Reason:** Tkinter lacked a non-blocking event loop compatible with ROS 2 threading. PyQt5 provides a proper signal/slot architecture that allows `QTimer`-driven ROS spinning, background threads for motor sequences, and `pyqtSignal(str)` for thread-safe GUI updates. PyQtGraph provides GPU-accelerated real-time plotting for 200Hz IMU data streams.

### Decision: IMU Integrated into Teensy Firmware (Not Standalone Node)
**Reason:** Initially, the IMU subsystem was a completely separate standalone Teensy + Python dashboard (`teensy_imu_daq.ino` + `dsp_analytics_dashboard.py`) running at 500Hz independently. On 2026-03-25, it was merged into the main `teensy_firmware_V4.ino` at 200Hz, sharing the same micro-ROS payload. This eliminated a separate USB serial connection, a separate Python process, and all synchronisation issues between IMU timestamps and motor encoder timestamps. The combined 21-double feedback payload packs everything into one atomic ROS message.

### Decision: SCB_AIRCR Hardware Silicon Reset on micro-ROS Disconnect
**Reason:** On WSL/Ubuntu, when the micro-ROS agent process is killed (Ctrl+C), the USB DTR/RTS signals are not properly torn down, leaving the Teensy permanently hung in `AGENT_CONNECTED` state. Graceful entity destruction works on native Jetson Ubuntu but not reliably on WSL. Rather than write OS-specific teardown logic, a 1Hz active ping (`rmw_uros_ping_agent(10, 1)`) with 3-failure threshold (1.5s total) triggers `SCB_AIRCR = 0x05FA0004` — an ARM Cortex-M7 hardware silicon reset. This guarantees a pristine memory pool and clean handshake on agent restart, regardless of host OS.

### Decision: Hard STOP (not Repeated Start) for I2C IMU Reads
**Reason:** The 30–40cm cable runs from the Teensy to the foam padding chassis create significant parasitic capacitance on the I2C lines. At 400kHz with Repeated Start (`endTransmission(false)`), the MPU6050 logic gates choke during the turnaround, causing `requestFrom()` to timeout and IMUs 1 and 2 to broadcast `-1` (0xFFFF). Fix: use `endTransmission(true)` (Hard STOP) before every `requestFrom()` call. This fully resets the I2C state machine before each read, eliminating dropouts entirely.

### Decision: np.max(buffer[-n_scan]) for Strike Detection (Nyquist Fix)
**Reason:** The firmware streams IMU data at 200Hz (5ms) but the GUI refreshes at 20Hz (50ms). The original strike check used `check_val = mag_arr[-1]` — only the single most recent sample aligned with the current GUI frame. Any punch that peaked and decayed within the 50ms GUI tick was invisible — a classic Nyquist aliasing blind spot. Fix: `np.max(buffer[-n_scan:])` searches all samples accumulated since the previous GUI tick. If ANY 5ms sample in the preceding 50ms exceeds the threshold, the strike is registered.

### Decision: Joint-Space Pitch Clamping in GUI (Not Firmware Endstops)
**Reason:** Earlier firmware implemented `apply_dynamic_endstops()` in C++ — when a joint limit was approached, it issued sudden counter-commands to the *uncommmanded* motor to enforce the coupled pitch/roll safe zone. This caused the "Jump-Back" defect: instantaneous counter-torque on a free motor, tripping the dI/dt detector as a false impact and triggering auto-retract. Fix implemented in GUI V4: target positions are converted to joint space in Python, pitch is clamped to `[pitch_lower, pitch_upper]`, then converted back with coupling compensation before any CAN command is sent. No sudden uncommanded motor movements, no jump-back.

### Decision: Dynamic Sparring FSM in Python (Not Embedded in Firmware)
**Reason:** The robot's combat decision logic (which strike to execute, transit routing between strikes, snap-back recovery) is too complex and iterative to embed in Teensy firmware. All FSM intelligence lives in `DynamicSparringTab` (GUI V3) on the Jetson. The Teensy remains a lean 200Hz motor controller and IMU publisher — the Python layer handles all sequencing, arrival checking, vector alignment, and transit waypoint insertion.

### Decision: PID Base Controller Direction Hardcoded in CAN Mapping (dirFlipped Removed)
**Reason:** Earlier base controller firmware used a `dirFlipped` boolean that could be toggled via a `FLIP` command. When the flag state was unknown at startup, positive PID outputs sometimes drove the motor the wrong way, creating positive feedback runaway. Fix: `dirFlipped` removed entirely. Direction is now deterministic: positive PID output → `dir=2` → CAN register `0x0001` → encoder-positive → physical RIGHT; negative → `dir=1` → `0x0002` → LEFT. No runtime state to lose track of.

### Decision: Direction-Aware Hard Limits for Base Rotation (±90°)
**Reason:** Original hard limit implementation blocked ALL motion when the encoder reached ±90°. If the motor overshot slightly, it was impossible to command it back — it was trapped at the boundary. Fix: limits are direction-aware. At +90°: only positive-direction commands are blocked; negative (return-to-centre) commands are always allowed. At -90°: only negative commands are blocked; positive always allowed. This ensures the system can always recover from a boundary condition.

### Decision: IMU Set to ±16g (ACCEL_CONFIG = 0x18, divisor 2048 LSB/g)
**Reason:** Empirical readings exceeded 19.62 m/s² (the ±2g saturation ceiling of 2g×9.81), confirming the sensor was NOT operating at ±2g despite the firmware writing `0x00` to ACCEL_CONFIG. Root cause: the register write was likely racing the MPU6050's internal power-on reset. The sensor was running at ±16g hardware default. The old conversion divisor of 16384 (only valid for ±2g) underscaled all readings by 8×. Fix: explicitly write `0x18` to force ±16g, change divisor to 2048. Max measurable: ±157 m/s² — more than sufficient for boxing training.

---

## 3. Current State: Firmware & GUI Integration

### 3.1 Software Version Registry (Active as of 2026-04-07)

| Component | File | Status |
|---|---|---|
| Teensy Firmware | `teensy_firmware_V4/teensy_firmware_V4.ino` | ✅ Validated. IMU ±16g fix applied 2026-04-06. **Needs reflash.** |
| GUI (Production) | `ros2_ws/unified_GUI_V3.py` | ✅ Validated. 2278 lines, 8 tabs, PyQt5/PyQtGraph |
| GUI (Modular V4) | `ros2_ws/unified_v4/unified_GUI_V4.py` + tab modules | In development — joint-space strike storage |
| Base Controller | `base_motor_control/ble_control/ble_control.ino` | ✅ Validated. PID bugs fixed 2026-04-05 |
| BLE Web UI | `base_motor_control/ble_control/controller.html` | ✅ Functional |
| Test Validation GUI | `testing/test_validation_GUI.py` | ~1346 lines, standalone |
| **Deprecated (do not modify):** | `unified_GUI.py` (Tkinter V1), `unified_GUI_V2.py` (PyQt5 V2) | Archived |

### 3.2 GUI Evolution History

**V1 — Tkinter (`unified_GUI.py`):**
- Original implementation. 5 tabs: Manual, Calibration, Action Board, Analytics, Height.
- Blocking Tkinter event loop not compatible with ROS 2 threading.
- Impact detection: static 1.33A threshold (later replaced by dI/dt).

**V2 — PyQt5/PyQtGraph (`unified_GUI_V2.py`):** `2026-03-25`
- Complete rewrite from Tkinter to PyQt5. All V1 tabs retained with full feature parity.
- **New Tab 6:** IMU Diagnostics — live accel plots, Butterworth LPF, auto-FFT, strike pad detection, publishes to `/robot/strike_detected`.
- Key integration fix (V2.1, 2026-03-26): Nyquist blind-spot — replaced `arr[-1]` with `np.max(buffer[-n_scan:])`.
- V2.2 additions: JSON extension fix, QDoubleSpinBox precision joysticks, power budget telemetry (`np.trapz` energy calculation).

**V3 — Production FSM (`unified_GUI_V3.py`):** `2026-03-29`
- 8-tab layout. Dynamic Sparring FSM fully ported from `dynamic_fsm_test.py`.
- Added `set_target_arm(speed2=...)` for independent per-motor speed control.
- **New Tab 3:** Strike Library — 2-point (Windup+Apex) teaching, Teach Pendant from live encoders, unified Load/Save JSON for both arms.
- **New Tab 7:** Dynamic Sparring — vector alignment skip, M1-based perimeter transit routing, synced per-motor speeds, proportional snap-back recovery, IMU-triggered auto-sparring, idle auto-return.
- **New Tab 8:** ROS Control — 6 strike slots, dynamic speed adaptation (`required_speed = distance / (duration - 0.3s)`), slot assignment via `/robot/punch_slots`.
- Thread-safe FSM logging via `pyqtSignal(str)`.

**V4 — Modular (`ros2_ws/unified_v4/`):** `In development`
- Strike library converted to joint-space storage (`"space": "joint"` field). Strikes survive motor recalibration.
- Separated into individual tab modules (`strike_library_tab.py`, `homing_tab.py`, etc.).
- Forward kinematics validated on hardware 2026-04-02. Joint-space pitch clamping implemented.

### 3.3 Teensy Firmware V4 — Unified 200Hz Loop

File: `teensy_firmware_V4/teensy_firmware_V4.ino`
Loop period: 5ms (`millis() - last_ctrl >= 5`)

**Per-cycle execution order:**
1. Read CAN feedback from all 4 arm motors
2. 200Hz current watchdog: if any motor exceeds 3.0A → `motors_enabled = false`, freeze targets
3. CAN command transmission (sparse edge-trigger: >0.01 rad change OR 100ms keep-alive)
4. Poll all 4 MPU6050 IMUs via dual I2C bus (Wire + Wire1, 400kHz, Hard STOP protocol)
5. Publish 21-double `/motor_feedback` payload via micro-ROS USB

**21-double feedback payload layout:**
```
[0..3]   Motor positions (rad)           — 4× Damiao
[4..7]   Motor currents (A)              — 12-bit MIT torque field, correctly extracted
[8]      CAN RX frame count              — diagnostic counter
[9..11]  IMU 0 accel XYZ (m/s²)         — Wire/0x68 = Centre Body
[12..14] IMU 1 accel XYZ (m/s²)         — Wire/0x69 = Left Body
[15..17] IMU 2 accel XYZ (m/s²)         — Wire1/0x68 = Right Body
[18..20] IMU 3 accel XYZ (m/s²)         — Wire1/0x69 = Reserved
```

**ROS 2 subscriptions:**
- `/motor_commands` (Float64MultiArray): [pos×4, speed×4, enable_flag]
- `/robot/height_cmd` (String): `UP:pwm`, `DOWN:pwm`, `STOP`, `REVERSE:0/1`

**IMU configuration:**
- ACCEL_CONFIG = `0x18` → ±16g (updated 2026-04-06)
- Conversion: `raw_int16 / 2048.0f * 9.81f` → m/s²
- Max: ±157 m/s² before saturation
- Gravity calibration: 500 samples on startup → static offset subtracted from all readings

**Disconnect watchdog:** `rmw_uros_ping_agent(10, 1)` fails 3× in a row → `SCB_AIRCR = 0x05FA0004` (ARM Cortex-M7 hard reset)

### 3.4 ROS 2 Topic Interface

**Subscribers (Jetson → Teensy/robot):**

| Topic | Type | Payload |
|---|---|---|
| `/motor_commands` | Float64MultiArray | [pos×4, speed×4, enable_flag] |
| `/robot/height_cmd` | String | `UP:pwm`, `DOWN:pwm`, `STOP`, `REVERSE:0/1` |
| `/robot/strike_command` | String (JSON) | `{slot, duration, speed}` |
| `/robot/punch_slots` | String (JSON) | `{1: {arm, strike}, ...}` |
| `/robot/system_enable` | String | `"enable"` / `"disable"` |

**Publishers (Teensy/GUI → Jetson/external):**

| Topic | Type | Payload |
|---|---|---|
| `/motor_feedback` | Float64MultiArray | 21 doubles |
| `/robot/strike_detected` | String (JSON) | `{pad_index, pad_name, peak_accel, calibrated_peak, relative_power}` |
| `/robot/strike_feedback` | String (JSON) | `{slot, strike, status, duration_allowed, duration_actual}` |

### 3.5 Dynamic Sparring FSM (Validated on Hardware 2026-03-27)

```
Strike triggered by IMU or operator
│
├── Compute θ = arccos(V_strike · V_approach / |V_strike||V_approach|)
│     V_strike = apex - windup     (intended direction = strike identity)
│     V_approach = apex - current  (actual path if windup skipped)
│
├── θ < threshold (default 30°)?
│     YES → Skip Windup: command Apex directly (fluid blend)
│
└── θ ≥ threshold?
      YES → Windup required:
            - Find all library windups with M1 between M1_start and M1_target
            - Sort by M1 in direction of travel (perimeter orbit = no center crossover)
            - Execute via-points → target Windup → Apex
      
All moves use synced per-motor speeds:
  spd_M1 = base_speed × (ΔM1 / max(ΔM1, ΔM2))  → straight-line trajectory
  spd_M2 = base_speed × (ΔM2 / max(ΔM1, ΔM2))

Snap-back: recovery = apex - snap_factor × (apex - windup)
```

### 3.6 Base Rotation PID Controller

File: `base_motor_control/ble_control/ble_control.ino`
Controller: Arduino Uno R4 WiFi → CAN 125kbps → ZBLD C20-800LRC → Z55BLD400 BLDC

| Parameter | Value |
|---|---|
| Loop rate | 50 Hz |
| Kp | 25.0 |
| Ki | 1.0 |
| Kd | 1.0 |
| Dead zone | ±1° |
| Default peak RPM cap | 1000 RPM (adjustable via `PEAK:rpm`) |

**Command protocol:**
- `L:deg` — relative left rotation
- `R:deg` — relative right rotation
- `GO:deg` — absolute angle target (signed degrees)
- `PEAK:rpm` — set RPM ceiling for PID output saturation
- `PID:Kp,Ki,Kd` — real-time gain tuning

**Direction mapping (hardcoded, dirFlipped removed):**
- Positive PID output → `dir=2` → CAN `0x0001` → encoder-positive → **Right**
- Negative PID output → `dir=1` → CAN `0x0002` → encoder-negative → **Left**

**Limits:** ±90° hard stops, direction-aware (only blocks further motion toward limit; return-to-centre always permitted)

**AS5047P encoder:** Software SPI on Pins 4–7 (CSn=4, CLK=5, MOSI=6, MISO=7) — avoids hardware SPI conflict with CAN RX on Pin 13.

---

## 4. Open Action Items

### 4.1 Firmware — Reflash Required
- `teensy_firmware_V4.ino` updated 2026-04-06 (IMU ±16g). **Must reflash to Teensy.**
- After reflash: re-run IMU gravity calibration in GUI (Calibration tab → Re-calibrate IMU).
- All strike detection thresholds need recalibration — physical values will read 8× higher than before. Any threshold set before 2026-04-06 reflash is invalid.

### 4.2 GUI V4 — Joint-Space Integration Incomplete
- `unified_v4/` tab modules are in development. Strike library uses joint-space storage but the GUI is not yet the production default.
- Validated FK model (2026-04-02): joint-space pitch clamping works. The production workflow still uses V3.

### 4.3 Hardware — Brake Resistors to Procure
- Height motor: 10Ω 50W aluminium wirewound → RegenClamp V0.3 → MDDS10
- Base motor: 5Ω 100W aluminium wirewound → RegenClamp V0.3 → ZBLD (RegenClamp itself also pending install)
- Software PWM ramp-down (6 steps / 300ms) on height motor is the active mitigation but does not eliminate OVP risk at high speeds.

### 4.4 Documentation HTML — Open Findings (from validation audit)
Key confirmed errors requiring HTML fixes:
- `padding/electrical-integration.html`: strike topic `/strike_events` → **`/robot/strike_detected`**
- `arm-actuation/electrical-integration.html`: command mode "position-velocity" → **"Position-Speed mode"**
- `rotation/electrical-control.html`: stale acceleration ramp alert (PID replaced it 2026-04-05)
- `rotation/electrical-control.html`: `<ol>` list in body prose → convert to prose paragraphs
- `height-adjustment/electrical-control.html`: `<div>` nesting error breaks layout
- `motor_specifications.md §9`: "500 Hz" IMU rate → **"200 Hz"**
- Full 33-finding tracker: `documents/validation_report_2.md`

---

## 5. Known Inconsistencies or Warnings

### IMU Polling Rate: 200Hz (NOT 500Hz)
- **Correct:** 200Hz — Teensy 5ms loop confirmed in `teensy_firmware_V4.ino` and `IMU_FS = 200.0` in GUI
- **Wrong:** `motor_specifications.md §9` says "500 Hz" — this was from the standalone DSP test rig (Agent 5), which ran at 500Hz independently. That rig was deprecated on merge.
- **Risk:** Designing filter window sizes or buffer lengths on 500Hz will be off by 2.5×.

### IMU Accelerometer Scale Factor: 2048 LSB/g (NOT 16384)
- **Correct (post 2026-04-06):** ACCEL_CONFIG = `0x18`, divisor = `2048.0`
- **Wrong (pre-fix):** ACCEL_CONFIG = `0x00` (intent ±2g, failed to set), divisor = `16384.0`
- **Risk:** Any strike threshold calibrated before the reflash is 8× too small. Old CSV data (from `base_chart_data.csv` session logs) reflects underscaled values.

### Strike ROS Topic — Three Conflicting Names
- **Correct:** `/robot/strike_detected` (confirmed from `unified_GUI_V4.py` line 100)
- **Wrong variant 1:** `/strike_events` (padding HTML page)
- **Wrong variant 2:** `/strike_detected` (motor_specifications.md §8, no `/robot/` prefix)
- **Risk:** External system subscribing to wrong topic never receives strike events.

### CAN Command Frame ID vs Motor Base ID
- **Motor base IDs (configuration / feedback):** 0x01, 0x02, 0x03, 0x04
- **CAN command frame IDs (TX):** 0x101, 0x102, 0x103, 0x104 (= 0x100 + base ID)
- **Wrong (HTML report column header):** "CAN Frame ID" column shows base IDs (0x01–0x04) — misleadingly labeled
- **Risk:** Writing firmware using HTML report values as TX IDs will send to wrong CAN addresses → motors unresponsive.

### Ghost Node / Boomerang Effect — Always Kill Before Relaunch
- **Symptom:** Motors oscillate between two positions. Old GUI instance still running publishes `[0,0,0,0]` at 100Hz while new GUI publishes actual targets. Teensy receives both, motors bounce.
- **Fix:** Always run `killall -9 python3` on the Ubuntu/Jetson terminal before launching a new GUI instance.

### 12-Bit Torque Parsing — Do Not Read as 16-bit Float
- **Correct:** Damiao CAN feedback torque is packed as a **12-bit integer** in the MIT protocol.
- **Wrong (early firmware):** Parsed as 16-bit, consuming the adjacent temperature byte → phantom 8–9A idle current readings.
- **Risk:** Any new firmware reading the feedback frame must extract the torque from bits [39:28] of the CAN payload, not as a full 16-bit word.

### MDDS10 Pin Assignment — Corrected, No Rewiring Needed
- **Correct:** Teensy Pin 3 = AN1 (speed/PWM), Teensy Pin 2 = DIG1 (direction)
- **Wrong (early docs and firmware):** Labels were swapped — Pin 2 was written as speed, Pin 3 as direction
- **Symptom:** Motor ran at full speed always; PWM slider had no effect; STOP command had no effect
- **Note:** Physical wires were correct all along; only the firmware `#define` was wrong. Corrected 2026-03-11. No rewiring required.

### Height Motor Name — CHP-36GP-555 Only
- **Correct:** CHP-36GP-555 (confirmed from physical motor label 2026-04-06)
- **Wrong:** "LGYMSZSS", "MY1016Z" — appear throughout integration log entries before 2026-04-06
- **Risk:** Searching for datasheets or specs under wrong names returns nothing or wrong motor specs.

### dirFlipped Flag — Removed from Base Controller
- **Correct (current firmware):** `dirFlipped` and the `FLIP` command do not exist. Direction is hardcoded in CAN register mapping.
- **Wrong (older firmware revisions):** `dirFlipped` boolean toggled at runtime, unknown state at startup.
- **Risk:** Any documentation or agent referencing `FLIP` command is describing deprecated behaviour.

---

*This document covers all contributions from 2026-03-11 through 2026-04-07.*
*Authoritative chronological record: `agent_knowledge/integration_log_copy.md` (search Agent 1, Agent 3, Lead Integration Engineer entries).*
