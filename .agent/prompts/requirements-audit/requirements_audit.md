# IS431 BoxBunny — Requirements Audit Report (Pass 4)
> Full re-audit: 2026-04-09 | All source files checked against live HTML
> Pass 4 adds 3 new pages discovered since Pass 3

---

## 1. Full Traceability Matrix

### 1A. System-Level Requirements (Ground Truth: `robot-mechanism.html`)

| Req ID | Requirement | Verification Method | Verification Location | Status | Evidence |
|--------|-------------|--------------------|-----------------------|--------|----------|
| RM-1 | Remain upright under worst-credible punching loads, FoS ≥ 1.5 | Tipping test + overturning-moment analysis | `testing.html` §5.2.1; `base.html` Validation | **Passed** | FoS ≥ 1.5 confirmed by overturning-moment method |
| RM-2 | Compact footprint preserving user footwork space | Footwork clearance observation | `testing.html` §5.2.1; `base.html` Validation | **Passed** | Zero foot contact, orthodox+southpaw stances |
| RM-3 | ≥ 400 mm vertical stroke, ≤ 32 s full travel | Full-stroke actuation test | `testing.html` §5.2.3 | **Pending** | Test not yet conducted; geometry confirms 400 mm |
| RM-4 | Yaw rotation ≥ 150°/s | 90° step command, measure time-to-target | `testing.html` §5.2.2 | **Pending** | Analytical: 205.7°/s calculated; physical pending |
| RM-5 | Execute strikes (90° in ≤ 0.70 s revised) | Strike speed timing, N=43 | `testing.html` §5.2.5; `arm-actuation.html` | **Partial** | Best: 0.64 s (Left Jab, 30 rad/s). Damiao PID overhead ~0.4–0.5 s |
| RM-6 | Absorb strikes; impact detection ≥ 95% TP | 60-punch detection test, 3 zones | `testing.html` §5.2.4 | **Pending** | Pipeline implemented; test not yet conducted |
| RM-7 | Portable: 1-person transport | Tip-and-roll test | `testing.html` §5.2.1; `base.html` | **Passed** | Single operator relocated robot within ≤ 5 min |

### 1B. Arm Subsystem Requirements (RM-5 decomposition — `arm-actuation.html`)

| Req ID | Requirement | Parent | Status | Evidence |
|--------|-------------|--------|--------|----------|
| RM-5a | 90° arm sweep in ≤ 0.70 s (revised) | RM-5 | **Passed** | 0.64 s best, N=43 |
| RM-5b | Three strike types: Jab, Hook, Uppercut | RM-5 | **Passed** | All 6 L/R variants validated, N=43 |
| RM-5c | Mass centralisation: minimise moment of inertia | RM-5 | **Passed** (design intent) | Co-located actuators; 3:1 helical-spur |
| RM-5d | Multi-layered safety: hardware, firmware, application | RM-5 | **Partial** | ARM-PC-3/4 tests pending; current watchdog deployed |
| RM-5e | Real-time impact detection across all target zones | RM-5 | **Pending** | Sensing pipeline built; 60-punch test pending |

### 1C. Arm Performance Criteria (`arm-actuation.html` + `appendix-arm.html`)

> All `ARM-PC-x` IDs are consistent across all pages. ✅

| PC ID | Criterion | Target | Status | Evidence |
|-------|-----------|--------|--------|----------|
| ARM-PC-1 | Strike speed (90° rotation) | ≤ 0.25 s (system) / ≤ 0.70 s (subsystem) | **Partial** (system) / **Passed** (subsystem) | 0.64 s best, N=43 |
| ARM-PC-2 | Sparring endurance | 5 min continuous, <60°C | **Pending** | Not yet tested |
| ARM-PC-3 | Regenerative braking safety | No PSU trip / 5 E-stops | **Pending** | Not yet tested |
| ARM-PC-4 | Multi-strike chain | 3-strike ≤ 5 s total | **Pending** | Not yet tested |
| ARM-PC-5 | Peak motor current | < 2.0 A per motor | **Passed** | 0.69 A max (Right Hook M4), N=43 |

### 1D. Padding Performance Criteria

> `PAD-PC-x` namespace is fully consistent across all pages. ✅

| PC ID | Criterion | Target | Status |
|-------|-----------|--------|--------|
| PAD-PC-1 | IMU strike detection rate | ≥ 95% TP | Pending |
| PAD-PC-2 | Impact force differentiation | Monotonic L < M < H | Pending |

---

## 2. Gap Analysis

### Pass 4 Net-New Gaps

| Gap | Severity | Description | Status |
|-----|----------|-------------|--------|
| GAP-P4-A | **Low** | 3 new pages discovered not listed in Pass 3 V-Model coverage table: `arm-actuation/firmware-software.html`, `rotation/load-analysis.html`, `rotation/timing-belt-selection.html` | ✅ **Classified** — all confirmed N/A (no RM-x references; pure design/calculation content) |
| GAP-P4-B | **Low** | `robot-mechanism.html` hub uses RM-x IDs only in SVG text elements and inline prose — not in machine-parseable `id` attributes, making automated RM-x grep return no matches on that file alone | ℹ️ **Informational** — IDs are present and correct in rendered HTML; no fix required for traceability |

> **Net-new actionable gaps: 0** — All Pass 4 findings are informational/classification updates only.

### All Prior Gaps (Pass 1–3) — All Resolved ✅

