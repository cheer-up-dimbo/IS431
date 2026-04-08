"""
ACADEMICALLY SOUND ETHNICITY-LAYERED LIVER POSITION CALCULATION
================================================================
Source A (Skeletal geometry): Drillis & Contini (1966)
  - Xiphoid process height = 0.618H  [Western cadaver + surface data; skeletal proportions
    are relatively ethnically invariant for this geometric ratio]
  - Right MCL costal margin sits ~3 cm BELOW xiphoid apex
    (xiphoid = midpoint of costal arch; right MCL margin = lateral/inferior slope)
    → Right costal margin height = 0.618H - 0.020H = 0.598H
      (using ~2cm offset ≈ 0.012H at mean stature 170cm → use 0.020H as conservative midpoint)
    Actually cleaner: right costal margin = xiphoid - 3cm (fixed offset, not stature-scaled)
    because the offset is anatomical, not proportional.

Source B (Liver span): Malaysian ultrasound study (Lim et al. and sources cited in searches)
  - Male liver span MCL:   12.2 cm (SD ~1.5 cm)
  - Female liver span MCL: 11.7 cm (SD ~1.5 cm)
  - Population: Malaysian adults (Malay, Chinese, Indian mix) -- relevant to our SEA target demographic

Method:
  liver_centre_from_floor = right_costal_margin_ht + (liver_span / 2)
  [Liver inferior border AT costal margin in healthy adults; centre is half-span ABOVE that]

Assumption: liver inferior border = costal margin (normal anatomy; no hepatomegaly)
Limitation: Combining Western skeletal proportion (D&C) with SEA organ span (Malaysian study)
           introduces ~±2 cm uncertainty. D&C xiphoid fraction accepted as ethnically stable
           (skeletal geometry); liver span is population-specific and SEA data is preferred.
"""

# ---- profiles ----
profiles = {
    '150F': {'H': 150, 'span_cm': 11.7},
    '150M': {'H': 150, 'span_cm': 12.2},
    '190F': {'H': 190, 'span_cm': 11.7},
    '190M': {'H': 190, 'span_cm': 12.2},
}

XIPHOID_FRAC = 0.618        # D&C
MCL_OFFSET   = 3.0          # cm below xiphoid → right costal margin (anatomical, fixed)
BODY_CORR    = 8.0          # cm stance (knee bend/crouch)

print("=== LIVER CENTRE — MALAYSIAN SPAN APPROACH ===\n")
print(f"Xiphoid fraction (D&C): {XIPHOID_FRAC}")
print(f"Right MCL offset below xiphoid: {MCL_OFFSET} cm")
print(f"Body stance correction: {BODY_CORR} cm\n")

liver_stance_vals = []
for name, d in profiles.items():
    H = d['H']
    span = d['span_cm']
    xiphoid    = XIPHOID_FRAC * H
    costal_mcl = xiphoid - MCL_OFFSET              # right costal margin
    liver_ctr_erect  = costal_mcl + span / 2       # liver centre erect
    liver_ctr_stance = liver_ctr_erect - BODY_CORR  # stance corrected

    print(f"{name}: H={H}, span={span}")
    print(f"  Xiphoid:          {xiphoid:.1f} cm")
    print(f"  Costal margin MCL:{costal_mcl:.1f} cm")
    print(f"  Liver ctr (erect): {liver_ctr_erect:.1f} cm")
    print(f"  Liver ctr (stance):{liver_ctr_stance:.1f} cm")
    print()
    liver_stance_vals.append(liver_ctr_stance)

mean_liver = round(sum(liver_stance_vals) / len(liver_stance_vals), 1)
print(f"Mean liver centre (stance) across all profiles: {mean_liver} cm")

# ---- Compare with previous approach ----
print("\n=== COMPARISON: old vs new ===")
old_liver_fracs = {'150F': 0.630, '150M': 0.638, '190F': 0.630, '190M': 0.638}
old_body_corr = 8.0
for name, d in profiles.items():
    H = d['H']
    old = old_liver_fracs[name] * H - old_body_corr
    new = profiles[name]['span_cm']
    xiphoid = XIPHOID_FRAC * H
    costal  = xiphoid - MCL_OFFSET
    new_val = costal + new/2 - BODY_CORR
    print(f"{name}: old={old:.1f} cm | new(Malaysian)={new_val:.1f} cm | diff={new_val-old:.1f} cm")

# ---- Also show solar plexus reference (unchanged) ----
print("\n=== SOLAR PLEXUS REFERENCE (unchanged) ===")
sp_fracs = {'150F': 0.582, '150M': 0.590, '190F': 0.582, '190M': 0.590}
sp_body_corr = 8.0
sp_vals = []
for name, d in profiles.items():
    H = d['H']
    sp = sp_fracs[name] * H - sp_body_corr
    sp_vals.append(sp)
    print(f"{name}: SP stance = {sp:.1f} cm")
mean_sp = round(sum(sp_vals)/4, 1)
print(f"Mean SP: {mean_sp} cm")

print(f"\nMean liver: {mean_liver} cm")
print(f"Liver - SP gap: {round(mean_liver - mean_sp, 1)} cm")
