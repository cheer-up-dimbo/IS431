# Final Base: Rotating + Transportation
**Date:** 18 February 2026, 16:23
**Project:** CDE4301 BoxBunny

> These notes document the design decisions, load calculations, and system analysis leading up to the final fabricated assembly: `v7_fab_assem_base_rotating.glb`

---

## Overview

**Core Decision: Inner vs Outer Ring Drive**
- Should be driven by motor — rotating the entire robot body
- Depends on mount stability, ring bearing, slewing
- **Recommended: Outer → Vertical ring drive**
  - Because the height effective radius, radial & radiate tooth form & torque availability under loads

**Rotating Thrust / Stability:**
- Actual Load: $F_a$ = robot output
- Radial Load: $F_r$ = four punches, off-centre (doing motion, alternating)
- Moment affects all
- Stability determined by the slewing ring's pitch / inner (if inner ring is connected)

---

## Load Calculations

**Notation:**
- $F_a$ = axial load (vertical)
- $F_r$ = radial load (horizontal impact)
- $F_b$ = radial load (horizontal) — punch row
- $M_h$ = static base force produced by force
- $M_s$ = overturning moment

$$F_a = mg = 592 \times g \approx 5 \times 10^3 \text{ N}$$
$$F_a \cdot \text{amp} = 592 \times g \approx 1 \times 10^4 \text{ N}$$
$$F_r = F_{punch} \times 2 = 200 \text{ N (static)}$$
$$F_r \cdot \text{amp} = 6100 \times 1 = 6100 \text{ N}$$
$$M_t = F_{punch} \times 1.5 \text{ m (Tilting Moment)}$$

**Summary Values:**
- Radial Load: $F_a = 575 \text{ kN}$
- Radial Load: $F_r = 1.76 \text{ kN}$
- Tilting Moment / Margin: $M = 3 \text{ kNm}$
- Rotational Speed: $n = 25 \text{ rpm}$

---

## Slewing Ring Bearing Selection

**OD 25 → 262 parameters:**
- Module: $m = 6$
- Tooth profile: $\theta = 9\%$
- Pitch angle: $\gamma = 16°$
- Pitch dia: $d = 3\pi$ mm
- Outer dia of alternating table: 50
- Inner dia of alternating table: 30
- Number of teeth: per MTC standard

**Bore types:**
- 0 = no gear
- 1 = external gear with small module
- 2 = internal bore with big module

**Final Decision: Robotic Slewed Ring / Fixed Outer Ring**
- Slewing Ring Teeth: 6 inner drive
- Handles axial load, radial load, and tilting moment simultaneously

---

## Torque Analysis for Rotating Base

**Three torque components:**
1. Belt Torque (resist + deformation)
2. Conformal Torque (steady rotation against friction/delay)
3. Holding / Stall Torque (torque for parts when stopped)

**Acceleration Torque:**
$$\tau = J \cdot \dot{\omega}$$
$$\dot{\omega} = \frac{\Delta\omega}{\Delta t} = \frac{\omega}{\text{min time (s)}}$$

$$\omega = \frac{2\pi \cdot \text{rpm}}{60}$$

**Stall Torque → Plateau → Friction:**
- Max stall rotation torque: ~102 Nm

**Transmissional:**
$$= 35 \times 0.9835 \times 95 \times 9 \text{ kNm}$$
$$= 0.12 \text{ N·m up}$$

**Startup Torque** must be enough for:
- Acceleration/deceleration (horizontal rigging)
- Low velocity positioning
- Check deceleration in contact scenarios

**Confirmed geometry:**
- H = 500 mm
- Belt section = end 2 slots
- Radial distance of belt force = 310 mm (31 cm)

---

## Motor Selection

**Z55D Series Parallel Shaft Reducer (ZD Motor, Gearhead):**
- Model: 755BLD 400-24GU, 5GU, 25EB
- Voltage: 24V
- Rated Power: 400W
- No-load Current: 7.2A
- No-load Speed: 3400 RPM
- Rated Current: 19.5A
- Rated Speed: 3400 RPM (before gear reduction)
- Rated Torque: 1.28 Nm
- Motor Lead Wire Type: Pinion Shaft
- Gearhead: Long life, low noise — 5GU25EB

**Output (after gear reduction):**
- O/P Shaft Speed = **120 RPM**
- Allowance Torque = **30.0 Nm**

---

## Calculated Design Power

$$P_d\ (\text{kW}) = \text{Transmission Power}\ (P_t)\ (\text{kW}) \times \text{Overload Factor}\ (K_s)$$

- Based on motor control point power
- $K_s = K_o + K_r + K_i$

---

## Belt Drive System

