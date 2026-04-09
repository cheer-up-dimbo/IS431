profiles = [('150 F', 150, 'F'), ('150 M', 150, 'M'), ('190 F', 190, 'F'), ('190 M', 190, 'M')]
BODY_DROP = 8
LIVER_SPAN_M = 12.2; LIVER_SPAN_F = 11.7
XIPHOID_FRAC = 0.618; ANSUR_F = 0.008
GAP_FORMULA = 0.182  # nose-to-subxiphoid in stance = 0.182H

subi_stances=[]; nose_stances=[]; liver_stances=[]; gh_stances=[]
for name, H, sex in profiles:
    f_corr = ANSUR_F * H if sex == 'F' else 0
    subi_erect  = XIPHOID_FRAC * H - f_corr
    subi_stance = subi_erect - BODY_DROP
    gap_nose = GAP_FORMULA * H
    nose_stance = subi_stance + gap_nose
    span = LIVER_SPAN_M if sex == 'M' else LIVER_SPAN_F
    costal_margin = XIPHOID_FRAC * H - 3.0
    liver_stance  = costal_margin + span / 2 - BODY_DROP
    gh_stance = 0.818 * H - 3.0 - BODY_DROP
    subi_stances.append(subi_stance)
    nose_stances.append(nose_stance)
    liver_stances.append(liver_stance)
    gh_stances.append(gh_stance)
    print(f'{name}: nose={nose_stance:.1f}  subi={subi_stance:.1f}  liver={liver_stance:.1f}  gh={gh_stance:.1f}  gap_A={gap_nose:.1f}')

m_nose  = sum(nose_stances)/4
m_subi  = sum(subi_stances)/4
m_liver = sum(liver_stances)/4
m_gh    = sum(gh_stances)/4
print()
print(f'MEANS: nose={m_nose:.1f}  subi={m_subi:.1f}  liver={m_liver:.1f}  gh={m_gh:.1f}')
print(f'Gap A (nose->subi):  {m_nose - m_subi:.1f} cm')
print(f'Gap B (subi->liver): {m_liver - m_subi:.1f} cm  ({"liver above" if m_liver > m_subi else "liver below"} subi)')
print(f'Gap C (nose->GH):    {m_nose - m_gh:.1f} cm')
print(f'Gap D (GH->subi):    {m_gh - m_subi:.1f} cm')
print(f'Zakir validation (177cm): {0.182*177:.1f} cm nose-to-subi (measured: 30cm)')
