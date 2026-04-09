# Academic Technical Writer — Domain Summary

**Agent Role:** Agent 4: Academic Technical Writer
**First Confirmed Contributions:** 2026-03-11 (initial thesis draft R1, R2 architectural pivot revision, R3 MDDS10/OVP revision)
**Subsequent Contributions:** 2026-04-06 through 2026-04-07 (IS-431 web report content audit, executive summary restructuring, academic standards enforcement across HTML pages)
**Summary Compiled:** 2026-04-07

> **Self-contained by design.** All values, rules, and decisions are embedded inline.
> A new agent reading this file needs no other document to understand the academic writing domain.

---

## 1. Agent Role

**Primary:** Academic Technical Writer (Agent 4) — responsible for translating engineering decisions, firmware bugfixes, and hardware test results into formal academic prose for two output formats:

1. **Thesis document** (`academic_thesis_report.md`): A traditional written undergraduate FYP report covering all mechanical, electrical, and software subsystems of the BoxBunny boxing robot.
2. **Web-based HTML report** (`documents/IS431/pages/`): A multi-page interactive report hosted as static HTML using Shoelace UI components, where each subsystem has dedicated sub-pages structured as: requirements, design rationale, and validation results.

**Responsibilities include:**
- Enforcing academic writing standards (passive voice, no bullet lists in prose, no em dashes, no bold in body text, prohibiting the § symbol)
- Performing content audits across HTML pages to identify factual inconsistencies, cross-page conflicts, and stylistic violations
- Restructuring page hierarchy to reflect the V-Model methodology (requirements → design → verification)
- Ensuring every quantitative claim has a cited source (sensor reading, test data, or datasheet reference)
- Coordinating revisions when other agents change architecture (e.g., reframing the superseded sensorless homing sequence as a design iteration rather than an active procedure)

---

## 2. Key Decisions Made — With Full Rationale

### Decision: Sensorless Homing Sequence Reframed as a Superseded Design Iteration
**Reason:** The original thesis draft (R1) described the sensorless homing as an active operating procedure. After the Lead Systems Integrator removed it from all code on 2026-03-11 due to three confirmed failure modes (false current-spike termination at wrong encoder position; inconsistent hard-stop positions across power cycles; Motor 2 resonance torque aborting the sequence before completion), the thesis had to be updated. In R2, Section 2.7 was reframed as "Design Iteration — Superseded" with a clear status block, and the failure modes were migrated to the Iterative Troubleshooting section (new §5.5). The homing mathematics (midpoint equation: `zero_pitch = (M1_max + M1_min) / 2`, span verification: `range_rad = (M1_max - M1_min) / (2 × 3.0)`) were preserved in Appendix A for academic record even though the code no longer uses them.

### Decision: Manual Calibration Framework Documented as the Active Procedure
**Reason:** Because the automated homing was removed, the thesis needed a formal description of what replaced it. A new Section 2.8 was added documenting the Calibration Tab jogging workflow: the operator jogs each motor in 0.5 rad increments, watches the live current ammeter, records the raw encoder position at which current spikes above the safety threshold (indicating a hard stop), and uses these discovered values to construct safe motor-space sequences. This workflow must be described in the present tense as the active operating procedure.

### Decision: dI/dt Impact Detection Documented as a Replacement for Static Threshold
**Reason:** Early documentation described the 1.33A static current limit as the active safety mechanism. After physical testing confirmed that legitimate high-speed motor acceleration transiently draws 8–10A (far exceeding 1.33A), the static limit was replaced by a dynamic rate-of-change detector. The thesis must describe dI/dt detection (default sensitivity: 40 A/s; grace period: 0.6 seconds suppressing detection at the start of each motion) as the primary sensorless impact system. The 1.33A limit appears only in historical context as the threshold used during the pre-fair firmware iteration.

### Decision: Executive Summary Structure for Arm Actuation Front Page
**Reason:** The arm-actuation.html page previously lacked a clear overview. It was restructured as an executive summary page following the flow: Design Requirements → Performance Criteria (linked to requirements by ID) → Subsection Highlights table → Final Arm Design (with interactive 3D model) → Power Architecture → Test and Evaluation Results → Video Evidence. Detailed technical derivations are delegated to the five subsection pages (design-ideation.html, mechanical-design.html, electrical-integration.html, firmware-software.html) and the appendix.

