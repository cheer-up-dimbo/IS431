# BoxBunny IS-431 — Mechanical & Kinematics Agent Summary

**Agent Role:** Agent 2 — Mechanical & Kinematics Engineer
**Domain:** Arm joint design, drivetrain kinematics, material selection, joint limits, calibration methodology
**Primary file maintained:** `Mechanical_arm/2DOF.md`
**Last updated:** 2026-04-07

---

## 1. Agent Role

Agent 2 is the Mechanical & Kinematics Engineer for the IS-431 BoxBunny boxing robot FYP (NUS CDE4301). This agent is responsible for:

- All arm joint mechanical design decisions and their rationale
- Kinematic derivations linking motor encoder space to physical joint space
- Material selection for 3D-printed drivetrain components
- Joint limit specification and calibration methodology
- Structural failure documentation and post-failure revision record

This agent does NOT own the height adjustment motor, base rotation motor, power architecture, software/firmware, or the web report pages. Those belong to Agent 1 (Electrical & Systems Architect), Agent 3 (Lead Systems Integrator & Software Developer), and Agent 4 (Academic Technical Writer) respectively.

---

## 2. Key Decisions Made — With Full Rationale

### Decision: 2-DOF Coaxial Differential Joint (not serial joint)
**Reason:** Consultations with padwork research identified that the two required striking degrees of freedom at the wrist are **pitch** (vertical tilt) and **roll** (axial rotation). A coaxial differential joint places both motors at the proximal pivot point of the arm (not at the distal end), centralising mass near the robot body. This reduces rotational inertia on the arm tube, allowing faster strikes without larger motors. A traditional serial arm would require motors cantilevered at the elbow, creating large dynamic moments that would require much higher torque and stiffer structure.

### Decision: Damiao DM-J4310-2EC motors selected (over ODrive + drone motor)
**Reason:** The initial test platform used an ODrive V3.6 controller with a 360KV drone motor and a hall-effect encoder. This produced three fatal issues: (1) substantial jitter from the hall-effect encoder's electrical noise, (2) absolute position loss on every power cycle (only one encoder — no multi-turn reference), and (3) the assembly was too bulky for the arm housing. The DM-J4310-2EC integrates motor, controller, CAN bus transceiver, and dual 14-bit absolute magnetic encoders into a single compact 56mm diameter unit. The dual encoders maintain absolute position across power cycles with no calibration sequence needed. Its native torque output is sufficient for a 3:1 external gear reduction (compact ratio), and it communicates via CAN bus at 1 Mbps in MIT Position-Velocity mode.

### Decision: 3:1 helical-spur external gear reduction (not higher)
**Reason:** The Damiao motor's native torque is sufficient for the boxing application at 3:1 — a higher ratio would increase torque beyond the 3D-printed gear's capability and would also reduce the output angular velocity below what is required for boxing tempo. A low reduction ratio also keeps the gear assembly compact. Helical gears (not straight-cut spur gears) were chosen because: (a) the angled tooth profile provides a contact ratio exceeding 1.5, meaning at least 1.5 tooth pairs share the load at any instant, distributing impulse loads from direction reversals across multiple teeth rather than concentrating stress on a single tooth pair; (b) this fatigue life improvement is critical because boxing strikes involve repeated rapid direction reversals.

### Decision: 2EC multi-turn mode MUST be enabled on Damiao motors
**Reason:** Both encoders in the DM-J4310-2EC are **single-turn absolute** (not incremental). Without 2EC multi-turn tracking, the motor's internal DSP position register is bounded to a single 360° range. The external 3:1 gear stage requires the motor output shaft to rotate 1080° (3 full turns) for the arm joint to traverse its full pitch range. Multi-turn mode enables the DSP to accumulate multi-revolution absolute position — without it, the motor cannot command positions beyond one revolution on its output shaft. This is a **critical configuration requirement** — the motors will appear to work initially but fail to reach full joint travel.

### Decision: Joint-space pitch clamping implemented in Python GUI (not firmware endstops)
**Reason:** The original approach implemented joint-space endstops in firmware (`apply_dynamic_endstops()` in Teensy). When the pitch limit was approached via a pure roll command, the differential coupling required the firmware to issue a sudden counter-command to the uncommanded pitch motor. This produced a visible "Jump-Back" defect: the arm bounced because the uncommanded motor was forced to accelerate instantaneously. The Python-side solution converts motor targets to joint space, clamps pitch to `[pitch_lower, pitch_upper]`, then converts back to motor positions via the full coupling-compensation inverse kinematics before sending the CAN command. No sudden counter-commands are ever issued to uncommanded motors.

