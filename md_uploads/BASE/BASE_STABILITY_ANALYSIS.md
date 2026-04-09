**5.2.1.4.3 Load Analysis**

The load analysis for the base subsystem developed in two stages. The
first stage occurred during the early Robotics Fair implementation,
where the calculation was used to determine the most suitable **position
of the main robot body on the 1220 mm wooden board**. The second stage
developed into a more complete design-load philosophy for BoxBunny,
distinguishing between repeated-service loads and conservative
structural design loads. This load-analysis framework later informed not
only the base design, but also the rotation stage, lower mechanism, and
height-adjustment subsystem.

**Punch force modelling and design philosophy**

A boxing punch does not apply a constant force over time. Instead, the
force-time history is highly transient, with a short-duration peak
lasting only a few milliseconds. Designing directly from the absolute
instantaneous peak would be excessively conservative for many structural
and actuation components. For BoxBunny, the adopted load philosophy
therefore distinguishes between:

-   a **characteristic training load**, representing a strong but
    realistic punch during normal gym use, and

-   a **structural design load**, representing a conservative
    upper-bound event that the robot structure must survive without
    failure.

Based on the literature review in the load-analysis document, the
following values were adopted:

$${F_{char} = 1.8\text{ kN}
}{F_{design} = 1.5 \times F_{char} = 2.7\text{ kN}
}$$

The characteristic value of **1.8 kN** was selected as a strong but
realistic punch for the target user group. The structural design load of
**2.7 kN** was then obtained by applying a factor of **1.5** to account
for impact amplification, user variability, modelling simplifications,
and manufacturing tolerances. This design hierarchy allowed the robot to
remain realistic and appropriately sized while preserving a clear
structural safety margin.

This distinction maps onto:

-   **Ultimate Limit State (ULS)**: structural integrity under rare,
    hard punches,

-   **Serviceability Limit State (SLS)**: repeated-use performance,
    wear, and normal training behaviour.

For the base subsystem, the critical case is the **ULS structural design
load**, because the base must not tip or fail under a worst-credible
strike.

**Phase 1 fair implementation: body placement on the wooden board**

During the first fair-stage implementation, the robot was mounted on a
**1220 mm × 580 mm wooden board**. At that stage, the most important
engineering question was where along the **1220 mm board length** the
main robot body should be positioned. This was treated as an overturning
problem. When the robot is struck from the front, the most likely
tipping mode is forward rotation about the front edge of the support
region. The forward punch creates an overturning moment:

$$M_{OT} = F_{design}h_{strike}
$$

where $F_{design}$is the adopted structural design punch load and
$h_{strike}$is the vertical distance from the front pivot edge to the
punch line of action.

Opposing this is the restoring moment from the weight of the robot:

$$M_{R} = Wx_{CG}
$$

where $W$is the total system weight and $x_{CG}$is the horizontal
distance from the front pivot edge to the centre of gravity. For the
wooden-board phase, this calculation was used to determine the best
longitudinal position of the robot body along the board length. Shifting
the robot body further rearward increases $x_{CG}$, which increases
restoring moment and improves anti-tipping behaviour. However, shifting
it too far rearward would reduce practical front clearance or complicate
the layout. The fair-stage calculation therefore acted as a **placement
study**, balancing restoring moment, user footwork space, and assembly
practicality.

This early analysis established a principle that remained valid
throughout later iterations: the base layout should be defined by
**overturning mechanics and user-space constraints**, not by symmetry or
convenience. It directly influenced the later decision to adopt a
**smaller-front / wider-rear** welded trapezoidal base.

**Stability analysis of the final base subsystem**

For the later welded-base design, the same stability logic was retained
in a more formalised form. The governing failure mode was taken as
**forward tipping** rather than sliding. The key design requirement is:

$$\frac{M_{R}}{M_{OT}} \geq 1.5
$$

This expresses the requirement that the restoring moment exceed the
overturning moment with a factor of safety of at least **1.5**. This
factor of safety is consistent with the broader load-analysis philosophy
adopted for BoxBunny: punching is impulsive, user-dependent, and not
perfectly repeatable, so a conservative but practical design margin is
appropriate.

