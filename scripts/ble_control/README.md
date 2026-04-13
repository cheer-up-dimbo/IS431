# BLE Base Rotation Controller V3

This directory contains the Version 3 firmware (`ble_control.ino`) and Bluetooth Web Controller (`controller.html`) for the BoxBunny boxing robot base.

V3 is a stripped-down, highly robust **Direct Command** architecture. It abandons PID control and ramping in favor of direct RPM commands, prioritizing instantaneous response and failsafe limits.

## Hardware Requirements
* **Board:** Arduino Uno R4 WiFi (Renesas RA4M1 48MHz ARM Cortex-M4)
* **Motor:** Z55BLD400-24GU Brushless DC Motor
* **Driver:** ZBLD C20‑800LRC (CAN Bus)
* **Encoder:** AS5047P Magnetic Encoder
* **Drive Ratio:** 91:1 Total (26:1 Gearbox × 3.5:1 Belt)

## The EMI Challenge & Software SPI
The Arduino Uno R4 WiFi runs exactly 3x faster than the old AVR Unos. Because of this, the `digitalWrite()` Bitbang Software SPI runs at roughly ~500kHz. 

When running unshielded SPI wires near the 24V/300RPM BLDC motor, the Electromagnetic Interference (EMI) shreds the SPI clock and data lines. 
* **The Problem:** The AS5047P sends a 1-bit Parity and Error flag. Under heavy motor load, EMI randomly flips bits, causing strict parity checks to reject 99% of frames, completely freezing the position tracking while the motor runs. If parity checks are turned off, the noise integrates into massive "phantom" position drift when the robot is completely stationary.
* **The Solution (Velocity Clamp):** V3 uses a "Physical Reality Clamp" inside `updateEncoder()`. The physics of the motor dictate a maximum speed of 3400 RPM (928k encoder counts/sec). In a 5ms loop window, the absolute maximum counts the base can physically move is ~4640. The software simply rejects any SPI delta `> 6000` counts. This instantly drops all massive EMI spikes (eliminating stationary phantom drift) while letting slightly noisy but mathematically feasible data through during motion. Because of the nature of integration (`totalCounts += diff`), random bit flips average out to exactly zero over time, resulting in perfectly accurate position tracking during full-speed motion.

## Direct Command Protocol (BLE UUID `0x1820`)

The BLE characteristic exposes simple string commands:

| Command | Action |
|---------|--------|
| `L:<RPM>` | Rotate LEFT (Encoder Negative) at specified RPM. Blocks if at -90°. |
| `R:<RPM>` | Rotate RIGHT (Encoder Positive) at specified RPM. Blocks if at +90°. |
| `P:<ANGLE>,<RPM>`| Auto-targets the specified angle (-90 to 90), capping the speed at the specified RPM to prevent aggressive launches. Interruptible by L/R/S. |
| `S` | Instant Stop. |
| `Z` | Re-zeros the encoder to the current physical position. |
| `STATUS` | Prints nicely formatted internal variables over Serial. |
| `DIAG` | Prints 10Hz buffered CAN data (Voltage/Current). Non-blocking. |
| `DEBUG` | Toggles the printing of raw CAN RX hexadecimal frames. |

## Limit Enforcement (`±90°`)
Safety limits are hard-enforced at the bottom of every `loop()` iteration. 
The system requires **BOTH** the commanded direction and the physical position to violate the limit:
* If `baseDeg >= 90.0` AND `motorDir == 2` (Right Cmd): Stop immediately.
* If `baseDeg <= -90.0` AND `motorDir == 1` (Left Cmd): Stop immediately.

This guarantees that a return command (`L:` when stuck at `+90°`) is instantly accepted, and coasting past the limit will never accidentally trigger a false lock.

## Usage
1. Flash `ble_control.ino` to the Arduino Uno R4 WiFi.
2. Open `controller.html` in Chrome or Edge (must support Web Bluetooth).
3. Connect to **BoxBunny Base**.
4. The system automatically zeroes the encoder on boot. Use the slider and buttons for direct physical response.