### Decision: Manual operator calibration (replace automated sensorless homing)
**Reason:** Automated sensorless homing worked by driving Motor 1 (pitch) slowly against the physical hard stops and detecting stops via current spikes. This failed because: (1) the current spike from bumping the hard stop was indistinguishable from the Motor 2 resonance torque spike — causing premature termination at the wrong encoder position; (2) hard-stop positions were inconsistent across power cycles due to mechanical assembly variations; (3) holding Motor 2 stationary while Motor 1 drove into stops caused violent transient torque spikes on Motor 2. The GUI Calibration Tab (manual jog ±0.5 rad increments per motor with live current ammeters) is now the active boundary-discovery tool. The operator manually records safe raw encoder positions.

### Decision: Stainless D-shaft + Delrin pin + M2 screw hybrid interface (replacing monolithic PLA shafts)
**Reason:** During a project fair demonstration, PLA shafts fractured at the D-flat motor interface. The failure mode was shear along FDM layer lines (not tensile failure) — PLA has good tensile strength but poor inter-layer shear resistance under torsional loading. The solution assigns each material to the stress mode it resists best: (a) stainless steel 6mm D-shaft for torsional rigidity — the D-flat profile creates a positive mechanical interlock, eliminating relative rotation at the shaft-gear interface; (b) 2mm Delrin (POM) alignment pin for vibration damping — low friction coefficient (μ ≈ 0.2), high impact resilience, and viscoelastic damping absorbs impulse vibration rather than transmitting it into the PLA housing; (c) M2 steel screws for axial retention. PLA is retained for gear teeth and housings only where compressive and bending loads dominate.

### Decision: PLA for gear teeth, PETG for structural housing — PETG-CF and PLA-CF rejected
**Reason:** PLA has the highest stiffness of common FDM filaments (~3.5 GPa), which minimises gear tooth deflection under load and improves meshing precision. Brittleness is acceptable because the 3A current-limit watchdog in firmware stops the motor before gear tooth fracture force is reached. PETG (not PLA) is used for the structural housing because its higher ductility absorbs impact loads from strikes and its glass transition temperature (~75°C) is ~20°C higher than PLA (~55°C), important near motors under sustained operation. PETG-CF and PLA-CF were physically tested and **rejected**: short chopped carbon fibres (typically <200 μm) act as crack initiation sites under dynamic loading and reduce inter-layer bond strength, causing unexpected brittle fracture without warning. The marginal in-plane stiffness gain (~10–20% over base polymer) does not offset this.

---

## 3. Current State — Embedded Specifications

### 3.1 Arm Motors — 4× Damiao DM-J4310-2EC

| Parameter | Value |
|-----------|-------|
| Quantity | 4 (M1/M2 = left arm; M3/M4 = right arm) |
| Voltage | 24V DC |
| Rated torque | 3 N·m (output shaft) |
| Peak torque | 7 N·m |
| Rated current | 2.5A |
| Peak current | 7.5A |
| CAN protocol | MIT Position-Velocity mode, 1 Mbps |
| Encoder type | Dual 14-bit single-turn magnetic absolute (motor-side + output-side) |
| Multi-turn mode | 2EC mode **mandatory** — DSP accumulates multi-turn absolute position |
| Internal planetary gearbox | 10:1 (inside the motor unit) |
| External gear stage | 3:1 helical-spur (arm joint coaxial differential) |
| Total gear ratio | 30:1 (10:1 internal × 3:1 external) |
| Motor naming | M1 = left roll; M2 = left pitch; M3 = right roll; M4 = right pitch |
| Measured sparring current | <1A per motor (well below 3A firmware safety limit) |
| Measured peak power (all 4) | ~33W peak / ~10W average |
| RegenClamp | NOT required — internal PID manages decel ramp |

### 3.2 Joint Kinematics — Validated on Hardware 2026-04-02

**Naming convention:** `m_r` = roll motor encoder position, `m_p` = pitch motor encoder position, `o_r`/`o_p` = calibrated home offsets, `G` = 3 (external gear reduction), `s_r`/`s_p` = direction signs (±1), `c` = bevel coupling direction (±1).

