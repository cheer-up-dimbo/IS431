**5.2.X Height Adjustment**

The height-adjustment subsystem allows BoxBunny to accommodate users of
different heights while preserving the robot's structural rigidity
during operation. From a user perspective, the intended workflow is
simple: the user selects a suitable training height, the robot adjusts
vertically, and the robot must then remain stable throughout the session
without visible wobble, jamming, or loss of alignment. Unlike a simple
positioning stand, however, the height-adjustment stage of BoxBunny lies
directly beneath the main striking body of the robot. This means it must
act not only as a lifting mechanism, but also as part of the structural
load path that carries punching-induced lateral forces and overturning
moments down into the rest of the robot.

The development of the height-adjustment subsystem progressed through
several stages. Early ideas included fixed-height configurations,
manually adjustable mast concepts, commercial telescopic columns, and a
rear-linear-guide plus screw-jack arrangement. These concept stages
gradually clarified the most important engineering principle of the
subsystem: **vertical lifting and lateral structural resistance should
be separated in function**, even if they are integrated into one
mechanical assembly. This insight ultimately led to the final concept of
a **custom telescopic lift column actuated by a motorised travelling-nut
screw jack**, where the screw jack provides axial lift and the
surrounding column structure resists side loading.

**5.2.X.1 Requirements & Considerations**

The first requirement was that the subsystem had to provide a **minimum
vertical stroke of 400 mm**. This came from the need to reposition the
robot's head and torso targets across a meaningful user height range, so
that the strike zone remains anatomically credible for users of
different stature. The 400 mm stroke therefore emerged as a direct
mechanical translation of the user requirement for adjustable target
alignment.

The second requirement was that the adjustment should be **practical for
setup use**. From a user-experience perspective, an ideal adjustment
time would be on the order of **10 seconds** from lowest to highest
position, similar to height-adjustable furniture. However, because of
the chosen screw-jack architecture and the available motor arrangement,
the implemented engineering target became approximately **32 seconds
over the full 400 mm stroke**, corresponding to a hoist speed of about
**0.75 m/min**. This became the realistic subsystem performance target
for the current prototype.

The third and most important requirement was that the subsystem must not
compromise the robot's ability to resist punching disturbances. Even
though the lifted mass is only about **10 kg**, the height-adjustment
stage sits directly beneath the upper robot body and therefore lies on a
major structural load path. This meant the design could not treat the
actuator as both the lifting device and the primary lateral support.
From an engineering standpoint, this became the central design principle
of the subsystem: **the screw jack should provide lift, while a separate
guide structure should carry lateral loads and moments**.

A further consideration was the operating environment. The robot may be
adjusted in public demonstrations or workshop conditions where minor
bumps, slight misalignments, and pushbutton start-stop transients are
realistic. This led to the adoption of a **light-shock service factor of
about 1.5** for sizing and concept evaluation. The subsystem therefore
had to balance stiffness, robustness, part count, fabrication
practicality, and motion performance within a prototype environment
rather than an ideal industrial setting.

The main subsystem requirements are summarised below.

  ---------------------------------------------------------------------------
  **ID**   **Requirement**              **Engineering rationale**
  -------- ---------------------------- -------------------------------------
  RM-3     Provide at least 400 mm      Accommodate user height range and
           vertical stroke              preserve anatomically meaningful
                                        target alignment

  RM-5     Maintain structural rigidity Height stage lies in a major load
           during and after height      path beneath the striking body
           adjustment                   

  RM-6     Separate vertical lifting    Avoid side-loading the screw jack and
           from lateral load-bearing    reduce risk of binding, wear, and
                                        misalignment

  RM-10    Provide practical setup-time Height adjustment should be usable in
           adjustment                   gym and demo settings

  RM-11    Remain manufacturable and    Avoid excessive part count, tolerance
           robust at prototype scale    stack-up, and overly delicate guide
                                        hardware
  ---------------------------------------------------------------------------

**5.2.X.2 Design**

The final height-adjustment system consists of two coupled subsystems:

1.  a **mechanical structure in the form of a telescopic lift column**,
    and

2.  a **motorised screw-jack mechanism** that drives the vertical
    motion.

