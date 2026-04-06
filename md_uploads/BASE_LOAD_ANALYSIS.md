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