**Forward Conversion (Motor → Joint):**
```
θ_roll  = s_r · (m_r − o_r) / G                                   (Eq. 1)
θ_pitch = s_p · [(m_p − o_p) + c · (m_r − o_r)] / G              (Eq. 2)
```

Eq. 2 expresses the differential coupling: pitch depends on the SUM of the pitch motor displacement and a coupling-weighted roll displacement. When both motors rotate same direction, the coupling term cancels bevel walking (pure roll condition).

**Inverse Conversion (Joint → Motor, used in firmware command path):**
```
Δ_r = (θ_roll / s_r) · G,   m_r = Δ_r + o_r                      (Eq. 3)
m_p = [(θ_pitch / s_p) · G − c · Δ_r] + o_p                      (Eq. 4)
```

Eq. 4 is the primary command equation. The subtraction of `c · Δ_r` is the software decoupling term that cancels the parasitic bevel-walking effect in real time.

**Forward Kinematics — Physical Arm End-Point Direction Vector:**
```
d_x = s_x · cos(θ_pitch)
d_y = sin(θ_pitch) · cos(θ_roll)
d_z = sin(θ_pitch) · sin(θ_roll)
```
Where `s_x = −1` (left arm) or `+1` (right arm). The Z-component `sin(p)·sin(r)` correctly models that both CW and CCW roll causes the arm to tilt upward (bevel walking reverses direction with roll direction).

**Old incorrect model (DO NOT USE):** treated roll as a global Z-tilt, independent of pitch swing plane. This is wrong — rolling rotates the pitch swing plane.

### 3.3 Calibrated Arm Parameters (Validated 2026-04-02)

| Parameter | Left Arm (M1/M2) | Right Arm (M3/M4) |
|-----------|------------------|-------------------|
| pitch_sign (s_p) | **−1** | **+1** |
| roll_sign (s_r) | **+1** | **−1** |
| coupling (c) | **−1** | **−1** |

Both arms share c = −1 (same bevel gear arrangement). Signs are mirrored (symmetric geometry). These values were validated by a 4-test calibration probe procedure.

### 3.4 Joint Limits

| Axis | Physical Hard Stop | Recommended Software Zone | Notes |
|------|-------------------|--------------------------|-------|
| Pitch | ±1.57 rad (±90°) | ±1.0 rad | 3D-printed features on inner shaft housing; 0.57 rad clearance buffer per side |
| Roll | **None** (free-spinning outer housing) | Cable-wrap dependent (~±2–3 full turns) | Operator must define software guard based on specific build wiring routing |

**Critical:** Roll has no structural mechanical hard stop. It is physically limited only by cable wrap. The operator must inspect wiring routing on their specific build and define a software guard accordingly.

### 3.5 Arm Physical Dimensions

- Total arm reach from pivot: **0.80 m** (arm tube + pool noodle padding)
- Shoulder pivot offset from body centre: **±0.2414 m** (symmetric)
- Motor housing diameter (Damiao): Ø56 mm × 46 mm depth
- Central shaft: 6 mm stainless steel D-shaft
- Alignment pin: 2 mm Delrin (POM)
- Securing screws: M2 steel

### 3.6 Strike Performance (43-Test Baseline, 2026-04-03)

| Strike | Arm | Windup→Apex (s) | Total Cycle (s) | Peak Motor RPM |
|--------|-----|-----------------|-----------------|----------------|
| Jab | Left | 0.66 | 1.24 | 239 |
| Left Hook | Left | 0.67 | 1.25 | 300 |
| Left Uppercut | Left | 0.55 | 1.09 | 218 |
| Cross | Right | 0.61 | 1.18 | 285 |
| Right Hook | Right | 0.62 | 1.20 | 207 |
| Right Uppercut | Right | 0.57 | 1.07 | 238 |

All strikes measured at 25 rad/s speed setting. Peak current <0.7A per motor on all strikes (well within 3A limit). End-to-end strike time ~0.64s (requirement was ≤0.25s — **not met**; root cause is PID accel/decel overhead of ~0.45s constant regardless of speed). This is deferred — no spare motors to safely tune higher Kp without risk of gear damage.

---

## 4. Open Action Items