The structural portion of the design comprises:

-   an **8080 aluminium extrusion** as the moving inner member,

-   **Delrin wear pads** acting as low-friction sacrificial guide
    interfaces,

-   and a **welded steel outer tube with integrated plate** forming the
    fixed sleeve of the telescopic column.

The actuation portion comprises:

-   the **travelling nut** of the screw jack,

-   the **HK2T screw jack** itself,

-   and a dedicated **screw jack--to--8080 mount** that transforms the
    jack's axial motion into the vertical movement of the inner column.

The most important design feature is the **separation of functions
between lift and structure**. In the final concept, the screw jack is
treated purely as an axial lifting device, operating mainly in
compression. Lateral loads and overturning moments caused by punching
are not intended to be carried by the screw. Instead, they are reacted
through the 8080 inner column, across the Delrin guides, into the welded
outer tube, and then into the lower support structure. This is what
makes the final design mechanically robust. The subsystem was not
selected simply because it could move the robot body up and down, but
because it could do so **without weakening the robot's resistance to
operational loads**.

The design also reflects practical fabrication choices. The outer
structural members were treated as substantial welded steel elements
rather than light brackets, and earlier design notes indicate a
preference for **large SHS members of at least 6 mm wall thickness** and
rigid welded plates to avoid distortion and preserve alignment. Gusseted
bracket logic was also favoured where aluminium extrusion meets steel
structure, in order to reduce joint flex and improve load transfer.
These decisions were not independent details; they were part of the same
load-path philosophy that shaped the rest of the subsystem.

In motion terms, the current concept achieves the required 400 mm
travel, but accepts that the present adjustment speed is slower than the
ideal user preference. This is a deliberate engineering compromise: the
design prioritises stiffness, reliable load separation, and robustness
over speed alone.

**5.2.X.3 Validation**

At the current stage, the height-adjustment subsystem has been validated
partly through **concept selection, packaging logic, and load-path
reasoning**, and partly through the coherence of the final mechanical
assembly. It has not yet been fully closed through every intended
physical validation test.

The most important subsystem-level success is that the final design
satisfies the core structural requirement: the lifting mechanism is
decoupled from the lateral load-bearing path. Compared with the earlier
rear-linear-guide concept, the telescopic lift column reduces part
count, simplifies alignment, and consolidates the load path into fewer,
better-integrated structural members. Compared with commercial lift
columns, it provides much higher confidence that side loads from punches
are being treated appropriately for a boxing robot application.

The architecture also meets the **400 mm stroke requirement**, and the
current movement target of approximately **32 seconds for full stroke**
is consistent with the inferred jack-speed requirement and the current
actuation logic. This means the subsystem is functionally adequate for
the current prototype, even if it does not yet achieve the more
desirable 10-second user-experience target.

The main gaps in validation are:

-   quantitative measurement of column deflection under lateral load,

-   long-term wear monitoring of the Delrin interfaces,

-   full repeated-cycle testing of the telescopic stage,

-   and confirmation of whether future motor revisions can move the
    stroke time closer to the ideal target.

A concise subsystem validation summary is given below.

  -------------------------------------------------------------------------
  **Aspect**                **Current      **Basis**
                            status**       
  ------------------------- -------------- --------------------------------
  400 mm stroke provision   Pass           Final concept sized around full
                                           required stroke

  Separation of lifting and Pass           Core design principle achieved
  structural functions                     

  Telescopic column as      Pass           Cleaner load path and lower part
  guide structure                          count than earlier rail-based
                                           design

  Current actuation speed   Pass           Meets present implementation
  (\~32 s full stroke)      (functional)   target

  Ideal user preference     Partial        Desired but not achieved with
  (\~10 s full stroke)                     current screw-jack arrangement

  Commercial off-the-shelf  Fail as final  Side-load confidence
  lift columns as final     solution       insufficient for boxing use
  solution                                 

  Long-term Delrin wear and Partial        Strong concept logic, but
  stiffness                                long-term physical validation
                                           still needed

  Full repeated-cycle and   Partial        Further testing required
  backlash testing                         
  -------------------------------------------------------------------------
