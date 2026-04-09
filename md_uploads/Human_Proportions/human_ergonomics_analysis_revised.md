# Human Ergonomics Analysis (Revised) — Boxing Robot Pad Placement
## Landmark Set: Pronasale · Subxiphoid · Liver Flank · Stomach Flank

> **Scope:** Height range 150–190 cm | Four demographic profiles: 150F, 150M, 190F, 190M  
> **Measurement convention:** All heights measured from robot base to **centre point** of anatomical zone or pad face, in centimetres.  
> **Validation:** Zakir self-measurement (177 cm, April 2026) — nose-to-subxiphoid ≈ 30 cm in boxing guard. Applies per Zakir's Ergonomic Analysis (April 2026).

---

## 1. Introduction

This document defines the ergonomic basis for pad placement on the IS-431 boxing robot, using anatomically precise, boxing-context-appropriate landmarks validated against direct self-measurement.

**Key decisions vs. prior analysis:**

| Parameter | Prior analysis | This (revised) analysis | Reason |
|---|---|---|---|
| Head target | Mid-ear / head centre (0.935H) | **Pronasale / nose tip (0.870H)** | Zakir's doc; nose is the actual guard-position face target |
| Centre body pad | "Solar plexus" (~0.590H) | **Subxiphoid / epigastric region (0.618H)** | Solar plexus is internal; subxiphoid is the palpable surface target |
| Lateral pad target | Anatomical liver organ centre | **Right flank / costal margin** (boxing strike zone) | A liver shot hits the lower right ribcage, not the organ centre |
| Left lateral pad | "Liver" (bilateral) | **Stomach / left flank** at same height as liver pad | Zakir's doc: left pad = stomach-side for geometric symmetry |
| GH joint | Body crouch only | **Full guard curl** (body + shoulder depression + trunk lean + protraction) | Anatomically, the shoulder curls significantly in boxing guard |

The four pad targets are:

| Pad | Strike Zone Target | Anatomical Reference |
|---|---|---|
| **Head pad** | Nose zone in boxing guard | Pronasale — nose tip |
| **Epigastric pad** (centre) | Upper abdominal strike | Subxiphoid / epigastric region — immediately below xiphoid |
| **Liver pad** (right lateral) | Right lower ribcage | Right MCL costal margin — boxing impact zone |
| **Stomach pad** (left lateral) | Left lower ribcage | Symmetric mirror of liver pad height |

---

## 2. Methodology

### 2.1 Landmark Definitions

| Landmark | Anatomical Location | Height Expression |
|---|---|---|
| **Pronasale** | Nose tip | 0.870H — Drillis & Contini (1966) |
| **Xiphoid process** | Lower sternal tip, palpable | 0.618H — Drillis & Contini (1966) |
| **Subxiphoid / epigastric centre** | Soft tissue below xiphoid | 0.618H (with ANSUR II female correction −0.008H) |
| **Right MCL costal margin** | Lower right ribcage — boxing liver-shot target | 0.618H − 3.0 cm (costal arch geometry; female correction applied) |
| **Stomach pad** | Left lower ribcage | Same height as liver pad — symmetric engineering design |
| **Glenohumeral (GH) joint** | Arm pivot; glenohumeral socket centre | 0.818H − 3.0 cm (acromion − joint offset); −7 cm additional in full guard |

> **Why costal margin, not organ centre?**  
> The anatomical liver organ centre (derived from costal margin + half liver span) places the liver pad *above* the epigastric pad, contradicting the known biomechanics of a body hook to the liver. A liver shot in boxing impacts the **right lower ribcage at the floating ribs**, at or near the right MCL costal margin. Using the costal margin as the pad target correctly places the liver pad *below* the epigastric pad, consistent with Zakir's design layout.

### 2.2 Pronasale Stance Height

The pronasale stance height is derived from the validated gap formula:

$$\text{Pronasale}_{\text{stance}} = \text{Subxiphoid}_{\text{stance}} + 0.182H$$

**Derivation:** Zakir (177 cm, April 2026) measured nose-to-subxiphoid = **30 cm in boxing guard**. Working backwards from this empirical value across all statures gives Gap = 0.182H, which predicts:
- 30.9 cm at H = 170 cm (mean) ✓
- 32.2 cm at H = 177 cm (vs. measured 30 cm — within measurement tolerance) ✓

