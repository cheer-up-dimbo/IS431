**5.2.2.4.2 Mechanical Design**

The mechanical design of the rotation subsystem evolved through several
iterations, each addressing a different engineering problem. The
earliest concern was how to generate realistic yaw motion while keeping
the robot stable under punching. Once the need for a dedicated yaw stage
had been established, the design progressed through bearing selection,
drive packaging, timing-belt sizing, and support refinement.

**Phase 1: Initial integrated geared slewing-ring concept**

The earliest serious concept used a **large integrated geared slewing
ring**, specifically the **011.25.400** concept, with direct pinion
drive. This was attractive because one component would provide both the
rotary support and the drive interface. Structurally it was strong, but
it proved too heavy, too difficult to handle, too costly, and too
demanding in motor torque and power. It therefore became clear that the
yaw stage needed to be designed for **appropriate capability**, not
maximum theoretical performance.

**Phase 2: Transition to a smaller non-geared slewing ring**

After the oversized geared concept was rejected, the design moved to the
**010.10.120 non-geared slewing ring**. This separated the problem of
**load carrying** from the problem of **torque transmission**. The
bearing still provides the required combined-load support, but with far
lower mass and much better handling at prototype scale. This was a major
improvement because it turned the yaw stage into a more modular
subsystem.

**Phase 3: Fixed-base off-axis motor and external drive strategy**

Once the non-geared bearing was selected, the drive strategy moved
toward an **off-axis motor mounted on the fixed base**, driving the
rotating stage through an external transmission. This was mechanically
advantageous because it keeps motor mass off the rotating structure,
simplifies wiring, and makes the drive easier to service. It also fits
more naturally into the welded-base architecture than a direct coaxial
drive.

**Phase 4: Timing-belt and pulley design**

The timing-belt stage was then sized as a real engineered transmission.
The drive used the following motor basis:

-   Z55D Series parallel-shaft reducer, ZD motor

-   Model: 755BLD 400-24GU, 5GU, 25KB

-   Rated power: 400 W

-   Output shaft speed after gearbox: 120 rpm

-   Gear ratio: 1:25

The original yaw-speed target was about **25 rpm**, so the required
ratio was first estimated as:

$$i = \frac{120}{25} = 4.8
$$

The belt was then sized using design power:

$$P_{d} = P_{t} \times K_{s} = 400 \times 2.2 = 880\text{ W} = 0.88\text{ kW}
$$

The selected belt series was **S8M**. The final currently selected
pulley combination became:

-   **small pulley = 20 teeth**

-   **large pulley = 60 teeth**

giving:

$$i = \frac{60}{20} = 3
$$

This is important because it shows the final pulley stage is a
**packaging-driven compromise** relative to the ideal target of 4.8:1.
Using the pitch-diameter relation:

$$D_{p} = \frac{pZ}{\pi}
$$

the pulley diameters were:

$${D_{p}(60T) = \frac{8 \times 60}{\pi} = 152.78\text{ mm}
}{d_{p}(20T) = \frac{8 \times 20}{\pi} = 50.92\text{ mm}
}$$

The final standard belt length converged to about **944 mm**, with a
corrected centre distance of:

$$C = 352.6\text{ mm}
$$

and a final selected **belt width of 30 mm**.

This stage of the design is important because it shows that the
transmission was developed through an industrial-style selection
process, not by approximation alone. It also shows clearly where
geometry and packaging constrained the final mechanical solution.

**Phase 5: Outboard support and stability refinement**

As the rotating stage matured, the next challenge was to improve edge
stiffness under off-axis loading. This led to the addition of
**cam-follower rollers** around the outer edge of the rotating top.
These improve the effective support radius and reduce local rocking at
the plate edge under elevated strikes. They do not replace the central
bearing, but refine the way overturning effects are supported.

**Phase 6: Final base-level packaging**

The final rotation subsystem was then packaged into the welded base as a
**load-bearing, transport-aware module**. The bearing remains central,
the drive remains off-axis on the fixed frame, the cam followers
stabilise the rotating plate, and the rear transport integration is kept
away from the user's main footwork zone. This is what turns the yaw
stage from a simple rotary plate into a coherent structural layer of the
whole robot.

