# Human Ergonomics Analysis — Boxing Robot Pad Placement

> **Scope:** Height range 150–190 cm | Four demographic profiles: 150F, 150M, 190F, 190M  
> **Pads analysed:** Head pad · Solar Plexus pad · Liver pad (both side pads use liver proportions)  
> **Measurement convention:** All heights measured from ground to **centre point** of anatomical zone or pad face.

---

## 1. Data Sources

| Source | Role |
|---|---|
| Drillis & Contini (1966) | Foundation body-segment proportionality constants (fraction of stature H) |
| ANSUR II (2012) — Natick/TR-15/007 | Male/female mean segment ratios; chest depth; sex-based corrections |
| ISO 7250-1 / ISO/TR 7250-2 | Landmark definitions; national population statistical tables |
| OpenStax Human Anatomy, 3rd Ed. (2022) | Organ position: liver, solar plexus (celiac plexus), xiphoid process |
| Pheasant — *Bodyspace*, 4th Ed. (2018) | Forward reach and functional reach tables by stature percentile |
| SEA Anthropometry studies, PLOS ONE / ResearchGate (2015–2023) | Malaysian/Singaporean stature and trunk proportion corrections |
| NHANES 2017–2020 (CDC) | Adult stature and upper arm length — cross-validation |

---

## 2. Anthropometric Proportionality Constants

All landmarks expressed as a fraction of total stature **H**, measured from the ground.  
Based on Drillis & Contini (1966) with ANSUR II sex corrections applied.

| Landmark | Male (fraction of H) | Female (fraction of H) | Anatomical Basis |
|---|---|---|---|
| **Head pad centre** | 0.935 | 0.935 | Mid-ear / centre between crown and chin |
| **Solar plexus pad centre** | 0.590 | 0.582 | ~3 cm below xiphoid (T10 level); centre of epigastric zone |
| **Liver pad centre** | 0.638 | 0.630 | Right costal margin, ribs 8–10; centre of common strike zone |
| **Shoulder (acromion) front** | 0.818 | 0.818 | Glenohumeral joint — punch origin |
| **Chest depth** | 0.120 | 0.115 | ANSUR II mean; subtracted from arm length for forward reach |

> **Female-specific correction:** ANSUR II shows females have proportionally longer legs and a shorter trunk relative to stature. This lowers all abdominal landmarks by approximately **0.008 H** relative to males. The head centre fraction remains the same (head-to-stature ratio is not sex-dimorphic at this scale).

> **SEA correction (informational):** Studies on Malaysian and Singaporean adults (2015–2023) show mean statures of 167–170 cm (male) and 155–158 cm (female) — comfortably within the 150–190 cm target range. Proportionality constants align closely with ANSUR II values; no separate coefficient adjustment required for this analysis.

---

## 3. Population Profiles — Erect Posture

Absolute centre-point heights (cm) derived from stature × proportionality constant.

| Profile | Stature H (cm) | Head Centre (cm) | Solar Plexus Centre (cm) | Liver Centre (cm) |
|---|---|---|---|---|
| **150 F** | 150 | 140.3 | 87.3 | 94.5 |
| **150 M** | 150 | 140.3 | 88.5 | 95.7 |
| **190 F** | 190 | 177.7 | 110.6 | 119.7 |
| **190 M** | 190 | 177.7 | 112.1 | 121.2 |

---

## 4. Boxing Stance Correction

In an active boxing stance, a defender tucks their chin and bends their knees, effectively lowering the entire centre of mass. Based on Q1 of the prior ergonomics discussion and biomechanics literature:

- **Stance correction = −15 cm** applied uniformly to all landmark heights  
- This reflects a combination of: chin tuck (~5–10 cm), slight knee bend (~5–10 cm), and forward lean  
- The proportional relationships between landmarks are **preserved** under this correction (it is a uniform vertical offset)

| Profile | Head Centre — Stance (cm) | Solar Plexus Centre — Stance (cm) | Liver Centre — Stance (cm) |
|---|---|---|---|
| **150 F** | 125.2 | 72.3 | 79.5 |
| **150 M** | 125.2 | 73.5 | 80.7 |
| **190 F** | 162.7 | 95.6 | 104.7 |
| **190 M** | 162.7 | 97.1 | 106.2 |

---

## 5. Ratio Analysis

### Ratio A — Head Centre to Solar Plexus Centre

This ratio captures how the head-to-body vertical relationship scales with stature and sex.  
A consistent ratio would allow a single fixed robot design to suit all users; variance motivates averaging.

