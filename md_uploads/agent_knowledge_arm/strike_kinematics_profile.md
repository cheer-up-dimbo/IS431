# Boxing Robot — Strike Kinematics and Power Profile

**File:** `agent_knowledge/strike_kinematics_profile.md`
**Scope:** Kinematic validation and electrical power tracking of FSM-driven strikes.
**Generated From:** Core CSV datasets in `boxing_robot/ros2_ws/unified_v4/data/`
**Target Audience:** Electrical Agents (for power limits), Mechanical Agents (for gear fatigue & velocities), and Lead Integrator (for tuning dynamics).

---

## 1. Executive Summary

This document aggregates the telemetry profiles from 23 physical FSM trials (10 Left Arm strikes, 10 Right Arm strikes, and 3 variable-speed Jabs). The system was commanded at 25.0 rad/s via the GUI (except for the speed scaling test).

The telemetry explicitly measures:
- **Kinematic metrics:** Time (Windup-to-Apex `wu_ap`, Apex-to-Windup `ap_wu`), Peak Angular Velocity (rad/s), Average Angular Velocity (rad/s).
- **Electrical metrics:** Peak instantaneous current (A) per motor, Peak Power (W) per motor, and Total Aggregate Power (W).

---

## 2. Speed Scaling Analysis (Left Jab)

This test measured the Left Jab commanded at 10.0, 20.0, and 25.0 rad/s to validate that the physical system scales velocities linearly and tracks the duration of execution.

| Commanded Speed | Total Duration | Peak Angular Vel. | Avg Angular Vel. | Peak Power (Total) |
|---|---|---|---|---|
| **10.0 rad/s** | 1.54 – 1.57 s | 19.3 – 46.2 rad/s | 6.5 – 7.1 rad/s | 42.5 – 43.9 W |
| **20.0 rad/s** | 1.25 – 1.28 s | 37.3 – 72.0 rad/s | 8.5 – 9.9 rad/s | 51.1 – 51.8 W |
| **25.0 rad/s** | 1.22 – 1.25 s | 64.5 – 98.6 rad/s | 9.3 – 10.4 rad/s | 51.6 – 52.6 W |

**Analysis:**
- **Execution Time:** Compresses from ~1.55s down to ~1.23s. 
- **Kinematic Yield:** Peak velocities naturally spike and easily exceed the nominal commanded speed mid-transit due to the inertial whip of the structure and aggressive motor acceleration before deceleration.
- **Power Draw:** Power climbs modestly with speed, maxing at ~52W for the 25.0 rad/s Jab.

---

## 3. Left Arm Strike Profiles (25.0 rad/s)

This section details the 10-sample averages for the Left Arm strikes executed at 25.0 rad/s. The Left Arm is primarily driven by **M1 (Pitch/Roll Coupling)** and **M2 (Roll)**. 

### 3.1 Kinematic Comparison
| Strike | Total Execute Time | Peak Angular Vel. | Avg Angular Vel. |
|---|---|---|---|
| **Jab** | ~1.25 s | 33 – 218 rad/s | 8.8 – 11.9 rad/s |
| **Left Hook** | ~1.27 s | 38 – 91 rad/s | 7.3 – 8.0 rad/s |
| **Left Uppercut** | ~1.09 s | 22 – 101 rad/s | 6.9 – 9.1 rad/s |

**Note:** The Uppercut is consistently the fastest to execute, taking < 1.1 seconds. 

### 3.2 Electrical Power & Load Balancing
| Strike | M1 Peak | M2 Peak | Total System Peak Power |
|---|---|---|---|
| **Jab** | 1.34 A (~32 W) | 0.54 A (~13 W) | ~52.5 W |
| **Left Hook** | 0.85 A (~20 W) | 0.89 A (~21 W) | ~49.5 W |
| **Left Uppercut** | 0.72 A (~17 W) | 0.89 A (~21 W) | ~46.5 W |

**Analysis:**
- **Asymmetric Loading:** The **Jab** heavily taxes Motor 1 (M1), pulling up to 1.39A during peak extension, whereas M2 barely contributes.
- **Symmetric Loading:** The **Left Hook** and **Left Uppercut** distribute the torque evenly across both gear trains, settling around ~0.85A per motor. 

---

## 4. Right Arm Strike Profiles (25.0 rad/s)

This section details the 10-sample averages for the Right Arm strikes executed at 25.0 rad/s. The Right Arm is driven by **M3** and **M4**.

### 4.1 Kinematic Comparison
| Strike | Total Execute Time | Peak Angular Vel. | Avg Angular Vel. |
|---|---|---|---|
| **Cross** | ~1.23 s | 40 – 208 rad/s | 9.0 – 11.5 rad/s |
| **Right Hook** | ~1.24 s | 29 – 91 rad/s | 6.7 – 7.8 rad/s |
| **Right Uppercut** | ~1.22 s | 41 – 170 rad/s | 7.0 – 9.4 rad/s |

### 4.2 Electrical Power & Load Balancing
| Strike | M3 Peak | M4 Peak | Total System Peak Power |
|---|---|---|---|
| **Cross** | 0.90 A (~21 W) | 0.60 A (~14 W) | ~46.5 W |
| **Right Hook** | 0.61 A (~14 W) | 0.83 A (~20 W) | ~44.5 W |
| **Right Uppercut** | 1.05 A (~25 W) | 0.83 A (~20 W) | **~55.0 to 68.9 W** |

**Analysis:**
- **Power Hungry:** The **Right Uppercut** is the most electrically intensive maneuver across both arms. During extreme transient spikes, M3 pulls over 1.5A on its own, pushing the total system peak power up to **68.9W**.
- **Right vs Left:** The Uppercut behaves inversely on the Right arm compared to the Left. The Left Uppercut is very power-efficient (~46W), whereas the Right Uppercut is power-hungry. The Cross (Right Arm Jab-equivalent) is slightly *more* efficient than the Left Jab. 

---

## 5. System Architecture Limits Validated

1. **Firmware Trip Wire (3.0A per motor):** The highest recorded single-motor peak in these 23 trials was **M3 at 1.57A** during a Right Uppercut. This establishes a robust **1.43A (~47%) safety headroom** below the firmware's 3.0A emergency kill switch.
2. **Current Budgeting:** The entire 4-motor cluster will theoretically never exceed the 24V/8.8A (211W) rating of the Mean Well PSU during sparring. Even the absolute worst-case recorded peak sum (68.9W) is **< 33% of the PSU capacity**, eliminating the need for a PSU upgrade for arm actuation alone.
