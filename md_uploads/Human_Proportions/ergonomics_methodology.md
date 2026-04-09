# Ergonomic Design Methodology — IS-431 Boxing Robot Pad Placement

## A Hybrid Dual-Stance Approach

> **Document scope:** Methodology, rationale, and academic basis for the ergonomic design decisions governing pad placement on the IS-431 boxing robot.  
> **Authors:** IS-431 project team, with reference to Zakir's Ergonomic Self-Measurement Analysis (April 2026).  
> **This document:** Focuses on methodology and reasoning. Computed design values are tabulated in `human_ergonomics_analysis_revised.md`.

---

## 1. Design Philosophy — The Dual-Stance Framework

The ergonomic specification for this robot resolves a fundamental tension in human-robot boxing training design: **the robot must feel like a real opponent, but must also be physically accessible to users at all experience levels.**

These two requirements pull in opposite directions. Realism demands that the robot's pad positions reflect how an actual boxer stands — in guard, crouched, and coiled. Accessibility demands that a beginner who simply walks up and faces the robot in everyday posture can still meaningfully interact with it.

The resolution adopted in this project is a **hybrid dual-stance framework**:

> **Principle 1 — Boxing stance governs relative pad spacing.**  
> The vertical distances between pads (head-to-body, body-to-flank) are derived from the biomechanics of a boxer in a proper orthodox guard. This ensures that the inter-pad ratios faithfully replicate the spatial geometry of a real opponent's strike zones.

> **Principle 2 — Erect posture governs minimum height specification.**  
> The minimum reachable pad height (constrained by mechanical extrusion limits) is matched to the anatomical target heights of a user standing in everyday erect posture, without boxing stance correction. This accommodates beginners who are not yet familiar with guard positioning and approach the robot in a natural standing posture.

This framework is grounded in the practical observation that training equipment, from heavy bags to speed balls, is designed for repeated use across a spectrum of user experience. A beginner's first interaction should not require the adoption of a trained guard position to achieve meaningful pad contact.

---

## 2. Landmark Selection and Rationale

Historically, this project's ergonomic foundation used imprecise colloquial terms ("solar plexus", "head centre") that do not correspond to palpable surface landmarks. The following revision adopts anatomically grounded, ergonomically testable reference points, consistent with the landmark definitions specified in ISO 7250-1 (2008) and the terminological guidance in Zakir's Ergonomic Analysis (April 2026).

### 2.1 Head Pad — Pronasale

The head pad target is anchored to the **pronasale** — the anatomical term for the nose tip. This landmark replaces the previous "head centre" (mid-ear level), which represents neither a visible target nor the actual face zone exposed in a boxing guard.

In a standard orthodox guard, the chin is tucked and the face is partially shielded by the lead glove. The nose tip, sitting at the apex of the visible face, represents the realistic upper exposure zone of a boxer's head. It is a palpable, externally visible, and reproducible anthropometric landmark (Drillis & Contini, 1966; ISO 7250-1, 2008).

The pronasale is expressed as a proportion of standing stature using the constants established by Drillis and Contini (1966), which remain the foundational reference for segment proportionality in applied ergonomics (Pheasant & Haslegrave, 2006).

### 2.2 Epigastric Pad — Subxiphoid / Epigastric Region

The central body pad targets the **subxiphoid / epigastric region** — the soft tissue area immediately below the xiphoid process, at the base of the sternum (Standring, 2020). In boxing, this is the recognised "body shot" target: the celiac plexus lies immediately deep to this surface, and impact here is both effective for scoring and technically demanding to land.

The term "solar plexus" is retained only as a colloquial boxing shorthand and is explicitly not used as an anatomical landmark in this analysis (Zakir, 2026). The xiphoid process — which forms the skeletal anchor for the subxiphoid region — is a palpable midline landmark expressed as a proportion of stature in Drillis and Contini (1966) and confirmed in ANSUR II (Gordon et al., 2014).

A sex-disaggregated correction from ANSUR II is applied: female participants show proportionally shorter trunks, placing abdominal landmarks slightly lower relative to stature than in males (Gordon et al., 2014).

### 2.3 Liver Pad — Right MCL Costal Margin (Boxing Strike Zone)

The liver pad targets the **right flank at the right midclavicular line (MCL) costal margin** — the lower right ribcage where a right-body hook makes surface contact. This is the recognised anatomical impact zone for a so-called liver punch in boxing.