### Decision: Testing and Troubleshooting Content Archived to Appendix 3
**Reason:** The arm-actuation executive summary page became overloaded with detailed test logs and troubleshooting records that should not appear in an overview. These were moved to a new `appendix-arm.html` page (Appendix 3), containing Section A3.1 (Testing and Evaluation) and Section A3.2 (Troubleshooting and Iteration). Navigation cards on the main page were updated with "(Appendix 3)" labels so readers understand they are navigating to archived material, not a primary subsystem section. The Dynamic Speed Adaptation section was also moved to troubleshooting because it was not deployed in the final system.

### Decision: Navigation Button Standardisation Across Arm Actuation Pages
**Reason:** Navigation buttons across the arm actuation subsection pages used inconsistent variants (some `variant="primary"`, others `variant="default"`). All navigation buttons were standardised to `variant="default" size="medium"` to match the pattern used across the rest of the report. This ensures visual consistency for a reader following the sequential documentation flow.

### Decision: Interactive 3D Model in Executive Summary Matches Mechanical Design Page
**Reason:** The arm-actuation front page uses the same `arm_joint_V5.glb` model as `mechanical-design.html`. The CSS (`.Hotspot`, `.HotspotAnnotation`, `.HotspotAnnotation::before`, and `model-viewer.hide-hotspots .Hotspot`) was replicated verbatim to ensure the blue dot markers, connector line, label box, and toggle behaviour are identical on both pages. The relative path differences between directory levels are accounted for: from `arm-actuation/mechanical-design.html` the model path is `../../assets/upper_mechanism/arm_joint_V5.glb`; from `arm-actuation.html` (one level higher) it is `../assets/upper_mechanism/arm_joint_V5.glb`.

### Decision: "Fair" Consistently Replaced with "CDE Fair" Throughout
**Reason:** All references to the project showcase event were previously inconsistent — some pages used "fair", "project fair", "fair-day", and "post-fair". The user confirmed the correct name is "CDE Fair". All instances across `arm-actuation.html` and `arm-actuation/mechanical-design.html` were updated to use: "CDE Fair", "CDE Fair structural failures", "post-CDE-Fair revision", and "post-CDE-Fair" in table cells.

---

## 3. Current State: Academic Standards and HTML Report

### 3.1 Enforced Academic Writing Rules (Complete List)

All HTML page body text must comply with these rules (source: `documents/academic_writing_skills.md`):

| Rule | Requirement |
|---|---|
| No bold in body prose | `<strong>` and `<b>` are forbidden inside `<p>` body paragraphs. Only permitted in `<h1>`–`<h5>`, `<th>` table headers, `<sl-alert>` callout components, and figure captions. Use `<em>` sparingly for emphasis, or rely on sentence structure. |
| No bullet lists in prose | `<ul>` and `<ol>` are forbidden inside body `<p>` prose sections. Convert list content to compound sentences with semicolons or commas. |
| Passive voice preferred | Use "testing was conducted" not "we tested"; "the firmware was updated" not "I updated the firmware". |
| No em dashes in prose | The `—` character and `&mdash;` entity are forbidden in `<p>`, `<td>`, `<li>`, and link text. Replace with commas, semicolons, colons, or parenthetical clauses. Em dashes are permitted in HTML comments, image subtitle attributes, and headings. |
| No § symbol | Never use `§` or `&sect;` in any visible body text. Write "Section 5.2.5.4" in full. |
| No emojis | All emoji characters are forbidden in academic text. |
| V-Model traceability | Each page must reference the relevant system requirements (RM-1 through RM-7). Tests must link back to specific requirements. |
| Section numbering consistency | HTML comment markers (e.g., `<!-- 3. SUBSECTION NAME -->`) must match visible heading numbers. No skipping from Section 2 to Section 4. |
| Quantitative claims need evidence | Every measurement (current, speed, timing) requires a citation of the data source: test session, sensor, or specific firmware output. |

### 3.2 HTML Report Page Hierarchy (Active as of 2026-04-07)

The report lives at `documents/IS431/pages/`. Key structure:

```
robot-mechanism.html                   — System overview, requirements, V-model plan, nav grid
robot-mechanism/
  arm-actuation.html                   — Executive summary (restructured 2026-04-06)
  arm-actuation/
    design-ideation.html               — Motor platform selection, 2-DOF concept
    mechanical-design.html             — IK, structural hardening, CDE Fair failure analysis
    electrical-integration.html        — Dual-supply, CAN wiring, IMU dual-bus
    firmware-software.html             — Teensy 200Hz loop, strike library, ROS interface
    testing-evaluation.html            — Speed tests (43 trials), current data
    troubleshooting.html               — Iteration history (incl. Dynamic Speed Adaptation)
  base.html / rotation.html / height-adjustment.html / padding.html — Other subsystems
  appendix-arm.html                    — Appendix 3: archived A3.1 Testing, A3.2 Troubleshooting
robot-intelligence.html                — Next section after firmware-software.html
```

