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
