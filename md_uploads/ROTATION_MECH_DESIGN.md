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

**Phase 2: Fixed-base off-axis drive with inner-ring rotation integration**

Once the non-geared bearing was selected, the drive strategy moved toward an off-axis motor mounted on the fixed base, driving the rotating stage through an external transmission. This was mechanically advantageous because it keeps motor mass off the rotating structure, simplifies wiring, and makes the drive easier to service. It also fits more naturally into the welded-base architecture than a direct coaxial drive.

At this stage the key choice was between a direct coaxial drive and an external timing-belt transmission. A direct coaxial solution would have required a significantly larger central shaft or a custom hollow shaft arrangement, adding complexity, mass, and a difficult routing challenge for cables and seals. In contrast, the external belt drive could be packaged around the periphery of the base, leaving the central bearing and rotating structure cleaner and easier to assemble.

A direct coaxial drive also could have affected the height profile of the base feet, because the base would need to accommodate the motor height and ensure clearance around the central drive. This conflicted with the requirement for a low-profile base to avoid obstructing footwork, making the off-axis solution better aligned with the ergonomic and packaging goals.

After the non-geared slewing ring had been selected, a further integration question arose: whether the inner ring or the outer ring should serve as the driven rotating member. Rotating the outer ring would push more of the rotating interface toward the perimeter of the base, increasing packaging difficulty for the external drive and potentially complicating the relationship between the rotating structure and the fixed support frame. In contrast, driving the inner ring allowed the upper robot structure to be treated more naturally as a single controlled rotating body, with the outer ring remaining fixed to the welded base.

The inner-ring-driven, external timing-belt approach was therefore preferred because it provided a cleaner integration path, reduced unnecessary outward bulk at the base perimeter, and simplified the structural relationship between the rotating top assembly and the fixed lower frame. Compared with a gear drive, the timing-belt transmission also offered lower noise, reduced backlash, simpler alignment requirements, and easier sourcing and maintenance. This decision was not only about convenience; it helped make the final yaw stage more compact, more modular, and easier to integrate with the rest of the lower mechanism.

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