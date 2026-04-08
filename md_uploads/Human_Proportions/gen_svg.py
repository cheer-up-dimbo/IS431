"""
Generate a clean, Figma-importable SVG for boxing robot ergonomic pad layout.
All positions are mathematically computed from real values — no guessing.
"""

OUT = r"C:\Users\elgin\Documents\GitHub\IS431\md_uploads\Human_Proportions\ergo_diagram.svg"

# ── Scale & canvas ─────────────────────────────────────────────────────────────
PX_PER_CM = 5.5          # 1 cm = 5.5 px — fits 200cm in ~1100px
CM_TOP    = 200.0        # top of canvas (cm) — clears 190cm user fully
CM_BOT    =   0.0        # bottom = robot base / floor
PAD_TOP   = 100          # px above diagram (title)
PAD_BOT   =  80          # px below diagram (footer)
W         = 720          # canvas width (no silhouettes)

def y(cm):
    """cm from floor → SVG y pixel (top=CM_TOP)"""
    return PAD_TOP + (CM_TOP - cm) * PX_PER_CM

DIAGRAM_H = PAD_TOP + (CM_TOP - CM_BOT) * PX_PER_CM + PAD_BOT
H = int(DIAGRAM_H)

# ── Values ─────────────────────────────────────────────────────────────────────
HEAD_CTR  = 143.9;  HEAD_HALF  = 11.5
LIVER_CTR = 100.0;  BODY_HALF  = 9.0
SP_CTR    =  91.6

# ── Colours ────────────────────────────────────────────────────────────────────
C_HEAD  = "#1a3a6b"
C_LIVER = "#0d7a6a"
C_SP    = "#c2620a"
C_GAP_A = "#4f46e5"
C_GAP_B = "#d97706"
C_GRID  = "#f0f2f5"
C_GRID2 = "#e4e7eb"

# ── Pad x positions ────────────────────────────────────────────────────────────
HEAD_XL,  HEAD_XR  = 215, 480
LIVER_LXL, LIVER_LXR = 145, 335
LIVER_RXL, LIVER_RXR = 350, 540
SP_XL,    SP_XR    = 145, 540

ANNOT_X = 555   # annotation start x
GAP_A_X = 100   # gap A arrow x
GAP_B_X =  60   # gap B arrow x

# ── SVG builder ────────────────────────────────────────────────────────────────
lines = []
def e(s): lines.append(s)