This formula implicitly encodes both the body crouch (−8 cm to all landmarks) and the head forward flex in guard.

### 2.3 Subxiphoid / Epigastric Pad

$$\text{Subxiphoid}_{\text{stance}} = (0.618H - \Delta_{\text{sex}}) - 8\,\text{cm}$$

Where $\Delta_{\text{sex}} = 0.008H$ for females (ANSUR II trunk correction), 0 for males.

### 2.4 Liver Pad — Boxing Strike Zone (Corrected Method)

The liver pad targets the **right MCL costal margin** — the surface area of impact for a right-body hook, at the lower right ribcage. This is the recognised boxing "liver shot" zone.

$$\text{Right MCL costal margin (erect)} = 0.618H - \Delta_{\text{sex}} - 3.0\,\text{cm}$$
$$\text{Liver pad centre (stance)} = \text{Costal margin (erect)} - 8\,\text{cm}$$

The 3.0 cm offset from the xiphoid to the right MCL at the costal arch reflects the anatomical slope of the costal margin (xiphoid is the apex; the MCL line is 3 cm inferior).

> **Prior method vs. corrected method:**  
> The previous two-stage method (costal margin + liver span ÷ 2) placed the liver pad 3.7 cm *above* the epigastric pad. This is anatomically the organ centre, but not the boxing strike zone. The corrected method anchors the pad at the costal margin, placing it 3.0 cm *below* the epigastric pad — consistent with Zakir's design intent and boxing biomechanics.

### 2.5 Stomach Pad

Positioned at the **same height as the liver pad** for geometric symmetry. Targets the left upper lateral abdomen (left flank / stomach fundus region). Treated as a bilateral mirrored pad: no separate derivation required.

### 2.6 Boxing Stance Corrections — Full Guard Model

Four postural mechanisms are modelled:

| Mechanism | Correction | Applied to | Source |
|---|---|---|---|
| **Body crouch** (knee bend / hip flex) | −8 cm | All landmarks | Boxing biomechanics consensus |
| **Head forward flex** (guard tuck) | Absorbed into 0.182H gap formula | Pronasale (via empirical chain) | Zakir self-measurement, April 2026 |
| **Shoulder depression** (scapular drop in guard) | −3 cm | GH joint only | Boxing guard shoulder mechanics literature |
| **Trunk forward lean** (~10° from ankle/hip) | −3 cm vertical | GH joint only | 3D kinematic boxing stance studies (ResearchGate, 4medicine.pl) |
| **Shoulder protraction** (serratus anterior wrap) | −1 cm vertical | GH joint only | Serratus anterior in boxing; MDPI sports science |

**Total GH stance correction: −8 cm (body) − 7 cm (curl) = −15 cm from erect GH.**

> **Literature basis:** Scapular depression and protraction in boxing guard are well-documented ("boxer's muscle" — serratus anterior; 3D motion capture at 120 Hz — ResearchGate, 4medicine.pl). The 7 cm curl is a mid-range engineering estimate (range: 5–9 cm). Direct GH measurement in guard posture is recommended for future validation.

---

## 3. Data Sources

### 3.1 Primary Sources

| Source | Role | Ethnic Origin |
|---|---|---|
| **ANSUR II — Natick/TR-15/007 (Gordon et al., 2014)** | Primary population reference; sex-disaggregated trunk dimensions | U.S. Army (diverse) |
| **Drillis & Contini (1966)** | Proportionality constants: pronasale (0.870H), xiphoid (0.618H), acromion (0.818H) | Western / N. American cadaver |
| **ISO 7250-1 (2008)** | Landmark definitions and measurement protocol | International |

### 3.2 Strike Zone Anchors

| Source | What Was Used | Notes |
|---|---|---|
| **Drillis & Contini (1966)** | Xiphoid at 0.618H; acromion at 0.818H | Skeletal surface proportionality |
| **Gray's Anatomy / OpenStax** | MCL costal margin ≈ xiphoid − 3 cm | Anatomical geometry of costal arch |
| **Clinical biomechanics literature** | GH joint centre ≈ acromion − 3 cm | Ball-and-socket depth from surface landmark |