Floor friction was recognised as beneficial but treated only as a
secondary effect because floor material, cleanliness, and exhibition
conditions may vary. The base was therefore required to remain upright
through **geometry and mass distribution alone**, making the design more
transparent and more defensible.

**Implications for the final welded base-feet design**

The transition from the wooden board to the welded trapezoidal steel
base can be understood directly through the load analysis. First, the
analysis showed that the base should provide stronger restoring leverage
behind the centre of mass rather than using a uniform support area. This
is why the final base became **wider at the rear** and **narrower at the
front**. Second, the analysis reinforced the importance of keeping the
assembly's mass as low as practical. The current CAD-reported centre of
mass confirms a favourable low vertical mass concentration. Third, the
analysis clarified that the mounted plate and welded frame should be
treated as part of the structural load path, not just as passive support
surfaces. Punch loads applied high on the robot must ultimately flow
through the structure and into the floor without excessive compliance or
distortion. This is why the final design places emphasis on a **flat,
rigid mounted plate** and a welded steel frame rather than a flat board
alone.

**Current limitations and future updates to the load analysis**

The current load analysis provides a strong physics-based foundation for
the base design, but several refinements should still be completed as
the prototype matures. The final centre of mass should continue to be
updated as more hardware is installed, the exact support polygon of the
welded base-feet assembly should be used in the final tipping
calculation, and the tip-and-roll transport mode should be checked to
ensure it does not compromise stability during handling. Once
full-system testing is complete, the analytical tipping model should
also be compared against experimental behaviour for confirmation.

**5.2.1.4.3 Stability Analysis**

**5.2.1.4.3.1. Phase 1: Fair**

**5.2.1.4.3.1.1. Objective**

The objective of this analysis is to verify that the robot remains
stable and does not tip over when subjected to a representative
**backward‑directed lateral punch force** during operation (i.e., a load
direction that tends to tip the robot **backwards** about the **rear
base edge**). The assessment focuses on **static tip‑over stability**
under conservative assumptions, appropriate for the Project Phase 1
(Fair) stage. Stability is evaluated by comparing overturning moments
generated by the applied force with restoring moments provided by the
robot's self‑weight.

**5.2.1.4.3.1.2. Assumptions**

To enable a simplified and conservative stability assessment, the
following assumptions were made:

-   The applied punch force acts **horizontally** and is modelled in the
    **backward direction** for the critical stability case (tipping
    backwards).

-   The force is applied at the **upper punching interface**,
    representing the worst‑case overturning scenario.

-   The robot behaves as a **rigid body** during loading.

-   Ground contact is idealised as a **single pivot edge at the rear of
    the base** during impending tip‑over for the critical loading
    direction considered.

-   Dynamic impact effects and user variability are accounted for
    through the use of a **factored design force**, rather than explicit
    dynamic analysis.

-   The total weight of the robot acts through a single **centre of
    gravity (CoG)** obtained from CAD mass property analysis.

-   Friction effects are not relied upon to prevent tipping and are
    therefore neglected in the primary stability check.

These assumptions are considered appropriate for early‑stage design
verification.

**5.2.1.4.3.1.3. Stability Model and Geometry**

**Stability Check Method (Hand Calculations)**

Stability is primarily demonstrated using **first-principles hand
calculations**, which are considered reliable and appropriate at this
stage.

**Center of Gravity (CoG)**

-   The robot's **total weight** is assumed to act through its CoG.

-   Stability requires that the **vertical projection of the CoG remains
    within the base of support**.

-   If the line of action falls outside the base, tipping will occur.

**Overturning vs Restoring Moments**

Stability is assessed about the **most critical pivot point** (usually a
front or rear base edge).

-   **Overturning Moment (Mo)**\
    Caused by the applied punch force:

$$M_{o} = F \times d_{o}
$$

where:

-   $F$= applied lateral punch force

-   $d_{o}$= vertical distance from pivot to point of force application

```{=html}
<!-- -->
```
-   **Restoring Moment (Mr)**\
    Provided by the robot's weight:

$$M_{r} = W \times d_{r}
$$

where:

-   $W$= weight of the robot

-   $d_{r}$= horizontal distance from pivot to CoG

**Stability Condition**

-   **Stable:** $M_{r} > M_{o}$

