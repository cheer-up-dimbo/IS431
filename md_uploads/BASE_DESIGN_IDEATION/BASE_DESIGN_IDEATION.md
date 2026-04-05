**5.2.1.4 Detailed Documentation**

**5.2.1.4.1 Design Ideation**

BoxBunny\'s base must satisfy two competing system-level requirements
simultaneously: **RM-1 --- structural stability under worst-credible
punching loads** and **RM-2 --- safe compactness for user footwork**.
This page documents the geometry selection rationale, footwork clearance
analysis, and comparison with alternative base shapes.

**The Problem: Competing Requirements**

A simple approach to stability would be to enlarge the base in all
directions, maximising the support polygon and restoring moment.
However, BoxBunny operates **within arm\'s reach of a boxer**, so the
base cannot extend significantly in front or to the sides without
creating trip hazards, obstructing pivots, and encroaching on the
boxer\'s working zone. Boxing gyms are often space-constrained, with
multiple users training in parallel, so the base must also minimise its
overall spatial footprint.

The design challenge is therefore to find a base geometry that:

-   Provides sufficient support width at the **rear** for stability and
    mechanism mounting

-   Remains **narrow at the front** to preserve the boxer\'s footwork
    envelope

-   Keeps the combined centre of gravity **biased rearward** to resist
    forward tipping under frontal punches

-   Accommodates rear-mounted **transport features** without
    compromising the planted operational stance

**Trapezoidal Geometry Rationale**

The final base solution is a **welded trapezoidal steel-tube
platform** with a **narrower front** and **wider rear**. This shape was
selected because it directly addresses both the stability and
compactness requirements in a single geometric form:

-   **Narrow front edge:** Reduces obstruction near the boxer\'s lead
    foot, leaving space for pivots, lateral adjustments, and stance
    changes. The boxer can position their lead foot close to the robot
    without risk of stepping on or colliding with the base during
    footwork drills.

-   **Wide rear section:** Provides more area for mounting the lower
    mechanisms (slewing bearing, linear stage), optional ballast (e.g.
    standard gym weights), and transport features. The wider rear also
    extends the support polygon rearward, directly increasing the
    restoring moment against forward tipping.

-   **Off-centre mechanism placement:** The support structure holding
    the robot --- particularly the slewing bearing and linear stage ---
    is intentionally offset towards the rear of the base. This shifts
    the combined centre of gravity backward, further increasing
    resistance to forward tipping under frontal punches.

![Figure: CAD overview of trapezoidal base component on
BoxBunny.](media/image1.png){width="1.5778685476815397in"
height="1.8571380139982503in"}*~Figure:\ CAD\ overview\ of\ trapezoidal\ base\ component\ on\ BoxBunny.~*

![Figure: Off-centre placement of motion mechanisms relative to base
centre axis for improved
stability.](media/image2.png){width="1.9368011811023622in"
height="1.7745898950131234in"}*~Figure:\ Off-centre\ placement\ of\ motion\ mechanisms\ relative\ to\ base\ centre\ axis\ for\ improved\ stability.~*

**Comparison with Alternative Shapes**

Three alternative base geometries were considered before the trapezoidal
layout was selected:

  ------------------------------------------------------------------------------
  **Shape**       **Stability**        **Footwork           **Verdict**
                                       Clearance**          
  --------------- -------------------- -------------------- --------------------
  Large circle    Good --- uniform     Poor --- extends     Rejected --- trip
                  support radius       into front/side      hazard during
                                       pivot zones          footwork

  Large rectangle Good --- wide        Poor --- front       Rejected ---
                  support polygon      corners extend into  obstructs lateral
                                       pivot arcs           movement

  Small square    Poor --- limited     Good --- compact     Rejected ---
                  restoring moment     footprint            insufficient
                                                            stability margin

  **Trapezoid**   **Good** --- wide    **Good** --- narrow  **Selected**
                  rear provides        front preserves      
                  restoring moment     working zone         
  ------------------------------------------------------------------------------

**Footwork Clearance Analysis**

