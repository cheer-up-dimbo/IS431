import time
from typing import Optional, List, Tuple

try:
    import serial  # type: ignore
except Exception as e:
    serial = None  # Will raise at runtime when used


def measure_punches(
    port: str = "COM10",
    baud: int = 115200,
    punch_threshold_ms2: float = 10.0,
    max_punches: int = 10,
    debounce_ms: int = 300,
    max_duration_s: Optional[float] = 120.0,
) -> List[Tuple[int, float]]:
    """Detect and measure individual punches from serial stream.

    Expects lines containing "Total_Accel:XX.XX" (optionally with commas),
    detects punches when acceleration > punch_threshold_ms2, and returns
    a list of (punch_number, g_force) tuples. Stops after `max_punches` or `max_duration_s`.

    Args:
        port: Serial port name (e.g., "COM10", "/dev/ttyACM0").
        baud: Serial baud rate.
        punch_threshold_ms2: Acceleration threshold to detect a punch (m/s^2).
        max_punches: Number of punches to detect before stopping.
        debounce_ms: Minimum time between detected punches.
        max_duration_s: Optional max wall-clock duration before giving up.

    Returns:
        List of tuples (punch_number, g_force) for each detected punch.
        Returns empty list if no punches detected.
    """
    if serial is None:
        raise RuntimeError("pyserial is not available; install 'pyserial'.")

    print(f"[PUNCH DETECTION] Starting measurement on {port}. Threshold: {punch_threshold_ms2} m/s²")
    
    try:
        ser = serial.Serial(port, baud, timeout=0.1)
    except Exception as e:
        print(f"[PUNCH DETECTION] Error opening serial port {port}: {e}")
        return []
    
    time.sleep(2.0)  # Allow device to reset

    count = 0
    punches: List[Tuple[int, float]] = []
    last_punch_time = 0.0
    start_time = time.time()
    data_received = False
    peak_in_window = 0.0  # Track peak during debounce window

    try:
        while count < max_punches:
            # Check timeout
            elapsed = time.time() - start_time
            if max_duration_s is not None and elapsed > max_duration_s:
                print(f"[PUNCH DETECTION] Timeout reached after {elapsed:.1f}s. Detected {count} punches.")
                break

            # Read available lines - process buffer but apply debounce per reading
            while ser.in_waiting:
                data_received = True
                raw = ser.readline().decode('utf-8', errors='ignore').strip()
                if not raw:
                    continue
                if "Total_Accel:" not in raw:
                    continue
                try:
                    parts = raw.split(',')
                    for p in parts:
                        if "Total_Accel:" in p:
                            accel_ms2 = float(p.split(':', 1)[1])
                            now = time.time()
                            time_since_last = (now - last_punch_time) * 1000.0
                            
                            # Check if we're in debounce window
                            if time_since_last <= debounce_ms:
                                # Still in debounce - track peak but don't register new punch
                                if accel_ms2 > peak_in_window:
                                    peak_in_window = accel_ms2
                            else:
                                # Outside debounce window - check for new punch
                                if accel_ms2 > punch_threshold_ms2:
                                    count += 1
                                    last_punch_time = now
                                    g_force = accel_ms2 / 9.81
                                    punches.append((count, g_force))
                                    peak_in_window = accel_ms2
                                    print(f"[PUNCH DETECTION] ✓ PUNCH #{count} detected! Accel: {accel_ms2:.2f} m/s² | G-Force: {g_force:.2f}g")
                                    
                                    # IMPORTANT: Break out of buffer processing to return punch immediately
                                    # This allows GUI to get real-time feedback
                                    break
                    else:
                        # Continue to next line in buffer
                        continue
                    # If we broke out (punch detected), stop processing buffer
                    break
                    
                except Exception as e:
                    print(f"[PUNCH DETECTION] Parse error: {e}")
                    continue
            
            # Small sleep to avoid busy spin when no data
            if not ser.in_waiting:
                time.sleep(0.01)
                
                # Every second, report if no data received
                if int(elapsed) % 1 == 0 and not data_received and elapsed < 1.5:
                    print(f"[PUNCH DETECTION] Waiting for data... ({elapsed:.1f}s)")
    
    except Exception as e:
        print(f"[PUNCH DETECTION] Exception during measurement: {e}")
    finally:
        try:
            ser.close()
        except Exception:
            pass

    print(f"[PUNCH DETECTION] Measurement complete. Detected {count}/{max_punches} punches in {time.time() - start_time:.1f}s")
    return punches