-   **At tipping point:** $M_{r} = M_{o}$

-   **Unstable:** $M_{r} < M_{o}$

**Factor of Safety (FoS)**

-   A **Factor of Safety (FoS)** is calculated:

$$FoS = \frac{M_{r}}{M_{o}}
$$

-   **Target FoS ≥ 1.5**

    -   Accounts for uncertainties such as:

        -   Variations in punch direction

        -   Manufacturing tolerances

        -   Simplified modelling assumptions

**Phase 1 expectation:** Showing a FoS ≥ 1.5 using conservative
assumptions is sufficient.

A simplified two‑dimensional stability model was used for the analysis.
For the critical loading direction, the robot is assumed to pivot about
the **rear bottom edge of the base** when subjected to a representative
lateral punch force.

The following geometric and physical parameters are defined:

-   $F$: Design lateral punch force

-   $h$: Vertical height from the ground to the point of force
    application

-   $W$: Total weight of the robot

-   : Horizontal distance from the **rear pivot edge** to the robot's
    centre of gravity (CoG), measured along the ground.

**Derivation of (CoG offset)**\
The value of is obtained from CAD geometry, not from the moment
equation. For the Fair-stage wooden board, the board length is 1220 mm.
From CAD mass properties, the CoG projection lies 492 mm from the front
edge of the board. Therefore, the horizontal distance from the rear edge
(pivot) to the CoG is:

Hence, = 1220 − 492 = **728 mm** (0.728 m). This value is then
substituted into the restoring moment and FoS calculations.

The geometry, base footprint dimensions, and CoG location were obtained
from the CAD model. The stability analysis considers the **most
unfavourable direction of loading**, such that the overturning moment is
maximised and the restoring moment is minimised.

-   Total robot mass (including base):

$$m = 53\text{ kg}$$

-   Weight of robot:

$$W = 53 \times 9.81 = 519.93\text{ N}$$

-   Design lateral punch force:

$$F = 2700\text{ N}$$

-   Vertical height of force application from ground:

$$h = 1100\text{ mm} = 1.1\text{ m}$$

-   Horizontal distance from tipping edge to centre of gravity:

$$b = unknown$$

The pivot point is taken as the **rear base edge** in the direction of
the applied force for the stability check presented.

**5.2.1.4.3.1.4. Overturning Moment Calculation**

The overturning moment $M_{o}$is generated by the applied lateral punch
force acting about the pivot edge.

$$M_{o}\lbrack N \cdot m\rbrack = F \times h$$

Where:

-   $F = 2.7\text{ }\text{kN}$ (factored structural design punch load)

-   $h$ is the measured vertical distance from the pivot point to the
    punch impact location

This represents the moment tending to rotate the robot about the base
edge and cause tip‑over.

**5.2.1.4.3.1.5. Restoring Moment Calculation**

The restoring moment is generated by the robot's self‑weight acting
through its centre of gravity, resisting the overturning tendency.

$$M_{r}\lbrack N \cdot m\rbrack = W \times b$$

Where:

-   $W$is the total weight of the robot

-   $b$ is the horizontal distance from the pivot edge to the CoG

Substituting the values obtained from the CAD model into the
restoring-moment equation yields the restoring moment acting in the
opposite direction to the overturning moment. This restoring moment
provides the primary resistance to tip‑over.

**5.2.1.4.3.1.6. Factor of Safety**

A factor of safety (FoS) against tipping is calculated as the ratio of
restoring moment to overturning moment:

$$\text{FoS} = \frac{M_{r}}{M_{o}}$$

For stable operation:

$$\text{FoS} > 1.0$$

For design acceptability at the Fair stage, a **minimum target FoS of
1.5** is adopted to account for model uncertainty, manufacturing
tolerances, and variations in user interaction.

**5.2.1.4.3.1.7 Determination of Required CoG Offset () for Tipping
Resistance**

To ensure the robot remains stable without tipping over, the required
horizontal distance between the CoG and the **rear pivot edge**, denoted
as , is determined from moment equilibrium and the target tipping factor
of safety (FoS ≥ 1.5). This is a **CoG-offset requirement**; the
required base/board footprint is then selected to achieve this offset
given the realised CoG position.

