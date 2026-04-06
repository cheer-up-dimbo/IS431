**5.2.1.4.2 Mechanical Design**

This page documents the physical realization of the base subsystem,
detailing the structural material choices, fabrication methods,
corrosion-protection strategy, and the integration of transport hardware
for deployment.

**Frame Structure & Fabrication**

The base frame is constructed from **70 × 50 mm Rectangular Hollow
Section (RHS)** mild steel tubing, joined by MIG welding. RHS was
selected over solid bar, angle iron, or channel for several mechanical
and practical reasons:

-   **High second moment of area per unit weight:** Hollow sections
    resist bending and torsion more efficiently than equivalent-weight
    solid sections, which is crucial for resisting overturning moments
    from punches.

-   **Flat external faces:** Enable straightforward mounting of the
    rigid top plate, brackets, and lower mechanisms without requiring
    extensive machining.

-   **Weldability:** Mild steel RHS is straightforward to MIG-weld,
    providing strong, reliable joints for the trapezoidal geometry.

-   **Availability:** SHS/RHS is readily available in standard sizes
    from local steel suppliers.

**Wall Thickness Rationale**

The RHS members are specified with a **wall thickness of 3 mm**. This
sizing provides an optimal balance between total mass and structural
integrity:

-   **Weld penetration:** Ensures adequate fusion depth at butt and
    fillet welds, avoiding the risk of burn-through or cold welds common
    on thinner-walled sections.

-   **Mounting loads:** Safely supports bolted connections for the flat
    mounted plate and mechanisms above without localized buckling or
    tearing at the bolt holes.

-   **Impact resistance:** The tubular sections must resist transmitted
    punching loads without permanent deformation at connection points.

**Portability & Deployment**

BoxBunny must be moved between storage areas, fabrication workshops, and
public demonstration venues. The transport strategy was driven by
requirement **RM-7 (Portability)**: the base must allow transport by 1
person between locations without compromising the planted operational
stance. The transport solution must not require disassembly of the robot
and must function effectively on typical gym and corridor surfaces
(e.g., rubber mats, concrete).

**Gym-Bench Inspiration**

The transport strategy was inspired by **commercial gym benches**, which
face a similar design challenge: they must be heavy and stable during
use, yet easily moved by one person. Gym benches achieve this through
rear-mounted wheels and a front handle, allowing the operator to tilt
the bench backward and roll it. This tip-and-roll approach was adopted
for BoxBunny because the wheels do not touch the floor during normal
use, meaning they introduce no compliance when the robot is under load.

**Transport Hardware**

The base features two rear-mounted wheels located at the widest rear
edge of the trapezoidal footprint:

  -------------------------------------------------------------------------
  **Component**   **Specification**    **Function**
  --------------- -------------------- ------------------------------------
  Transport       **RMNA100** (100mm   Smooth rolling on gym and corridor
  wheels          diameter)            surfaces when tilted backward.

  Wheel mounting  **KCLSBF12-62**      Secure axle retention; standard
  pins                                 clevis-pin format for easy
                                       replacement.
  -------------------------------------------------------------------------

**Planted vs Transport Stance**

A key design principle is that transport features must **not compromise
the planted operational stance**.

-   **Planted:** During training, the base rests flat on the floor with
    its full trapezoidal footprint in contact with the surface,
    maximising friction and stability.

-   **Passive Wheels:** The transport wheels are positioned slightly
    elevated relative to the base feet. They do not contribute to the
    support polygon or introduce rolling compliance while flat.

-   **No Locks Required:** This dual-mode behaviour eliminates the need
    for brake locks, deployment levers, or other complex mechanisms that
    could fail under punching impacts.

**Phase 1: Early Robotics Fair implementation**

The first implemented base configuration was used during the **NUS CDE
Robotics Fair in Week 4 of Semester 2**. At this stage, the primary
objective was safe and rapid deployment using materials that were
immediately available. The robot was mounted on a **1220 mm × 580 mm
wooden board**, which served as the initial support platform for the
early exhibition-stage build.

\[Interactive 3D model: assem_bottom_FAB1\_-\_fair.glb\]

Although this wooden board was not intended to represent the final
engineered base, it provided the first opportunity to assess the
relationship between footprint, body placement, stability, and user
working space. It allowed the robot to be assembled and demonstrated
safely in public and gave the team an early reference point for space
claim, support behaviour, and practical handling.