| Item | Status | Next Step |
|------|--------|-----------|
| Strike speed requirement ≤0.25s end-to-end | ❌ NOT MET (currently ~0.64s) | Requires Damiao PID tuning (higher Kp) or MIT torque-direct mode. Deferred — no spare motors. Do not attempt without spare set. |
| Arm pitch clamping limits (`pitch_lower`, `pitch_upper`) | ⏳ Per-build calibration required | Each physical build requires the operator to run the 4-test calibration probe (`motor_probe.py`) to determine `s_p`, `s_r`, `c`. These are NOT fixed across builds — depends on which way bevel gear is assembled. |
| Roll cable-wrap software guard | ⏳ Per-build | Operator must physically check wiring routing and define max roll turns before cable strain. Document as build-specific commissioning step. |
| PLA gear thermal monitoring | ⏳ Monitoring | PLA glass transition is ~55–60°C. If motor casing temperature approaches 40°C near printed gears during sustained high-duty-cycle operation, evaluate PETG substitution for gear teeth. |
| PETG housing upgrade | ⚠️ Partial | Housing walls were thickened post-fair (V5 revision). Not all housing sections confirmed PETG — some still PLA. Recommend full audit before sustained operation above 100 strikes/session. |

---

## 5. Known Inconsistencies or Warnings

### W1 — Old kinematics still in some files (DO NOT USE)
Earlier versions of `2DOF.md` and log entries used a simplified kinematic model where roll was treated as a global Z-tilt independent of pitch swing plane. This is **incorrect**. The correct model (Eq. 1–4 above, plus the forward kinematics d_x/d_y/d_z equations) was validated on hardware 2026-04-02 and captures the bevel coupling correctly. Any code or document referencing the old model must be updated.

Earlier incorrect equations (before 2026-04-02):
```
θ_m2_target = 3 · θ_roll_desired          ← WRONG, ignores coupling
θ_m1_target = 3 · (θ_pitch_desired + θ_roll_desired)   ← partially correct
```
These formulae do not apply to the final calibrated sign-parameter model.

### W2 — Sensorless homing is DEPRECATED (do not re-implement)
Integration log entries prior to 2026-03-11 describe an automated sensorless homing sequence (drive Motor 1 against hard stops, detect by current spike, compute midpoint). This was tested and **failed** due to false spike termination. Section 8 of `2DOF.md` documents it as a superseded design iteration. Do not re-implement. The active calibration method is manual jogging via the GUI Calibration Tab.

### W3 — Firmware joint-space endstops are REMOVED (do not re-add)
`apply_dynamic_endstops()` in Teensy firmware was removed because it caused the "Jump-Back" defect. The firmware now only has a global ±50 rad failsafe. Joint-space pitch clamping lives in `homing_tab.py` (Python GUI). Do not add joint-space clamping back to Teensy without understanding why it was removed.

### W4 — External gear reduction is 3:1 (G=3), internal is 10:1
When reading kinematics equations, G = 3 refers to the external helical-spur gear stage only. The motor's internal 10:1 planetary gearbox is invisible to the encoder (the encoder reads after the 10:1, before the external 3:1). The total drive ratio per arm joint is 30:1 (10:1 × 3:1).

### W5 — Do NOT confuse arm encoder model with base motor encoder
The DM-J4310-2EC arm motors use dual single-turn absolute encoders with 2EC DSP multi-turn accumulation. The Z55BLD400 base motor uses a separate external AS5047P 14-bit encoder on the motor input shaft. These are completely different encoder architectures and must not be confused in documentation.

### W6 — Motor naming M1/M2 = left arm ROLL/PITCH (not M1=pitch)
M1 and M3 are the **roll motors** (outer housing rotation). M2 and M4 are the **pitch motors** (inner shaft via bevel gear). Some older log entries inconsistently refer to "Motor 1 (Pitch)" because early in the project the assignment was opposite. The validated assignment confirmed by calibration 2026-04-02 is: **M1/M3 = roll, M2/M4 = pitch**.

### W7 — PETG-CF must NOT be used for gear components
PETG-CF was physically tested and rejected. Short chopped carbon fibres act as stress concentrators and crack initiation sites under dynamic loading. They also reduce inter-layer bond strength. Some supplier marketing claims significantly overstate the stiffness benefit for FDM-grade CF filament. If a new agent or operator suggests PETG-CF for gears, reject this — the physical test evidence is documented in `2DOF.md` §5 and `arm-actuation/mechanical-design.html`.