A prior iteration of this analysis computed the pad target from the anatomical organ centre of the liver (costal margin plus half the liver span). This was found to be incorrect for the robot's purpose: the organ centre, derived via a two-stage method using Malaysian ultrasound liver span data (Zahir et al., 2020; Lim et al., 2017), places the pad *above* the epigastric pad. This contradicts both the anatomical reality of a body hook's impact zone and the design intent stated in Zakir's Ergonomic Analysis (April 2026), which specifies that the liver pad occupies a *lower lateral band* relative to the epigastric centreline.

The corrected approach anchors the liver pad to the **right MCL costal margin** using a fixed anatomical offset from the xiphoid, as documented in Gray's Anatomy (Standring, 2020) and OpenStax Anatomy and Physiology (Betts et al., 2022). This positions the liver pad correctly below the epigastric pad, consistent with the biomechanics of a body hook and with the design intent.

### 2.4 Stomach Pad — Left Lateral (Symmetric)

The left-lateral pad mirrors the liver pad's height for geometric and structural symmetry. It targets the left upper abdominal region (stomach fundus / left flank). Anatomically naming this pad "spleen-side" is avoided; it is designated "stomach-side" for simplicity and to avoid implying anatomical precision not supported by measurement (Zakir, 2026).

### 2.5 Glenohumeral Joint — Arm Pivot Reference

The **glenohumeral (GH) joint** — the ball-and-socket shoulder joint — is included as an anatomical reference point, not a pad target. It represents the pivot axis for the human arm, relevant to understanding the reach envelope from joint to pad and for any future arm-actuation analysis.

The GH joint centre is estimated from the acromion landmark (Drillis & Contini, 1966) with a downward offset derived from clinical biomechanics literature, which places the joint centre approximately 3 cm inferior-medial to the bony acromion tip (Standring, 2020).

---

## 3. Boxing Stance Correction Model

### 3.1 Why Stance Corrections Are Applied to Pad Spacing

The relative spacing between pads is derived from **boxer-in-guard posture** rather than erect standing. This is essential to the first design principle: if pad spacing reflected erect anatomy, striking the pads would feel anatomically misaligned when the user adopts even a basic guard. The head-to-body distance in a guard is not the same as in erect standing; the chin tuck and body crouch bring the head significantly closer to the torso.

By computing inter-pad gaps from boxing stance geometry, the robot replicates the spatial relationship of a real opponent's strike zones, providing meaningful tactile and biomechanical feedback during training.

### 3.2 Body Crouch

In an orthodox boxing guard, the knees are partially bent and the hips flex slightly, producing a uniform vertical drop of all anatomical landmarks. This mechanism lowers the entire body relative to standing height and is a consistent feature across boxing styles and skill levels (Lenetsky et al., 2013).

### 3.3 Head Tuck and Guard Position

The most significant postural correction for the head pad is the combined effect of the **chin tuck and head forward flex** in guard. As the chin descends toward the chest, the nose tip drops substantially relative to erect posture — far more than the body crouch correction alone.

Rather than applying an estimated angular correction (which would require motion capture data not available to this project), the head-to-body gap in full guard was calibrated empirically from a direct self-measurement. A 177 cm male student measured the nose-tip-to-subxiphoid distance while holding an orthodox guard position, obtaining approximately 30 cm (Zakir, 2026). This empirical value was used to derive a gap formula expressed as a fraction of standing stature, consistent with the proportionality approach of Drillis and Contini (1966). The formula predicts values in close agreement with the measured result across the target stature range.

This approach is preferred over angular estimation because it:
- Is grounded in a real measurement in the actual posture of interest
- Avoids assumptions about head rotation geometry
- Produces a result validated against a known data point

### 3.4 Shoulder Curl Correction (GH Joint)

In a full boxing guard, the GH joint is lowered beyond simple body crouch by three additional postural mechanisms, each documented in boxing biomechanics literature:

**Scapular depression.** Boxers are coached to actively depress (lower) the scapula in guard, stabilising the shoulder against the ribcage and reducing unnecessary elevation that could expose the neck (bamamoo.com; MDPI Sports Sciences). This directly lowers the GH joint below the level predicted by body crouch alone.

**Trunk forward lean.** Three-dimensional kinematic studies of boxing stances (ResearchGate; 4medicine.pl) using 120 Hz motion capture systems have documented forward trunk inclination of approximately 10° in an orthodox guard. At the angular and height dimensions of the shoulder, this lean produces a measurable vertical drop of the shoulder joint even when expressed against the vertical axis.

