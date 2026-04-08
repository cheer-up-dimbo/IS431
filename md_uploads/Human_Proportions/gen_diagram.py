"""
Precision ergonomics diagram — clean visual style, no Y-axis scale,
mathematically guaranteed centre-to-centre gap arrows.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

OUT_FILE = r"C:\Users\elgin\Documents\GitHub\IS431\md_uploads\Human_Proportions\ergo_diagram.png"

# ── Values ────────────────────────────────────────────────────────────────────
HEAD_CTR  = 143.9;  HEAD_HALF  = 11.5
LIVER_CTR = 100.0;  BODY_HALF  =  9.0
SP_CTR    =  91.6

# ── Canvas — tall portrait, no axes ──────────────────────────────────────────
fig, ax = plt.subplots(figsize=(11, 15), facecolor="white")
ax.set_facecolor("white")
ax.set_xlim(0, 10)
ax.set_ylim(74, 164)
ax.axis("off")          # ← removes ALL axes, spines, ticks, labels

# Subtle horizontal reference lines (behind everything)
for y in np.arange(75, 164, 5):
    ax.axhline(y, color="#f0f0f0", lw=0.8, zorder=0)
for y in [SP_CTR, LIVER_CTR, HEAD_CTR]:
    ax.axhline(y, color="#e8e8e8", lw=1.2, linestyle=":", zorder=0)

# ── Colours ───────────────────────────────────────────────────────────────────
C_HEAD  = "#1a3a6b"
C_LIVER = "#0d7a6a"
C_SP    = "#c2620a"
C_GAP_A = "#4f46e5"   # indigo
C_GAP_B = "#d97706"   # amber

# ── Pad drawing helper ────────────────────────────────────────────────────────
def pad(xl, xr, ctr, half, col, label1, label2):
    top, bot = ctr + half, ctr - half
    # Shadow
    rect_s = mpatches.FancyBboxPatch((xl+0.05, bot-0.25), xr-xl, top-bot,
        boxstyle="round,pad=0.15", fc="#00000012", ec="none", zorder=2)
    ax.add_patch(rect_s)
    # Main pad
    rect = mpatches.FancyBboxPatch((xl, bot), xr-xl, top-bot,
        boxstyle="round,pad=0.15", lw=2,
        ec=col, fc=col+"1a", zorder=3)
    ax.add_patch(rect)
    # Top / bottom dashes + edge labels
    for y_e, sym, lbl in [(top, "▲", f"{top:.1f} cm"), (bot, "▼", f"{bot:.1f} cm")]:
        ax.plot([xl, xr], [y_e, y_e], color=col, lw=1.2, ls="--", zorder=4)
        ax.text(xr + 0.12, y_e, f"{sym} {lbl}", va="center",
                fontsize=8, color=col+"bb")
    # Centre dot
    cx = (xl + xr) / 2
    ax.plot(cx, ctr, "o", ms=8, color=col, zorder=5)
    ax.plot(cx, ctr, "o", ms=4, color="white", zorder=6)
    # Labels inside
    ax.text(cx, ctr + 0.8, label1, ha="center", va="bottom",
            fontsize=10, fontweight="bold", color=col, zorder=6)
    ax.text(cx, ctr - 1.0, label2, ha="center", va="top",
            fontsize=8.5, color=col+"cc", zorder=6)

# ── Draw pads ─────────────────────────────────────────────────────────────────
pad(3.3, 6.7, HEAD_CTR, HEAD_HALF, C_HEAD,   "HEAD PAD",     "(230 mm)")
pad(2.2, 4.4, LIVER_CTR, BODY_HALF, C_LIVER, "LIVER (L)",    "(180 mm)")
pad(5.6, 7.8, LIVER_CTR, BODY_HALF, C_LIVER, "LIVER (R)",    "(180 mm)")
pad(2.2, 7.8, SP_CTR,   BODY_HALF, C_SP,     "SOLAR PLEXUS", "(180 mm)")

# ── Centre annotations (right side) ──────────────────────────────────────────
for ctr, col, lbl in [
    (HEAD_CTR,  C_HEAD,  "● Centre  143.9 cm"),
    (LIVER_CTR, C_LIVER, "● Centre  100.0 cm  [SEA data]"),
    (SP_CTR,    C_SP,    "● Centre   91.6 cm"),
]:
    ax.annotate(lbl, xy=(7.9, ctr), xytext=(8.05, ctr),
                fontsize=9, color=col, va="center",
                fontweight="bold",
                arrowprops=dict(arrowstyle="-", color=col+"66", lw=0.8))

# ── Gap A arrow — SP CENTRE → HEAD CENTRE ────────────────────────────────────
ax.annotate("", xy=(1.5, HEAD_CTR), xytext=(1.5, SP_CTR),
            arrowprops=dict(arrowstyle="<->", color=C_GAP_A, lw=2.0))
mid_a = (HEAD_CTR + SP_CTR) / 2
ax.text(1.35, mid_a, "Gap A\n52.3 cm\n(centre–centre)",
        ha="right", va="center", fontsize=9, color=C_GAP_A, fontweight="bold",
        linespacing=1.4)

# ── Gap B arrow — SP CENTRE → LIVER CENTRE ───────────────────────────────────
ax.annotate("", xy=(0.75, LIVER_CTR), xytext=(0.75, SP_CTR),
            arrowprops=dict(arrowstyle="<->", color=C_GAP_B, lw=2.0))
mid_b = (LIVER_CTR + SP_CTR) / 2
ax.text(0.60, mid_b, "Gap B\n8.4 cm\n(centre–centre)",
        ha="right", va="center", fontsize=8.5, color=C_GAP_B, fontweight="bold",
        linespacing=1.4)

# ── Silhouettes (right side) ──────────────────────────────────────────────────
def silhouette(x, body_top, head_ctr, col, lbl):
    # Vertical body
    ax.plot([x, x], [76, body_top], color=col, lw=2.5, alpha=0.5, zorder=2)
    # Head
    ax.plot(x, head_ctr, "o", ms=18, color=col, alpha=0.25, zorder=2)
    # Shoulders
    ax.plot([x-0.4, x+0.4], [head_ctr-4.5, head_ctr-4.5],
            color=col, lw=3, alpha=0.4)
    # Waist
    ax.plot([x-0.25, x+0.25], [head_ctr-14, head_ctr-14],
            color=col, lw=2, alpha=0.35)
    # Dashed head-height line
    ax.plot([x-0.6, x+0.6], [head_ctr, head_ctr],
            color=col, lw=1, ls="--", alpha=0.6)
    ax.text(x, 75.5, lbl, ha="center", va="top",
            fontsize=8, color=col, style="italic")

silhouette(9.1, 134, 125.2, "#9ca3af", "150 cm user")   # 150cm stance
silhouette(9.6, 174, 162.7, "#4b5563", "190 cm user")   # 190cm stance

# ── Robot base ────────────────────────────────────────────────────────────────
ax.axhline(76, color="#374151", lw=2.5, zorder=3)
ax.text(5, 75.5, "ROBOT BASE", ha="center", va="top",
        fontsize=10, fontweight="bold", color="#374151")

# ── Title ─────────────────────────────────────────────────────────────────────
ax.text(5, 163, "Boxing Robot — Ergonomic Pad Layout",
        ha="center", va="top", fontsize=14, fontweight="bold", color=C_HEAD)
ax.text(5, 161.2, "Stance-corrected centre heights from robot base",
        ha="center", va="top", fontsize=9.5, color="#6b7280", style="italic")

# ── Footer ────────────────────────────────────────────────────────────────────
ax.text(5, 74.5,
        "Stance: −8 cm body crouch  |  −7 cm chin tuck (head only)  |  "
        "Liver via Malaysian ultrasound span data (PubMed/NIH)",
        ha="center", va="top", fontsize=7.5, color="#9ca3af", style="italic")

plt.tight_layout(pad=0.5)
plt.savefig(OUT_FILE, dpi=180, bbox_inches="tight")
print(f"Saved: {OUT_FILE}")