| Profile | Head Centre (cm) | Solar Plexus Centre (cm) | Ratio A (Head ÷ SP) | Gap A — Head to SP (cm) |
|---|---|---|---|---|
| **150 F** | 125.2 | 72.3 | **1.732** | 52.9 |
| **150 M** | 125.2 | 73.5 | **1.703** | 51.7 |
| **190 F** | 162.7 | 95.6 | **1.702** | 67.1 |
| **190 M** | 162.7 | 97.1 | **1.676** | 65.6 |

**Observation:** Ratio A ranges from **1.676 to 1.732** — a spread of **0.056**. This confirms the ratio is not constant across height and sex. A 150 cm female has a proportionally higher head relative to her solar plexus than a 190 cm male. Fixing a single head-to-solar-plexus spacing based on one profile would mis-target the others.

---

### Ratio B — Solar Plexus Centre to Liver Centre

This ratio validates the relative vertical offset between the two body pads.

| Profile | Solar Plexus Centre (cm) | Liver Centre (cm) | Ratio B (SP ÷ Liver) | Gap B — SP to Liver (cm) |
|---|---|---|---|---|
| **150 F** | 72.3 | 79.5 | **0.909** | 7.2 |
| **150 M** | 73.5 | 80.7 | **0.911** | 7.2 |
| **190 F** | 95.6 | 104.7 | **0.913** | 9.1 |
| **190 M** | 97.1 | 106.2 | **0.915** | 9.1 |

**Observation:** Ratio B is far more consistent — ranging from **0.909 to 0.915** (spread of only **0.006**). The solar-plexus-to-liver vertical relationship is nearly anatomically fixed as a proportion of stature, varying mainly with absolute height. The liver pad consistently sits **7–9 cm above** the solar plexus pad centre.

---

## 6. Averaged Ergonomic Scale

Taking the mean across all four profiles:

| Metric | 150F | 150M | 190F | 190M | **Mean** |
|---|---|---|---|---|---|
| Ratio A (Head ÷ Solar Plexus) | 1.732 | 1.703 | 1.702 | 1.676 | **1.703** |
| Gap A — Head to SP (cm) | 52.9 | 51.7 | 67.1 | 65.6 | **59.3 cm** |
| Ratio B (Solar Plexus ÷ Liver) | 0.909 | 0.911 | 0.913 | 0.915 | **0.912** |
| Gap B — SP to Liver (cm) | 7.2 | 7.2 | 9.1 | 9.1 | **8.2 cm** |

> **Ergonomic scale targets for robot design:**
> - The head pad centre should sit at **~1.70× the solar plexus pad centre height**
> - The solar plexus pad centre should sit at **~0.91× the liver pad centre height**
> - Average head–to–solar-plexus **gap = 59.3 cm** (centre-to-centre)
> - Average solar-plexus–to–liver **gap = 8.2 cm** (centre-to-centre)

---

## 7. Robot Dimension Translation

### Pad Sizes (fixed)
| Pad | Height |
|---|---|
| Head pad | 230 mm |
| Solar plexus pad | 180 mm |
| Liver pad (both sides) | 180 mm |

### Applying the Averaged Scale

Using the mean Gap A (59.3 cm centre-to-centre) and solar plexus baseline:

The averaged stance solar plexus centre across all 4 profiles:

| Profile | Solar Plexus Centre — Stance (cm) |
|---|---|
| 150 F | 72.3 |
| 150 M | 73.5 |
| 190 F | 95.6 |
| 190 M | 97.1 |
| **Mean** | **84.6 cm** |

**Robot target solar plexus pad centre height from base = 84.6 cm**

Derived pad positions from robot base:

| Pad | Centre Height from Base | Calculation |
|---|---|---|
| **Solar Plexus pad centre** | **84.6 cm** | Mean across all 4 profiles |
| **Liver pad centre (both sides)** | **84.6 + 8.2 = 92.8 cm** | Solar plexus + mean Gap B |
| **Head pad centre** | **84.6 + 59.3 = 143.9 cm** | Solar plexus + mean Gap A |

### Pad Edge Positions (for mechanical mounting reference)

| Pad | Centre (cm) | Top edge (cm) | Bottom edge (cm) |
|---|---|---|---|
| Solar Plexus | 84.6 | 93.6 | 75.6 |
| Liver (both sides) | 92.8 | 101.8 | 83.8 |
| Head | 143.9 | 155.4 | 132.4 |

> Head pad: 230 mm ÷ 2 = 11.5 cm offset. Body pads: 180 mm ÷ 2 = 9 cm offset.

---

## 8. Forward Punch Reach

**Definition:** Horizontal distance from the **front face of the user's torso** to the **tip of the extended fist** when punching forward. Used to determine how far the robot pads must be set back from the user's standing position.