**5.2.2.4.3 Load Analysis**

The load analysis for the rotation subsystem was developed to answer a
more specific question than simply whether the robot could rotate. The
real engineering question was whether the yaw stage could rotate
responsively enough for realistic re-angling while remaining
structurally safe and stable under punching. This meant that the yaw
stage had to be analysed as both a **support structure** and a **drive
system**.

**Load philosophy and design basis**

The starting point is the BoxBunny punch-force hierarchy:

$${F_{char} = 1.8\text{ kN}
}{F_{design} = 1.5 \times F_{char} = 2.7\text{ kN}
}$$

The **characteristic training load** represents a strong but realistic
punch during normal use, while the **structural design load** represents
a conservative upper-bound event that the main structure must survive.
For the yaw stage, the bearing, rotating support structure, and
supporting frame are checked against $F_{design}$, while the motor and
transmission are selected primarily from $F_{char}$and motion demands.

**Structural loading of the yaw stage**

The yaw stage experiences three main structural loads.

First, the **axial load** from the mass above the bearing:

$$F_{a} \approx m_{upper}g
$$

Second, the **radial load** from the horizontal component of a strike:

$$F_{r} \approx F_{design}
$$

or its resolved in-plane component.

Third, the **overturning moment** generated because the punch acts above
the bearing plane:

$$M_{o} = F_{design}h
$$

where $h$is the vertical distance from the yaw-bearing plane to the
strike location. This overturning moment is especially important because
it drives both the bearing-capacity requirement and the need for
outboard edge support.

**Role of the outboard cam followers**

The load analysis made it clear that the central bearing should not be
expected to act alone as the sole source of rotational support
stiffness. Because the robot is tall and is struck at elevated points,
the rotating plate is prone to local rocking at the edge. The
**cam-follower supports** were therefore added so that the overturning
effect is shared between the slewing bearing and discrete perimeter
supports. This increases the effective support radius and improves the
planted feel of the stage.

**Drive-side load analysis**

The yaw stage also has to be analysed as a motion axis. The original
target yaw speed was around **150°/s**, equivalent to:

$$150^{\circ}/\text{s} = 2.618\text{ rad/s} \approx 25\text{ rpm}
$$

To achieve this motion, the motor and transmission must overcome:

-   inertial torque from the rotating mass,

-   friction and mechanical resistance,

-   disturbance torque caused by user strikes.

The timing-belt calculations then formalised the transmission sizing.
The drive used:

-   design power $P_{d} = 0.88\text{ kW}$,

-   an **S8M** belt,

-   **20T / 60T pulleys**,

-   a **3:1 ratio**,

-   **944 mm** belt length,

-   **352.6 mm** centre distance,

-   and **30 mm** belt width.

The load analysis shows that the current belt stage is mechanically
credible, but still represents a compromise between the ideal kinematic
reduction and real packaging constraints. This is why the final
integrated yaw speed still requires physical confirmation.

**Worst-case strike scenario**

The timing-belt notes explicitly identify a **worst-case straight strike
at a 45° angle strike point**. This is a realistic framing because
punches are rarely perfectly centred or perfectly radial. In practice,
the yaw stage must tolerate a combination of radial load, overturning
moment, and torsional disturbance. The motor is not expected to resist
every extreme strike by brute torque alone. Instead, the **bearing,
rotating plate, outer supports, and welded frame** carry the bulk of the
structural disturbance, while the motor and transmission are sized for
realistic operational control and recovery. This is fully consistent
with the wider BoxBunny philosophy of separating **structural survival**
from **actuator serviceability**.

**Remaining analytical gaps**

The current load analysis gives a strong design basis, but several
checks still remain:

-   physical measurement of yaw speed and acceleration,

-   validation of belt compliance, tooth-jump margin, and tension
    stability,

-   confirmation of cam-follower contact behaviour under real load,

-   and checking that the bearing--roller system is not overconstrained
    by fabrication tolerances.