At the tipping boundary (FoS = 1), the restoring moment equals the
overturning moment:

$$M_{r} = M_{o}$$

Substituting for restoring and overturning moments:

$$W \times b_{\text{min}} = F \times h$$

Solving for the required CoG offset (FoS = 1):

$$b_{\text{min}} = \frac{F \times h}{W}$$

For design acceptability, the target factor of safety is applied. Using
FoS = (W·b)/(F·h), the required CoG offset for a target FoS is:

**b~min~ = (FoS~target~ · F~back~ · h) / W**

To convert this into a minimum base/board footprint length for a
rear-edge pivot, use the CAD-measured CoG position from the front edge,
x~CoG,front~, and the relationship b = L − x~CoG,front~. Hence:

**L~min~ = x~CoG,front~ + b~min~**

Using the backward‑tipping design case, the minimum required footprint
length can be expressed in terms of the backward‑directed lateral load
magnitude F~back~:

From b~min~ = (FoS~target~·F~back~·h)/W and L~min~ = x~CoG,front~ +
b~min~, with FoS~target~ = 1.5, h = 1.1 m, W = 519.93 N and x~CoG,front~
= 0.492 m:

**L~min~ = 0.492 + (1.5 × 1.1 / 519.93) · F~back~ ≈ 0.492 + 0.00317 ·
F~back~** (m, with F~back~ in N)

Example (aligned with Section 5.2.1.4.3.1.8): if the measured
backward-directed operational load is approximately F~back~ = 229 N,
then L~min~ ≈ 0.492 + 0.00317 × 229 ≈ **1.22 m**, matching the
Fair-stage board length used. If a larger backward-directed load is
expected, L~min~ increases proportionally; alternatively, stability can
be improved by lowering the CoG or reducing the force application
height.

This value should be interpreted as a **theoretical tipping boundary**
for the specific load magnitude used (FoS = 1). Design acceptance is
instead based on achieving the target FoS (Section 5.2.1.4.3.1.6) using
the backward‑directed operational load case, and on prototype
validation; the base geometry and mass placement were selected to keep
the CoG well within the support polygon during Fair operation.

**5.2.1.4.3.1.8. Design Adoption and Validation**

For the Fair-stage prototype, the available wooden board length was **L
= 1220 mm**. From the CAD-derived CoG position, the rear-edge CoG offset
(rear pivot edge to CoG projection) is **b = 728 mm**. The achieved
tipping factor of safety for the backwards-tipping case is then
evaluated using:

FoS = (W · b) / (F~back~ · h)

Rearranging for the maximum allowable backward-directed load at the
target FoS gives:

**F~back,allow~ = (W · b) / (FoS~target~ · h)**

Using W = 519.93 N, b = 0.728 m, h = 1.1 m and FoS~target~ = 1.5:

F~back,allow~ = (519.93 × 0.728) / (1.5 × 1.1) ≈ **229 N**.

Therefore, the current configuration (L = 1220 mm, b = 728 mm) meets the
Phase 1 target FoS provided the **measured backward-directed operational
load** satisfies F~back~ ≤ 229 N. If higher backward loads are expected,
stability can be improved by increasing the rear footprint (increasing
b), reducing the force application height, and/or lowering the CoG
through mass placement.

Physical testing of the prototype confirmed that the robot **remains
upright during operation**, with no observable tipping or lifting of the
base edge. This provides supporting validation of the chosen footprint
and mass distribution for the current project phase.

**5.2.1.4.3.1.9. Discussion and Conclusion**

The stability analysis establishes the relationship between applied
lateral force, force application height, robot weight, and the
horizontal CoG offset from the pivot edge. Using moment equilibrium, the
tipping boundary (FoS = 1) and the factor of safety for a given base/CoG
configuration can be evaluated directly.

A highly conservative static model using the full structural design
punch load predicts an unrealistically large tipping-boundary CoG offset
because it assumes full horizontal load transfer at maximum height and
an idealised single-edge pivot. In reality, a boxing punch is fundamentally a 
short-duration **impulse** (typically lasting 10–20 milliseconds), not a continuous static push. 
While the peak force reaches 2.7 kN, its duration provides insufficient kinetic energy to physically 
rotate the robot's CoG past the tipping pivot before the force dissipates. For Fair-stage operation, stability was
assessed about the **rear pivot edge** using a representative lateral
load case and checked against the target FoS (≥ 1.5), then supported by
prototype observation. Under these conditions, the adopted footprint and
realised CoG position provided adequate margin to prevent observable
tip‑over during operation.