Derived from Drillis & Contini proportionality constants:
- Upper arm + forearm + hand (total arm length) ≈ **0.440 H**
- Chest depth ≈ **0.118 H** (mean of male 0.120, female 0.115)
- **Forward reach = 0.440 H − 0.118 H = 0.322 H**

| Profile | H (cm) | Forward Punch Reach (cm) |
|---|---|---|
| **150 F** | 150 | 48.3 |
| **150 M** | 150 | 48.3 |
| **190 F** | 190 | 61.2 |
| **190 M** | 190 | 61.2 |
| **Average** | 170 | **54.7 cm** |

**Design implication:** The robot pad faces should be positioned approximately **50–55 cm in front of the user's torso** (i.e., the front edge of the robot pad should be at the average punch-out distance) to allow full arm extension on contact — matching the realistic feel of punching a human opponent.

---

## 9. Ergonomic Scale Diagram

```
HEIGHT FROM BASE (cm)
                                               
 160 ─┬───────────────────────────────────────
      │  ┌─────────────┐                      
 155 ─┤  │  HEAD PAD   │ ← Top edge: 155.4 cm
      │  │  (230 mm)   │                      
 150 ─┤  │             │                      
      │  │ ● Centre    │ ← 143.9 cm           
      │  │             │                      
 140 ─┤  │             │                      
      │  └─────────────┘ ← Bottom edge: 132.4 cm
      │                                        
 130 ─┤    ╔═══════════╗                       
      │  Gap A avg = 59.3 cm (centre-to-centre)
      │    ╚═══════════╝                       
      │                                        
 105 ─┬──────────────────────────────────────  
      │  ┌───────┐   ┌───────┐                 
 102 ─┤  │ LIVER │   │ LIVER │ ← Top: 101.8 cm
      │  │  (L)  │   │  (R)  │                 
  93 ─┤  │ ● Ctr │   │ ● Ctr │ ← 92.8 cm      
      │  │       │   │       │                 
  84 ─┤  └───────┘   └───────┘ ← Bottom: 83.8 cm
      │      ↕  Gap B avg = 8.2 cm             
  94 ─┤  ┌─────────────────┐                   
      │  │  SOLAR PLEXUS   │ ← Top: 93.6 cm   
  85 ─┤  │    (180 mm)     │                   
      │  │    ● Centre     │ ← 84.6 cm         
  76 ─┤  │                 │                   
      │  └─────────────────┘ ← Bottom: 75.6 cm
      │                                        
   0 ─┴───────────────────────────────────────
         ROBOT BASE                            
```

### Reference Overlay — Human Silhouettes

| Landmark | 150 cm user (stance) | 190 cm user (stance) | Robot pad centre |
|---|---|---|---|
| Head centre | 125.2 cm | 162.7 cm | **143.9 cm** |
| Solar plexus centre | 72.3–73.5 cm | 95.6–97.1 cm | **84.6 cm** |
| Liver centre | 79.5–80.7 cm | 104.7–106.2 cm | **92.8 cm** |

The robot pad layout targets the averaged stance-corrected height across the full 150–190 cm range. A 150 cm user will strike slightly below the pad centres; a 190 cm user slightly above — both within one pad-height of ergonomic accuracy.

---

## 10. Summary

| Design Parameter | Value |
|---|---|
| Solar plexus pad centre from base | **84.6 cm** |
| Liver pad centre from base (both sides) | **92.8 cm** |
| Head pad centre from base | **143.9 cm** |
| Head–to–solar-plexus gap (centre-to-centre) | **59.3 cm** |
| Liver–to–solar-plexus gap (centre-to-centre) | **8.2 cm** |
| Average forward punch reach | **54.7 cm** |
| Ergonomic head-to-SP ratio (Ratio A) | **1.703** |
| Ergonomic SP-to-liver ratio (Ratio B) | **0.912** |

> **Note on ratio consistency:** Ratio A (head ÷ solar plexus) varies by **±0.028** across the target population, confirming it is not a fixed biological constant. Ratio B (solar plexus ÷ liver) is far more stable (±0.003), meaning the liver-to-solar-plexus vertical offset can be treated as nearly fixed at **8 cm** regardless of user height. The averaged Ratio A of **1.703** is adopted as the single ergonomic design target to balance coverage across all four demographic combinations.

---

*Sources: Drillis & Contini (1966); ANSUR II Natick/TR-15/007 (2012); ISO 7250-1; OpenStax Human Anatomy 3rd Ed. (2022); Pheasant Bodyspace 4th Ed. (2018); SEA anthropometry literature (2015–2023); NHANES 2017–2020.*
