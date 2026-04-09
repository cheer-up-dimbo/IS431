# IS431 BoxBunny — Requirements Audit Report (Pass 3)
> Full re-audit: 2026-04-09 | All source files checked against live HTML

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

## 2. Gap Analysis — All Gaps Resolved ✅

| Gap | Severity | Description | Status |
|-----|----------|-------------|--------|
| GAP-A | Medium | `padding/testing-evaluation.html` used old PAD-PC-3/5 instead of PAD-PC-1/2 | ✅ **Resolved** — renamed throughout |
| GAP-B | Medium | PAD-PC-11/12/13 orphaned criteria in sub-page | ✅ **Resolved** — completely removed |
| GAP-C | Low | `appendix-arm.html` prose used bare `PC-2, PC-3, PC-4` | ✅ **Resolved** — updated to ARM-PC-2/3/4 |
| GAP-D | Low | V-Model alert in `padding/testing-evaluation.html` referenced bare `PC-3` and `PC-5` | ✅ **Resolved** — updated to PAD-PC-1 and PAD-PC-2 |

---

## 3. Confirmed Resolved (all passes)

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

## 4. V-Model Traceability Alert Coverage (Pass 3)

> **Standard:** Every `testing-evaluation.html` and all subsection pages with explicit RM-x references must open with a `<sl-alert variant="primary">` V-Model Traceability badge immediately below the `<h2>` heading.

### 4A. Testing & Evaluation Pages

| File | Requirements Tagged | Added This Pass |
|------|--------------------|----|
| `base/testing-evaluation.html` | RM-1, RM-2, RM-7, BASE-1 | ✅ Pass 3 |
| `rotation/testing-evaluation.html` | RM-4, ROT-1, ROT-2 | ✅ Pass 3 |
| `height-adjustment/testing-evaluation.html` | RM-3 | ✅ Pass 3 |
| `padding/testing-evaluation.html` | RM-6, PAD-PC-1, PAD-PC-2 | ✅ Pass 3 (GAP-D fix) |
| `arm-actuation/testing-evaluation.html` | RM-5, ARM-PC-1 to ARM-PC-5 | ✅ Pass 3 |

### 4B. Other Subsection Pages (applicable)

| File | Requirements Tagged | Added This Pass |
|------|--------------------|----|
| `base/design-ideation.html` | RM-1, RM-2 | ✅ Pass 3 |
| `base/mechanical-design.html` | RM-7, RM-1 | ✅ Pass 3 |
| `base/load-stability-analysis.html` | RM-1, RM-7 | ✅ Pass 3 |
| `height-adjustment/load-analysis.html` | RM-3 | ✅ Pass 3 |
| `padding/mechanical-design.html` | RM-6 | pre-existing ✅ |
| `padding/electrical-integration.html` | RM-6 | ✅ Pass 3 |
| `rotation/electrical-control.html` | RM-4, RM-1 | pre-existing ✅ |
| `height-adjustment/electrical-control.html` | RM-3, RM-1 | pre-existing ✅ |

### 4C. Not-Applicable Pages (no RM-x references, pure design/calculation content)

| File | Reason |
|------|--------|
| `rotation/design-ideation.html` | No system-level RM-x references |
| `rotation/mechanical-design.html` | No system-level RM-x references |
| `height-adjustment/design-ideation.html` | No system-level RM-x references |
| `height-adjustment/mechanical-design.html` | No system-level RM-x references |
| `arm-actuation/design-ideation.html` | No system-level RM-x references |
| `arm-actuation/mechanical-design.html` | No system-level RM-x references |
| `arm-actuation/electrical-integration.html` | No system-level RM-x references |

---

## 5. Summary

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
| Pages not applicable (no RM-x refs) | 7 |
| Pages missing alert | **0** ✅ |