In boxing, the lead foot is placed **closest to the target**,
approximately one shoulder-width forward of the rear foot. During
training, the boxer continuously adjusts their stance through:

-   **Forward steps** (closing distance to deliver combinations)

-   **Lateral pivots** (re-angling to create new attack/defence lines)

-   **Backward retreats** (creating distance after exchanges)

The base must not interfere with any of these motions. The trapezoidal
geometry satisfies this by providing a **tapered clearance zone** at the
front and sides, while the wider rear section lies behind the robot\'s
torso and out of the boxer\'s immediate working zone. If the robot is
positioned so that the boxer faces the narrow end, the majority of the
base structure remains behind the robot, safely removed from the
boxer\'s footwork envelope.

![Figure: Pivot clearance analysis --- trapezoidal base preserves the
boxer\'s lead-foot working
zone.](media/image3.png){width="1.6188527996500437in"
height="0.8433245844269466in"}*~Figure:\ Pivot\ clearance\ analysis\ ---\ trapezoidal\ base\ preserves\ the\ boxer\'s\ lead-foot\ working\ zone.~*

**Ballast Provision**

If subsequent weight estimates reveal that the base\'s own mass is
insufficient to guarantee stability with an adequate safety factor (FoS
≥ 1.5), the rear region of the base can be configured to
accept **standard gym weights** as removable ballast. This approach
keeps the design modular and adaptable to different deployment
environments --- the ballast requirement may vary depending on the
specific floor surface (rubber mats vs concrete), the height setting of
the robot, and the expected user population.

\--

The ideation process for the base was not carried out as a single
one-time decision. Instead, it developed through a sequence of design
questions, where each stage of the base concept was compared against the
project's most important needs: stability under punching loads,
preservation of user footwork space, manufacturability at prototype
scale, subsystem integration, and eventual portability. To make these
choices systematic, selection matrices were used as a decision-support
tool.

The role of the selection matrix was used to structure the design
conversation and make trade-offs explicit. The base subsystem had to
satisfy several competing requirements at the same time. A concept that
scored well in stability might perform poorly in footwork clearance. A
concept that was easy to fabricate might be poor in long-term subsystem
integration. The matrices therefore helped to compare options against
the criteria that mattered most to BoxBunny, and to justify why certain
concepts were progressed while others were rejected.

The ideation journey can be divided into three linked selection stages.
The first addressed the **overall base-platform architecture**, the
second addressed the **material and structural concept**, and the third
addressed the **portability approach**. Each matrix narrowed the
solution space and informed the next level of design refinement.

**Concept Selection Matrix: Base-platform Architecture**

This first matrix was used to decide the overall shape and platform
strategy of the base. At this stage, the main design problem was not yet
detailed tube sizing or bracket design, but the more fundamental
question of what kind of base geometry best matched the way BoxBunny
would be used.

  --------------------------------------------------------------------------------------------------------------------
  **Concept**   **Stability**   **User        **Manufacturability**   **Integration   **Portability   **Final
                                footwork                              with            potential**     decision**
                                clearance**                           mechanisms**                    
  ------------- --------------- ------------- ----------------------- --------------- --------------- ----------------
  Flat wooden   Moderate        Poor to       Excellent               Poor            Moderate        Used only in
  board                         moderate                                                              early phase due
                                                                                                      to material
                                                                                                      availability in
                                                                                                      tight time
                                                                                                      constraint of
                                                                                                      the fair

  Large         High            Poor          Moderate                Moderate        Poor            Rejected due to
  rectangular                                                                                         footwork
  steel                                                                                               obstruction and
  platform                                                                                            excess footprint

  Circular /    Moderate to     Poor          Moderate                Moderate        Poor            Rejected; wastes
  uniform       high                                                                                  space near user
  footprint                                                                                           zone
  base                                                                                                

  Welded        High            High          High                    High            High            Selected
  trapezoidal                                                                                         
  steel frame                                                                                         
  --------------------------------------------------------------------------------------------------------------------