Navigation convention: each subsection page has a Prev/Next button row using `variant="default" size="medium"`. The Next button at the end of firmware-software.html correctly links to `../../robot-intelligence.html`.

### 3.3 Arm Actuation Executive Summary — Section Structure

The arm-actuation.html page (updated 2026-04-06/07) follows this flow:

**5.2.5 Arm Actuation** (h2, introductory paragraph)

**5.2.5.0.1 Design Requirements** — Table mapping PC-1 through PC-4 to RM-5/RM-6, with acceptance criteria and validated status.

**5.2.5.0.2 Performance Criteria** — Table linking each performance criterion to its parent requirement, with current test status (PC-1 validated; PC-2, PC-3, PC-4 pending full validation).

**5.2.5.0.3 Subsection Highlights** — Two-column table (Section | Key Contribution) with four rows:
- 5.2.5.1 Design and Ideation: 2-DOF coaxial differential joint selected from three motor platforms; mass centralised at pivot.
- 5.2.5.2 Mechanical Design: CDE Fair failures informed revision from polymer shafts to 6 mm stainless D-shaft with Delrin pin reinforcement.
- 5.2.5.3 Electrical Integration: Dual-supply architecture (24 V motor bus / 12 V isolated logic rail) prevents OVP events from triggering a full robotic shutdown.
- 5.2.5.4 Firmware and Software: Teensy 4.0 executes a deterministic 200 Hz unified loop; two-tier ROS 2 architecture separates real-time control from combat decision logic on Jetson Orin NX.

**Design Evolution table** — Five-row table tracing the arm from servo prototype through ODrive, Damiao, and post-CDE-Fair structural revision to the final deployed configuration.

**5.2.5.0.4 Final Arm Design** — Interactive model-viewer (`arm_joint_V5.glb`) with 5 hotspots: Motor 1 (Roll, DM-J4310-2EC), Motor 2 (Pitch, DM-J4310-2EC), Central Gear Stack (3:1 Helical-Spur), Bevel Gear Coupling, Stainless Steel D-Shaft (6 mm). Toggle button for annotations (`variant="default" size="small"`).

**5.2.5.0.5 Power Architecture** — `image-component` referencing the power diagram (assumes diagram in assets).

**5.2.5.0.6 Data Architecture** — `image-component` referencing the data diagram (assumes diagram in assets).

**5.2.5.0.7 Test and Evaluation Results** — `sl-alert variant="success"` callout with key finding (peak per-motor current never exceeded 0.69 A across all 43 tests; total arm peak power approximately 33 W; zero safety trips). Followed by the strike timing data table.

**Video Evidence** — Embedded `Arm_Chain_Execution.mp4` (path: `../../assets/upper_mechanism/videos/Arm_Chain_Execution.mp4` from arm-actuation.html). Caption: strike library chain execution demonstration.

**Navigation buttons** (Continue to Detailed Documentation) → design-ideation.html.
**Detailed Documentation grid** — Four nav cards linking to design-ideation, mechanical-design, electrical-integration, firmware-software.
**Appendix navigation cards** — Two nav cards: "Testing and Evaluation (Appendix 3)" → `appendix-arm.html#a3-testing`; "Troubleshooting (Appendix 3)" → `appendix-arm.html#a3-troubleshooting`.

### 3.4 Thesis Document History

File: `documents/academic_thesis_report.md`

| Revision | Date | Sections Changed |
|---|---|---|
| R1 (initial draft) | 2026-03-11 | All 6 sections + Appendices A/B/C. Full kinematic derivations, MDDS10 docs, dI/dt algorithm (Eq.11). |
| R2 (pivot) | 2026-03-11 | §2.7 reframed as superseded; §2.8 (Manual Calibration Protocol) added; §3.3 renamed "Calibration Impact Limit"; §5.5 (homing failure case study) added; §6.1 contribution count updated. |
| R3 | 2026-03-11 | §Abstract expanded (pin swap + OVP); §3.4 Regen Braking upgraded to confirmed failure; §3.5 MDDS10 wiring corrected; §4.3 HeightTab documented; §5.6 (pin transposition) + §5.7 (OVP incident) added as new troubleshooting case studies. |