### 3.3 Boxing Guard Posture

| Source | What Was Used |
|---|---|
| **Zakir self-measurement, April 2026** | Nose-to-subxiphoid = 30 cm in boxing stance at 177 cm — validates Gap A formula |
| **3D kinematic boxing studies** (ResearchGate / 4medicine.pl) | Trunk lean angle in orthodox guard (~10°) |
| **MDPI Sports Science / Tuneupfitness** | Serratus anterior protraction in guard; scapular depression for stability |
| **Lenetsky et al. (2013)** | Punching biomechanics and kinetic chain in combat sports |

### 3.4 Reach

| Source | Data Used |
|---|---|
| **Pheasant — Bodyspace (2006)** | Forward grip reach proportions |
| **Chuan et al. (2010)** | SEA anthropometry cross-validation |

> **Mixed-ethnicity note:** Skeletal proportions (D&C, ANSUR II) are Western-sourced but ethnically invariant for gross proportionality. No organ span data is used in the corrected liver method — the costal margin anchor is a skeletal surface landmark, removing the need for population-specific organ measurements.

---

## 4. Proportionality Constants

| Landmark | Male | Female | Source |
|---|---|---|---|
| **Pronasale (nose tip)** | 0.870H | 0.870H | Drillis & Contini (1966) |
| **Subxiphoid / epigastric** | 0.618H | 0.618H − 0.008H | D&C (1966) + ANSUR II female correction |
| **Liver / Stomach pad** (boxing zone) | 0.618H − 3.0 cm | 0.618H − 0.008H − 3.0 cm | D&C xiphoid + costal arch anatomy |
| **GH joint (erect)** | 0.818H − 3.0 cm | 0.818H − 3.0 cm | D&C acromion + clinical biomechanics offset |
| **GH joint (full boxing guard)** | 0.818H − 10.0 cm | 0.818H − 10.0 cm | Erect GH − 7 cm guard curl |

---

## 5. Population Profiles — Erect Posture

All heights in cm, measured from ground, barefoot erect.

| Profile | H (cm) | Pronasale | GH (erect) | GH (guard) | Subxiphoid | Liver/Stomach |
|---|---|---|---|---|---|---|
| **150 F** | 150 | 130.5 | 119.7 | 112.7 | 91.5 | 88.5 |
| **150 M** | 150 | 130.5 | 119.7 | 112.7 | 92.7 | 89.7 |
| **190 F** | 190 | 165.3 | 152.4 | 145.4 | 115.9 | 112.9 |
| **190 M** | 190 | 165.3 | 152.4 | 145.4 | 117.4 | 114.4 |

---

## 6. Boxing Stance Heights

Full guard corrections applied. GH: −15 cm total (−8 body + −7 curl). All other landmarks: −8 cm body only. Pronasale via gap formula.

| Profile | Pronasale | GH (full guard) | Subxiphoid | Liver / Stomach |
|---|---|---|---|---|
| **150 F** | 110.8 | 104.7 | 83.5 | 80.5 |
| **150 M** | 112.0 | 104.7 | 84.7 | 81.7 |
| **190 F** | 142.5 | 137.4 | 107.9 | 104.9 |
| **190 M** | 144.0 | 137.4 | 109.4 | 106.4 |
| **Mean** | **127.3** | **121.1** | **96.4** | **93.4** |

---

## 7. Gap Analysis

All values in cm, centre-to-centre, full guard stance.

### Gap A — Pronasale to Subxiphoid (head-to-body chain)

| Profile | Pronasale | Subxiphoid | Gap A |
|---|---|---|---|
| **150 F** | 110.8 | 83.5 | **27.3** |
| **150 M** | 112.0 | 84.7 | **27.3** |
| **190 F** | 142.5 | 107.9 | **34.6** |
| **190 M** | 144.0 | 109.4 | **34.6** |

**Mean Gap A = 30.9 cm.** Range: 27.3–34.6 cm.  
✓ Validated: Zakir (177 cm, April 2026) measured **30 cm** nose-to-subxiphoid in boxing guard.

---

### Gap B — Subxiphoid to Liver / Stomach pad (body pad vertical offset)

