# IS-431 Report Validation — 2026-04-09

## Audit Scope
- **Pages examined:** robot-mechanism.html, robot-mechanism/arm-actuation.html, robot-mechanism/arm-actuation/electrical-integration.html, robot-mechanism/arm-actuation/firmware-software.html, robot-mechanism/padding/electrical-integration.html, robot-mechanism/rotation/electrical-control.html, robot-mechanism/height-adjustment/electrical-control.html
- **Knowledge sources consulted:** PROJECT_KNOWLEDGE_BRIEF.md (embedded in report_validator_agent.md), academic_writing_skills.md, academic_writer_summary.md, lead_systems_integrator_summary.md, mechanical_agent_summary.md
- **Examiner:** Report Validator Agent (run 2026-04-09)

> **Note:** arm-actuation/mechanical-design.html, arm-actuation/design-ideation.html, arm-actuation/testing-evaluation.html, arm-actuation/troubleshooting.html, and appendix-arm.html were not read in this run. They are marked UNVERIFIABLE in the status table.

---

## Summary Table

| Page | Factual Findings | Writing Violations | Navigation Issues | Overall |
|---|---|---|---|---|
| robot-mechanism.html | 1 LOW | 2 MEDIUM | 0 | ISSUES |
| arm-actuation.html | 1 MEDIUM | 1 MEDIUM | 1 LOW | ISSUES |
| arm-actuation/electrical-integration.html | 1 HIGH, 1 MEDIUM | 2 MEDIUM | 0 | ISSUES |
| arm-actuation/firmware-software.html | 1 MEDIUM | 0 | 0 | ISSUES |
| padding/electrical-integration.html | 1 HIGH | 1 MEDIUM | 0 | ISSUES |
| rotation/electrical-control.html | 0 | 1 MEDIUM | 0 | ISSUES |
| height-adjustment/electrical-control.html | 0 | 1 MEDIUM | 1 MEDIUM | ISSUES |

---

## Findings by Page

---

### robot-mechanism.html

#### Factual Consistency

