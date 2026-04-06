**5.2.2 Rotation**

The rotation subsystem forms the yaw-motion layer of BoxBunny's lower
mechanism and is responsible for reproducing one of the key movement
behaviours observed in real boxing drills: **re-angling**. In live
padwork, a coach does not only move forward and backward; they also
pivot and rotate to create new attack lines, defensive responses, and
counter opportunities. For BoxBunny, this meant the robot needed a
dedicated yaw stage capable of rotating the upper structure in a
controlled way while remaining stable under impact. The subsystem
therefore had to be treated as both a **motion mechanism** and a
**structural support interface**.

The development of the rotation subsystem progressed through several
major design stages. The earliest serious concept used a large geared
slewing ring that combined structural support and direct drive. This was
later refined into a smaller non-geared slewing ring with an external
transmission, and then further developed into the current low-profile
yaw module comprising a **010.10.120 slewing bearing**, an **off-axis
timing-belt drive**, **cam-follower edge supports**, and integrated rear
transport features. This final arrangement is more buildable, more
appropriate to the realistic load case, and better integrated with the
wider lower-mechanism architecture.

**5.2.2.1 Requirements & Considerations**

The rotation subsystem was governed by several linked requirements and
engineering considerations.

The first requirement was that the robot must provide **yaw
re-orientation** sufficient to simulate coach-like pivoting behaviour
during boxing drills. The motion had to feel deliberate and responsive
rather than slow or decorative. This led to the earlier adopted yaw
target of approximately **150°/s**, or about **25 rpm**, which is fast
enough to create meaningful angle changes while remaining controllable
at prototype scale.

The second requirement was that the yaw stage must **hold commanded
angle under impact**. Because the robot receives punches at an elevated
height, the yaw stage is not loaded like a light turntable. It must
withstand combined axial load from the upper structure, radial load from
the horizontal component of a punch, and overturning moment due to the
vertical distance between the yaw plane and the strike location. This
made rotational stiffness and disturbance resistance just as important
as nominal speed.

The third requirement was that the subsystem had to be **compact and
mechanically coherent** within the lower-mechanism stack. The yaw stage
needed to sit at the bottom of the lower mechanism so that the primary
rotary support remained closest to the ground, where overturning
resistance is most effective. This also meant the drive system had to be
packaged in a way that did not intrude excessively into the boxer's
footwork zone.

The fourth requirement was **manufacturability at prototype scale**. The
design had to be buildable using a welded base, accessible bearing
components, and practical transmission hardware, without depending on a
single oversized specialised part. This was one of the reasons the early
large geared slewing-ring concept was eventually rejected.

The fifth requirement was **portability and deployment practicality**.
Since the lower mechanism had to be transported and demonstrated, the
yaw-stage assembly also had to integrate sensibly with the rear wheel
and tip-and-roll logic of the base. Even though transport is not the
core function of the yaw stage, it influenced the final packaging and
support layout.

For clarity, the main subsystem requirements and their rationale are
summarised below.

  ----------------------------------------------------------------------------
  **ID**   **Requirement**               **Engineering rationale**
  -------- ----------------------------- -------------------------------------
  RM-4     Provide yaw re-angling with   Reproduce coach-like pivoting and
           target angular velocity ≈     angle changes during boxing drills
           150°/s                        

  RM-5     Hold angle and remain         Yaw stage sees combined axial,
           structurally stable under     radial, and overturning loading
           punching disturbance          

  RM-6     Provide smooth, predictable   Avoid slip, backlash, and poor
           torque transmission           controllability during positioning

  RM-7     Remain compact within the     Preserve footwork clearance and
           user working zone             integrate cleanly into
                                         lower-mechanism stack

  RM-8     Remain buildable and          Avoid over-engineered components that
           serviceable at prototype      impose excessive mass, cost, or
           scale                         fabrication difficulty

  RM-9     Integrate with wider base     Yaw module must coexist with
           transport and deployment      low-profile base and rear transport
           logic                         features
  ----------------------------------------------------------------------------

**5.2.2.2 Design**

The final rotation design is a **low-profile yaw module** built around a
**010.10.120 non-geared slewing ring bearing**, an **external
timing-belt drive**, **cam-follower roller supports** at the perimeter
of the rotating plate, and rear interfaces for transport integration.
The motor is mounted off-axis on the fixed base, drives a small pulley,
and transmits torque via an **S8M timing belt** to a larger pulley
concentric with the rotating stage. The rotating top is additionally
stabilised by discrete outboard cam followers, while the welded base
members provide the fixed reaction structure for the bearing, motor,
belt drive, and rear transport interfaces.

A central design decision was that the yaw stage should act as a
**dedicated rotary support layer**, rather than as part of a general
wheel-based mobile platform. This is why the final lower mechanism uses
**decoupled axes**, with yaw implemented by a slewing-based rotating
stage and translation handled separately. That decision improved
stiffness, repeatability, and resistance to floor-dependent slip.