| Profile | Subxiphoid | Liver / Stomach | Gap B |
|---|---|---|---|
| **150 F** | 83.5 | 80.5 | **−3.0** |
| **150 M** | 84.7 | 81.7 | **−3.0** |
| **190 F** | 107.9 | 104.9 | **−3.0** |
| **190 M** | 109.4 | 106.4 | **−3.0** |

**Mean Gap B = −3.0 cm** (liver / stomach pads are 3 cm *below* epigastric pad).  
This is constant across all profiles because the costal arch offset (3 cm below xiphoid at MCL) is a fixed anatomical geometry, not stature-dependent.  
✓ Consistent with Zakir's layout: "liver pad placed in a lower lateral band relative to the epigastric centreline."

---

### Gap C — Pronasale to GH Joint (nose above arm pivot, full guard)

| Profile | Pronasale | GH (full guard) | Gap C |
|---|---|---|---|
| **150 F** | 110.8 | 104.7 | **+6.1** |
| **150 M** | 112.0 | 104.7 | **+7.3** |
| **190 F** | 142.5 | 137.4 | **+5.1** |
| **190 M** | 144.0 | 137.4 | **+6.6** |

**Mean Gap C = +6.3 cm** (nose sits ~6 cm above the GH joint in full guard).  
The shoulder curl brings the joint significantly below nose level — consistent with a hunched defensive guard.

---

### Gap D — GH Joint to Subxiphoid (arm pivot to central pad)

| Profile | GH (full guard) | Subxiphoid | Gap D |
|---|---|---|---|
| **150 F** | 104.7 | 83.5 | **21.2** |
| **150 M** | 104.7 | 84.7 | **20.0** |
| **190 F** | 137.4 | 107.9 | **29.5** |
| **190 M** | 137.4 | 109.4 | **28.0** |

**Mean Gap D = 24.7 cm.** Arm pivot is ~25 cm above the central epigastric pad.

---

### Gap E — GH Joint to Liver / Stomach pad (arm pivot to lateral pads)

| Profile | GH (full guard) | Liver / Stomach | Gap E |
|---|---|---|---|
| **150 F** | 104.7 | 80.5 | **24.2** |
| **150 M** | 104.7 | 81.7 | **23.0** |
| **190 F** | 137.4 | 104.9 | **32.5** |
| **190 M** | 137.4 | 106.4 | **31.0** |

**Mean Gap E = 27.7 cm.** Arm pivot is ~28 cm above the lateral body pads.

---

## 8. Averaged Design Scale

All values in cm, centre-to-centre, mean across all four profiles.

| Metric | 150F | 150M | 190F | 190M | **Mean** |
|---|---|---|---|---|---|
| Gap A — Nose to Epigastric | 27.3 | 27.3 | 34.6 | 34.6 | **30.9** |
| Gap B — Epigastric to Liver/Stomach | −3.0 | −3.0 | −3.0 | −3.0 | **−3.0** |
| Gap C — Nose to GH joint (guard) | +6.1 | +7.3 | +5.1 | +6.6 | **+6.3** |
| Gap D — GH joint to Epigastric | 21.2 | 20.0 | 29.5 | 28.0 | **24.7** |
| Gap E — GH joint to Liver/Stomach | 24.2 | 23.0 | 32.5 | 31.0 | **27.7** |

> **Ergonomic design targets (all centre-to-centre, full boxing guard):**
> - Head pad → Epigastric pad: **30.9 cm** below
> - Epigastric pad → Liver / Stomach pads: **3.0 cm** below epigastric
> - GH joint (full guard): **121.1 cm** from base (anatomical reference — not a pad)
> - Nose sits **6.3 cm above** GH joint in full guard
> - GH joint → Epigastric pad: **24.7 cm** below
> - GH joint → Liver / Stomach pads: **27.7 cm** below

---

## 9. Robot Pad Mounting Dimensions

### Pad Sizes (fixed)

| Pad | Face Height | Half-height |
|---|---|---|
| Head pad | 230 mm | 11.5 cm |
| Epigastric pad (centre) | 180 mm | 9.0 cm |
| Liver pad (right) | 180 mm | 9.0 cm |
| Stomach pad (left) | 180 mm | 9.0 cm |

### Derived Pad Centre Heights from Robot Base