**Why Belt Drive over Gear Drive:**
1. Lower reflected costs — replacement parts cheaper
2. Tolerates upper-spec clearances — more forgiving of motor mounting
3. Better flexibility — motor safety (acts as mechanical fuse)
4. Ease of development — not engine-adjustable, regular cycling loads supported
5. Balance flexibility — belt can permit elastic give after gear

**Factors affecting positioning accuracy:**
- Elasticity in cord → non-transmit power loss
- Low elongation → high modulus of elasticity (e.g. Carbon cord)
- Improves response, reduces power difference
- Backlash: large gap → reverse delay during step/reverse direction

**Tooth Profile Options Considered:**
- **AT-Series (AT5/AT10):** Designed for high precision system control
  - Large section, trapezoidal profile → increased clearance example
  - Ideal for feedback/drop drive: belt & pulley
- **HTD (3M/5M series):** Designed for high torque applications
  - May have pulley feedback issues

**→ Main Selection: Pilmor CA750 (5M/5M series)**
- Recommended for heavy duty applications where the rotating step requires
- Large modular stiffness/speed absorption

**⚠ Belt Tension = extra position / limit = stability**
- Belt tension is optimal limit = extremal point = stability
- Potential for increased throttle if over-tensioned

**Selection Steps for Timing Belt & Pulley:**
1. Determine belt load (single/plane)
2. Determine output position
3. Select tooth profile (AT5, 8%, etc.)
4. Calculate transmission ratio
5. Determine pulley size
6. Calculate belt length and shaft distance

**Changing motor flexibility = swapping pulleys (no. of teeth) = changing belt lengths**

---

## 2.6 Tooth Skip Under Shock

If a user hits hard while accelerating or reversing, belt can skip if:
- Belt width too small
- Pulley too small
- Wrap angle too low
- Tension insufficient

**Mitigation:**
- Choose appropriate belt pitch (HTD 5M/8M etc.)
- Increase pulley diameter
- Increase belt width
- Increase wrap angle via idler
- Limit acceleration profile in control
- Keep belt tension only as high as needed
- Use larger pulley wrap angle and/or idlers to prevent skip without extreme tension
- Use a rigid motor mount plate

---

## Transportation System

**Target load: 650 kg**

**Mechanism: Tip-and-roll with rear wheels**
- Inspired by portable gym equipment (built-in wheels for easy mobility)
- Handle at front, rear wheels at back

**Force calculation when tilted (2 rear wheels):**
- Applying principle of momentum (torques) around rear axle as fulcrum
- $W = mg = 650 \times 9.6 = 6307 \text{ N}$
- $D$ = Horizontal distance from rear axle to CG
- $D$ = Horizontal distance from rear axle to front axle
- $\theta$ = Angle of inclination when tilted

**Static stability cases:**
1. Only rear wheels in front, handle in front
2. Big drive wheels at back, handles at back — opposed to front

$$\Sigma M_A = 0$$

**Note:** If tilting (upward), the load's CG must be vertically above the pivot — otherwise tipping is uncontrollable. The horizontal distance (balance arm) is critical.

**Using steel tubes in spring-type frame:**
- Slot force calculation: end cord + slide + sin
- Shape: 25 mm

---

## Design Requirements Summary

**Stability / Fitness:**
- Must not fall over (to ground) or slide/rotate during punching
- Must not require step from hardware when user steps/pushes
- Must not create push replaces from high testing pull

**Strength:**
- Pillars want ~9000 N (1500 of the loads) → load-based design
- Must drive thinkable → Closure, shoot diameter mounting
- Must not require adjacent pivots → stable short class tool

**Usability:**
- About width/weight balance
- Incubation pads want to take good feedback (replays, followers, in loose rate)

---

## Key Design Decisions Summary

| Decision | Choice | Rationale |
|---|---|---|
| Inner vs Outer Ring Drive | Fixed Outer Ring / Inner Drive | Cleaner mechanical load path, concentric rotating assembly |
| Belt vs Gear Drive | Belt Drive (S8M / 5M series) | Lower cost, tolerates misalignment, flexible, replaceable |
| Slewing Bearing Type | Robotic Slewed Ring | Handles axial, radial, and tilting moment simultaneously |
| Motor for Rotation | Z55D Series, 400W, 24V | 120 RPM output after gear reduction, 30 Nm allowance |
| Transport System | Tip-and-roll with rear wheels | Gym equipment inspired; handles 650 kg load |
| Tooth Skip Mitigation | HTD 5M/8M belt, wider belt, larger pulley, idlers | Prevents skip under shock punch loads |

---

*Final fabricated assembly: `v7_fab_assem_base_rotating.glb`*
