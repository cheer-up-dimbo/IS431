# Timing Belt & Pulley Selection — BoxBunny Rotational Drive

## Motor Specs (Z55D Series Parallel Shaft Reducer, ZD Motor)

- Model: 755BLD 400-24GU, 5GU, 25KB
- Voltage: 24V, Rated Power: 400W
- Rated Speed: 3000 RPM (before gear reduction)
- Rated Torque: 1.28 Nm
- Gearhead: Long life, low noise — 5GU25KB, **Gear Ratio: 1:25**
- O/P Shaft Speed: **120 RPM** (after gear reduction)
- Allowance Torque: 20.0 Nm → Actual Torque: **32 Nm**

**Input RPM = 120 rpm → Output RPM = 25 rpm**
**Input Torque = 30 Nm → Output Torque = 150 Nm**

---

## Step 1: Required Speed Ratio

$$i = \frac{n_{in}}{n_{out}} = \frac{120}{25} = 4.8$$

In pulley terms: $i = \frac{Z_{large}}{Z_{small}} \approx 4.8$

→ Requires approximately **4.8:1 reduction**

---

## Step 2: Design Power (Misumi Calculation)

$$P_d = P_t \times K_s = 400W \times 2.2 = 880W = 0.88\ \text{kW}$$

- RPM of small pulley = Motor RPM = **120 RPM**

---

## Step 3: Belt Series Type Selection

From Misumi Selection Guide Tables, candidate series identified:

1. H series
2. S8M series
3. **P8M600 Series** → Pitch width: 8mm, Belt width: 600mm, Applicable pulley tooth number: 20 teeth
4. MTS8M series
5. UP8M series
6. EV5GT series

**Selected: S8M series**

---

## Step 4: Pulley Selection and Final Ratio

Predetermined speed ratio: **1:4.8** → $\frac{Z_{large}}{Z_{small}} \approx 4.8$

From Table 26 (Allowable min. number of teeth), at 120 RPM for S8M series → min. teeth = **22**

**Small pulley:**
- $Z_{small} = 20$ teeth, Pitch: 8mm
- $d_p = \frac{8 \times 20}{\pi} = 50.93\ \text{mm}$

**Large pulley (updated):**
- $Z_{large} = 70$ teeth *(revised from 60T — to match slewing-bearing inner-ring geometry and allow screw-through fastening into threaded inner-ring mounting holes)*
- $D_p = \frac{8 \times 70}{\pi} = 178.25\ \text{mm}$

**Final implemented ratio:**

$$i_{actual} = \frac{Z_{large}}{Z_{small}} = \frac{70}{20} = 3.5$$

$$\boxed{1:3.5}$$

**Output speed:**

$$n_{out} = \frac{120}{3.5} = 34.3\ \text{RPM}$$

Equivalent angular speed:

$$34.3 \times 6 = 205.7°/\text{s}$$

> This is above the original 25 RPM / 150°/s target, but closer than the earlier 60T arrangement.

---

## Step 5: Belt Length and Centre Distance

**Approximate initial centre distance:**

$$C' = 286.18\ \text{mm}$$

Using updated pulley diameters ($D_p = 178.25\ \text{mm}$, $d_p = 50.93\ \text{mm}$):

**Theoretical pitch length:**

$$L_p' = 2C' + \frac{\pi(D_p + d_p)}{2} + \frac{(D_p - d_p)^2}{4C'}$$

$$L_p' \approx 946.5\ \text{mm}$$

**Selected standard belt length:**

$$L_p = 952\ \text{mm}$$

**Corrected centre distance:**

$$b = 2L_p - \pi(D_p + d_p) = 2(952) - \pi(178.25 + 50.93) = 1184.0$$

$$C = \frac{b + \sqrt{b^2 - 8(D_p - d_p)^2}}{8}$$

$$\boxed{C \approx 289.0\ \text{mm}}$$

---

## Step 6: Belt Width

$$B_w = \frac{P_d}{P_o \times K_m} \times W_p$$

- $P_d$ = design power = 0.88 kW
- $P_o$ = Reference Transmission Capacity
  - 150T: $1.61 \times 0.21 = 0.3376$
  - 200T: $1.76 \times 0.13 = 0.6572$
  - 300T: $1.76 \times 0.47 = 0.3920$
  - 400T: $1.92 \times 0.43 = 1.1088$
- $K_m$ = Engagement Correction Coefficient
- $W_p$ = Reference Belt Width, S8M = 60mm
- No. of teeth engaged $(B_m)$ = $\frac{\theta \cdot Z_{small}}{360°} = \frac{24(120)(123)}{360} = 12\ \text{teeth}$

$$B_w = \frac{0.88}{1.176 \times 1} \times 60 = 3.0$$

**→ Final selected belt width = 32 mm** *(hardware selection; updated from calculated 30mm)*

---

## Final Selections Summary

| Parameter | Updated Selected Value |
|---|---|
| Belt series | S8M |
| Pitch | 8mm |
| Belt width | **32mm** |
| Small pulley teeth | 20 |
| Large pulley pitch diameter | 50.93mm |
| Large pulley teeth | **70** |
| Large pulley pitch diameter | **178.25mm** |
| Final speed ratio | **1:3.5** |
| Output RPM | **34.3 RPM** |
| Output angular speed | **205.7°/s** |
| Theoretical belt length | **946.5mm** |
| Selected standard belt length | **952mm** |
| Corrected centre distance | **289.0mm** |
| Small pulley RPM | 120 RPM |

**Worst Case Scenario: Straight strike at 45° angle point**

---

## Updated Report-Ready Summary

The large pulley was revised from 60 teeth to 70 teeth in order to match the slewing-bearing inner-ring geometry more effectively and allow screw-through fastening into the threaded inner-ring mounting holes. With the small pulley retained at 20 teeth, the final implemented transmission ratio became 70/20 = 3.5, giving a speed reduction of 1:3.5. Using an input speed of 120 RPM from the geared motor, the resulting output speed is 34.3 RPM, equivalent to approximately 205.7°/s. Although this remains above the original target of 25 RPM (150°/s), it is closer to the desired value than the earlier 60-tooth design. The updated large-pulley pitch diameter is 178.25 mm, while the small-pulley pitch diameter remains 50.93 mm. Using an approximate initial centre distance of 286.18 mm gives a theoretical belt pitch length of about 946.5 mm, so the next available standard belt length of 952 mm was selected. This results in a corrected inter-shaft distance of approximately 289.0 mm. The selected belt series remains S8M with 8 mm pitch, and the final implemented belt width is 32 mm.