### 3.5 Content Audit — Open Findings Summary (as of 2026-04-06)

A 22-finding validation audit was completed (`documents/validation_report_2.md`). Key open items requiring HTML fixes:

**High severity:**
| File | Issue | Correct Value |
|---|---|---|
| `arm-actuation/electrical-integration.html` | PSU rated "8.3A" in text | Correct: 8.8A (Mean Well LRS-200-24 datasheet) |
| `arm-actuation/electrical-integration.html` | IMU described as "I2C chain" | Correct: "parallel dual-bus" (two independent hardware I2C ports on Teensy) |
| `rotation/electrical-control.html` | Power table lists "Total from PSU: 5V rail" for Arduino | Correct: Arduino R4 WiFi powered from 12V VIN via HW-140 buck converter |
| `height-adjustment/electrical-control.html` | Unclosed `</div>` tag | HTML structural nesting error; breaks page layout |
| `padding/electrical-integration.html` | Strike topic name: `/strike_events` | Correct: `/robot/strike_detected` |
| `arm-actuation/design-ideation.html` | IK equations duplicated with inconsistent numbering | Equns labelled Eq.1–2 in design-ideation vs Eq.3–4 in mechanical-design; must be harmonised |

**Pending (firmware source confirmation required):**

| Finding | Discrepancy |
|---|---|
| CAN Motor ID format | HTML report shows 0x01–0x04; motor_specifications.md shows 0x101–0x104 (= 0x100 + base ID). These are BOTH correct for different uses: base IDs for configuration frames, 0x101–0x104 for command TX frames. HTML column header is misleadingly labelled. Needs firmware source confirmation. |
| IMU polling rate | HTML pages state 200 Hz (correct for Firmware V4 unified loop); older motor_specifications.md states 500 Hz (from the standalone DSP rig — deprecated). The 200 Hz figure is correct. Any filter window or buffer length must be calculated at 200 Hz. |

---

## 4. Open Action Items

### 4.1 HTML Report — High-Severity Fixes Outstanding

- **`arm-actuation/electrical-integration.html`:** PSU figure in body text reads "8.3A" — must be corrected to 8.8A.
- **`arm-actuation/electrical-integration.html`:** "I2C chain" description — must be changed to "parallel dual-bus".
- **`rotation/electrical-control.html`:** `<ol>` list inside "Design Rationale" body prose — must be converted to paragraph prose (lists are prohibited in body sections).
- **`rotation/electrical-control.html`:** Section HTML comment numbers are out of order (Section 2, Section 4, Section 3 in DOM sequence).
- **`height-adjustment/electrical-control.html`:** Unclosed `<div>` breaks page layout.
- **`padding/electrical-integration.html`:** `<strong>InvenSense MPU6050</strong>` inside body `<p>` — bold must be removed from body prose.
- **`padding/electrical-integration.html`:** Strike topic `/strike_events` — must be corrected to `/robot/strike_detected`.

### 4.2 Thesis Document

- `academic_thesis_report.md` is at Revision R3 (2026-03-11). It has NOT been updated with any of the following developments that occurred after R3:
  - IMU ±16g fix (ACCEL_CONFIG = 0x18, divisor 2048 instead of 16384) — performed 2026-04-06
  - CHP-36GP-555 height motor positive identification (replaced "LGYMSZSS"/"MY1016Z") — 2026-04-06
  - Base rotation PID controller validated with tuned gains (Kp=25, Ki=1, Kd=1) — 2026-04-05
  - Forward kinematics model corrected and validated on hardware (2026-04-02)
  - Joint-space pitch clamping in GUI as replacement for firmware endstops (2026-04-02)
  - 43-trial strike speed test results (0.64s cycle; 33W peak) — 2026-04-03
  - Dynamic Sparring FSM validated on hardware — 2026-03-27
  - Brake resistor specification complete (height: 10Ω 50W; base: 5Ω 100W) — 2026-04-06
  - **A full Revision R4 of the thesis is required** to incorporate all of the above.

### 4.3 Robot-Mechanism Page — Electrical and Control Architecture Section