**Shoulder protraction.** The serratus anterior, long described as the "boxer's muscle" for its role in scapular protraction in the guard position (Tuneupfitness; MDPI Sports Sciences), wraps the scapula forward around the ribcage. While the primary effect of protraction is horizontal (extending reach), this scapular movement also has a minor vertical component as the scapula slides anteriorly.

The sum of these mechanisms produces a total guard curl correction that is applied to the GH joint stance height beyond the standard body crouch. This correction is acknowledged as an engineering estimate — a mid-range value derived from documented biomechanical mechanisms rather than direct measurement. It is flagged as the primary source of uncertainty in the GH joint reference position, and direct measurement of GH height in boxing guard posture is recommended for future validation.

---

## 4. Erect Posture as the Minimum Height Specification Basis

The second design principle addresses inclusivity. The minimum height at which the robot's pads can be positioned is a mechanical constraint of the extrusion system. Rather than optimising this minimum for a boxer in guard, it is specified against **users standing in everyday erect posture**.

The rationale is straightforward: beginners — who form a meaningful portion of any boxing training platform's user base — may not yet have internalised a guard stance. Requiring a guard position before meaningful pad interaction is possible would create a barrier at the very first use. By setting the minimum height based on erect landmark heights, the robot can be used effectively even by a user who simply stands in front of it naturally.

Erect landmark heights are higher than boxing-stance heights by the body crouch correction. This means that the same mechanical minimum height accommodates a shorter user in erect posture than it does a taller user in boxing stance. The difference is the body crouch offset, which is treated as a fixed correction based on boxing biomechanics consensus (Lenetsky et al., 2013).

This principle also supports the robot's role as a training progression tool: as a beginner develops their guard posture over time, the robot remains ergonomically valid — the pad spacing (derived from boxing stance geometry) becomes increasingly appropriate as the user's guard improves.

---

## 5. Population Basis and Averaging

The analysis spans a stature range of 150–190 cm, which covers the practical adult user range for a boxing training context in the Southeast Asian context, as confirmed by regional anthropometry (Chuan et al., 2010).

Four boundary profiles are used: the extremes of the stature range, each computed for both male and female body proportions. Since all landmark height formulas are linear in standing stature, the mean of the four boundary profiles is mathematically equivalent to the mean across the full continuous stature range — that is, it corresponds exactly to a 170 cm mean user. This is a standard approach in ergonomic design for the full population, consistent with the methodology described in Pheasant and Haslegrave (2006).

A sex-disaggregated correction is applied to abdominal landmarks (subxiphoid and liver pad), following ANSUR II (Gordon et al., 2014), which documents that female participants have proportionally shorter trunks relative to stature compared to males. Head and shoulder landmarks are treated as sex-neutral at the proportionality level, consistent with Drillis and Contini (1966).

---

## 6. Why the Malaysian Population Context Matters

The target user population for this robot is SEA adult users. While the structural proportionality constants used (xiphoid at a fixed fraction of stature, acromion fraction) are sourced from Western datasets and are widely accepted as ethnically invariant for gross proportionality analysis at this scale of accuracy (Drillis & Contini, 1966; ISO 7250-1, 2008), the corrected liver pad methodology no longer uses organ-specific liver span measurements.

The prior version of this analysis used Malaysian clinical ultrasound liver span data from PubMed-reviewed studies (Lim et al., 2017; Zahir et al., 2020) to compute the organ centre. With the corrected anchor at the costal margin (a skeletal surface landmark), this population-specific organ data is no longer required. The costal arch geometry — specifically the 3 cm inferior offset from the xiphoid at the right MCL — is an anatomical constant documented in standard anatomy references (Standring, 2020; Betts et al., 2022) and is not population-dependent.

This simplification improves the methodological cleanliness of the analysis by eliminating the mixed-ethnicity data combination that was flagged as a source of uncertainty in the prior version.

---

## 7. Limitations and Recommended Validation

### 7.1 Head Gap Formula

The empirical gap formula for the boxing guard head-to-body distance is derived from a single self-measurement (Zakir, 2026). While this is treated as a validated anchor point, it represents one individual, one guard posture, and one measurement occasion. The formula's stature-scaling behaviour (gap as a fraction of standing height) is assumed but not empirically tested across multiple subjects.

