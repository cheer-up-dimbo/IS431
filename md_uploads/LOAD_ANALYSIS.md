# Load Analysis

## Punch Force Modelling

A boxing punch does not apply a constant force over time. Instead, the
force-time profile is highly transient, with a short, sharp peak that
lasts only a few milliseconds. Designing the robot directly from this
instantaneous peak value would be overly conservative, because most
structural and actuation components (such as bearings, linear rails and
screw jacks) are specified in terms of equivalent or average working
loads rather than isolated spikes.

In addition, measured punch forces depend strongly on context. During
real matches, boxers throw a mix of jabs, set-up punches and full-power
shots; in contrast, laboratory studies often record deliberate maximal
punches delivered under controlled conditions. The resulting values
represent different parts of the same distribution and must be
interpreted carefully when used for design.

For BoxBunny, we therefore distinguish between:

-   a **characteristic training load**, representing a strong but
    realistic punch from our target users during regular use; and

-   a **structural design load**, representing a conservative upper
    bound that the main structure must withstand without failure.

This hierarchy allows the robot to remain realistic and appropriately
sized, while still maintaining a clear safety margin against rare,
harder-than-average impacts.

### Reference Punch Forces from Literature

Published measurements of boxing punches report a wide range of forces,
depending on athlete level, measurement method and whether average or
maximal punches are considered. Pierce et al. directly instrumented
gloves during six professional boxing matches and reported mean punch
forces of approximately **0.9 -- 1.2 kN** per boxer, with only 5.3% of
punches exceeding 2.0 kN, 1.1% exceeding 3.0 kN, and a very small number
of outliers above 4.0 kN (maximum ≈ 5.3 kN) (Pierce, Reinbold, Lyngard,
& Goldman, 2007). These values represent the average of all punches
thrown in a bout (jabs, set-ups, partial-power shots), not deliberate
maximum efforts.

In contrast, laboratory studies in which trained boxers deliver
intentional maximal straight punches report substantially higher peak
forces. Boxing Science summarises such work by noting that punching
forces in amateur boxing are around **2.5 kN**, corresponding to roughly
3.5 times body weight for a 70 kg athlete (Boxing Science, 2021). This
is consistent with a recent experimental study by Xu et al., where
university-level boxing athletes produced backward straight punches with
mean impact forces of 3.96 ± 0.45 times body weight; for the reported
body masses (\~64 kg), this corresponds to peak forces on the order of
**2.5 kN** (Xu, Sun, & Zhu, 2025). Elite Olympic boxers can generate
even higher values: one study reported average peak straight-punch
forces of approximately **3.4 kN**, with some punches exceeding 4 kN
when striking a headshot (Walilko, Viano, & Bir, 2005).

In summary:

-   **\~1.0 kN** -- typical *average* in-fight punch force across all
    punches (professional bouts).

-   **\~2.5 kN** -- typical *peak* force of a deliberate maximal
    straight punch from trained amateurs / high-level athletes.

-   **\~3.4 kN and above** -- maximal straight punches from elite
    Olympic-level boxers.

### Selected Characteristic and Design Punch Loads

BoxBunny is intended for recreational and amateur users in commercial
gyms, rather than heavyweight professionals or Olympic-level athletes
repeatedly delivering KO-class punches to a static head target. The
design assumptions are therefore anchored around the amateur /
high-level athlete range, while remaining above the average in-fight
forces reported for professionals.

We first define a **characteristic amateur punch force**:

F~char~ = 1.8 kN

This value is taken as a strong but realistic training punch for our
target user group as it lies well:

-   above the ≈ 1.0 kN average in-fight force reported in professional
    matches, and

-   below the ≈ 2.5 kN maximal peaks measured for trained amateur /
    university-level boxers,

To obtain a conservative **structural design load**, we apply a combined
design factor of [1.5]{.mark} to account for the impulsive nature of
punching and possible short-duration amplification relative to the
nominal average, and user-to-user variability, modelling simplifications
and manufacturing tolerances.

