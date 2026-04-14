# Kinematic Derivation — Coaxial Differential Joint

---

## 1. Physical Architecture

The wrist joint consists of two **concentric coaxial tubes** enclosed within the arm housing:

- **Outer tube** — driven by the **roll motor (M1/M3)**
- **Inner tube** — driven by the **pitch motor (M2/M4)**

Both motors are mounted proximally (at the shoulder end) and connect to their respective tube via an **identical 3:1 herringbone spur gear reduction**: a small spur gear on the motor shaft meshes with a larger coaxial herringbone gear keyed to the tube. The motor must therefore complete **three full revolutions** for the tube to complete **one full revolution**.

At the distal end of the arm, a **1:1 bevel gear pair** converts the *difference* in rotation between the inner and outer tubes into pitch — the angle at which the arm tip swings away from the tube axis.

```
Motor shaft (M1)
    │
    ├─[small spur gear]──────[large coaxial gear]── Outer tube (roll)
    │                              3:1 reduction
Motor shaft (M2)
    │
    ├─[small spur gear]──────[large coaxial gear]── Inner tube
    │                              3:1 reduction                    
    │                                               └──[1:1 bevel gear]── Arm tip (pitch)
```

---

## 2. Notation

| Symbol | Meaning |
|--------|---------|
| $m_r, m_p$ | Raw motor encoder positions (radians) — roll and pitch motors |
| $o_r, o_p$ | Calibration offsets — encoder value at mechanical zero |
| $G = 3$ | Gear reduction ratio (motor turns : tube turns) |
| $s_r, s_p$ | Sign parameters: $\pm 1$, account for motor mounting orientation |
| $c$ | Coupling parameter: $\pm 1$, determined by bevel gear mounting side |
| $\phi_\text{outer}, \phi_\text{inner}$ | Absolute rotation of each tube, measured from their shared zero (radians) |
| $\theta_\text{roll}, \theta_\text{pitch}$ | Joint angles at the arm tip: roll = tube body rotation; pitch = arm swing from tube axis (radians) |

---

## 3. Simplified Derivation (Canonical Case)

Before introducing sign conventions and calibration offsets, it is instructive to derive the kinematic equations for a **canonical configuration**: positive motor rotation produces positive tube rotation for both motors, and the bevel gear is mounted such that inner-tube rotation in the positive direction produces positive pitch. All encoder offsets are zero (motors zeroed at the mechanical neutral position).

### 3.1 Gear Reduction

Both motors drive their respective tubes through the 3:1 herringbone reduction:

$$\phi_\text{outer} = \frac{m_r}{G}, \qquad \phi_\text{inner} = \frac{m_p}{G}, \qquad G = 3$$

### 3.2 Pitch from the Tube Rotation Difference

The bevel gear is fixed inside the outer tube. It only actuates when the two tubes rotate by *different amounts* — the difference in their rotations turns the bevel and swings the arm tip. Because the bevel ratio is 1:1, the swing angle (pitch) equals that difference directly:

$$\theta_\text{pitch} = \phi_\text{inner} - \phi_\text{outer} = \frac{m_p - m_r}{G}$$

Roll is simply how far the outer tube has turned:

$$\theta_\text{roll} = \phi_\text{outer} = \frac{m_r}{G}$$

### 3.3 Canonical Forward Kinematics

$$\boxed{\theta_\text{roll} = \frac{m_r}{3}, \qquad \theta_\text{pitch} = \frac{m_p - m_r}{3}}$$

### 3.4 Canonical Inverse Kinematics

Solving for motor commands given desired joint angles:

$$m_r = 3\,\theta_\text{roll}$$

$$m_p = 3\,\theta_\text{pitch} + m_r = 3(\theta_\text{pitch} + \theta_\text{roll})$$

### 3.5 Canonical Pure-Roll Condition

Setting $\theta_\text{pitch} = 0$:

$$\frac{m_p - m_r}{3} = 0 \;\Rightarrow\; m_p = m_r$$

Both motors must advance by the same amount. This is the mechanical rule stated in Section 10 of 2DOF.md, here recovered as a direct algebraic consequence.

> **Note on real hardware:** Physical motor mounting, gear meshing direction, and bevel gear side may reverse the positive direction of either motor axis. The sign parameters $s_r$, $s_p$, $c$ in Sections 5–9 are book-keeping variables that restore the canonical relationship for any physical build without altering the underlying geometry.

### 3.6 From Canonical to General: Physical Mounting Factors

Three physical decisions made during assembly can cause the real hardware to deviate from the canonical equations. Each deviation is captured by a single variable in the general equations.

---

#### Factor 1 — Motor Mounting Orientation → $s_r$, $s_p$

In the canonical case, a positive command to each motor was assumed to produce a positive rotation of its corresponding tube (i.e., the motor shaft and the tube share the same positive-rotation convention).