e(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Inter, Helvetica Neue, Arial, sans-serif">')

# Background
e(f'<rect width="{W}" height="{H}" fill="white"/>')

# Grid lines — every 10cm major, every 20cm labelled
for cm in range(0, 201, 10):
    yy = y(cm)
    col = C_GRID2 if cm % 20 == 0 else C_GRID
    e(f'<line x1="160" y1="{yy:.1f}" x2="{W-20}" y2="{yy:.1f}" stroke="{col}" stroke-width="{1.2 if cm%20==0 else 0.7}"/>')
    if cm % 20 == 0:
        e(f'<text x="158" y="{yy+4:.1f}" text-anchor="end" fill="{C_GRID2}" font-size="9">{cm} cm</text>')

# Centre reference lines (subtle dashed)
for cm, col in [(HEAD_CTR, C_HEAD), (LIVER_CTR, C_LIVER), (SP_CTR, C_SP)]:
    yy = y(cm)
    e(f'<line x1="160" y1="{yy:.1f}" x2="{ANNOT_X-10}" y2="{yy:.1f}" stroke="{col}" stroke-width="0.7" stroke-dasharray="4,6" opacity="0.35"/>')

# ── Helper: rounded rect ───────────────────────────────────────────────────────
def rrect(xl, xr, ctr_cm, half_cm, col, rx=8):
    yt = y(ctr_cm + half_cm)
    yb = y(ctr_cm - half_cm)
    h_ = yb - yt
    w_ = xr - xl
    # shadow
    e(f'<rect x="{xl+3}" y="{yt+4}" width="{w_}" height="{h_}" rx="{rx}" fill="#00000018"/>')
    # fill
    e(f'<rect x="{xl}" y="{yt:.1f}" width="{w_}" height="{h_:.1f}" rx="{rx}" fill="{col}18" stroke="{col}" stroke-width="2.2"/>')
    # top dashed edge
    e(f'<line x1="{xl}" y1="{yt:.1f}" x2="{xr}" y2="{yt:.1f}" stroke="{col}" stroke-width="1.5" stroke-dasharray="6,4"/>')
    # bottom dashed edge
    e(f'<line x1="{xl}" y1="{yb:.1f}" x2="{xr}" y2="{yb:.1f}" stroke="{col}" stroke-width="1.5" stroke-dasharray="6,4"/>')

# ── Helper: centre dot ─────────────────────────────────────────────────────────
def cdot(cx, ctr_cm, col):
    yy = y(ctr_cm)
    e(f'<circle cx="{cx}" cy="{yy:.1f}" r="6" fill="{col}"/>')
    e(f'<circle cx="{cx}" cy="{yy:.1f}" r="3" fill="white"/>')

# ── Helper: pad label ──────────────────────────────────────────────────────────
def label(cx, ctr_cm, col, top_txt, bot_txt):
    yy = y(ctr_cm)
    e(f'<text x="{cx}" y="{yy-6:.1f}" text-anchor="middle" fill="{col}" font-size="14" font-weight="700">{top_txt}</text>')
    e(f'<text x="{cx}" y="{yy+18:.1f}" text-anchor="middle" fill="{col}bb" font-size="11">{bot_txt}</text>')

# ── Helper: edge label ─────────────────────────────────────────────────────────
def edge_label(xl, xr, cm, col, sym):
    yy = y(cm)
    mid = (xl + xr) / 2
    e(f'<text x="{xr+8}" y="{yy+4:.1f}" fill="{col}99" font-size="10">{sym} {cm:.1f} cm</text>')

# ── Helper: annotation callout ─────────────────────────────────────────────────
def annotation(xr, ctr_cm, col, txt):
    yy = y(ctr_cm)
    e(f'<line x1="{xr}" y1="{yy:.1f}" x2="{ANNOT_X}" y2="{yy:.1f}" stroke="{col}66" stroke-width="1"/>')
    e(f'<circle cx="{ANNOT_X+6}" cy="{yy:.1f}" r="4.5" fill="{col}"/>')
    e(f'<text x="{ANNOT_X+16}" y="{yy+4:.1f}" fill="{col}" font-size="12" font-weight="600">{txt}</text>')

# ── Helper: double-headed arrow ────────────────────────────────────────────────
def gap_arrow(x, cm_from, cm_to, col, label_txt):
    y1 = y(cm_from); y2 = y(cm_to)
    mid_y = (y1 + y2) / 2
    aw = 7   # arrowhead size
    # shaft
    e(f'<line x1="{x}" y1="{y1:.1f}" x2="{x}" y2="{y2:.1f}" stroke="{col}" stroke-width="2.2"/>')
    # arrowhead top (pointing to cm_to = higher cm = lower y)
    e(f'<polygon points="{x},{y2:.1f} {x-aw},{y2+aw*1.5:.1f} {x+aw},{y2+aw*1.5:.1f}" fill="{col}"/>')
    # arrowhead bottom (pointing to cm_from = lower cm = higher y)
    e(f'<polygon points="{x},{y1:.1f} {x-aw},{y1-aw*1.5:.1f} {x+aw},{y1-aw*1.5:.1f}" fill="{col}"/>')
    # label (multi-line via tspan)
    parts = label_txt.split("\n")
    dy_start = mid_y - (len(parts) - 1) * 8
    e(f'<text x="{x-10}" y="{dy_start:.1f}" text-anchor="end" fill="{col}" font-size="12" font-weight="700">')
    for i, p in enumerate(parts):
        e(f'  <tspan x="{x-10}" dy="{0 if i==0 else 16}">{p}</tspan>')
    e('</text>')

# ══════════════════════════════════════════════════════════════════════════════
# DRAW PADS
# ══════════════════════════════════════════════════════════════════════════════

# HEAD PAD
rrect(HEAD_XL, HEAD_XR, HEAD_CTR, HEAD_HALF, C_HEAD)
cx_head = (HEAD_XL + HEAD_XR) / 2
cdot(cx_head, HEAD_CTR, C_HEAD)
label(cx_head, HEAD_CTR, C_HEAD, "HEAD PAD", "(230 mm)")
edge_label(HEAD_XL, HEAD_XR, HEAD_CTR + HEAD_HALF, C_HEAD, "▲")
edge_label(HEAD_XL, HEAD_XR, HEAD_CTR - HEAD_HALF, C_HEAD, "▼")
annotation(HEAD_XR, HEAD_CTR, C_HEAD, "Centre  143.9 cm")

# LIVER PADS
rrect(LIVER_LXL, LIVER_LXR, LIVER_CTR, BODY_HALF, C_LIVER)
rrect(LIVER_RXL, LIVER_RXR, LIVER_CTR, BODY_HALF, C_LIVER)
cx_liver_l = (LIVER_LXL + LIVER_LXR) / 2
cx_liver_r = (LIVER_RXL + LIVER_RXR) / 2
cdot(cx_liver_l, LIVER_CTR, C_LIVER)
cdot(cx_liver_r, LIVER_CTR, C_LIVER)
label(cx_liver_l, LIVER_CTR, C_LIVER, "LIVER (L)", "(180 mm)")
label(cx_liver_r, LIVER_CTR, C_LIVER, "LIVER (R)", "(180 mm)")
edge_label(LIVER_LXL, LIVER_RXR, LIVER_CTR + BODY_HALF, C_LIVER, "▲")
edge_label(LIVER_LXL, LIVER_RXR, LIVER_CTR - BODY_HALF, C_LIVER, "▼")
annotation(LIVER_RXR, LIVER_CTR, C_LIVER, "Centre  100.0 cm  [SEA data]")

# SOLAR PLEXUS PAD
rrect(SP_XL, SP_XR, SP_CTR, BODY_HALF, C_SP)
cx_sp = (SP_XL + SP_XR) / 2
cdot(cx_sp, SP_CTR, C_SP)
label(cx_sp, SP_CTR, C_SP, "SOLAR PLEXUS", "(180 mm)")
edge_label(SP_XL, SP_XR, SP_CTR + BODY_HALF, C_SP, "▲")
edge_label(SP_XL, SP_XR, SP_CTR - BODY_HALF, C_SP, "▼")
annotation(SP_XR, SP_CTR, C_SP, "Centre  91.6 cm")

# ══════════════════════════════════════════════════════════════════════════════
# GAP ARROWS  — strictly centre to centre
# ══════════════════════════════════════════════════════════════════════════════
gap_arrow(GAP_A_X, SP_CTR, HEAD_CTR, C_GAP_A, "Gap A\n52.3 cm\n(centre–centre)")
gap_arrow(GAP_B_X, SP_CTR, LIVER_CTR, C_GAP_B, "Gap B\n8.4 cm\n(centre–centre)")

# ══════════════════════════════════════════════════════════════════════════════
# ROBOT BASE
# ══════════════════════════════════════════════════════════════════════════════
y_base = y(0)
e(f'<line x1="120" y1="{y_base:.1f}" x2="{W-40}" y2="{y_base:.1f}" stroke="#374151" stroke-width="3"/>')
e(f'<text x="{W//2}" y="{y_base+18:.1f}" text-anchor="middle" fill="#374151" font-size="12" font-weight="700">ROBOT BASE  (0 cm)</text>')

# ══════════════════════════════════════════════════════════════════════════════
# TITLE & FOOTER
# ══════════════════════════════════════════════════════════════════════════════
e(f'<text x="{W//2}" y="42" text-anchor="middle" fill="{C_HEAD}" font-size="20" font-weight="800">Boxing Robot — Ergonomic Pad Layout</text>')
e(f'<text x="{W//2}" y="66" text-anchor="middle" fill="#6b7280" font-size="12" font-style="italic">Stance-corrected centre heights from robot base</text>')

y_foot = y_base + 48
e(f'<text x="{W//2}" y="{y_foot:.1f}" text-anchor="middle" fill="#9ca3af" font-size="9.5" font-style="italic">'
  f'Stance: −8 cm body crouch  |  −7 cm chin tuck (head only)  |  '
  f'Liver positioned via Malaysian ultrasound span data (PubMed/NIH)'
  f'</text>')

e('</svg>')

# ── Write file ─────────────────────────────────────────────────────────────────
with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"SVG saved: {OUT}")
print(f"Canvas: {W} × {H} px  |  Scale: {PX_PER_CM} px/cm")
