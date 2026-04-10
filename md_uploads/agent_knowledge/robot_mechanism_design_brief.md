# BoxBunny IS-431 — Robot Mechanism Design Brief
*For agent handoff. Last updated: 2026-04-10.*

---

## 1. Project Context

BoxBunny is a boxing training robot with five mechanical subsystems: **Base, Rotation, Height Adjustment, Padding, Arm Actuation**. Documentation lives in `pages/robot-mechanism/` with one hub HTML per subsystem and sub-pages for Design Ideation, Mechanical Design, Electrical Integration, and Testing & Evaluation.

The report follows the **Systems Engineering V-Model** (Section 3.2): requirements fixed first, decomposed into subsystem criteria, then verified on the right side of the V.

---

## 2. System-Level Requirements (RM baseline)

| ID | Subsystem | Requirement | Status |
|----|-----------|-------------|--------|
| RM-1 | Base | Remain upright under worst-credible punching loads, FoS ≥ 1.5 | Passed |
| RM-2 | Base | Compact footprint — no intrusion into boxer's footwork zone | Passed |
| RM-3 | Base | Portable: transportable by 1 person between venues | Passed |
| RM-4 | Rotation | Yaw re-orientation at ≥ 150°/s | Pending |
| RM-5 | Height Adjustment | ≥ 400 mm vertical stroke; full stroke ≤ 32 s | Pending |
| RM-6 | Padding | Absorb repeated strikes without damage; impact detection across 3 zones (Head, Celiac Plexus, Liver) | Pending |
| RM-7 | Arm Actuation | Deliver 3 distinct strike types: Jab (pitch), Hook (roll), Uppercut (pitch + roll) | Pending |
| RM-8 | Arm Actuation | Execute a 90° arm sweep in ≤ 0.70 s | **Partial** — Damiao PID ramps add ~0.4–0.5 s overhead per strike |

> **Critical:** RM-3 = Portability (Base). RM-5 = Vertical stroke (Height Adj.). These are frequently confused. RM-7 and RM-8 are both Arm Actuation, not the same requirement.

---

## 3. Subsystem Acceptance Criteria

These are **design-decision-driven** criteria layered on top of the RM requirements — they cover failure modes the RM codes do not explicitly address.

### Base
| ID | Criterion | Verification |
|----|-----------|-------------|
| BAS-AC-1 | Modular mounted plate flat and rigid; passes flatness + fastener torque inspection | Visual + physical inspection |

### Rotation
| ID | Criterion | Verification |
|----|-----------|-------------|
| ROT-AC-1 | Zero tooth-skip under shock load/reversal; stable belt tension and cam-follower contact | Rapid accel/reversal test + off-axis punch loading |
| ROT-AC-2 | Command frame loss rate < 1% over 1,000 UDP frames via WiFi | 1,000-frame packet-loss test at 20 Hz |

### Height Adjustment
| ID | Criterion | Verification |
|----|-----------|-------------|
| HA-AC-1 | Full 400 mm stroke in ≤ 32 s under 22.5 kg load for 5 consecutive cycles | Timed full-stroke test under load |
| HA-AC-2 | Delrin pad wear < 1 mm after 200 cycles; backlash < 2 mm lateral play at top of stroke | 200-cycle endurance test; micrometer + backlash check |

### Padding
| ID | Criterion | Verification |
|----|-----------|-------------|
| PAD-AC-1 | IMU strike detection rate ≥ 95% true positive (60-punch controlled test, 20/zone) | 20 punches × 3 zones |
| PAD-AC-2 | IMU L2 norm force differentiation monotonic: light < medium < heavy (ANOVA p < 0.05) | 3 users × 30 punches; one-way ANOVA |

### Arm Actuation
| ID | Criterion | Verification |
|----|-----------|-------------|
| ARM-AC-1 | 90° sweep in ≤ 0.70 s (N=43 benchmark) | Speed timing test — **Partial** |
| ARM-AC-2 | All 6 strike variants delivered in sustained sparring | Strike demonstration session — Pending |
| ARM-AC-3 | Peak phase current ≤ rated threshold (0.69 A peak measured, N=43) | Current logging — **Passed** |
| ARM-AC-4 | Motor temperature < Tg 55°C sustained | Thermal monitoring — Pending |
| ARM-AC-5 | No kinematic decoupling failure in 200 Hz CAN loop | Firmware verification — Passed |

> **Namespace:** Arm actuation uses `ARM-AC-X`. Stale code `ARM-PC-X` is deprecated — do not use.

---

## 4. Key Design Decisions Per Subsystem

### 4.1 Base (5.2.1)
- Trapezoidal plan geometry: narrower front, wider rear — resolves RM-1 vs RM-2 tension in one geometric decision
- Separate modular mounted plate (screwed, not welded) as structural datum for entire mechanism stack above → BAS-AC-1

### 4.2 Rotation (5.2.2)
- Slewing ring bearing (010.10.120 four-point contact) + off-axis timing-belt drive (S8M, 1:3.5 pulley ratio) + cam-follower edge supports
- Wireless-only UDP command path (no cable through rotating joint) → ROT-AC-2
- BLDC servo motor with 25:1 planetary gearbox