def measure_punches_with_callback(
    port: str = "COM10",
    baud: int = 115200,
    punch_threshold_ms2: float = 100.0,
    max_punches: int = 10,
    debounce_ms: int = 300,
    max_duration_s: Optional[float] = 120.0,
    callback=None,
) -> List[Tuple[int, float]]:
    """Detect punches with real-time callback for GUI updates.
    
    This version calls callback(punch_number, g_force) immediately when a punch is detected,
    allowing the GUI to update in real-time.
    
    Args:
        port: Serial port name (e.g., "COM10", "/dev/ttyACM0").
        baud: Serial baud rate.
        punch_threshold_ms2: Acceleration threshold to detect a punch (m/s^2).
        max_punches: Number of punches to detect before stopping.
        debounce_ms: Minimum time between detected punches.
        max_duration_s: Optional max wall-clock duration before giving up.
        callback: Optional function(punch_num: int, g_force: float) called on each punch.
    
    Returns:
        List of tuples (punch_number, g_force) for each detected punch.
    """
    if serial is None:
        raise RuntimeError("pyserial is not available; install 'pyserial'.")

    print(f"[PUNCH DETECTION] Starting measurement on {port}. Threshold: {punch_threshold_ms2} m/s²")
    
    try:
        ser = serial.Serial(port, baud, timeout=0.1)
    except Exception as e:
        print(f"[PUNCH DETECTION] Error opening serial port {port}: {e}")
        return []
    
    time.sleep(2.0)  # Allow device to reset

    count = 0
    punches: List[Tuple[int, float]] = []
    last_punch_time = 0.0
    start_time = time.time()
    data_received = False

    try:
        while count < max_punches:
            # Check timeout
            elapsed = time.time() - start_time
            if max_duration_s is not None and elapsed > max_duration_s:
                print(f"[PUNCH DETECTION] Timeout reached after {elapsed:.1f}s. Detected {count} punches.")
                break

            # Read and process data
            if ser.in_waiting:
                data_received = True
                raw = ser.readline().decode('utf-8', errors='ignore').strip()
                if raw and "Total_Accel:" in raw:
                    try:
                        parts = raw.split(',')
                        for p in parts:
                            if "Total_Accel:" in p:
                                accel_ms2 = float(p.split(':', 1)[1])
                                now = time.time()
                                time_since_last = (now - last_punch_time) * 1000.0
                                
                                # Only register punch if above threshold AND outside debounce window
                                if accel_ms2 > punch_threshold_ms2 and time_since_last > debounce_ms:
                                    count += 1
                                    last_punch_time = now
                                    g_force = accel_ms2 / 9.81
                                    punches.append((count, g_force))
                                    print(f"[PUNCH DETECTION] ✓ PUNCH #{count} detected! Accel: {accel_ms2:.2f} m/s² | G-Force: {g_force:.2f}g")
                                    
                                    # Call GUI callback immediately
                                    if callback:
                                        callback(count, g_force)
                    except Exception as e:
                        print(f"[PUNCH DETECTION] Parse error: {e}")
            else:
                time.sleep(0.01)
    
    except Exception as e:
        print(f"[PUNCH DETECTION] Exception during measurement: {e}")
    finally:
        try:
            ser.close()
        except Exception:
            pass

    print(f"[PUNCH DETECTION] Measurement complete. Detected {count}/{max_punches} punches in {time.time() - start_time:.1f}s")
    return punches


def measure_peak(
    port: str = "COM10",
    baud: int = 115200,
    threshold: float = 35.0,
    max_punches: int = 10,
    debounce_ms: int = 300,
    max_duration_s: Optional[float] = 120.0,
) -> float:
    """Measure peak total acceleration from serial stream until max_punches.

    Expects lines containing "Total_Accel:XX.XX" (optionally with commas),
    counts a punch on values above threshold with simple debounce, and returns
    the maximum value observed. Stops after `max_punches` punches or `max_duration_s`.

    Args:
        port: Serial port name (e.g., "COM10", "/dev/ttyACM0").
        baud: Serial baud rate.
        threshold: Acceleration threshold to count a punch (m/s^2).
        max_punches: Number of punches to measure before stopping.
        debounce_ms: Minimum time between counted punches.
        max_duration_s: Optional max wall-clock duration before giving up.

    Returns:
        The maximum g-force observed (in g). Returns 0.0 if no data.
    """
    if serial is None:
        raise RuntimeError("pyserial is not available; install 'pyserial'.")

    ser = serial.Serial(port, baud, timeout=0.1)
    time.sleep(2.0)  # Allow device to reset

    count = 0
    peak = 0.0
    last_punch_time = 0.0
    start_time = time.time()

    try:
        while count < max_punches:
            # Check timeout
            if max_duration_s is not None and (time.time() - start_time) > max_duration_s:
                break

            # Read available lines
            while ser.in_waiting:
                raw = ser.readline().decode('utf-8', errors='ignore').strip()
                if not raw:
                    continue
                if "Total_Accel:" not in raw:
                    continue
                try:
                    parts = raw.split(',')
                    for p in parts:
                        if "Total_Accel:" in p:
                            val = float(p.split(':', 1)[1])
                            if val > peak:
                                peak = val
                            now = time.time()
                            if val > threshold and (now - last_punch_time) * 1000.0 > debounce_ms:
                                count += 1
                                last_punch_time = now
                except Exception:
                    # Ignore parse errors and continue
                    continue

            # Small sleep to avoid busy spin
            time.sleep(0.01)
    finally:
        try:
            ser.close()
        except Exception:
            pass

    # Convert acceleration (m/s²) to g-force (g = m/s² / 9.81)
    return peak / 9.81


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Measure peak from serial punches")
    parser.add_argument("--port", default="COM12")
    parser.add_argument("--baud", type=int, default=115200)
    parser.add_argument("--threshold", type=float, default=100.0)
    parser.add_argument("--max-punches", type=int, default=10)
    parser.add_argument("--debounce-ms", type=int, default=300)
    parser.add_argument("--max-duration", type=float, default=120.0)
    args = parser.parse_args()

    # Use the callback version for testing
    def print_punch(num, g):
        print(f"\n🥊 PUNCH {num}: {g:.2f}g\n")
    
    results = measure_punches_with_callback(
        port=args.port,
        baud=args.baud,
        punch_threshold_ms2=args.threshold,
        max_punches=args.max_punches,
        debounce_ms=args.debounce_ms,
        max_duration_s=args.max_duration,
        callback=print_punch
    )
    
    print(json.dumps({"punches": [(n, round(g, 2)) for n, g in results]}))