| Gap | Resolution |
|---|---|
| GAP-01: ARM-PC-1 not propagated to testing.html RM-5 | ✅ 0.64 s / Partial now in both ARM-PC-1 and RM-5 rows |
| GAP-02: testing.html showing bare `—` for RM-3/4/5/6 | ✅ Explicit Pending for RM-3/4/6; Partial for RM-5 |
| GAP-03: Namespace collision bare PC-x in appendix-arm tables | ✅ All table cells updated to ARM-PC-x |
| GAP-04: PAD-PC numbering gap (orphaned 3/5) | ✅ Updated to PAD-PC-1/2 in hub pages |
| GAP-05: Broken troubleshooting cross-references | ✅ All 10 files updated; zero broken links |
| GAP-06: base.html RM-7 Partial/Passed contradiction | ✅ Detail table updated to Pass with test evidence |
| GAP-07: rotation.html duplicate 3:1 paragraph | ✅ Duplicate removed; 1:3.5 only |
| GAP-08: robot-mechanism.html RM-3/4/6 bare `—` status | ✅ Updated to Pending |
| GAP-09: report-nav links to deleted files | ✅ report-nav.js updated |
| GAP-A: testing-evaluation.html PAD-PC-3/5 mismatch | ✅ Renamed to PAD-PC-1/2 throughout |
| GAP-B: PAD-PC-11/12/13 orphaned criteria | ✅ Completely removed |
| GAP-C: appendix-arm.html bare PC-2/3/4 in prose | ✅ Updated to ARM-PC-2/3/4 |
| GAP-D: V-Model alert bare PC-3/PC-5 | ✅ Updated to PAD-PC-1/PAD-PC-2 |

---

## 3. V-Model Traceability Alert Coverage (Pass 4)

> **Standard:** Every subsection page with explicit RM-x references must open with a `<sl-alert variant="primary">` V-Model Traceability badge immediately below the `<h2>` heading.

### 3A. Testing & Evaluation Pages

| File | Requirements Tagged | Alert Status |
|------|--------------------|---|
| `base/testing-evaluation.html` | RM-1, RM-2, RM-7, BASE-1 | ✅ Has alert |
| `rotation/testing-evaluation.html` | RM-4, ROT-1, ROT-2 | ✅ Has alert |
| `height-adjustment/testing-evaluation.html` | RM-3 | ✅ Has alert |
| `padding/testing-evaluation.html` | RM-6, PAD-PC-1, PAD-PC-2 | ✅ Has alert |
| `arm-actuation/testing-evaluation.html` | RM-5, ARM-PC-1 to ARM-PC-5 | ✅ Has alert |

### 3B. Other Subsection Pages (applicable)

| File | Requirements Tagged | Alert Status |
|------|--------------------|---|
| `base/design-ideation.html` | RM-1, RM-2 | ✅ Has alert |
| `base/mechanical-design.html` | RM-7, RM-1 | ✅ Has alert |
| `base/load-stability-analysis.html` | RM-1, RM-7 | ✅ Has alert |
| `height-adjustment/load-analysis.html` | RM-3 | ✅ Has alert |
| `padding/mechanical-design.html` | RM-6 | ✅ Has alert |
| `padding/electrical-integration.html` | RM-6 | ✅ Has alert |
| `rotation/electrical-control.html` | RM-4, RM-1 | ✅ Has alert |
| `height-adjustment/electrical-control.html` | RM-3, RM-1 | ✅ Has alert |

### 3C. Not-Applicable Pages (no RM-x references — alert not required)

| File | Reason |
|------|--------|
| `rotation/design-ideation.html` | No system-level RM-x references |
| `rotation/mechanical-design.html` | No system-level RM-x references |
| `rotation/load-analysis.html` | **[NEW Pass 4]** Pure structural calculation; no RM-x refs |
| `rotation/timing-belt-selection.html` | **[NEW Pass 4]** Pure belt-drive selection; no RM-x refs |
| `height-adjustment/design-ideation.html` | No system-level RM-x references |
| `height-adjustment/mechanical-design.html` | No system-level RM-x references |
| `arm-actuation/design-ideation.html` | No system-level RM-x references |
| `arm-actuation/mechanical-design.html` | No system-level RM-x references |
| `arm-actuation/electrical-integration.html` | No system-level RM-x references |
| `arm-actuation/firmware-software.html` | **[NEW Pass 4]** Two-tier firmware architecture doc; no RM-x refs |

---

## 4. Summary

### Active Gaps: **0** — All requirements documentation is consistent ✅

### Requirement Counts

| Namespace | Count | IDs |
|-----------|-------|-----|
| System (RM-x) | 7 | RM-1 to RM-7 |
| Arm subsystem (RM-5x) | 5 | RM-5a to RM-5e |
| Arm Performance Criteria | 5 | ARM-PC-1 to ARM-PC-5 |
| Padding Performance Criteria | 2 | PAD-PC-1, PAD-PC-2 |
| **Total unique logical criteria** | **19** | — |

### Status Breakdown (RM-x)

| Status | Count | Requirements |
|--------|-------|---|
| Passed | 3 | RM-1, RM-2, RM-7 |
| Partial | 1 | RM-5 |
| Pending | 3 | RM-3, RM-4, RM-6 |

### Status Breakdown (ARM-PC-x)

| Status | Count |
|--------|-------|
| Passed | 2 (ARM-PC-1 subsystem-revised, ARM-PC-5) |
| Partial | 1 (ARM-PC-1 against original 0.25 s target) |
| Pending | 3 (ARM-PC-2, ARM-PC-3, ARM-PC-4) |

### V-Model Alert Coverage

| Status | Count |
|--------|-------|
| Pages with alert (applicable) | 13 |
| Pages not applicable (no RM-x refs) | 10 (+3 new pages since Pass 3) |
| Pages missing alert | **0** ✅ |

### Top 3 Gaps Requiring Attention

> **None — all requirement documentation gaps are resolved.**
>
> The 3 outstanding **Pending** requirements (RM-3, RM-4, RM-6) are awaiting **physical testing**, not documentation work. These are not documentation gaps; they are known engineering work items pending lab time.