### 4.3 Height Adjustment (5.2.3)
- **Critical design principle:** Lift function (screw jack, axial only) separated from lateral structural resistance (telescopic column + Delrin wear pads)
- HK2T screw jack + travelling-nut mount + 8080 aluminium inner extrusion + welded steel outer tube
- Self-locking jack geometry provides inherent fail-safe position retention
- Motor: 24 V DC gear motor, ~800 rpm input requirement under 22.5 kg load

### 4.4 Padding (5.2.4)
- Multi-layer: polyethylene foam (energy absorption) → anti-vibration isolation mounts (drivetrain protection) → MPU6050 IMUs at interface layer
- Quad-IMU topology: 4× MPU6050 across 2 I²C hardware buses on Teensy 4.0 (dual-bus avoids address collision)
- Detection algorithm: L2 vector norm ≥ 2.0 g threshold
- Known firmware issues resolved: (1) I²C bus hang from parasitic capacitance → Hard STOP recovery protocol; (2) Nyquist blind-spot in punch detection → sampling rate corrected
- ROS 2 topic: `/strike_events`

### 4.5 Arm Actuation (5.2.5)
- 2-DOF coaxial differential joint: both motors co-located at pivot (minimises inertia)
- Actuator: Damiao DM-J4310-2EC brushless servo (final selection after servo → ODrive iteration)
- V5 design: 6 mm stainless steel D-shaft + Delrin pin + M2 screw reinforcement (replaced polymer shafts post-CDE Fair)
- Gear reduction: 3:1 helical-spur gear
- Power: 24 V motor bus / 12 V logic rail (dual-supply architecture)
- Control: 200 Hz unified Teensy 4.0 loop; Sparse Edge-Trigger CAN strategy; micro-ROS USB bridge to Jetson Orin NX
- Strike library: Left/Right Jab, Hook, Uppercut (6 variants)
- RM-8 partial: kinematic geometry achieves target, but Damiao PID acceleration/deceleration ramps add ~0.4–0.5 s constant overhead per strike

---

## 5. System Integration Architecture

- **Power:** Dual-rail — 24 V motor bus isolated from 12 V logic rail (prevents regenerative braking disruption of control layer)
- **Control hierarchy:** Jetson Orin NX (ROS 2 Humble, combat FSM, GUI) ↔ Teensy 4.0 (200 Hz firmware loop, CAN/PWM/I²C) via micro-ROS USB bridge
- **Rotation axis:** Secondary WiFi-enabled MCU receiving angle references from Jetson over UDP
- **Height axis:** Open-loop timed commands; passive position retention via screw-jack self-locking

---

## 6. Academic Writing Rules (Enforced Throughout)

These apply to all subsystem HTML pages:

| Rule | Correct | Wrong |
|------|---------|-------|
| Section references | `Section 5.2.3` | `§5.2.3` |
| Empty table cells | `N/A` | `—` (em dash) |
| Em dash in prose/tables | Use `;` or `,` or `:` | `—` or `&mdash;` |
| Bold in body `<p>` | Use `<em>` for emphasis | `<strong>` in running prose |
| Approximate symbol | `approximately 800 rpm` | `~800 rpm` |

---

## 7. Page Structure Conventions

Each hub page (`base.html`, `rotation.html`, etc.) follows this section order:
1. Subsystem Overview `<div id="[subsystem]-subsystem">`
2. Requirements & Considerations (RM table + AC table)
3. System Design Narrative (V-Model SVG + Left/Base/Right of V paragraphs)
4. Interactive 3D Model viewer (with hotspot annotations)
5. Design (detailed mechanical rationale)
6. sub-pages via `<sl-card>` navigation grid

**V-Model SVG wrapper structure** (must follow exactly — unclosed divs break page layout):
```html
<div style="margin: 28px 0; text-align: center; overflow-x: auto;">   <!-- outer wrapper -->
  <div class="vmodel-wrap" ...>                                         <!-- click-to-expand -->
    <svg ...>...</svg>
  </div>
  <sub>Figure caption...</sub>
</div>                                                                  <!-- MUST close outer -->
```

**Lightbox:** All V-Model SVGs use `.vmodel-wrap` class with a shared `<dialog>` lightbox injected before `</body>`. Click to expand is functional on all 5 hub pages.

---

## 8. File Map

```
pages/
  robot-mechanism.html          — Master hub (RM table, V-model, verification plan)
  robot-mechanism/
    base.html                   — 5.2.1 Base subsystem hub
    rotation.html               — 5.2.2 Rotation subsystem hub
    height-adjustment.html      — 5.2.3 Height Adjustment subsystem hub
    padding.html                — 5.2.4 Padding subsystem hub
    arm-actuation.html          — 5.2.5 Arm Actuation subsystem hub
    arm-actuation/
      design-ideation.html
      mechanical-design.html
      electrical-integration.html
      testing-evaluation.html   — ARM-AC-1…5 test results; ARM-AC-3, ARM-AC-5 passed
```