However, this arrangement had several limitations. The footprint was
availability-driven rather than optimised, the load path into the floor
was not intentionally structured, and the board occupied too much
uniform plan area near the user. It also did not integrate naturally
with wheel brackets, welded hardware, or a central mounting datum. This
made it acceptable for early deployment, but not appropriate as a final
engineered base.

**Phase 2: Stability-driven rethinking of the footprint**

Once the base was treated as an engineered subsystem rather than a
temporary support, the key question became how the robot could remain
stable without making the front working area too bulky for the user.
This led to the shift toward a **trapezoidal footprint**. Instead of
enlarging the base equally in all directions, the design narrowed the
front and widened the rear. This was the most suitable mechanical
compromise because the front remained compact where the user interacts
most closely, while the rear gained support width where stability
leverage is most useful.

**Phase 3: Transition from flat platform to framed steel base**

After the footprint logic was clarified, the next decision was how to
realise it physically. A flat plate or board could provide area, but not
a very clear structural load path. The project therefore moved toward a
**welded steel frame** using rectangular hollow sections. This brought
several mechanical advantages: better bending stiffness for the material
used, clearer load transfer into the floor, easier bracket and subsystem
integration, and a lower profile than a thick monolithic support. The
chosen structural members were **70 mm × 50 mm rectangular steel tubes
with 3 mm wall thickness**.

The section size provides enough depth to act as a true structural frame
member while still remaining close to the floor. The 3 mm wall thickness
is a balanced prototype-scale choice because it is thick enough to be
practical and tolerant in welding, more robust near local bracket and
mounting regions than lighter-gauge tube, and still avoids unnecessary
mass and fabrication burden. From a mechanical-engineering standpoint,
this is a sensible middle-ground choice for a welded prototype base.

**Phase 4: Mounted plate as a structural datum**

As the lower-mechanism stack matured, it became clear that the base did
not only need to support weight; it also needed to define a
geometrically reliable interface for the mechanisms above. This made the
mounted plate critical. The mounted plate therefore had to be both
sufficiently rigid not to flex significantly under subsystem loads and
sufficiently flat not to induce misalignment into the rotation
subsystem. At the current stage, the mounted plate is confirmed to be
**flat and rigid**, which is an important success in the
mechanical-design process.

**Phase 5: Integration of transport intent**

The next iteration step was to incorporate the transport concept
directly into the base rather than treating movement as an external
logistics problem. This led to rear interfaces intended for wheel
hardware and tip-and-roll handling. This decision is mechanically
sensible because the wider rear already provides the best location for
wheel integration, the rear is naturally farther from the user footwork
zone, and moving the robot by tipping from the rear is compatible with
portable gym-equipment handling logic. However, this remains one of the
incomplete areas of the subsystem because the **tip-and-roll feature has
not yet been physically tested**.

**Phase 6: Durability and corrosion thinking**

Once the welded steel base became the final direction, corrosion had to
be treated as part of the base design. Early observations of rust on
steel members showed that both interior and exterior surfaces needed
realistic protection. A key insight was that interior and exterior
corrosion conditions are fundamentally different: exterior surfaces are
accessible and paintable, whereas interior hollow sections are
inaccessible and more prone to trapped moisture. This led to a dual-path
strategy, with interior sections relying on forgiving, penetrating
protective coatings and exterior surfaces relying on mechanical
cleaning, anticorrosion primer, and paint. This is good mechanical
practice because it recognises the real maintenance limits of hollow
welded steel structures. Therefore, during manufacturing stage, it was
deemed important to allocate cost to include in professional primer and
powder coating service as well together with the welding.

**Final Design State**

The final base subsystem can therefore be summarised as follows:

-   it began as a **1220 mm × 580 mm wooden-board prototype base** for
    early fair deployment,

-   it evolved into a **purpose-built welded trapezoidal steel frame**
    after the need for better footwork clearance, clearer load paths,
    and more intentional subsystem integration became clear,

-   the final frame uses **70 × 50 × 3 mm rectangular steel tubes**,

-   the base keeps a **narrower front and wider rear** for user
    clearance and stability,

-   it incorporates a **flat, rigid mounted plate** as the geometric
    interface for the lower-mechanism stack,

-   it includes **rear transport intent**, although tip-and-roll testing
    remains incomplete,

-   and its current CAD-reported centre of mass is **X = 1.89 mm, Y =
    379.29 mm, Z = 67.912 mm** in the assembly coordinate system.

\[include in table stating the hardware component specs and function\]