In practice, the motor may be mounted in any orientation that fits the housing. **If the motor is flipped or rotated 180° around the tube axis, its shaft's positive direction is reversed relative to the tube.** The gear mesh cannot correct this — it simply transmits whatever direction the motor provides.

| Motor mounting | Effect on tube rotation | Variable value |
|----------------|------------------------|----------------|
| Positive motor → positive tube | Canonical — no correction needed | $s = +1$ |
| Positive motor → negative tube | Directions are reversed | $s = -1$ |

The same analysis applies independently to M1 (roll) and M2 (pitch), giving two independent sign parameters $s_r$ and $s_p$. Multiplying the motor displacement by $s$ before dividing by $G$ restores the canonical relationship regardless of how the motor is mounted.

---

#### Factor 2 — Bevel Gear Mounting Side → $c$

The canonical derivation assumed that positive inner-tube rotation relative to the outer tube produces positive pitch. Whether this holds physically depends on **which face of the central driving bevel gear the driven bevel gear is meshed against**.

When the driven bevel is mounted on the opposite side, the direction of pitch reversal is reversed:

| Bevel configuration | Effect on pitch direction when inner tube leads | Variable value |
|---------------------|------------------------------------------------|----------------|
| Configuration A (left side) | Inner-tube advance → arm pitches downward | $c$ takes the negative sign |
| Configuration B (right side) | Inner-tube advance → arm pitches upward | $c$ takes the positive sign |

Because both arms in this build use the same physical bevel orientation, both share $c = -1$. If the bevel is remounted to the opposite side after disassembly, the calibration probe (`motor_probe.py`) re-determines $c$ automatically.

> **Why magnitude is always 1:** The bevel gear ratio is 1:1 and both gear trains have the same 3:1 reduction. The walking effect therefore occurs at exactly the same angular rate as the outer-tube rotation. There is no partial coupling — the coupling magnitude is geometrically fixed at $|c| = 1$.

---

#### Factor 3 — Encoder Zero Position → $o_r$, $o_p$

Motor encoders report an angle relative to wherever the shaft was when the encoder was last zeroed (typically at power-on or factory calibration). There is no guarantee that this electrical zero coincides with the **mechanical neutral position** of the joint (arm pointing straight out, zero pitch).

The offset $o_r$ (roll) and $o_p$ (pitch) are the raw encoder readings recorded when the arm is physically positioned at its neutral pose. Subtracting these offsets from every subsequent encoder reading shifts the origin of the motor coordinate system to match the mechanical zero, so that $m_r - o_r = 0$ and $m_p - o_p = 0$ when the arm is at rest.

---

#### Combined Effect

Applying all three corrections simultaneously — sign flip for mounting, coupling sign for bevel side, and offset subtraction for encoder zero — extends the canonical equations into the general form derived in Sections 5–9, valid for any physical build of the assembly.

| Canonical equation | General equation |
|--------------------|-----------------|
| $\theta_\text{roll} = \dfrac{m_r}{G}$ | $\theta_\text{roll} = s_r \cdot \dfrac{m_r - o_r}{G}$ |
| $\theta_\text{pitch} = \dfrac{m_p - m_r}{G}$ | $\theta_\text{pitch} = \dfrac{s_p(m_p - o_p) + c(m_r - o_r)}{G}$ |

The underlying geometry is unchanged. The additional variables are purely a coordinate bookkeeping layer.

---

## 5. Step 1 — Gear Reduction: Motor Space → Tube Space (General Case)

Each motor drives its respective tube through the 3:1 herringbone reduction. The tube angle in the **lab frame** is therefore the motor displacement divided by $G$, with a sign convention applied for mounting orientation and an offset subtracted to establish the calibration zero:

$$\phi_\text{outer} = s_r \cdot \frac{m_r - o_r}{G}$$

$$\phi_\text{inner} = s_p \cdot \frac{m_p - o_p}{G}$$

Both equations share the same form because both gear trains are mechanically identical (same tooth counts, same reduction ratio).

---

## 6. Step 2 — Bevel Gear Differential

The 1:1 bevel gear is fixed inside the outer tube. It actuates when the two tubes turn by *different amounts*. When both tubes turn together, the bevel sees no differential and the arm stays put. When the inner tube turns more (or less) than the outer, the bevel converts that difference directly into pitch — the arm swings away from the tube axis.

The differential rotation driving the bevel is:

$$\delta\phi = \phi_\text{inner} - \phi_\text{outer}$$

Because the bevel ratio is **1:1**, this maps directly to pitch:

$$\theta_\text{pitch} = \delta\phi = \phi_\text{inner} - \phi_\text{outer}$$

Substituting the gear-reduced expressions from Step 1:

$$\boxed{\theta_\text{pitch} = \frac{s_p(m_p - o_p) - s_r(m_r - o_r)}{G}}$$

Roll is the outer tube rotation:

$$\boxed{\theta_\text{roll} = s_r \cdot \frac{m_r - o_r}{G}}$$

---

## 7. Step 3 — The Coupling Term

The pitch equation contains a subtraction of the outer tube's rotation. This is not an empirical fit — it follows directly from the bevel gear differential: the bevel only swings the arm by the *difference* in tube rotations. Roll motor motion contributes to that difference just as much as pitch motor motion does.

Rewriting in the generalised firmware notation:

$$\theta_\text{pitch} = \frac{s_p(m_p - o_p) + c \cdot (m_r - o_r)}{G}$$

Comparing with the derived equation, the coupling parameter is:

$$c = -s_r$$

When the roll motor is wired so that positive commands produce positive roll ($s_r = +1$), the coupling is $c = -1$. This is confirmed by the calibration results for both arms (§13.6 of 2DOF.md), where $c = -1$ for both assemblies.

> **Key conclusion:** $c$ is not a tuned parameter. Its magnitude is always $|c| = 1$ because both gear trains share the same 3:1 reduction and the bevel ratio is 1:1. Its sign is set by which face of the driving bevel the driven bevel meshes on (§11, 2DOF.md — Configuration A vs B).

---

## 8. Step 4 — Verification: Pure-Roll Condition

Pure roll requires the arm tip to spin around the tube axis with no pitch change ($\theta_\text{pitch} = 0$). Setting the pitch equation to zero:

$$\frac{s_p(m_p - o_p) - s_r(m_r - o_r)}{G} = 0$$

$$\Rightarrow s_p(m_p - o_p) = s_r(m_r - o_r)$$

Both motors must advance by the same signed displacement, so that the bevel sees zero differential and the arm angle stays fixed. This reproduces the physical rule from §10 of 2DOF.md — *"both motors must be commanded to move at the same speed and distance"* — as a direct algebraic consequence of the bevel gear differential, requiring no physical testing to discover.

---

## 9. Step 5 — Inverse Kinematics (Algebraic Inversion)

Given desired joint angles $(\theta_\text{roll},\ \theta_\text{pitch})$, the required motor commands are found by solving the two-equation forward system algebraically.

**From the roll equation:**

$$\Delta_r = s_r \cdot G \cdot \theta_\text{roll}, \qquad m_r = \Delta_r + o_r$$

**Substituting into the pitch equation and solving for $m_p$:**

$$m_p = \left(s_p \cdot G \cdot \theta_\text{pitch} + c \cdot \Delta_r\right) + o_p$$

The $c \cdot \Delta_r$ term is the **differential compensation**: because the pitch motor must produce the desired arm swing *on top of* whatever the roll motor has already contributed to the bevel differential, the roll motor's displacement is added back in before converting to a motor command.

---

## 10. Summary

| Quantity | Origin |
|----------|--------|
| $G = 3$ | Herringbone gear tooth count ratio |
| $s_r,\ s_p = \pm 1$ | Motor wiring / mounting orientation — determined by calibration probe |
| Bevel ratio $= 1:1$ | Bevel gear tooth count |
| Pitch = bevel differential | Arm swings by the difference in tube rotations; intrinsic to the tube axis |
| $c = -s_r$ | Sign of the bevel differential — set by which bevel face is meshed |
| Pure-roll rule | Algebraic consequence of $\theta_\text{pitch} = 0$ |
| Inverse kinematics | Direct algebraic inversion of forward equations |

The complete kinematic model is derived entirely from **gear tooth ratios** and **bevel gear differential geometry**. No system identification, curve fitting, or software back-derivation was employed.

---

## 11. Forward Kinematics: Arm Tip Position in 3D Space

Pitch ($\theta_\text{pitch}$) is the angle between the arm and the tube axis — zero when the arm points straight out along $x$, increasing as it swings away. Roll ($\theta_\text{roll}$) selects the *direction* of that swing in the plane perpendicular to the tube. Together they act as polar coordinates for the arm tip:

$$\vec{d}_\text{arm} = \begin{bmatrix} s_x \cdot \cos(\theta_\text{pitch}) \\ \sin(\theta_\text{pitch}) \cdot \cos(\theta_\text{roll}) \\ \sin(\theta_\text{pitch}) \cdot \sin(\theta_\text{roll}) \end{bmatrix}$$

where $s_x = -1$ for the left arm and $s_x = +1$ for the right arm.

**Inverse kinematics from a 3D target:** Given a normalised direction vector $\vec{d} = (\vec{t} - \vec{s}) / |\vec{t} - \vec{s}|$ from shoulder $\vec{s}$ to target $\vec{t}$:

$$\theta_\text{pitch} = \arccos(d_x \cdot s_x)$$

$$\theta_\text{roll} = \text{atan2}(d_z,\ d_y) \qquad (\text{valid when } \theta_\text{pitch} \neq 0)$$
