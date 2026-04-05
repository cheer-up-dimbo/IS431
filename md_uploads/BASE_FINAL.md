**5.2.1 Base**

The base subsystem forms the physical foundation of BoxBunny and is
responsible for supporting the full robot structure, maintaining
stability under punching loads, preserving the boxer's working space,
and enabling practical handling during deployment. Unlike a conventional
static machine base, BoxBunny's base must operate near a moving user. It
therefore cannot be designed purely for maximum footprint or maximum
mass. Instead, it must balance stability, compactness, safety,
manufacturability, and portability within a single structural assembly.

The development of the base progressed through two main phases. The
first phase took place during a robotics fair showcase in first half,
where the robot was mounted on a **long** **wooden board** because this
was the most practical material available at the time. The second phase
was the transition toward a purpose-built **welded steel base-feet
assembly**, developed to better satisfy the long-term engineering needs
of the project. The final design direction now consists of a **welded
trapezoidal base-feet frame** fabricated from **rectangular steel
tubes**, a **flat and rigid mounted steel plate**, and **rear wheels**
intended for tip-and-roll transport.

**5.2.1.1 Requirements & Considerations**

The base subsystem responds to system-level
requirements **RM-1** (*Stability*), **RM-2** (*Compact footprint*),
and **RM-7** (*Portability*) defined in the [Robot
Mechanism] landing
page:

-   **Stability under punching loads:** Remain upright against forward
    tipping under worst-credible strikes, with a factor of safety (FoS)
    ≥ 1.5.

-   **Compact footprint:** Preserve the user\'s footwork space, allowing
    the boxer to approach, pivot, and shift stances without obstruction.

-   **Rigid mounting foundation:** Provide a flat, stiff structural
    interface to prevent misalignment and ensure clear load transfer
    from the mechanisms above.

-   **Practical portability:** Support tip-and-roll transport and
    deployment between workshop and exhibition environments without
    requiring full manual lifting.

-   **Environmental durability:** Withstand repeated exposure to humid
    gym conditions with a realistic corrosion-protection strategy for
    the hollow steel sections.

**5.2.1.2 Design**

The final base design is a **welded trapezoidal base-feet assembly**
built from **70 × 50 mm rectangular steel tubes (RHS) with 3 mm wall
thickness**, combined with a **flat, rigid mounted steel plate** and
rear wheels intended for the transport system.

\[Media placeholder : Base\]

**Trapezoidal Footprint**

*Stability + User Clearance*

The most important geometric feature of the final design is that the
base is **narrower at the front and wider at the rear**. This
trapezoidal strategy reduces the amount of structure intruding into the
boxer's immediate working zone (especially around the lead foot and
pivot region), while increasing restoring leverage against forward
tipping. The wider rear also creates integration space for
lower-mechanism hardware and supports the later addition of rear wheel
brackets and transport features.

**Low-profile Frame:**

*Lower CG + Reduced Obstruction*

The base is intentionally **low profile**. Keeping the main welded frame
close to floor level reduces obstruction and helps keep the centre of
mass of the full system low. The low coordinate of the current centre of
mass is favourable, indicating that mass is concentrated close to the
floor and supporting passive anti-tipping behaviour. While the exact
support margin still depends on the final support polygon and coordinate
reference, the low vertical mass placement is clearly beneficial.

**Rigid Mounted Plate:**

*Datum + Subsystem Alignment*

The mounted plate in the current design is **flat and rigid**, providing
a reliable geometric datum for the mechanism stack above. In mechanical
terms, the base is therefore not only carrying load but also defining
alignment for lower subsystems. This is especially important for the
rotation mechanism and other components that depend on a consistent
plate interface.

**Rear-wheel Transport**

*Tip-and-Roll Portability*

The final design includes rear wheels for transport, consistent with the
tip-and-roll concept. These are intended to support rear-wheel hardware
and the corresponding handling approach. \[placeholder to edit in
conclusion after testing of rear wheels transport system\]

Overall, the final base is not just a support platform. It is a
**purpose-built welded structural subsystem** that combines:

-   a trapezoidal support footprint for stability and user clearance,

-   a low-profile steel frame for efficient load transfer,

-   a rigid mounted plate for subsystem integration,

-   and rear transport intent for future operational portability.

**5.2.1.3 Validation**

At the current stage, the base subsystem has been validated partly
through **analysis and realised geometry**, and partly through **direct
observation of the fabricated assembly**. It has not yet been fully
validated through all planned physical tests.

The primary validation method for the base was the **overturning-moment
check**. The design punch force was converted into a forward tipping
moment about the front edge of the support region, while the self-weight
of the assembly provided a restoring moment through the centre of mass.
The design requirement was that the restoring moment exceed the
overturning moment with a factor of safety of at least **1.5**. This
method was intentionally chosen because it is transparent, conservative,
and directly tied to geometry and mass distribution. It avoids
overreliance on favourable floor conditions or simulation assumptions.
Floor friction was treated as a secondary benefit only, not as the main
stabilising mechanism.

At subsystem level, the following aspects are currently successful:

-   the shift from a temporary wooden support to a proper welded steel
    base,

-   the use of a trapezoidal footprint to improve rearward stability
    while preserving front footwork space,

-   the low-profile geometry and low centre-of-mass strategy,

-   and the flat, rigid mounted plate that provides a suitable datum for
    the mechanism stack.

The main items that remain incomplete are:

-   physical **tip-and-roll transport testing**,

-   final **full-system tipping verification** using the realised
    support polygon and complete mass distribution,

-   and long-term durability verification under repeated use and
    environmental exposure.

A concise subsystem validation summary is given below.

  -------------------------------------------------------------------------
  **Aspect**       **Current    **Basis**
                   status**     
  ---------------- ------------ -------------------------------------------
  Stability logic  Pass         Overturning-moment vs restoring-moment
                   (analysis)   method established and used as primary
                                design check

  Trapezoidal      Pass (design Narrow-front / wide-rear geometry directly
  footprint        intent)      addresses footwork clearance and rearward
  concept                       stability margin

  Low              Pass         CAD mass properties indicate low vertical
  centre-of-mass                mass concentration
  strategy                      

  Mounted plate    Pass         Mounted plate is flat and rigid
  rigidity         (observed)   

  Structural       Pass (design Welded frame provides clearer load path
  load-path        intent)      than the original wooden board
  clarity                       

  Fabrication      Pass         70 × 50 × 3 mm steel tube choice is
  suitability                   appropriate for welded prototype
                                construction

  Tip-and-roll     Partial      Hardware intent present, but physical
  portability                   testing not yet performed

  Long-term        Partial      Protection strategy defined, but long-term
  corrosion                     field validation ongoing
  robustness                    
  -------------------------------------------------------------------------
