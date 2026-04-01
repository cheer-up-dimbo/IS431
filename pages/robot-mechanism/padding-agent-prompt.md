# Upper Assembly Agent Prompt — Padding & Arm Actuation

## Context

You are working on the IS-431 FYP web report for BoxBunny, an intelligent boxing robot. The report is a static HTML site hosted locally at `http://127.0.0.1:5500`. However you need to push changes back to the GITHUB folder for it to reflect.

You are responsible for **two upper-body subsystems**: **5.2.4 Padding** and **5.2.5 Arm Actuation**. The Padding subsystem has its own dedicated sub-pages. The Arm Actuation subsystem links to existing `upper-mechanism/` sub-pages that contain detailed content. Your task is to **populate detailed technical content** into scaffold pages, **ensure existing pages are complete**, and **design the required validation tests**.

---

## Part A: Padding Subsystem (5.2.4)

### Page Structure

| Page | Path | Current State |
|------|------|---------------|
| Parent | `pages/robot-mechanism/padding.html` | ✅ Complete — overview, requirements, design summary, IMU pipeline summary |
| Mechanical Design | `pages/robot-mechanism/padding/mechanical-design.html` | Scaffold — needs detailed content |
| Electrical Integration | `pages/robot-mechanism/padding/electrical-integration.html` | Partial — I²C topology table and timing budget populated, needs expansion |
| Testing & Evaluation | `pages/robot-mechanism/padding/testing-evaluation.html` | Scaffold — test framework defined, needs detailed procedures and results |
| Troubleshooting | `pages/robot-mechanism/padding/troubleshooting.html` | Scaffold — defect tables populated, needs detailed root-cause narratives |

### Tasks

#### A1. Mechanical Design Page (`padding/mechanical-design.html`)

Populate the following sections (currently placeholder alerts):

- **Multi-Layer Padding Architecture**: Detailed material properties of the polyethylene foam (density, Shore hardness, energy absorption capacity). Thickness rationale for each layer. Why polyethylene foam was chosen over alternatives (EVA, neoprene, closed-cell rubber).
- **Anti-Vibration Isolation Interface**: Specific mount model/specs. Isolation frequency characteristics. Why transverse impact loads from user punches are incompatible with the 3D-printed PLA/Delrin drivetrain optimised for torsional loads.
- **Attachment to Arm Mechanism**: Fastener types, alignment features, how the padding is serviced/replaced. Interface drawing or CAD screenshot.
- **IMU Sensor Mounting**: Physical mounting orientation of each MPU6050 within the foam. Potting or protection method. Wire routing from sensor to Teensy.
- **Media**: Add annotated cross-section image showing the three-layer stack (foam → mount → housing). Place in `assets/upper_mechanism/padding/` and use `<image-component>`.

#### A2. Electrical Integration Page (`padding/electrical-integration.html`)

The I²C topology table and timing budget are already populated. Expand:

- **MPU6050 Sensor Selection**: Why MPU6050 over alternatives (ADXL345, BNO055, LSM6DS3). Cost/performance trade-off, 6-axis vs 9-axis consideration.
- **Wiring Considerations**: Detailed analysis of parasitic capacitance on 30–40 cm jumper wires. Why shielded cables or shorter runs weren't feasible at prototype stage. Reference to Hard STOP protocol fix.
- **Noise Rejection**: Expand on the scan-window peak detection logic with a code snippet or pseudocode showing `np.max(mag_arr[-n_scan:])`.
- **ROS 2 Integration**: How the `/motor_feedback` payload (21 doubles) is structured. Which indices correspond to IMU data. How `/strike_events` topic is published.

#### A3. Testing & Evaluation Page (`padding/testing-evaluation.html`)

The test framework (PC-3, PC-5) is defined. You need to:

- **Design detailed test procedures** for each criterion. Include: equipment needed, setup steps, data collection method, success criteria, and expected evidence format.
- **Generate additional tests** beyond PC-3 and PC-5 that would thoroughly validate the padding subsystem:
  - False positive rate (robot arm moving without being punched — should not trigger)
  - Spatial discrimination accuracy (can the system correctly identify which zone was hit?)
  - Latency measurement (time from physical impact to `/strike_events` publication)
  - Sensor degradation over time (repeated impact test over extended sessions)
- **Populate results** once testing is complete. Include screenshots from GUI Diagnostics Tab, video evidence of test sessions, and L2 norm distribution plots.

#### A4. Troubleshooting Page (`padding/troubleshooting.html`)

The defect summary tables are populated. Expand each defect with:

- **Defect 7 (I²C Bus Hang)**: Full root-cause narrative. Include oscilloscope captures if available. Explain the MPU6050 internal state machine behaviour. Compare Repeated Start vs Hard STOP timing diagrams. Quantify the ~20 µs latency penalty.
- **Defect 8 (Nyquist Blind-Spot)**: Explain the aliasing problem with a timing diagram. Show before/after detection rates. Include the Python code diff that implemented scan-window peak detection. Explain why n_scan ≈ 10 (200 Hz firmware / 20 Hz GUI).

