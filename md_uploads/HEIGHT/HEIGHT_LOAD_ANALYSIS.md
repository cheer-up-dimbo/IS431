**5.2.X.4.3 Load Analysis**

The load analysis for the height-adjustment subsystem was developed to
answer a more specific question than simply whether the robot body could
be lifted. The real engineering question was whether the robot could be
lifted through the required range **without forcing the actuator to
absorb punching-induced side loads and overturning effects**. This is
why the load analysis of this subsystem is fundamentally a **load-path
analysis** as much as it is a lifting-load calculation.

**Design basis and service assumptions**

The initial lifting load is based on an estimated **10 kg payload**,
corresponding to a gravitational load of about:

$$F = mg = 10 \times 9.81 \approx 98\text{ N}
$$

A light-shock service factor of about **1.5** was adopted because the
robot may be adjusted in demo or workshop environments where minor
bumps, start-stop transients, and slight misalignments are realistic.
This gives a design lifting basis of approximately:

$$F_{lift,design} \approx 1.5 \times 98 \approx 147\text{ N}
$$

This confirms that the pure axial lifting demand is modest relative to
the capacity of the selected screw jack. The more important design
challenge is therefore not axial strength, but ensuring that lateral
disturbances are diverted into the guide structure rather than the
screw.

**Separation of vertical and lateral load paths**

The load analysis of this subsystem is driven by the distinction
between:

-   the **vertical lifting load path**, and

-   the **lateral punch-disturbance load path**.

For vertical lifting, the preferred load path is:

$$\text{Upper robot body} \rightarrow \text{8080 inner tube} \rightarrow \text{screw jack mount} \rightarrow \text{travelling nut} \rightarrow \text{HK2T screw jack} \rightarrow \text{lower support structure}
$$

For lateral punching loads and overturning moments, the preferred
structural path is:

$$\text{Upper robot body} \rightarrow \text{8080 inner tube} \rightarrow \text{Delrin wear pads} \rightarrow \text{outer welded lift tube} \rightarrow \text{welded plate and lower structure} \rightarrow \text{robot base}
$$

This separation is the core reason the final design is mechanically
robust. It means the screw jack is not expected to carry the bending
effects associated with punching, while the telescopic column is
explicitly designed to behave as the lateral stabiliser and structural
guide.

**Effect of punching loads on the subsystem**

Although the height-adjustment system is not intended to be actively
driven during punching, it must still remain structurally sound when the
robot is struck. This is why the subsystem is tied to the wider BoxBunny
load philosophy, where:

-   **structural survival** is checked against the **2.7 kN structural
    design punch load**, and

-   **serviceability and moving-component behaviour** are generally
    sized closer to the **1.8 kN characteristic training load**.

For the height stage, the most important implication is not that the
screw jack must resist a full punch load axially, but that the **column,
outer tube, wear pads, and interfaces** must provide a sufficiently
stiff reaction path for punch-induced lateral disturbance. In earlier
concepts this role was assigned to the rear vertical rails; in the final
design it is assigned to the telescopic column itself.

**Speed and motor-sizing logic**

The motion side of the load analysis also addressed the practical speed
target of the subsystem. The current full-stroke target is **400 mm in
32 s**, corresponding to:

$$v = \frac{400}{32} = 12.5\text{ mm/s} = 0.75\text{ m/min}
$$

From observed or inferred screw-jack motion, the required jack input
speed was estimated to be approximately **800 rpm**. This showed that
the earlier motor arrangement was **significantly slower than desired**
for practical setup use. That result helped clarify the design strategy:
the height-adjustment subsystem should not be designed as an excessively
slow, torque-heavy actuator, because height change is an infrequent
setup action that benefits more from usable responsiveness than from
extreme torque margin.

At the same time, the load analysis also explains why the current
subsystem does not yet meet the more ambitious 10-second full-stroke
preference. The present screw-jack architecture is structurally
sensible, but its lead and motor constraints limit the achievable
adjustment speed unless the mechanism itself is changed more
fundamentally.

**Main implication of the load analysis**

Taken together, the load analysis shows that the height-adjustment
subsystem works not because the screw jack is exceptionally strong, but
because the subsystem was designed so that the screw jack does **not
need to carry the wrong kind of load**. The final design is successful
because:

-   the screw jack carries the axial lift demand,

-   the telescopic guide structure carries the lateral and overturning
    effects,

-   and the system therefore preserves stiffness and alignment under a
    boxing-relevant load case.

**Remaining analytical gaps**

The most important analytical and validation gaps that remain are:

-   quantitative measurement of deflection under lateral strike loading,

-   long-term wear testing of the Delrin interfaces,

-   confirmation of backlash or play growth over repeated cycles,

-   and evaluation of whether a future actuator revision can approach
    the ideal user-experience target without sacrificing load-path
    clarity.