The flat wooden board scored well only in terms of immediate
manufacturability, which explains why it was suitable for the early
Robotics Fair implementation. However, it was not a good long-term
architecture because it did not provide a deliberate structural load
path, occupied too much uniform floor area, and integrated poorly with
the rest of the mechanism stack. A large rectangular steel base would
have improved structural confidence, but it would also have obstructed
the boxer's movement and introduced unnecessary footprint. A circular or
uniform footprint suffered from a similar problem: although it could
provide support area, it used space inefficiently in the user's working
zone.

The welded trapezoidal steel frame was selected because it was the only
concept that addressed all the major requirements together. Its narrower
front preserved user footwork space, while its wider rear improved
structural support, restoring leverage, and subsystem integration. This
made it the most balanced concept and the most appropriate direction for
further development.

**Concept Selection Matrix: Material / Structural**

Once the overall base architecture had been narrowed toward a
trapezoidal form, the next selection matrix was used to decide **how
that form should be physically realised**.

  --------------------------------------------------------------------------------------------------------------
  **Concept**   **Structural   **Repeatability   **Fabrication    **Weight       **Durability**   **Final
                stiffness**    of geometry**     practicality**   efficiency**                    decision**
  ------------- -------------- ----------------- ---------------- -------------- ---------------- --------------
  Wooden board  Low to         Moderate          Excellent        Moderate       Poor to moderate Used only as
                moderate                                                                          temporary
                                                                                                  prototype base

  Thick single  Moderate       High              Moderate         Poor           High             Not preferred;
  steel plate                                                                                     inefficient
                                                                                                  mass
                                                                                                  distribution

  Welded        High           High              High             High           High             Selected
  RHS/SHS steel                                                                                   
  frame with                                                                                      
  plate                                                                                           
  --------------------------------------------------------------------------------------------------------------

The wooden board again remained useful only as a temporary prototype
solution. It offered speed and availability, but it did not provide the
repeatable stiffness, durability, or geometric reliability expected from
a permanent structural subsystem. A thick single steel plate was
mechanically feasible, but it was not efficient. Much of its mass would
contribute only to bulk rather than to well-distributed structural
stiffness, and it would be less flexible for integrating welded brackets
and subsystem interfaces.

The welded RHS/SHS steel frame with plate was selected because it
offered the best overall structural behaviour for the intended
prototype. It provides higher stiffness for the amount of material used,
clearer load paths into the floor, better compatibility with welded
fabrication, and better integration with mounting features. It also
aligns with the design language of gym-equipment-style structures, which
was relevant to the project's intended function and portability logic.
This matrix therefore confirmed that the base should evolve from a
simple support platform into a proper framed steel structural subsystem.

**Concept Selection Matrix: Portability**

After the footprint and structural concept had been selected, the final
matrix was used to consider **how portability should be incorporated
into the base design**.

  ------------------------------------------------------------------------------------------------
  **Concept**      **Simplicity**   **Operational   **Ease of    **Integration   **Final
                                    stability**     movement**   with base**     decision**
  ---------------- ---------------- --------------- ------------ --------------- -----------------
  Manual lifting   High             High            Poor         High            Rejected as
  only                                                                           long-term
                                                                                 approach

  Separate         Moderate         High            High         Poor            Not preferred
  external trolley                                                               

  Integrated rear  High             High            High         High            Selected in
  wheels + handle                                                                concept, pending
  / tip-roll                                                                     physical test
  ------------------------------------------------------------------------------------------------

Manual lifting was rejected as a long-term solution because, although
simple, it becomes impractical and potentially unsafe as the robot grows
in mass and complexity. A separate external trolley would solve
movement, but it would do so outside the base subsystem, meaning
portability would remain disconnected from the main design and would
depend on extra equipment being available.

The integrated rear-wheel plus tip-and-roll concept was selected because
it allowed portability to become part of the base design itself. From a
mechanical perspective, this was the most elegant solution. The wider
rear portion of the trapezoidal base already provides the best location
for transport-related hardware, and the tip-and-roll handling method is
consistent with portable gym equipment and workshop machinery. This
concept was therefore selected in principle because it preserves
operational stability while improving deployment practicality.
