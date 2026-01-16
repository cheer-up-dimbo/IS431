import time
from typing import Optional

try:
    import serial  # type: ignore
except Exception as e:
    serial = None  # Will raise at runtime when used


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
        port: Serial port name (e.g., "COM12", "/dev/ttyACM0").
        baud: Serial baud rate.
        threshold: Acceleration threshold to count a punch (m/s^2).
        max_punches: Number of punches to measure before stopping.
        debounce_ms: Minimum time between counted punches.
        max_duration_s: Optional max wall-clock duration before giving up.

    Returns:
        The maximum acceleration observed (m/s^2). Returns 0.0 if no data.
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

    return peak


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Measure peak from serial punches")
    parser.add_argument("--port", default="COM12")
    parser.add_argument("--baud", type=int, default=115200)
    parser.add_argument("--threshold", type=float, default=35.0)
    parser.add_argument("--max-punches", type=int, default=10)
    parser.add_argument("--debounce-ms", type=int, default=300)
    parser.add_argument("--max-duration", type=float, default=120.0)
    args = parser.parse_args()

    peak_val = measure_peak(
        port=args.port,
        baud=args.baud,
        threshold=args.threshold,
        max_punches=args.max_punches,
        debounce_ms=args.debounce_ms,
        max_duration_s=args.max_duration,
    )
    print(json.dumps({"peak": peak_val}))