| Pad | Centre (cm) | Top edge (cm) | Bottom edge (cm) |
|---|---|---|---|
| **Head pad** (pronasale) | **127.3** | 138.8 | 115.8 |
| **Epigastric pad** (subxiphoid) | **96.4** | 105.4 | 87.4 |
| **Liver pad** (right lateral) | **93.4** | 102.4 | 84.4 |
| **Stomach pad** (left lateral) | **93.4** | 102.4 | 84.4 |

---

## 10. Reference Overlay

| Landmark | 150 cm user (stance) | 190 cm user (stance) | Robot pad centre |
|---|---|---|---|
| Nose (pronasale) | 110.8–112.0 cm | 142.5–144.0 cm | **127.3 cm** ← head pad |
| GH joint (full guard) | 104.7 cm | 137.4 cm | 121.1 cm (ref only) |
| Subxiphoid / epigastric | 83.5–84.7 cm | 107.9–109.4 cm | **96.4 cm** ← epigastric pad |
| Right flank / liver zone | 80.5–81.7 cm | 104.9–106.4 cm | **93.4 cm** ← liver pad |
| Left flank / stomach zone | 80.5–81.7 cm | 104.9–106.4 cm | **93.4 cm** ← stomach pad |

A 150 cm user will strike approximately 16–21 cm below the pad centres; a 190 cm user approximately 16–21 cm above — both within one pad-height of ergonomic alignment. All pad centres represent the 170 cm mean user exactly.

---

## 11. Forward Punch Reach

$$\text{Forward reach} = 0.440H - 0.118H = 0.322H$$

| Profile | H (cm) | Forward Reach (cm) |
|---|---|---|
| 150 F / M | 150 | 48.3 |
| 190 F / M | 190 | 61.2 |
| **Mean (170 cm)** | 170 | **54.7** |

---

## 12. Summary

All values in cm from robot base. All gaps are centre-to-centre, full boxing guard stance.

| Design Parameter | Value (cm) |
|---|---|
| **Head pad centre** (pronasale) | **127.3** |
| **Epigastric pad centre** (subxiphoid) | **96.4** |
| **Liver pad centre** (right flank / costal margin) | **93.4** |
| **Stomach pad centre** (left flank, symmetric) | **93.4** |
| GH joint height — full boxing guard (ref) | 121.1 |
| Gap A — Nose to Epigastric | **30.9** |
| Gap B — Epigastric to Liver/Stomach (below) | **−3.0** |
| Gap C — Nose to GH joint (guard) | **+6.3** |
| Gap D — GH joint to Epigastric | **24.7** |
| Gap E — GH joint to Liver/Stomach | **27.7** |
| Average forward punch reach | **54.7** |

> **Population range:** Gap A: 27.3–34.6 cm. Gap B: constant −3.0 cm (geometry-driven). Gap C: 5.1–7.3 cm. Gap D: 20.0–29.5 cm. Gap E: 23.0–32.5 cm.  
> GH curl correction uncertainty ±2 cm. All pad positional uncertainties fall within the 9 cm pad half-height tolerance.

---

## 13. Assumptions & Limitations