---

## Part B: Arm Actuation Subsystem (5.2.5)

### Page Structure

| Page | Path | Current State |
|------|------|---------------|
| Parent | `pages/robot-mechanism/arm-actuation.html` | ✅ Complete — overview, requirements, design, validation, nav cards |
| Design & Ideation | `pages/upper-mechanism/design-ideation.html` | Existing — motion analysis, concept selection, motor selection |
| Mechanical Design | `pages/upper-mechanism/mechanical-design.html` | Existing — joint kinematics, gear reduction, structural revisions |
| Electrical Integration | `pages/upper-mechanism/electrical-integration.html` | Existing — power architecture, CAN bus, dual-rail isolation, MDDS10 |
| Firmware & Software | `pages/upper-mechanism/firmware-software.html` | Existing — V4 firmware, GUI V3, Dynamic Sparring FSM, ROS 2 |
| Testing & Evaluation | `pages/upper-mechanism/testing-evaluation.html` | Existing — performance criteria PC-1 through PC-10 |
| Troubleshooting | `pages/upper-mechanism/troubleshooting.html` | Existing — 9 cross-layer defects (8 resolved, 1 mitigated) |

### Tasks

#### B1. Review & Complete Existing Sub-Pages

All six `upper-mechanism/` sub-pages have existing content. Review each and ensure:

- All sections are fully populated (no leftover placeholder alerts or TODO comments)
- V-Model requirements traceability is explicit (map content to RM-5, RM-6)
- Cross-references between pages are correct (back buttons point to `../robot-mechanism/arm-actuation.html`)
- Media assets are present and `<image-component>` tags reference correct paths (`../assets/upper_mechanism/...`)

#### B2. Testing & Evaluation — Populate Results (`upper-mechanism/testing-evaluation.html`)

The page defines **10 performance criteria** (PC-1 through PC-10). For each:

| ID | Criterion | Target |
|----|-----------|--------|
| PC-1 | Strike speed | 90° ≤ 0.25 s |
| PC-2 | Repeatability | ≤ 10 mm |
| PC-3 | IMU detection rate | ≥ 95% TP |
| PC-4 | Endurance | 10 min continuous, < 60°C |
| PC-5 | Force differentiation | Monotonic (L < M < H) |
| PC-6 | FSM combo chain | 3 strikes ≤ 5 s |
| PC-7 | Regen safety | No PSU OVP trip |
| PC-8 | Agent recovery | ≤ 3 s after disconnect |
| PC-9 | Current cutoff | ≤ 100 ms |
| PC-10 | ROS command fidelity | Correct strike executed |

You need to:
- **Design and execute test procedures** for each PC
- **Record measured values** and pass/fail status
- **Capture evidence**: GUI screenshots, video recordings, oscilloscope traces where applicable
- **Note**: PC-3 and PC-5 results should cross-reference the Padding testing page since those criteria originate from the padding/IMU subsystem

#### B3. Coordinated Strike Validation (IMU as Input)

Document the integration test where **IMU strike detection from the padding subsystem triggers coordinated arm responses**. This stays under Arm Actuation as a validation component:

- Test setup: padding IMU detects user punch → `/strike_events` topic published → FSM triggers counter-strike
- Measure: latency from impact detection to arm movement initiation
- Measure: correct strike type selection based on zone detected
- This validates the cross-subsystem integration between Padding (5.2.4) and Arm Actuation (5.2.5)

#### B4. Troubleshooting — Ensure All 9 Defects Documented (`upper-mechanism/troubleshooting.html`)

Review all 9 defects and ensure each has:
- Layer classification (Hardware / Firmware / Application)
- Root-cause analysis with evidence
- Resolution description with verification
- Status (Resolved / Mitigated)

**Note**: Defects 7 and 8 (I²C bus hang, Nyquist blind-spot) are also documented on the Padding troubleshooting page. Ensure cross-references are consistent.

---

## Technical Constraints

- **Asset paths**: From `padding/` sub-pages, use `../../../assets/upper_mechanism/...`. From `upper-mechanism/` pages, use `../assets/upper_mechanism/...`
- **Components**: Use existing `<image-component>`, Shoelace alerts (`<sl-alert>`), and inline tables. GridJS is available if needed for large data tables.
- **Style**: Follow existing page conventions — `<h3>` for sections, `<h4>` for subsections, `<sl-alert>` for callouts
- **V-Model**: Each page must show how content maps to the requirements cascade (RM-5 for arm actuation, RM-6 for padding)

## Scope Boundaries

- **DO NOT** modify `padding.html` or `arm-actuation.html` (parent pages are complete)
- **DO NOT** create new sub-pages beyond those listed above
- **DO** remove yellow "Content Pending" warning banners from padding sub-pages once content is populated
- **DO** reference sibling pages and cross-subsystem pages via relative links
- **DO** ensure Defects 7 & 8 are cross-referenced consistently between padding and arm actuation troubleshooting pages