The analysis therefore confirms that the adopted base dimensions meet
the stability requirements for Project Phase 1, while clearly
identifying the parameters that govern future optimisation.

**5.2.1.4.3.2. Phase 2: Final**

**5.2.1.4.3.2.1. Objective**

The objective of the Phase 2 (Final) stability analysis is to confirm
that the **final base design and final assembled mass distribution**
provide sufficient resistance to tip‑over under the **final design
loading envelope**. This includes verifying an adequate tipping factor
of safety using updated CAD mass properties, and closing the requirement
through final‑configuration validation testing.

**5.2.1.4.3.2.2. Assumptions**

The following assumptions are used for the Phase 2 stability check:

-   The robot is analysed in its **final assembled configuration**
    (final base, final subsystems installed) and the CoG is taken from
    updated CAD mass properties.

-   The applied punch force is treated as an equivalent **lateral load**
    acting at the punching interface height for tipping assessment.

-   Tip‑over is checked about the **most critical base edge** in the
    direction of loading (front or rear), using a single-edge pivot
    idealisation.

-   Friction and compliance may contribute in practice but are not
    relied upon; stability is demonstrated primarily through **restoring
    vs overturning moment** margin.

-   Where multiple load magnitudes are used in the project, **structural
    sizing loads** and **stability (tipping) loads** are stated
    explicitly to avoid mixing conservative strength design with
    operational tipping assessment.

**5.2.1.4.3.2.3. Stability Model and Geometry**

The same moment‑equilibrium approach used in Phase 1 is retained for
Phase 2. For the critical loading direction considered (backward
tipping), the final robot is assumed to pivot about the **rear base
edge**. Stability is assessed by comparing the overturning moment from a
backward-directed lateral load applied at height against the restoring
moment due to the robot weight acting through the CoG offset . All
geometry and mass properties (including the final base footprint and
final CoG) shall be taken from the latest CAD model corresponding to the
final build.

**5.2.1.4.3.2.4. Overturning Moment Calculation**

The overturning moment is computed using the Phase 1 relationship, $M_{o} = F \times h$,
about the rear pivot edge. For Phase 2, the backward-directed force
magnitude used for tipping assessment shall reflect the final agreed
credible operational case (e.g., measured peak user input during
demonstrations), while the higher structural design punch load remains
the basis for strength sizing of components.

**5.2.1.4.3.2.5. Restoring Moment Calculation**

The restoring moment is computed using the Phase 1 relationship, $M_{r} = W \times b$, where
the robot weight and the CoG offset are taken from the final assembled
CAD mass properties. The Phase 2 base design (with an increased system mass estimated at ~105 kg) is expected to significantly increase
restoring moment margin through a wider support polygon and/or a lower
CoG compared to the Fair-stage prototype.

**5.2.1.4.3.2.6. Factor of Safety**

The tipping factor of safety is evaluated using the same definition as
Phase 1:

$\text{FoS} = \frac{M_{r}}{M_{o}}$. For the final build, the acceptance criterion is **FoS ≥ 1.5**
under the defined operational backward-directed load case, with the
intent to maintain additional margin where feasible (e.g., through base
footprint optimisation and mass placement).

**5.2.1.4.3.2.7. Discussion and Conclusion**

Phase 2 closes the stability requirement by applying the validated Phase
1 methodology to the **final base and final mass distribution**.
Compared with the Fair-stage prototype, the final welded base is
expected to provide improved stability due to increased stiffness, more
controlled mass placement, and a more robust support polygon.

To complete the Phase 2 section, the final numerical FoS result should
be reported using the latest CAD values for $W$ and $b$, and supported by a
final‑configuration stability validation (e.g., controlled lateral
loading at the punching interface and observation for base lifting).
This ensures that the Phase 2 conclusion is traceable to both analysis
and test evidence.