Another major design decision was the move away from the earlier **large
integrated geared slewing ring (011.25.400)**. Although that concept was
structurally strong, it was too heavy, too expensive, too difficult to
handle, and too demanding in motor power relative to the actual needs of
the robot. The final selected **010.10.120 non-geared slewing ring**
still provides the required combined-load capacity, but with much better
design appropriateness. This change also forced the drive system to
become an explicitly designed subassembly rather than something
inherited from the bearing.

The timing-belt drive was selected because it gives **positive torque
transmission**, keeps the motor on the fixed structure, offers flexible
ratio selection through pulley sizing, and is easier to package into the
welded base than a bulky direct-drive or integrated gear solution. In
the current design, the timing-belt transmission converged to the
following selected parameters:

  -----------------------------------------------------------------------
  **Parameter**                                     **Value**
  ------------------------------------------------- ---------------------
  Belt series                                       S8M

  Pitch                                             8 mm

  Belt width                                        30 mm

  Small pulley teeth                                20

  Large pulley teeth                                60

  Speed ratio                                       1:3

  Approximate belt length                           944 mm

  Centre distance                                   352.6 mm

  Small pulley speed                                120 rpm
  -----------------------------------------------------------------------

These values came from the timing-belt selection process and represent a
practical balance between the ideal reduction target and the real
packaging constraints of the current rotating-base geometry.

The outer **cam-follower supports** were added because the yaw stage is
loaded not only by torque demand but also by plate-edge rocking under
elevated off-axis punches. These supports do not replace the central
slewing bearing; rather, they share the anti-tilt function by increasing
the effective support radius of the rotating plate. This makes the stage
feel more planted and reduces local rocking at the edge.

The final design also incorporates **rear transport interfaces** as part
of the wider lower-mechanism architecture. Within the full base
assembly, these are intended to accommodate the rear-wheel hardware and
provide the structural connection points needed for the robot to be
tipped and rolled during movement between locations. From a mechanical
perspective, locating these features at the rear is sensible because
that region already provides the larger footprint, greater structural
support, and more separation from the user's immediate footwork zone.
However, because this transport function has not yet been physically
tested, it should currently be treated as an **integrated design
provision** rather than a fully verified operational capability.

**5.2.2.3 Validation**

At the current stage, the rotation subsystem has been validated partly
through **concept selection, load-path reasoning, and transmission
calculations**, and partly through the coherence of the realised CAD
assembly. It has not yet been fully validated through all intended
physical tests.

The most important completed success is that the final concept retains
the correct **system-level architecture**: yaw and translation remain
decoupled, the yaw stage stays at the bottom of the lower mechanism, and
the main rotary support is based on a slewing-bearing approach capable
of carrying combined loads. This means the subsystem is mechanically
aligned with the realistic needs of a strike-receiving boxing robot
rather than with a generic mobile-robot platform.

The timing-belt transmission has also been validated to the extent that
it has been sized through a structured engineering process rather than
by approximation alone. The pulley ratio, belt series, belt width,
centre distance, and belt length were all developed through real
selection calculations. This gives confidence that the drive system is
mechanically credible and manufacturable. However, the final selected
**3:1 pulley ratio** is also known to be a packaging-driven compromise
relative to the earlier ideal reduction target of about **4.8:1**, so
the actual integrated yaw speed should still be measured physically to
confirm that the system still achieves the desired re-angling
performance.

The current design also succeeds in structural intent. The load path is
clearly divided between:

-   the **motor and belt**, which provide controlled rotation,

-   the **slewing bearing**, which carries the main rotary support load,

-   the **cam followers**, which improve anti-rocking behaviour,

-   and the **welded base**, which closes reaction loads back into the
    floor.

The main gaps in validation are:

-   physical confirmation of the actual yaw speed and acceleration,

-   physical assessment of belt compliance, tooth-jump margin, and
    tension stability,

-   contact-stress and stiffness validation of the cam-follower
    supports,

-   and physical confirmation that the rear transport arrangement does
    not interfere with planted operation.

A concise subsystem validation summary is given below.

  ------------------------------------------------------------------------
  **Aspect**          **Current    **Basis**
                      status**     
  ------------------- ------------ ---------------------------------------
  Decoupled yaw-stage Pass         Selected as the most appropriate motion
  architecture                     architecture for boxing use

  Slewing-bearing     Pass         Combined-load capacity and stiffness
  support concept                  logic are appropriate

  Geared large        Fail as      Structurally capable but
  bearing as final    final        over-engineered in mass, cost, and
  concept             solution     power demand

  Non-geared slewing  Pass         Better fit-for-purpose engineering
  ring concept                     choice

  Timing-belt         Pass         Belt, pulley, ratio, width, and centre
  transmission sizing (analysis)   distance selected through structured
                                   calculations

  Final 3:1 ratio vs  Partial      Mechanically valid, but final yaw speed
  ideal target                     still requires integrated physical
                                   confirmation

  Cam-follower        Partial      Strong design logic, but physical
  anti-tilt support                stiffness/contact validation still
                                   needed

  Rear transport      Partial      Good packaging logic, but tip-and-roll
  integration                      use not yet physically tested
  ------------------------------------------------------------------------