A content document has been drafted (`brain/.../elec_control_arch_content.md`) expanding the thin Electrical and Control Architecture subsection in `robot-mechanism.html`. The agent receiving this document should:
- Replace lines 192–240 in `robot-mechanism.html` with the provided HTML snippet
- The snippet adds: compute node table (Jetson/Teensy/Damiao/IMU), power architecture table (24V motor bus / 12V logic rail), communication buses paragraph (CAN 1 Mbps sparse edge-trigger, dual I2C 400 kHz, micro-ROS), and three-tier PID cascade paragraphs
- Both existing `<image-component>` stubs (`component_overview.png` and `closed_loop.jpg`) remain at unchanged paths

---

## 5. Known Inconsistencies or Warnings

### IMU Scale Factor and Polling Rate Changed on 2026-04-06

- **Correct (post-2026-04-06):** ACCEL_CONFIG register = `0x18` (±16g range); divisor = `2048 LSB/g`; max readable: ±157 m/s²
- **Wrong (before reflash):** ACCEL_CONFIG = `0x00` (intent ±2g, failed to apply); divisor = `16384 LSB/g`
- **Impact:** All strike detection thresholds set before the 2026-04-06 reflash are 8× too small. Any calibration CSV data from before this date reflects underscaled acceleration values. All thresholds must be re-calibrated after reflashing.
- **Correct polling rate:** 200 Hz (Teensy V4 5ms unified loop). The 500 Hz figure in older documentation refers to the deprecated standalone IMU DAQ rig (Agent 5, `teensy_imu_daq.ino`), which ran independently before being merged into the main firmware.

### Three Conflicting Strike Topic Names Across HTML Pages

- **Correct (from active GUI V3/V4 code):** `/robot/strike_detected`
- **Wrong variant 1:** `/strike_events` — appears in `padding/electrical-integration.html`
- **Wrong variant 2:** `/strike_detected` — appears in `motor_specifications.md` (no `/robot/` prefix)
- **Risk:** An external system subscribing to the wrong topic name will never receive strike events. All HTML pages must be updated to use `/robot/strike_detected`.

### CAN Frame IDs — Two Numbers Both Correct for Different Purposes

- **Motor configuration/feedback base IDs:** 0x01, 0x02, 0x03, 0x04
- **CAN TX command frame IDs:** 0x101, 0x102, 0x103, 0x104 (= 0x100 + base ID)
- **Wrong (HTML column header):** "CAN Frame ID" column shows 0x01–0x04 with an implied meaning of TX frame IDs
- **Risk:** Writing firmware using the base IDs as TX frame IDs will send to wrong CAN addresses. New firmware must transmit on 0x101–0x104.

### Height Motor Name — CHP-36GP-555 Only

- **Correct:** CHP-36GP-555 GEAR BOX MOTOR (confirmed from physical motor label 2026-04-06)
- **Wrong (in all log entries and documents before 2026-04-06):** "LGYMSZSS", "MY1016Z"
- **Risk:** Searching for datasheets or specifications under the wrong names returns nothing. All HTML pages that reference the height motor must use CHP-36GP-555.

### Sensorless Homing Is NOT the Active Procedure

- **Active procedure:** Manual boundary discovery via Calibration Tab; operator jogs with 0.5 rad increments; reads live current to identify hard stops
- **Superseded:** Automated sensorless homing sequence (current sweep against mechanical stops) — removed from all code 2026-03-11
- **Risk:** Any new documentation describing automated current-sweep homing as currently active will be incorrect.

### Dynamic Speed Adaptation Is Archived, Not Active

- The Dynamic Speed Adaptation feature (veff = min(max(vbase, dtotal / (T - 0.3)), vmax)) was removed from `firmware-software.html` on 2026-04-07 because it is archived in `troubleshooting.html`. Any new documentation that places this equation in an active-feature context is incorrect. It belongs in the superseded design iterations section.

### § Symbol and Em Dash Are Prohibited in Visible HTML

Older HTML pages (particularly outside the arm-actuation subsection) may contain:
- `&sect;` or the literal § character in body text — **prohibited**; write "Section X.X" in full
- `&mdash;` or `—` in `<p>`, `<td>`, or `<li>` — **prohibited**; replace with comma, semicolon, or colon
- `<strong>` tags inside body `<p>` paragraphs — **prohibited**; remove bolding

The `documents/academic_writing_skills.md` file is the authoritative reference for all writing rules.

---

*This document covers contributions from 2026-03-11 (initial thesis drafts) through 2026-04-07 (HTML report restructuring, content audit, and standards enforcement).*
*Authoritative chronological record: `agent_knowledge/integration_log_copy.md` (search "Agent 4: Academic Technical Writer").*