**[General
Recommendations](https://safetyculture.com/topics/factor-of-safety)**

  -----------------------------------------------------------------------
  **Applications**                          **Factor of Safety -- FOS
                                            --**
  ----------------------------------------- -----------------------------
  For use with highly reliable materials    1.3 -- 1.5
  where loading and environmental           
  conditions are not severe and where       
  weight is an important consideration      

  [For use with reliable materials where    [1.5 -- 2]{.mark}
  loading and environmental conditions are  
  not severe]{.mark}                        

  For use with ordinary materials where     2 -- 2.5
  loading and environmental conditions are  
  not severe                                

  For use with less tried and for brittle   2.5 -- 3
  materials where loading and environmental 
  conditions are not severe                 

  For use with materials where properties   3 -- 4
  are not reliable and where loading and    
  environmental conditions are not severe,  
  or where reliable materials are used      
  under difficult and environmental         
  conditions                                
  -----------------------------------------------------------------------

  : Table 1: Design Load Summary of Punch Forces set for BoxBunny.

This gives:

F~design~ = F~char~ × 1.5 = 1.8 kN × 1.5 = 2.7 kN.

The design load of 2.7 kN sits slightly above the ≈ 2.5 kN peak forces
reported for trained amateurs and high-level boxing athletes yet remains
below the more extreme values observed in Olympic-level or knockout
punches. It therefore represents a conservative upper bound appropriate
for BoxBunny's intended use. Table 1 summarises the adopted punch force
levels and their roles in the design.

+---------------+-----+-------+--------------------+-----------------+
| **            | *   | **Va  | **Basi             | **Primary Use   |
| Description** | *Sy | lue** | s/Interpretation** | in Design**     |
|               | mbo |       |                    |                 |
|               | l** |       |                    |                 |
+===============+=====+=======+====================+=================+
| **Average     | --  | ≈ 1.0 | Mean force across  | Context only    |
| in-fight      |     | kN    | all punches (jabs, | (benchmark for  |
| punch         |     |       | set-ups, power     | typical         |
| (professional |     |       | shots); not        | match-level     |
| bouts)**      |     |       | necessarily        | loading)        |
|               |     |       | maximal            |                 |
+---------------+-----+-------+--------------------+-----------------+
| **Peak        | --  | ≈ 2.5 | Maximal straight   | Target range    |
| straight      |     | kN    | punch under lab    | for "strong"    |
| punch         |     |       | conditions from    | gym-level       |
| (trained      |     |       | trained amateurs / | punches         |
| amateur /     |     |       | university-level   |                 |
| high-level    |     |       | boxers             |                 |
| athlete)**    |     |       |                    |                 |
+---------------+-----+-------+--------------------+-----------------+
| **C           | $   | **1.8 | Strong but         | Repeated-load   |
| haracteristic | $F_ | kN**  | realistic punch    | estimates,      |
| amateur       | {\t |       | for BoxBunny       | serviceability  |
| training      | ext |       | target users;      | checks          |
| punch**       | {ch |       | between 1.0 kN     |                 |
|               | ar} |       | match average &    |                 |
|               | }$$ |       | 2.5 kN maxima      |                 |
+---------------+-----+-------+--------------------+-----------------+
| **Structural  | $$F | *     | F~char~ × 1.5      | Sizing of all   |
| design punch  | _{\ | *[2.7 |                    | structural load |
| load**        | tex | kN    | -   combined       | paths and       |
|               | t{d | ]{.ma |     factor for     | global          |
|               | esi | rk}** |     impact effects | stability       |
|               | gn} |       |     & user /       |                 |
|               | }$$ |       |     modelling      |                 |
|               |     |       |     uncertainty    |                 |
+---------------+-----+-------+--------------------+-----------------+

# References

Boxing Science. (18 November, 2021). *The Science Behind The Punch*.
Retrieved from Boxing Science Website:
https://boxingscience.co.uk/science-behind-punch/

Pierce, J., Reinbold, K. A., Lyngard, B. C., & Goldman, R. J. (February,
2007). Direct Measurement of Punch Force During Six Professional Boxing
Matches. *Journal of Quantitative Analysis in Sports, 2(2)*(3-3).
doi:10.2202/1559-0410.1004

Walilko, T., Viano, D., & Bir, C. (2005). Biomechanics of the head for
Olympic boxer punches to the face. *Br J Sports Med, 39*(10), 710--719.
doi:10.1136/bjsm.2004.014126

Xu, X., Sun, Y., & Zhu, D. (31 March, 2025). Analysis of the impact
force and key technique of backward straight punch in different combat
sports. *Scientific Reports, 15*(10958).
doi:https://doi.org/10.1038/s41598-025-96264-4

## Structural vs Actuator Design Philosophy (ULS vs SLS)

The load levels in Table 1 are applied differently depending on the
design objective. When designing a system that is repeatedly struck, two
complementary design problems arise :

**Ultimate Limit State (ULS) -- structural safety & integrity**

*Purpose:* For cases when rare and very hard punch lands, BoxBunny is
prevented from cracking, bending permanently, or tip over.

This analysis uses the **worst-case load** F~design~ = 2.7 kN to check
that all primary load paths (arms, frame, rails, rotating base, height
adjustment system and base) remain structurally sound and stable under
extreme but credible events.

**Serviceability Limit State (SLS) -- actuator & fatigue behaviour**

*Purpose:* For the motors and moving components to handle the frequent
load level during normal training both thermally and mechanically.

This analysis is governed by the **characteristic training load**
F~char~ = 1.8 kN and the dynamic demands of repositioning the arms,
since these conditions dominate actuator heating, wear and long-term
performance.

Actuators occupy both worlds: their **internal mechanics and mountings**
must not fracture under ULS loads, but their **torque and power
ratings** are chosen primarily based on service loads. An example of
this is shown In BoxBunny's 2DOF foam-arm design, this is addressed as
follows:

-   The **mechanical arm structure** is checked against F~design~ = 2.7
    kN so that it does not fail under rare hard punches.

-   The **motors** for the yaw and pitch axes are sized based on F~char~
    = 1.8 kN and the arm inertia, with additional safeguarding provided
    by the compliance of the polyethylene foam and the ability of the
    joints to back-drive under extreme impacts. Where necessary,
    mechanical fuses or slipping interfaces can be introduced to protect
    the motor gears from loads approaching the structural design level.

With this philosophy established, the following subsections summarise
the load analysis for each major subsystem.

## Subsystem Load Analyses

### Rotating Base: Slewing Bearing and Gear Drive

The rotating base consists of a four-point contact ball slewing ring
with external gear, driven by a pinion attached to a motor. It must
support the weight of the upper robot, transmit punching loads into the
lower mechanism, and rotate smoothly for user tracking.

**Load components considered:**

-   **Axial load** F~a~ **:**

> F~a~ ≈ m~upper~ g, where m~upper~ is the mass of the entire structure
> above the bearing (torso, arms, frame, height stage, etc.). This is
> used to check the bearing's axial capacity.

-   **Radial load** F~r~ **:**\
    The horizontal component of F~design~ is transmitted through the
    frame into the bearing as a radial load. This is used against the
    bearing's radial load rating.

-   **Overturning moment** $M_{o}$**:**

> M~o~ = F~design~ × h,
>
> where h is the vertical distance between the bearing centre plane and
> the punch impact point (head or torso). This moment is critical for
> checking the bearing's moment capacity and the stiffness of the
> connection between bearing and base frame.

-   **Gear mesh forces and motor torque:**\
    To resist $M_{o}$, the external gear is driven by a pinion that
    develops a tangential force

> $$F_{t} = \frac{T_{\text{pinion}}}{r_{\text{pitch}}},$$
>
> where T~pinion~ is the torque at the pinion and r~pitch~ its pitch
> radius. F~t~ contributes to additional radial loading on the bearing
> and defines the tooth loading in the gear mesh. The motor torque
> T~motor~ (after gearbox) is selected so that it can overcome bearing
> friction and accelerate the rotating mass and also provide sufficient
> margin to resist reaction torques associated with M~o~, with
> appropriate factor of safety.

In summary, the slewing bearing and its drive are designed against
F~design~ = 2.7 kN for radial, axial and moment capacity, while the
motor is sized based on rotational inertia and expected operational
torques, with checks that its mounts and shaft remain safe under ULS
loading.

### Lower Mechanism: Design and Load Analysis

The key selection criteria for both the translational and rotational
axes are:

(i) the ability to **hold position under impact** (angle and position
    rigidity),

(ii) the ability to **carry combined static and dynamic loads** from the
     full robot mass and user strikes, and

(iii) the provision of **moderate speed with high torque**, enabling
      confident starts, stops and direction changes without excessive
      overshoot or vibration.

These criteria are evaluated using the characteristic and design punch
loads defined:

-   **Characteristic training punch:** F~char~ = 1.8 kN

-   **Structural design punch load:** F~design~ = 2.7 kN

The structural elements of the lower mechanism (rails, sliding table,
slewing ring, base frame) are checked primarily against F~design~
(ultimate limit state), while the motors and ball screw are sized for
F~char~ and motion demands (serviceability), with additional checks to
ensure their mountings and shafts remain safe under ULS loading.

#### 5.3.1.4 Linear Motion (Translational Axis)

For the translational axis, the final concept is a **motorised
sliding-table linear rail driven by a ball screw** (Figure 13). This
decision followed the evaluation of three power transmission options
(lead screw, ball screw, and belt drive), summarised in Appendix A
(Power Transmission Drive Selection, Table A11).

The selected mechanism comprises:

-   A **sliding table**, which serves as the platform for the entire
    upper portion of the robot (torso, arms, height adjustment and
    frame).

-   **Two linear rails with preloaded blocks**, which guide the table
    and carry longitudinal forces and overturning moments arising from
    both motion and punching.

-   A **ball screw drive**, which converts motor rotation into linear
    motion of the sliding table.

The decision matrix in Appendix A (Table A11) shows that the ball
screw--driven linear rail scores highest on the high-priority criteria
of **load and thrust capacity**, **positional stiffness**, and
**accuracy/repeatability**, while remaining acceptable in cost and
maintenance. Therefore, a ball screw-driven sliding table on linear
rails is adopted as the **linear footwork mechanism**.

##### Load Analysis of Translational Stage

###### Static support and vertical loads

Let $m_{\text{robot}}$ be the total mass supported by the sliding table
(upper structure plus any additional fixtures). The vertical reaction
carried by the four rail blocks is approximately

$$F_{v} \approx \frac{m_{\text{robot}}g}{4}$$

per block in the ideal case. A load-sharing factor (e.g. 1.2--1.3) is
applied to account for misalignment, and the resulting loads are
compared to the catalogue static and dynamic load ratings
$\left( C_{0},C \right)$ for each block. This ensures that the rails can
support the robot's self-weight plus dynamic motion forces with an
adequate factor of safety.

###### Punch-induced Horizontal Loads & Moments

When the robot is struck, the punch force is transmitted down to the
sliding table and rails. For ultimate checks, the **design punch load**
F~design~ = 2.7 kN is resolved into components:

-   $F_{h,x}$: component along the rail axis (forward--backward)

-   $F_{h,y}$: component transverse to the rail axis (side--side)

These components generate:

-   **Shear forces** in the rail blocks and fasteners, and

-   **Overturning moments** about the rail plane due to the height of
    the impact point and any lateral offset of the torso relative to the
    rail centreline.

The resulting moments (pitch, roll and yaw) are calculated as

$$M = F_{\text{design}} \times \text{lever arm},$$

where the lever arm is the vertical distance from the rail plane to the
impact point (for pitch/roll) or the horizontal eccentricity in plan
(for yaw). Using the manufacturer's moment-to-equivalent-load
relationships, these moments are converted into equivalent loads per
block and checked against the allowable moment ratings (e.g. M~A~, M~B~,
M~C~). This confirms that the rails provide sufficient angular rigidity
to satisfy criterion (i): **holding position under impact**.

###### Ball Screw Thrust and Motor Torque

The ball screw and its motor are sized primarily from **service loads**:

-   Required thrust to accelerate the sliding table plus upper structure
    to the desired translational speed and to overcome friction, and

-   Required motor torque, given by

> $$T_{\text{screw}} = \frac{F_{\text{thrust}} \times p}{2\pi\eta},$$
>
> where p is the screw lead and η is its efficiency.

Because the robot is stationary during punching, the ball screw is not
normally subjected to the full dynamic punch load. However, a check is
carried out to ensure that:

-   The screw's **critical buckling load** and **static capacity**
    exceed any additional axial loads that may be induced by impact
    reactions, and

-   The screw nuts, bearings and motor coupling are not overstressed if
    a punch occurs while the stage is in motion.

In line with the design philosophy, the **ball screw and motor** are
sized for repeated operation around F~char~ and motion demands
(serviceability), while their structural attachments and bearings are
checked against F~design~ so that no mechanical failure occurs under
extreme punches.

#### 5.3.1.5 Rotational Motion (Yaw Axis)

For yaw rotation, the selected concept is a **slewing ring bearing with
external gear teeth**, driven by a **pinion gear and BLDC servo motor**
(Figure 14). This solution emerged from the bearing and motor selection
processes described in Appendix B (Bearing Selection, Table B13; Motor
Selection, Table B14).

A **four-point contact ball slewing ring with external gear** was
selected as the yaw bearing because it can handle combined **axial,
radial and overturning loads** with good stiffness, while being cheaper
and more widely available than cross-roller types. A **BLDC servo motor
with encoder** was chosen to drive this stage, as it offers low
backlash, smooth torque, precise position control and strong disturbance
rejection under punching, satisfying the lower-mechanism selection
criteria.

##### Load analysis of Yaw Stage

###### Bearing axial, radial and moment loads

The slewing ring bearing supports:

-   The **axial load** from the upper structure:

> $$F_{a} \approx m_{\text{upper}}g,$$
>
> where m~upper~ is the mass supported by the bearing.

-   The **radial load** from the horizontal component of a punch:

> $$F_{r} \approx \text{horizontal component of }F_{\text{design}},$$
>
> transmitted through the upper frame into the bearing raceways.

-   The **overturning moment**:

> $$M_{o} = F_{\text{design}} \times h,$$
>
> where $h$is the vertical distance between the bearing's rotational
> plane and the punch impact point (head or torso).

The manufacturer's combined-load diagrams for four-point contact ball
slewing rings are then used to verify that
$\left( F_{a},F_{r},M_{o} \right)$fall within the allowable region for
both **static** and **dynamic** loading, with a suitable safety margin.
This addresses criteria (i) and (ii) by ensuring that the yaw bearing
can hold angle under impact and safely carry the combined loads from
robot weight and user strikes.

###### Gear mesh forces and yaw motor torque

The external gear is driven by a pinion attached to the BLDC servo
motor. To resist the overturning moment while providing controlled
motion, the pinion must develop a tangential tooth force

$$F_{t} = \frac{T_{\text{pinion}}}{r_{\text{pitch}}},$$

where $T_{\text{pinion}}$ is the torque at the pinion and
$r_{\text{pitch}}$ is the pitch radius of the external gear. This
tangential force produces the yaw driving torque, and adds a
**circumferential component** to the bearing loading.

The BLDC servo motor is sized based on:

-   The **reflected inertia** of the rotating masses (torso, arms, upper
    frame),

-   The desired **angular acceleration and deceleration** for user
    tracking, and

-   The need to resist disturbances corresponding approximately to
    F~char~ during normal training.

Using the gearbox ratio and manufacturer torque--speed curves, the motor
must:

-   Provide sufficient **continuous torque** to execute nominal yaw
    motions and reject typical disturbances, and

-   Provide sufficient **peak torque** to momentarily resist impacts
    without losing position control under normal punches.

###### Actuator integrity under worst-case punches

Although the BLDC servo is sized from service conditions (around
F~char~), its **mechanical mounting**, **shaft** and **pinion hub** are
checked against loads induced by F~design~:

-   The worst-case pinion torque associated with M~o~ is used to verify
    that the motor shaft, keyway (if present) and pinion hub do not
    exceed allowable shear and bending stresses.

-   The motor mounting bolts and base plate are checked to ensure that
    the reaction forces from the gear mesh under F~design~ do not cause
    slippage or permanent deformation.

In practice, the slewing ring and frame carry the majority of the
extreme load, while the BLDC servo, with its encoder feedback and
control, maintains accurate yaw positioning under typical training
punches and recovers quickly after disturbances. This satisfies
criterion (iii): **moderate speed with high torque and good disturbance
rejection**, without requiring the motor to be unrealistically oversized
for the absolute worst-case impulse.

### Height Adjustability: Design and Load Analysis

#### 5.3.3.2 Height Adjustment Mechanism Selection

Several concepts were generated to achieve the required stroke and load
capacity and were evaluated against the criteria above (Appendix B,
Height Adjustment section).

-   An **office-chair gas cylinder with guides** was rejected because
    the gas lift behaves like a spring--damper, causing vertical
    "bounce" and insufficient stiffness under punches. It also offers
    limited control over position under sustained load.

-   An **electric gas strut plus motorised guides** allows push-button
    adjustment but introduces a complex, shared load path between the
    strut and guides. This increases cost and control complexity and is
    unjustified for an adjustment that occurs only occasionally.

The next concept consists of a **manual screw jack with rear vertical
linear guides**:

-   The **screw jack** carries the **axial load** and is inherently
    **self-locking / non-backdrivable**, satisfying the fail-safe
    requirement.

-   The **vertical linear guides** carry **lateral forces and
    overturning moments** from punching, providing the necessary
    vertical stiffness and impact resistance.

This concept offers high stiffness, clear load paths, fail-safe
behaviour and acceptable manual effort, making it the most suitable for
BoxBunny. The main trade-off is that height adjustment is not as
convenient or fast as a powered system. However, this is acceptable
given the low frequency of adjustment and the strong benefits in
stiffness, reliability and simplicity.

Consequently, the **Manual Screw Jack with Rear Vertical Linear Guides**
concept is selected as the height-adjustment mechanism.

#### 5.3.3.3. Height Adjustment Load Analysis

The height-adjustment system is analysed using:

-   **Static / gravity loads** from the upper structure; and

-   **Impact-induced lateral loads and overturning moments** derived
    from the structural design punch load: F~design~ = 2.7 kN.

##### 5.3.3.3.1. Axial load in the screw jack (ULS + SLS)

Let m~upper~ be the mass of all components supported by the
height-adjustment stage (torso, arms, upper frame, etc.). Using a
**single** manual screw jack, the total lifted load is:

$$W = m_{\text{upper}}g.$$

Because there is only one jack, it must carry **the full axial load**
$W$, rather than a fraction of it. The jack's **static and operating
load capacities** are therefore checked directly against $W$with an
appropriate safety factor to ensure that:

-   The screw threads, nut, housing and mounting brackets do not yield
    or strip under the supported weight; and

-   The jack can withstand any additional minor axial load fluctuations
    due to user movement and dynamic repositioning.

The **slenderness and stroke length** of the screw (≈ 400 mm) are used
to verify that the screw remains below its **Euler buckling load** at
maximum extension. The check includes any small eccentricity of the
upper structure relative to the jack axis (e.g. a slight offset between
the jack line and the upper-stage centre of gravity), which introduces a
secondary bending component in the screw. The effective critical load
P~cr~ is compared with the factored axial load $W$to confirm that
buckling is not governing.

Because height adjustment happens infrequently and at low speed, the
jack is not significantly affected by dynamic effects during motion.
Under normal operation, jack loads are dominated by gravity; impact
forces from punching are **not** intended to be carried by the screw but
by the vertical guides and frame.

##### 5.3.3.3.2. Manual Screw Jack Selection Calculation

The manual screw jack is required to support the full weight of the
upper structure (torso, arms, upper frame and attached components) and
provide a 400 mm stroke. As established in Section 5.3.3.3.1, lateral
and impact loads from punching are carried primarily by the rear
vertical guides and frame, while the jack is responsible for **axial
support and vertical positioning**.

The supported mass of the upper structure is estimated as:

$$m_{\text{upper}} = 15\text{ kg}.$$

The corresponding gravitational load is:

$$W = m_{\text{upper}}g = 15 \times 9.81 \approx 147.15\text{ N}.$$

To account for modelling uncertainty, possible future attachments and
minor dynamic effects during height adjustment, a **factor of safety of
1.5** is applied to this axial load:

$$F_{\text{jack,design}} = W \times \text{FoS} = 147.15 \times 1.5 \approx 220.7\text{ N}.$$

In "kg-equivalent" terms, this is:

$$m_{\text{equiv}} = \frac{F_{\text{jack,design}}}{g} \approx \frac{220.7}{9.81} \approx 22.5\text{ kg}.$$

Thus, the screw jack must safely support at least **220 N (≈ 0.22 kN, or
≈ 22.5 kg)** under static loading, with a self-locking thread so that
the stage does not back-drive under this weight.

In practice, commercially available manual screw jacks are typically
rated in the **kilonewton** range (e.g. 1 kN, 2 kN, 5 kN). A jack with a
**rated axial capacity ≥ 1 kN** therefore exceeds the required design
load $F_{\text{jack,design}} \approx 0.22\text{ kN}$ by a large margin.
This provides additional implicit safety against:

-   modest underestimation of $m_{\text{upper}}$,

-   small eccentricities between the jack axis and the upper-stage
    centre of gravity, and

-   long-term effects such as wear or minor overloads.

Finally, the selected jack's **stroke** (≥ 400 mm) and **thread
form/lead** are checked to ensure:

-   adequate **buckling resistance** of the screw at full extension for
    the design axial load; and

-   **self-locking behaviour** (non-backdrivable under 15 kg),
    satisfying the fail-safe requirement in Table 17.

This confirms that the chosen manual screw jack is more than sufficient
from a load-bearing standpoint for the BoxBunny height-adjustment
application.

##### 5.3.3.3.1. Lateral loads and moments in guides (ULS)

Punches applied to the head or torso generate lateral forces and
overturning moments that act on the **upper carriage** of the
height-adjustment stage. These are resisted primarily by the **rear
vertical linear guides** and their fixings, while the jack provides
axial support and vertical positioning.

For ultimate checks, the **design punch load** F~design~ = 2.7 kN is
applied at the head/torso height. In the worst-case direction:

-   The **lateral reaction** carried by the guide pair is taken
    approximately as:

$$F_{\text{lat}} \approx F_{\text{design}}.$$

-   The resulting **overturning moment** about the guide rail supports
    is:

> $$M_{\text{guide}} = F_{\text{design}} \times e,$$
>
> where $e$ is the horizontal offset between the line of action of the
> punch and the guide rail plane (or mid-plane between the two guides).

These values are used to:

-   Size the **guide rail cross-section** and their carriages to resist
    lateral shear and bending;

-   Check **bearing stresses and bolt shear** at the guide-to-frame
    interfaces; and

-   Verify that vertical deflection and racking of the upper carriage
    under impact remain small, so the head and torso targets do not feel
    loose or "bouncy" during strikes.

The screw jack base and top mounting plates are also checked to ensure
that any secondary lateral loads transferred through the jack housing
(e.g. from small misalignments) remain within allowable stresses, but
the design intent is that **punch-induced lateral forces are carried
primarily by the guides**, not by bending of the screw.

##### 5.3.3.3.1. Fail-safe and serviceability behaviour

The manual screw jack is **self-locking / non-backdrivable**, so a loss
of user input or accidental release of the handwheel does not cause
sudden descent. Under repeated training-level loads (around F~char~ =
1.8 kN), the combined jack--guide system is checked to ensure:

-   No significant **creep, settlement or thread wear** occurs in the
    jack under sustained axial loading; and

-   No **loosening of guide rail fasteners** or play develops at the
    guide interfaces.

In this way, the height-adjustment system meets the criteria in Tables
16 and 17 using a **single** screw jack: the jack is sized for **axial
gravity loads and buckling**, while the **vertical guides** are sized
for **punch-induced lateral loads and overturning moments based on**
F~design~, providing both fail-safe behaviour and realistic stiffness
under impact.
