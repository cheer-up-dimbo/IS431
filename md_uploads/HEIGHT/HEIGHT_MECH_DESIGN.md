**5.2.X.4.2 Mechanical Design**

The mechanical design of the height-adjustment subsystem evolved through
several iterations, each addressing a different engineering problem. The
earliest concern was simply how to provide vertical adjustability. As
the design matured, however, it became clear that the real challenge was
how to do so **without compromising structural integrity under
punching**. This caused the subsystem to evolve from a simple adjustment
problem into a load-path-driven mechanical design problem.

**Phase 1: Basic adjustment concepts**

The earliest concept space included fixed-height and manually adjustable
configurations. These were useful in framing the problem but were not
serious long-term solutions. Fixed height could not satisfy the
user-adjustability requirement, and manual telescoping solutions were
too coarse and inconvenient for repeatable, user-friendly setup. This
phase was important mainly because it showed that vertical adjustment
had to be treated as a real subsystem, not as a one-off manual
convenience feature.

**Phase 2: Rear linear-guide plus central screw-jack concept**

The first serious structural concept used **two rear-mounted vertical
linear rails**, spaced as far apart as practical, with a lift carriage
plate supported on multiple linear blocks. The screw jack was positioned
near the centreline to minimise torsional effects, and a compliant jack
interface was proposed to absorb minor angular misalignment.

This phase was significant because it established the correct
**mechanical principle** of the subsystem: the guides should determine
motion accuracy and resist moments, while the jack should supply
vertical force only. In other words, this concept was the first explicit
recognition that the lifting mechanism and the lateral load path should
be separated.

However, although structurally sound, this arrangement required many
precision-mounted parts. It introduced alignment sensitivity, tolerance
stack-up, and additional potential failure points at rail blocks,
mounting plates, and bracket interfaces. This was the point at which the
design team began looking for a way to preserve the same structural
principle with fewer fitted components.

**Phase 3: Transition to a telescopic lift column**

The next major refinement was the move from exposed rear linear guides
to a **custom telescopic lift column**. This was not a change in
structural logic, but an improvement in how that logic was implemented.
The telescopic concept consolidated the guide function into one
structural column assembly.

The final layout uses:

-   an **8080 aluminium extrusion** as the moving inner member,

-   **Delrin wear pads** as the guide interface,

-   and a **welded steel outer tube with integrated plate** as the fixed
    outer sleeve.

Mechanically, this is a stronger subsystem because it:

-   reduces the number of precision-critical components,

-   simplifies the overall load path,

-   lowers the chance of misalignment-induced binding,

-   and makes the structure more robust for prototype conditions and
    repeated handling.

**Phase 4: Screw-jack integration**

Once the telescopic guide structure had been defined, the screw jack was
retained as the dedicated lifting mechanism. The selected actuator is
the **HK2T screw jack** with a **travelling nut**, connected to the 8080
inner column through a dedicated mount. In this arrangement, the screw
jack is no longer expected to guide the robot body or resist large
bending loads; it acts as a lifting device only. That makes the
subsystem mechanically safer and easier to reason about.

**Phase 5: Fabrication-driven refinement**

As the design matured, fabrication realism became more important. The
earlier notes show that the final structural solution was developed with
stiffness, weldability, and durability in mind. Large SHS members were
retained at **at least 6 mm wall thickness**, welded plates were kept
sufficiently rigid, and gusseted joints were preferred where aluminium
extrusion met steel platework. These details matter because the final
performance of the subsystem depends not only on the actuator and guide
concept, but also on whether the surrounding structure preserves
alignment under load.

**Final mechanical design state**

The final height-adjustment subsystem can therefore be summarised as
follows:

-   it moved from basic adjustability concepts toward a structurally
    guided lifting concept,

-   it initially clarified its load-path logic through a
    **rear-linear-guide plus screw-jack concept**,

-   it then consolidated that same logic into a **custom telescopic lift
    column**,

-   it retained the **HK2T screw jack** as the lifting device,

-   and it now separates axial lift from lateral load resistance in a
    much cleaner and more integrated way than the earlier concepts.
