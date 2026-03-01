import time
from typing import Optional, List, Tuple

try:
    import serial  # type: ignore
except Exception as e:
    serial = None  # Will raise at runtime when used


def _send_command(ser, command: str):
    ser.write(f"{command}\n".encode("utf-8"))


def _read_line_with_timeout(ser, timeout_s: float) -> str:
    start = time.time()
    while (time.time() - start) < timeout_s:
        if ser.in_waiting:
            return ser.readline().decode('utf-8', errors='ignore').strip()
        time.sleep(0.01)
    return ""


def check_protocol_version(ser) -> str:
    """Detect if Arduino supports command-based protocol."""
    try:
        ser.reset_input_buffer()
    except Exception:
        pass

    _send_command(ser, "MODE:CONTINUOUS")
    response = _read_line_with_timeout(ser, timeout_s=1.0)
    if response.startswith("OK:"):
        return "command_based"
    return "streaming"


def _expect_prefix(ser, command: str, expected_prefix: str, timeout_s: float) -> bool:
    _send_command(ser, command)
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        response = _read_line_with_timeout(ser, timeout_s=0.2)
        if not response:
            continue
        if response.startswith(expected_prefix):
            return True
        if response.startswith("ERROR:"):
            print(f"[POWER PROTOCOL] {response}")
            return False
    return False


def _parse_power_result(line: str) -> Tuple[Optional[float], Optional[float], Optional[int]]:
    # Expected format: RESULT:PEAK:<peak>,AVG:<avg>,COUNT:<count>
    if not line.startswith("RESULT:"):
        return None, None, None

    payload = line[len("RESULT:"):]
    fields = payload.split(",")
    parsed: dict[str, str] = {}
    for field in fields:
        if ":" not in field:
            continue
        key, value = field.split(":", 1)
        parsed[key.strip().upper()] = value.strip()

    try:
        peak_val = float(parsed["PEAK"]) if "PEAK" in parsed else None
    except Exception:
        peak_val = None
    try:
        avg_val = float(parsed["AVG"]) if "AVG" in parsed else None
    except Exception:
        avg_val = None
    try:
        count_val = int(parsed["COUNT"]) if "COUNT" in parsed else None
    except Exception:
        count_val = None

    return peak_val, avg_val, count_val


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

    try:
        protocol = check_protocol_version(ser)
        if protocol == "command_based":
            punches = _measure_punches_command_with_callback(
                ser=ser,
                max_punches=max_punches,
                max_duration_s=max_duration_s,
                callback=callback,
            )
        else:
            print("WARNING: Arduino firmware outdated - please update for best experience")
            punches = _measure_punches_streaming_with_callback(
                ser=ser,
                punch_threshold_ms2=punch_threshold_ms2,
                max_punches=max_punches,
                debounce_ms=debounce_ms,
                max_duration_s=max_duration_s,
                callback=callback,
            )
    
    except Exception as e:
        print(f"[PUNCH DETECTION] Exception during measurement: {e}")
        punches = []
    finally:
        try:
            ser.close()
        except Exception:
            pass

    print(f"[PUNCH DETECTION] Measurement complete. Detected {len(punches)}/{max_punches} punches")
    return punches


def _measure_punches_command_with_callback(
    ser,
    max_punches: int,
    max_duration_s: Optional[float],
    callback=None,
) -> List[Tuple[int, float]]:
    if not _expect_prefix(ser, "MODE:POWER", "OK:MODE_POWER", timeout_s=2.0):
        print("[POWER PROTOCOL] MODE:POWER failed; switching to streaming fallback")
        return _measure_punches_streaming_with_callback(
            ser=ser,
            punch_threshold_ms2=100.0,
            max_punches=max_punches,
            debounce_ms=300,
            max_duration_s=max_duration_s,
            callback=callback,
        )

    if not _expect_prefix(ser, "START", "OK:POWER_STARTED", timeout_s=2.0):
        print("[POWER PROTOCOL] START failed; switching to streaming fallback")
        return _measure_punches_streaming_with_callback(
            ser=ser,
            punch_threshold_ms2=100.0,
            max_punches=max_punches,
            debounce_ms=300,
            max_duration_s=max_duration_s,
            callback=callback,
        )

    punches: List[Tuple[int, float]] = []
    start_time = time.time()

    while len(punches) < max_punches:
        elapsed = time.time() - start_time
        if max_duration_s is not None and elapsed > max_duration_s:
            print(f"[POWER PROTOCOL] Timeout reached after {elapsed:.1f}s. Detected {len(punches)} punches.")
            break

        line = _read_line_with_timeout(ser, timeout_s=0.1)
        if not line:
            continue

        if line.startswith("POWER_PUNCH:"):
            try:
                power_value = float(line.split(":", 1)[1].strip())
            except Exception:
                continue

            punch_num = len(punches) + 1
            punches.append((punch_num, power_value))
            if callback:
                callback(punch_num, power_value)
        elif line.startswith("ERROR:"):
            print(f"[POWER PROTOCOL] {line}")
        elif line.startswith("RESULT:"):
            # Some firmware may auto-finish and return result before explicit STOP.
            break

    _send_command(ser, "STOP")
    peak, avg, count = _wait_for_power_result(ser, timeout_s=2.0)
    if count is not None and count > len(punches):
        fill_value = avg if avg is not None else (peak if peak is not None else 0.0)
        while len(punches) < count:
            punch_num = len(punches) + 1
            punches.append((punch_num, fill_value))

    return punches


def _wait_for_power_result(ser, timeout_s: float) -> Tuple[Optional[float], Optional[float], Optional[int]]:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        line = _read_line_with_timeout(ser, timeout_s=0.2)
        if not line:
            continue
        if line.startswith("RESULT:"):
            return _parse_power_result(line)
        if line.startswith("ERROR:"):
            print(f"[POWER PROTOCOL] {line}")
            return None, None, None
    return None, None, None


def _measure_punches_streaming_with_callback(
    ser,
    punch_threshold_ms2: float,
    max_punches: int,
    debounce_ms: int,
    max_duration_s: Optional[float],
    callback=None,
) -> List[Tuple[int, float]]:
    count = 0
    punches: List[Tuple[int, float]] = []
    last_punch_time = 0.0
    start_time = time.time()

    while count < max_punches:
        elapsed = time.time() - start_time
        if max_duration_s is not None and elapsed > max_duration_s:
            print(f"[PUNCH DETECTION] Timeout reached after {elapsed:.1f}s. Detected {count} punches.")
            break

        if ser.in_waiting:
            raw = ser.readline().decode('utf-8', errors='ignore').strip()
            if raw and "Total_Accel:" in raw:
                try:
                    parts = raw.split(',')
                    for p in parts:
                        if "Total_Accel:" in p:
                            accel_ms2 = float(p.split(':', 1)[1])
                            now = time.time()
                            time_since_last = (now - last_punch_time) * 1000.0

                            if accel_ms2 > punch_threshold_ms2 and time_since_last > debounce_ms:
                                count += 1
                                last_punch_time = now
                                g_force = accel_ms2 / 9.81
                                punches.append((count, g_force))
                                print(f"[PUNCH DETECTION] ✓ PUNCH #{count} detected! Accel: {accel_ms2:.2f} m/s² | G-Force: {g_force:.2f}g")

                                if callback:
                                    callback(count, g_force)
                except Exception as e:
                    print(f"[PUNCH DETECTION] Parse error: {e}")
        else:
            time.sleep(0.01)

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