- [PASS] RM-1 through RM-7 requirements table — all 7 requirements present and correctly stated.
- [PASS] V-Model SVG diagram — correctly shows 6 nodes, design decomposition on left, verification on right, dashed traceability lines.
- [PASS] System Design Narrative — correctly states 200 Hz Teensy loop, dual-rail power architecture, two-tier control hierarchy (Teensy + Jetson), WiFi UDP for base rotation.
- [PASS] Verification Matrix — RM-5 correctly marked as "Partial" with correct rationale (Damiao PID ramp ~0.4–0.5 s overhead). RM-1, RM-2, RM-7 marked Passed; RM-3, RM-4, RM-6 marked Pending. Consistent with knowledge base.
- [FINDING] Section comment numbering — the page uses `<!-- 4. OVERALL SUBSYSTEM ARCHITECTURE -->` for what appears to be the second `4.` in the DOM (there is already a `<!-- 4. VERIFICATION PLAN (V-Model Right Side) -->` at line 395 and `<!-- 4. OVERALL SUBSYSTEM ARCHITECTURE -->` at line 320. Two sections numbered 4.
  - Correct structure from visible headings: Section 1 = System Overview, Section 2 = Design Requirements, Section 3 = System Design Narrative, Section 4 = Overall Subsystem Architecture, Section 5 = Verification Plan, Section 6 = Navigation Grid.
  - HTML comment at line 395 reads `<!-- 4. VERIFICATION PLAN -->` — should be `<!-- 5. VERIFICATION PLAN -->`.
  - Severity: LOW

#### Academic Writing

- [VIOLATION] `<ol>` list inside body prose — Lines 349–354 contain an `<ol>` with four `<li>` items inside a `<div>` following a body `<p>` paragraph ("The mechanism is organised as a vertical stack, ordered from the ground up."). The list directly substitutes prose and is therefore prohibited under the no-bullet/numbered-lists-in-prose rule.
  - Location: "Overall Subsystem Architecture → Mechanical Stack" section
  - Found: `<ol>` with `<li><strong>Trapezoidal Base</strong>...`, `<li><strong>Rotation Yaw Stage</strong>...`, etc.
  - Required: Convert to a compound prose sentence, e.g. "From the ground up, the stack comprises the trapezoidal base, the rotation yaw stage, the telescopic height-adjustment column, and the upper body with 2-DOF striking arms and multi-layer padding."
  - Severity: MEDIUM

- [VIOLATION] `<strong>` inside `<li>` body text — Each `<li>` inside the above `<ol>` wraps the component name in `<strong>`. Although `<li>` is not `<p>`, these list items are functioning as prose substitutes; the bold emphasis is therefore also a violation of the no-bold-in-body-prose rule.
  - Location: Same `<ol>` block, lines 350–353.
  - Found: `<strong>Trapezoidal Base</strong>`, `<strong>Rotation Yaw Stage</strong>`, etc.
  - Required: Remove `<strong>` tags; integrate into prose sentence.
  - Severity: MEDIUM

#### Navigation

- [PASS] Back button to Main Report present and correct.
- [PASS] Subsystem navigation grid links to all 5 subsystem pages.

---

### arm-actuation.html

#### Factual Consistency

- [PASS] Motor model: correctly identified as DM-J4310-2EC throughout.
- [PASS] PSU: correctly stated as Mean Well LRS-200-24 (200 W, 24 V, 8.8 A) in Section 5.2.5.0.5.
- [PASS] Peak power: 33 W peak / 10 W average — matches knowledge base.
- [PASS] Peak current: 0.69 A max (Right Hook, M4), N=43 — matches knowledge base.
- [PASS] 43-trial test count — correctly stated.
- [PASS] Gear reduction: 3:1 external helical-spur mentioned in Section 5.2.5.0.4 — correct.
- [PASS] RM-5 classified as "partially fulfilled" — correct; Damiao PID ramp overhead correctly identified.
- [FINDING] GUI version discrepancy in Section 5.2.5.0.6 — the Data Architecture section text states "GUI V4 application" (`unified_GUI_V4.py`). However, the knowledge base (lead_systems_integrator_summary.md §3.1) establishes that GUI V3 (`unified_GUI_V3.py`) is the **production** GUI and V4 is still in development. The HTML page's reference to "GUI V4" as the current application is technically premature.
  - Correct value: Production GUI is V3. V4 is in development (joint-space storage, not yet production default).
  - Found: "publishes motor commands on the `/motor_commands` topic at 100 Hz" attributed to `unified_GUI_V4.py`
  - Severity: MEDIUM (factually nuanced — V4 may be being used for testing, but V3 is the production default per knowledge base)

#### Academic Writing

- [VIOLATION] Em dash (`&mdash;`) inside caption `<span>` — Line 405 contains `<span style="color:#3b82f6;">&mdash; Click to enlarge.</span>` inside a visible `<div>` below an `<img>`. This is visible body text and the em dash is prohibited.
  - Location: Power Architecture section, image caption div
  - Found: `&mdash; Click to enlarge.`
  - Required: Remove em dash, rewrite as "Click image to enlarge." or similar.
  - Severity: MEDIUM
  - **Also present** at line 438 (Data Architecture image caption): `&mdash; Click to enlarge.`

#### Navigation

- [FINDING] No Appendix navigation cards for Testing (Appendix 3) and Troubleshooting (Appendix 3) — The academic_writer_summary.md §3.3 specifies that the arm-actuation.html page should include two appendix navigation cards: "Testing and Evaluation (Appendix 3)" → `appendix-arm.html#a3-testing` and "Troubleshooting (Appendix 3)" → `appendix-arm.html#a3-troubleshooting`. The current page only has four nav cards (design-ideation, mechanical-design, electrical-integration, firmware-software) and one additional card for testing-evaluation.html but linking directly, not to appendix-arm.html. The appendix-labelled cards are absent.
  - Severity: LOW (navigation gap; readers may not find archived appendix content)

---

### arm-actuation/electrical-integration.html

#### Factual Consistency

- [FINDING — HIGH] PSU rated current — **CLOSED from previous audit.** Section 5.2.5.3.3 now correctly states "Mean Well LRS-200-24 (200W, 24V / **8.8A**)". Previous finding of "8.3A" is no longer present.
- [FINDING — HIGH] IMU I2C description — **CLOSED from previous audit.** The page no longer contains "I2C chain." Section 5.2.5.3 does not describe the IMU topology; it delegates to the arm electrical layer. The padding/electrical-integration.html page correctly describes "parallel dual-bus."
- [FINDING] Section number anomaly — The page heading order does not match the section HTML comments. Section 5.2.5.3.1 is "Motor & Actuator Selection", Section 5.2.5.3.3 is "Dual-Rail Power Architecture", and Section 5.2.5.3.2 is "CAN Bus Communication". In the DOM, sections appear as 3.1 → 3.3 → 3.2 (out of sequence). The visible heading numbers 3.3 and 3.2 appear in non-ascending order.
  - Correct: 3.1 Motor Selection → 3.2 Power Architecture → 3.3 CAN Bus, OR renumber so visible headings ascend.
  - Severity: HIGH (section numbering inversion creates academic inconsistency)
- [FINDING] `<strong>` in `<td>` cells — The ODrive issues table (lines 88, 93, 98) and Damiao features table (lines 137, 142, 147, 152) use `<strong>` inside `<td>` for feature names. Table headers (`<th>`) may use bold, but `<td>` body-cell bold is borderline. Per academic_writing_skills.md, bold is permitted in table headers; `<td>` cell bold for non-header emphasis is marginal but not explicitly prohibited. Flagging as LOW for awareness.
  - Severity: LOW
- [PASS] CAN ID table: Column is correctly labelled "Motor Base ID" and the footer note correctly explains that TX command frames use `0x100 + Base ID = 0x101–0x104`. This is fully correct per knowledge base guidance.
- [PASS] Appendix link uses `&mdash;` inside a `<p>` (line 179–180): "Appendix 1 &mdash; Torque Calculations"
  - Found: `&mdash;` inside body `<p>` link text
  - Required: "Appendix 1: Torque Calculations" or "Appendix 1 (Torque Calculations)"
  - Severity: MEDIUM — flagging under Academic Writing below.

#### Academic Writing

- [VIOLATION] Em dash (`&mdash;`) inside body `<p>` — Line 179: `<a href="../../appendix-upper.html">Appendix 1 &mdash; Torque Calculations</a>` inside a `<p>` paragraph. Em dashes in link text are prohibited.
  - Found: `Appendix 1 &mdash; Torque Calculations`
  - Required: `Appendix 1: Torque Calculations`
  - Severity: MEDIUM

- [VIOLATION] Em dash in visible `<div>` caption — Line 238: `&mdash; Click to enlarge.` inside image caption `<div>`.
  - Found: `&mdash; Click to enlarge.`
  - Required: Remove em dash; plain text "Click to enlarge."
  - Severity: MEDIUM

#### Navigation

- [PASS] Prev/Next navigation row present at bottom: Prev = Mechanical Design (correct), Next = Firmware & Software (correct). Both use `variant="default" size="medium"` (correct).

---

### arm-actuation/firmware-software.html

#### Factual Consistency

- [PASS] Teensy 4.0 executes 200 Hz unified loop (5 ms period) — correct.
- [PASS] CAN sparse edge-trigger strategy: 0.01 rad threshold + 100 ms keep-alive — correct per knowledge base.
- [PASS] I2C dual-bus 400 kHz with Hard STOP protocol — correct.
- [PASS] 21-double feedback payload structure [pos×4, current×4, CAN_count, IMU_accel×12] — correct.
- [PASS] Strike topic `/robot/strike_detected` — correctly listed in Publisher Topics table at line 189. **CLOSED** from previous audit.
- [FINDING] GUI version in Two-Tier Architecture section — Line 48: `unified_GUI_V4.py` named as active Tier 1 GUI. Same issue as arm-actuation.html (see above); production GUI is V3.
  - Severity: MEDIUM

#### Academic Writing

- [PASS] No `<strong>` in body `<p>` prose found.
- [PASS] No em dashes in body `<p>` prose found.
- [PASS] No `§` symbol found.
- [PASS] No emoji found.
- [PASS] No bullet/numbered lists in prose sections found.

#### Navigation

- [PASS] Prev/Next navigation: Prev = Electrical Integration, Next = Robotics Intelligence. Next button links to `../../robot-intelligence.html` — **CORRECT** per agent spec requirement.
- [PASS] Both buttons use `variant="default" size="medium"`.

---

### padding/electrical-integration.html

#### Factual Consistency

- [FINDING — HIGH] Strike topic name — **CLOSED from previous audit.** Line 228: topic correctly listed as `/robot/strike_detected`. The previously reported `/strike_events` error is no longer present. ✅
- [PASS] IMU model: "InvenSense MPU6050" correctly identified.
- [PASS] IMU accelerometer range: Table (lines 88–91) correctly states "configured to ±16 g" and references software L2 norm threshold of 20 m/s². This reflects the post-2026-04-06 reflash correctly.
- [PASS] IMU polling rate: Table line 95 correctly states "Sampled at 200 Hz (matched to Teensy unified loop)."
- [PASS] I2C topology: Correctly described as two independent hardware I2C buses (Wire + Wire1), NOT a chain. Table shows Wire (Pins 18/19): 0x68 = Centre Body, 0x69 = Left Body; Wire1 (Pins 17/16): 0x68 = Right Body, 0x69 = Head Pad. Matches knowledge base exactly.
- [PASS] Hard STOP protocol: Correctly documented as the fix for parasitic capacitance bus hang.
- [PASS] Nyquist-aware scanning: `np.max(mag_arr[-n_scan:])` correctly documented.

#### Academic Writing

- [FINDING — HIGH from previous audit] `<strong>InvenSense MPU6050</strong>` inside body `<p>` — **STATUS: CLOSED.** Line 72 reads "The InvenSense MPU6050 6-axis MEMS inertial measurement unit was selected..." — no `<strong>` tags present. ✅
- [VIOLATION] `<strong>` inside `<td>` for "IMU Diagnostics Tab" — Line 217: inside a body `<p>`, the text uses `<strong>IMU Diagnostics Tab</strong>`. This is `<strong>` inside a `<p>` body paragraph — prohibited.
  - Found: `<strong>IMU Diagnostics Tab</strong>` in body prose
  - Required: Remove bold; "the IMU Diagnostics Tab" in plain text or italics
  - Severity: MEDIUM

#### Navigation

- [PASS] V-Model Traceability alert present at top: correctly references RM-6. ✅
- [PASS] Prev/Next navigation present: Prev = Mechanical Design, Next = Testing & Evaluation.

---

### rotation/electrical-control.html

#### Factual Consistency

- [PASS] Base motor model: Z55BLD400-24GU (400 W BLDC) — correct.
- [PASS] Total gear ratio: 91:1 (26:1 integrated gearbox × 3.5:1 belt stage) — correct.
- [PASS] Base motor driver: ZBLD C20-800LRC — correct.
- [PASS] CAN bus speed: 125 kbps — correct.
- [PASS] Controller: Arduino Uno R4 WiFi with WiFi UDP link to Jetson — correct.
- [PASS] Arduino powered from 12V logic rail via HW-140 buck converter (LM2596) outputting 6V VIN — correct. **CLOSED from previous audit** (prior finding was "5V rail").
- [PASS] AS5047P encoder: SPI interface — correctly documented.
- [PASS] RegenClamp required for base motor: 5Ω 100W mentioned (sl-alert at line 320–330) — however, the alert text says "RegenClamp V0.3 unit must be installed" but does not specify the resistor value (5Ω 100W). Not explicitly wrong but the resistor spec from the knowledge base is absent.
  - Severity: LOW — intentional omission acceptable at this level of detail.
- [PASS] Hard limits ±90° direction-aware — correctly documented in test results table.

#### Academic Writing

- [FINDING from previous audit] `<ol>` list in Design Rationale prose — **STATUS: CLOSED.** The "Design Rationale" section (lines 229–239) is now written entirely in prose paragraphs. No `<ol>` or `<ul>` lists present. ✅
- [FINDING from previous audit] Section HTML comment numbers out of order — **STATUS: CLOSED.** Sections now appear in correct ascending order in DOM: Requirements Cascade → Motor Specification → Control Architecture → Power Integration → Verification Targets.
- [VIOLATION] Em dash inside `<td>` body cell — Line 59: requirements cascade table cell contains "Yaw angular velocity ≥ 150°/s &mdash; motor and drive ratio must deliver sufficient speed under load". Em dashes inside `<td>` are prohibited.
  - Found: `&mdash;` inside `<td>` body cell
  - Required: Rewrite with colon or semicolon: "Yaw angular velocity ≥ 150°/s; the motor and drive ratio must deliver sufficient speed under load."
  - Severity: MEDIUM
- [PASS] No `<strong>` in body `<p>` prose.
- [PASS] No `§` symbol or emoji.
- [PASS] V-Model Traceability alert present: references RM-4 and RM-1.

#### Navigation

- [PASS] Prev/Next navigation present at bottom.

---

### height-adjustment/electrical-control.html

#### Factual Consistency

- [PASS] Height motor model: CHP-36GP-555 — correctly identified (line 82, 97). **CLOSED from previous audit** (prior finding was "LGYMSZSS"/"MY1016Z"). ✅
- [PASS] Supply voltage: 24V DC — correct.
- [PASS] Gearbox ratio: 27:1 — correct.
- [PASS] Stall current: ~21 A — correct.
- [PASS] Motor driver: Cytron MDDS10 — correct.
- [PASS] Pin assignments: Teensy Pin 3 → AN1 (PWM/speed), Pin 2 → DIG1 (direction) — correct. Matches knowledge base exactly.
- [PASS] DIP switch configuration not listed on this page — this is an intentional omission; the page focuses on the corrected pin assignment.
- [PASS] RegenClamp: 10Ω 50W correctly specified.
- [PASS] Brake resistor derivation: winding resistance 1.14Ω = 24V / 21A — correct.

#### Academic Writing

- [VIOLATION] Em dash inside image caption `<div>` — Line 295: `&mdash; Click to enlarge.` inside visible caption text below the height motor power diagram image.
  - Found: `&mdash; Click to enlarge.`
  - Required: Remove em dash; "Click to enlarge."
  - Severity: MEDIUM
- [PASS] No `<strong>` in body `<p>` prose.
- [PASS] No `§` symbol or emoji found.
- [PASS] No lists in body prose sections.
- [PASS] V-Model Traceability alert: references RM-3 and RM-1 — correct.

#### Navigation

- [FINDING from previous audit] Unclosed `<div>` tag breaking layout — **STATUS: PARTIALLY RESOLVED.** Line 350 contains `<div></div>` as the placeholder for a "Next" button that is absent. The page currently has a Prev button only (linking to `lift-structure-separation.html`) with no Next button — reflected in the empty `<div></div>` on line 350. This is not an unclosed tag (the div is closed) but the navigation row is structurally broken: there is no Next page linked.
  - Note: If the next expected page is the height-adjustment verification/testing page, a Next button should be added. If this is intentionally the last page in the section, the `<div></div>` placeholder should be removed.
  - Severity: MEDIUM

---

## Previously Identified Open Findings (Status Check)

| Finding | File | Previous Status | Current Status |
|---|---|---|---|
| PSU rated "8.3A" in body text | arm-actuation/electrical-integration.html | Open | **CLOSED** — now correctly states 8.8A |
| "I2C chain" description | arm-actuation/electrical-integration.html | Open | **CLOSED** — replaced with parallel dual-bus description |
| Strike topic `/strike_events` | padding/electrical-integration.html | Open | **CLOSED** — now correctly `/robot/strike_detected` |
| `<ol>` list in Design Rationale prose | rotation/electrical-control.html | Open | **CLOSED** — section is now prose paragraphs |
| Section HTML comments out of order | rotation/electrical-control.html | Open | **CLOSED** — order now ascending in DOM |
| Unclosed `<div>` nesting error | height-adjustment/electrical-control.html | Open | **PARTIALLY RESOLVED** — no unclosed div, but navigation row Missing Next button |
| `<strong>` in body `<p>` | padding/electrical-integration.html | Open | **CLOSED** — bold removed from IMU model name |
| Arduino powered from "5V rail" | rotation/electrical-control.html | Open | **CLOSED** — correctly states 12V via HW-140 buck converter |
| Height motor model "LGYMSZSS"/"MY1016Z" | height-adjustment/electrical-control.html | Open | **CLOSED** — correctly states CHP-36GP-555 |

---

## Intentional Omissions (Not Defects)

- `robot-mechanism.html` does not include motor specifications, firmware details, or kinematic derivations — these are correctly delegated to subsystem pages.
- `arm-actuation.html` does not contain full kinematic derivations, raw firmware code, or complete test data tables — correctly delegated to subsection pages (design-ideation, mechanical-design, testing-evaluation).
- `electrical-integration.html` does not document IMU wiring details — correctly delegated to `padding/electrical-integration.html`.
- `rotation/electrical-control.html` does not specify the brake resistor value (5Ω 100W) — acceptable at this summary level.
- `arm-actuation/firmware-software.html` does not include the Dynamic Speed Adaptation equation — correctly absent from active firmware documentation (it is archived in troubleshooting.html).
- Height motor DIP switch configuration not present on `height-adjustment/electrical-control.html` — acceptable given the page focus on corrected pin assignments; full DIP switch table would be expected in a detailed specification appendix.

---

## Recommended Fixes (Prioritised)

### High Severity (factually wrong or structurally broken)

1. **Section number inversion (3.3 before 3.2)** — `arm-actuation/electrical-integration.html`: Section 5.2.5.3.2 CAN Bus appears after Section 5.2.5.3.3 Dual-Rail Power. Renumber so headings read 3.1 → 3.2 → 3.3 in DOM order, or reorder sections.

### Medium Severity (academic writing violation or content gap)

2. **Em dash `&mdash;` in `<td>` cell** — `rotation/electrical-control.html` line 59: replace with semicolon or colon.
3. **Em dash `&mdash;` in image captions** — `arm-actuation.html` (×2), `arm-actuation/electrical-integration.html` (×2), `height-adjustment/electrical-control.html` (×1): remove from all `&mdash; Click to enlarge.` captions. Use "Click to enlarge." or add it as a separate parenthetical.
4. **Em dash `&mdash;` in link text** — `arm-actuation/electrical-integration.html` line 179: `Appendix 1 &mdash; Torque Calculations` → `Appendix 1: Torque Calculations`.
5. **`<strong>IMU Diagnostics Tab</strong>` in body `<p>`** — `padding/electrical-integration.html` line 217: remove bold tags.
6. **GUI version ambiguity** — `arm-actuation.html` (§0.6) and `firmware-software.html` (§4.1): References to `unified_GUI_V4.py` as the active production GUI should be corrected to `unified_GUI_V3.py`. If V4 is being actively used in testing, add a clarifying note that V3 is the production default and V4 is the in-development successor.
7. **Missing "Next" button** — `height-adjustment/electrical-control.html`: the navigation row has a Prev button but no Next button. Add Next button linking to the appropriate next page (testing-evaluation.html or back to height-adjustment.html as appropriate), or remove the empty `<div></div>` placeholder.
8. **Appendix navigation cards absent** — `arm-actuation.html`: navigation grid lacks the two appendix cards ("Testing and Evaluation (Appendix 3)" → `appendix-arm.html#a3-testing` and "Troubleshooting (Appendix 3)" → `appendix-arm.html#a3-troubleshooting`) specified in the academic_writer_summary.md §3.3.

### Low Severity (recommendation or style)

9. **HTML comment section numbering** — `robot-mechanism.html`: section comment `<!-- 4. VERIFICATION PLAN -->` should be `<!-- 5. VERIFICATION PLAN -->` to avoid two section-5 comments with number 4.
10. **`<ol>` list in Mechanical Stack prose** — `robot-mechanism.html` lines 349–354: convert to a compound prose sentence. Remove `<strong>` from list items.
11. **`<strong>` in `<td>` cells** — `arm-actuation/electrical-integration.html`: ODrive issues table and Damiao features table use `<strong>` for feature names in `<td>` cells. Low priority but marginally violates the spirit of the no-bold-in-prose rule.

---

*Validation performed against: `report_validator_agent.md` instruction set, `academic_writer_summary.md`, `lead_systems_integrator_summary.md`, `mechanical_agent_summary.md`, `academic_writing_skills.md`.*
*Next recommended validation: arm-actuation/mechanical-design.html, arm-actuation/design-ideation.html, arm-actuation/testing-evaluation.html, arm-actuation/troubleshooting.html, appendix-arm.html.*