**Recommendation:** Obtain nose-to-subxiphoid measurements in boxing guard from a minimum of three to five subjects spanning the 150–190 cm range. This would allow the scaling factor to be confirmed or adjusted, and would reduce inter-subject uncertainty from the current ±3–4 cm to a smaller, better-characterised value.

### 7.2 GH Joint Guard Position

The guard curl correction applied to the GH joint is an engineering estimate constructed from three separately documented biomechanical mechanisms. No direct measurement of GH height in boxing guard posture has been performed.

**Recommendation:** Direct measurement — GH joint palpated and marked on the skin, measured from the floor while holding a guard position — would immediately validate or refine the correction. This is a low-effort measurement similar to the nose-to-subxiphoid method and would reduce the current ±2 cm uncertainty on the GH reference height.

### 7.3 Guard Style Variation

The boxing guard is not a single fixed posture. Different styles — orthodox, Philly shell, peek-a-boo, southpaw — produce meaningfully different shoulder heights, head positions, and trunk angles (Lenetsky et al., 2013; ResearchGate 3D kinematic studies). The current model uses a generic orthodox guard as the reference. Users with significantly non-standard guard styles may experience pad alignment outside the design intent.

**Recommendation:** Document the assumed guard reference in the robot's user manual and training guidance. Frame the pad positions as optimised for a standard upright orthodox guard.

---

## 8. References

1. Drillis, R., & Contini, R. (1966). *Body segment parameters.* Technical Report No. 1166.03. New York University.

2. Gordon, C. C., Blackwell, C. L., Bradtmiller, B., Parham, J. L., Barrientos, P., Paquette, S. P., Corner, B. D., Carson, J. M., Venezia, J. C., Rockwell, B. M., Mucher, M., & Kristensen, S. (2014). *2010–2012 Anthropometric Survey of U.S. Army Personnel: Methods and summary statistics.* Technical Report NATICK/TR-15/007.

3. ISO. (2008). *ISO 7250-1:2008 — Basic human body measurements for technological design — Part 1: Body measurement definitions and landmarks.* ISO, Geneva.

4. ISO. (2010). *ISO/TR 7250-2:2010 — Basic human body measurements for technological design — Part 2: Statistical summaries of body measurements from national populations.* ISO, Geneva.

5. Pheasant, S., & Haslegrave, C. M. (2006). *Bodyspace: Anthropometry, ergonomics and the design of work* (3rd ed.). CRC Press.

6. Standring, S. (Ed.). (2020). *Gray's Anatomy: The Anatomical Basis of Clinical Practice* (42nd ed.). Elsevier.

7. Betts, J. G., Young, K. A., Wise, J. A., Johnson, E., Poe, B., Kruse, D. H., Korol, O., Johnson, J. E., Womble, M., & DeSaix, P. (2022). *Anatomy and physiology* (3rd ed.). OpenStax. https://openstax.org/books/anatomy-and-physiology

8. Lenetsky, S., Harris, N., & Brughelli, M. (2013). Assessment and contributors of punching forces in combat sports athletes: Implications for strength and conditioning. *Strength & Conditioning Journal, 35*(2), 1–7.

9. Chuan, T. K., Hartono, M., & Kumar, N. (2010). Anthropometry of the Singaporean and Indonesian populations. *International Journal of Industrial Ergonomics, 40*(6), 757–766. https://doi.org/10.1016/j.ergon.2010.05.001

10. Lim, C. C., Sobri, M., & Krishnan, V. K. (2017). Normal liver size in Malaysian adults measured by ultrasonography. *Medical Journal of Malaysia, 72*(2), 87–91.

11. Zahir, S. T., Zare, M. A., Moghimi, M., & Mosadegh, M. (2020). Normal liver dimensions in ultrasound and its correlation with anthropometric parameters in adults. *Journal of Medical Ultrasound, 28*(3), 159–164. https://doi.org/10.4103/JMU.JMU_62_19

12. Serratus anterior in boxing — scapular protraction mechanics. MDPI Sports Science / Tuneupfitness.com. Retrieved April 2026.

13. Boxing stance kinematic analysis — trunk lean and scapular positioning. ResearchGate / 4medicine.pl (3D motion capture, 120 Hz studies). Retrieved April 2026.

14. Zakir (2026, April). *Ergonomic self-measurement analysis and strike-zone placement decisions.* Internal project reference document, IS-431.

---

*Document version: April 2026*  
*Companion document: `human_ergonomics_analysis_revised.md` (computed design values)*
