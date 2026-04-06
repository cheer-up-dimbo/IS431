# Agent Prompt: Full-Document Requirements Validation and V-Model Propagation

## Purpose
Use this prompt to commission an agent to traverse the entire IS431 engineering report, audit all requirement IDs, and propagate verification status according to the Systems Engineering V-Model.

---

## Prompt

You are performing a structured requirements audit on a GitHub Pages-hosted engineering report for a boxing training robot named BoxBunny (project IS431). The report is located at:

```
c:\Users\elgin\Documents\GitHub\IS431\
```

Your task is to:

### 1. Read and inventory all requirement IDs across the document tree

Read the following pages in order and extract every requirement identifier used (e.g. RM-1, RM-5a, PC-1, SR-x, etc.) and where each appears:

- `pages/robot-mechanism.html` (system-level: RM-1 to RM-7)
- `pages/robot-mechanism/base.html` and its sub-sections under `pages/robot-mechanism/base/`
- `pages/robot-mechanism/rotation.html` and its sub-sections under `pages/robot-mechanism/rotation/`
- `pages/robot-mechanism/height-adjustment.html` and its sub-sections under `pages/robot-mechanism/height-adjustment/`
- `pages/robot-mechanism/padding.html` and its sub-sections under `pages/robot-mechanism/padding/`
- `pages/robot-mechanism/arm-actuation.html` and its sub-sections under `pages/robot-mechanism/arm-actuation/`
- `pages/appendix-arm.html`
- `pages/appendix-lower.html`
- `pages/appendix-upper.html`
- `index.html` (main report, especially the design requirements and methodology sections)

### 2. Build a unified requirements traceability matrix

For each requirement ID found, produce a row in a traceability table with:
- **Req ID** (e.g. RM-1, RM-5a, PC-3)
- **Level** (System / Subsystem / Component)
- **Parent Req** (which higher-level requirement it traces to, if any)
- **Requirement text** (verbatim or summarised)
- **Subsystem / page where defined**
- **Verification method** (analysis / test / inspection / similarity)
- **Verification location** (page or sub-section where the test/validation is documented)
- **Current status** (Passed / Partial / Pending / Not tested)
- **Evidence** (measured value or brief note)

### 3. Identify gaps and inconsistencies

Flag any of the following:
- Requirement IDs that appear in one place but not another (orphaned requirements)
- Requirements with no listed verification method or result
- Verification results that exist on subsystem pages but have not been propagated back to the parent system-level verification matrix on `robot-mechanism.html`
- Requirement IDs that conflict (same ID, different text) across pages
- Requirements on subsystem pages that do not trace to a system-level RM-x requirement

### 4. Produce a propagation report

Write a structured markdown report (`/tmp/requirements_audit.md`) containing:
1. The full traceability matrix (as a markdown table)
2. A gap analysis section listing all issues found with specific file references
3. A propagation action list: concrete edits needed to bring all pages into alignment, listed as `File: [path] | Change: [description]`

### Constraints

- Do not make any changes to source files — this is an audit-only pass
- If a page references a sub-section by name but the sub-section file does not exist yet, note it as a broken link
- Use the system-level requirement definitions in `pages/robot-mechanism.html` (RM-1 to RM-7) as the ground truth
- The arm actuation subsystem uses internal PC-IDs (PC-1 to PC-5); map these to the system-level RM-5 row and note which PCs map to RM-5 vs. which are arm-internal only

### Output

Return your findings as the markdown file at `/tmp/requirements_audit.md`, and provide a short summary of:
- Total requirement IDs found
- Number of requirements with Passed / Partial / Pending / Not tested status
- Top 3 most critical gaps requiring immediate attention