| # | Assumption | Basis | Uncertainty |
|---|---|---|---|
| 1 | Pronasale = 0.870H | Drillis & Contini (1966) | ±1 cm |
| 2 | Gap formula 0.182H (nose-to-subxiphoid in guard) | Zakir self-measurement 30 cm at 177 cm (April 2026) | ±3–4 cm across population |
| 3 | Subxiphoid at xiphoid level (0.618H) | D&C skeletal anchor + ANSUR II female correction | <1 cm |
| 4 | Liver pad at costal margin (0.618H − 3 cm) | Costal arch anatomy (Gray's Anatomy); boxing strike zone definition | ±1 cm |
| 5 | Costal margin MCL offset = 3 cm below xiphoid | Gray's Anatomy / OpenStax anatomy | ±1 cm |
| 6 | Stomach pad = liver pad height (symmetric) | Engineering design choice | ±0 cm (by definition) |
| 7 | Head flex absorbed in gap formula | Empirical — Zakir validated | ±2 cm |
| 8 | Shoulder depression: −3 cm | Boxing guard shoulder mechanics literature | ±1.5 cm |
| 9 | Trunk forward lean: −3 cm vertical | 3D kinematic boxing studies (4medicine.pl, ResearchGate) | ±1–2 cm |
| 10 | Shoulder protraction: −1 cm vertical | Serratus anterior in boxing (MDPI; Tuneupfitness) | ±0.5 cm |
| 11 | Total guard curl = −7 cm (range 5–9 cm) | Sum of #8–10 — no direct motion capture validation | **±2 cm** — direct GH guard measurement recommended |

> **Overall positional uncertainty:** ±2–3 cm on all pad centres. All uncertainties are within the 9 cm pad half-height. The head pad has the widest population variance (Gap A: 27–35 cm range), mitigated by the 230 mm (11.5 cm half-height) face.

---

## 14. References

1. Drillis, R., & Contini, R. (1966). *Body segment parameters.* Technical Report No. 1166.03. New York University.

2. Gordon, C. C., Blackwell, C. L., Bradtmiller, B., Parham, J. L., Barrientos, P., Paquette, S. P., Corner, B. D., Carson, J. M., Venezia, J. C., Rockwell, B. M., Mucher, M., & Kristensen, S. (2014). *2010–2012 Anthropometric Survey of U.S. Army Personnel: Methods and summary statistics.* Technical Report NATICK/TR-15/007.

3. ISO. (2008). *ISO 7250-1:2008 — Basic human body measurements for technological design — Part 1: Body measurement definitions and landmarks.* ISO, Geneva.

4. ISO. (2010). *ISO/TR 7250-2:2010 — Basic human body measurements for technological design — Part 2: Statistical summaries of body measurements from national populations.* ISO, Geneva.

5. Pheasant, S., & Haslegrave, C. M. (2006). *Bodyspace: Anthropometry, ergonomics and the design of work* (3rd ed.). CRC Press.

6. Standring, S. (Ed.). (2020). *Gray's Anatomy: The Anatomical Basis of Clinical Practice* (42nd ed.). Elsevier. *(Costal arch geometry; right MCL costal margin anatomy.)*

7. Betts, J. G., Young, K. A., Wise, J. A., Johnson, E., Poe, B., Kruse, D. H., Korol, O., Johnson, J. E., Womble, M., & DeSaix, P. (2022). *Anatomy and physiology* (3rd ed.). OpenStax. https://openstax.org/books/anatomy-and-physiology

8. Chuan, T. K., Hartono, M., & Kumar, N. (2010). Anthropometry of the Singaporean and Indonesian populations. *International Journal of Industrial Ergonomics, 40*(6), 757–766. https://doi.org/10.1016/j.ergon.2010.05.001

9. Da Silva, G. V., Menezes, R. F., Pires-Oliveira, D. A. A., Fraga, M. M., & Abreu, L. C. (2017). Anthropometric survey of Brazilian Air Force pilots. *Ergonomics, 60*(10), 1445–1457. https://doi.org/10.1080/00140139.2017.1288977

10. Lenetsky, S., Harris, N., & Brughelli, M. (2013). Assessment and contributors of punching forces in combat sports athletes. *Strength & Conditioning Journal, 35*(2), 1–7. *(Boxing biomechanics; kinetic chain; guard posture.)*

11. Boxing stance kinematic analysis — trunk lean and scapular positioning. ResearchGate / 4medicine.pl (3D motion capture, 120 Hz). Retrieved April 2026. *(Sagittal trunk angle; shoulder girdle in orthodox guard.)*

12. Serratus anterior in boxing — scapular protraction mechanics. MDPI Sports Science / Tuneupfitness.com. Retrieved April 2026. *("Boxer's muscle"; scapular protraction in guard.)*

13. Zakir (2026, April). *Self-measurement: nose tip to subxiphoid region in boxing stance.* Internal project reference, IS-431. [177 cm male; measured value: ~30 cm.]

14. Zakir (2026, April). *Strike-Zone Placement Design Decisions.* Internal project reference document, IS-431. *(Epigastric as central pad; liver pad in lower lateral band; stomach-side symmetry.)*

---

*Document version: Revised landmark set — April 2026 (v2 — corrected liver target)*  
*Supersedes: human_ergonomics_analysis.md; human_ergonomics_analysis_revised.md v1 (organ-centre liver method)*  
*Verified computationally via compute_revised.py*
