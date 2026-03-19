import random
import time
from dataclasses import dataclass
from typing import Callable, Dict, List
from power.power_runner import (
    check_protocol_version,
    _send_command,
    _read_line_with_timeout,
    _expect_prefix,
)

try:
    import serial  # type: ignore
except Exception:
    serial = None


import os
USE_ARDUINO = os.getenv('STAMINA_USE_ARDUINO', 'false').lower() == 'true'


@dataclass
class StaminaResult:
    total_punches: int
    average_rate: float
    first_30_rate: float
    last_30_rate: float
    stamina_score: int
    fatigue_percentage: float
    duration: int

    def to_dict(self) -> Dict[str, float | int]:
        return {
            "total_punches": self.total_punches,
            "average_rate": self.average_rate,
            "first_30_rate": self.first_30_rate,
            "last_30_rate": self.last_30_rate,
            "stamina_score": self.stamina_score,
            "fatigue_percentage": self.fatigue_percentage,
            "duration": self.duration,
        }


class StaminaRunner:
    def __init__(self, com_port: str = None, duration_seconds: int = 120, use_arduino: bool = USE_ARDUINO):
        self.com_port = com_port or os.getenv('ARDUINO_BUTTON_PORT', 'COM10')
        self.duration = duration_seconds
        self.use_arduino = use_arduino
        self.punch_count = 0
        self.punch_times: List[float] = []
        self.running = False

    def stop(self):
        self.running = False

    def measure_stamina_with_callback(
        self,
        progress_callback: Callable[[int, int, float], None],
        result_callback: Callable[[Dict[str, float | int]], None],
    ):
        if self.use_arduino:
            self._measure_with_arduino(progress_callback, result_callback)
        else:
            self._measure_simulated(progress_callback, result_callback)

    def _measure_with_arduino(
        self,
        progress_callback: Callable[[int, int, float], None],
        result_callback: Callable[[Dict[str, float | int]], None],
    ):
        if serial is None:
            self._measure_simulated(progress_callback, result_callback)
            return

        try:
            ser = serial.Serial(self.com_port, 115200, timeout=0.1)
            time.sleep(2.0)
        except Exception:
            self._measure_simulated(progress_callback, result_callback)
            return

        try:
            protocol = check_protocol_version(ser)
            if protocol == "command_based":
                self._measure_stamina_command(ser, progress_callback, result_callback)
            else:
                print("WARNING: Arduino firmware outdated - please update for best experience")
                self._measure_stamina_streaming(ser, progress_callback, result_callback)
        finally:
            try:
                ser.close()
            except Exception:
                pass

    def _measure_stamina_command(
        self,
        ser,
        progress_callback: Callable[[int, int, float], None],
        result_callback: Callable[[Dict[str, float | int]], None],
    ):
        if not _expect_prefix(ser, "MODE:STAMINA", "OK:MODE_STAMINA", timeout_s=2.0):
            print("[STAMINA PROTOCOL] MODE:STAMINA failed; falling back to streaming")
            self._measure_stamina_streaming(ser, progress_callback, result_callback)
            return

        if not _expect_prefix(ser, "START", "OK:STAMINA_STARTED", timeout_s=2.0):
            print("[STAMINA PROTOCOL] START failed; falling back to streaming")
            self._measure_stamina_streaming(ser, progress_callback, result_callback)
            return

        self.running = True
        current_punch_count = 0
        punch_times: List[float] = []
        start_time = time.time()

        while self.running:
            elapsed = time.time() - start_time
            if elapsed >= self.duration:
                break

            line = _read_line_with_timeout(ser, timeout_s=0.1)
            if line:
                if line.startswith("PUNCH_DETECTED:"):
                    try:
                        count = int(line.split(":", 1)[1])
                        if count > current_punch_count:
                            for _ in range(count - current_punch_count):
                                punch_times.append(elapsed)
                        current_punch_count = count
                    except Exception:
                        pass
                elif line.startswith("ERROR:"):
                    print(f"[STAMINA PROTOCOL] {line}")

            current_rate = self._calculate_current_rate_from_times(punch_times, elapsed)
            progress_callback(int(elapsed), current_punch_count, current_rate)

        _send_command(ser, "STOP")
        final_count = self._wait_for_stamina_result(ser, timeout_s=2.0)
        if final_count is None:
            final_count = current_punch_count

        if final_count > len(punch_times):
            punch_times.extend([float(self.duration)] * (final_count - len(punch_times)))

        result_callback(self._build_results(final_count, punch_times, self.duration))

    def _measure_stamina_streaming(
        self,
        ser,
        progress_callback: Callable[[int, int, float], None],
        result_callback: Callable[[Dict[str, float | int]], None],
    ):
        self.running = True
        self.punch_count = 0
        self.punch_times = []
        start_time = time.time()
        last_punch_time = 0.0

        while self.running:
            elapsed = time.time() - start_time
            if elapsed >= self.duration:
                break

            if ser.in_waiting:
                raw = ser.readline().decode("utf-8", errors="ignore").strip()
                if "Total_Accel:" in raw:
                    for part in raw.split(","):
                        if "Total_Accel:" not in part:
                            continue
                        try:
                            accel_ms2 = float(part.split(":", 1)[1])
                        except Exception:
                            continue

                        if accel_ms2 > 80.0 and (elapsed - last_punch_time) > 0.2:
                            self.punch_count += 1
                            self.punch_times.append(elapsed)
                            last_punch_time = elapsed

            current_rate = self._calculate_current_rate(elapsed)
            progress_callback(int(elapsed), self.punch_count, current_rate)
            time.sleep(0.05)

        result_callback(self._calculate_results())

    def _wait_for_stamina_result(self, ser, timeout_s: float) -> int | None:
        deadline = time.time() + timeout_s
        while time.time() < deadline:
            response = _read_line_with_timeout(ser, timeout_s=0.2)
            if not response:
                continue
            if response.startswith("RESULT:PUNCHES:"):
                try:
                    return int(response.split(":", 2)[2])
                except Exception:
                    return None
            if response.startswith("ERROR:"):
                print(f"[STAMINA PROTOCOL] {response}")
                return None
        return None

    def _calculate_current_rate_from_times(self, punch_times: List[float], elapsed: float) -> float:
        if elapsed <= 0:
            return 0.0

        if elapsed < 10.0:
            window_start = 0.0
        else:
            window_start = elapsed - 10.0

        recent_punches = [timestamp for timestamp in punch_times if timestamp >= window_start]
        window_duration = min(10.0, elapsed)
        if window_duration <= 0:
            return 0.0

        return (len(recent_punches) / window_duration) * 60.0

    def _build_results(self, total_punches: int, punch_times: List[float], duration: int) -> Dict[str, float | int]:
        self.punch_count = total_punches
        self.punch_times = list(punch_times)
        self.duration = duration
        return self._calculate_results()

    def _measure_simulated(
        self,
        progress_callback: Callable[[int, int, float], None],
        result_callback: Callable[[Dict[str, float | int]], None],
    ):
        self.running = True
        self.punch_count = 0
        self.punch_times = []
        start_time = time.time()

        base_rate = random.uniform(60, 90)
        fatigue_factor = random.uniform(0.7, 0.9)
        last_punch_time = 0.0

        while self.running:
            elapsed = time.time() - start_time
            if elapsed >= self.duration:
                break

            progress_ratio = min(1.0, elapsed / self.duration)
            current_rate = base_rate * (1 - (progress_ratio * (1 - fatigue_factor)))
            time_between_punches = 60.0 / max(current_rate, 1.0)

            if elapsed - last_punch_time >= time_between_punches:
                if random.random() > 0.1:
                    self.punch_count += 1
                    self.punch_times.append(elapsed)
                    last_punch_time = elapsed

            current_rate_display = self._calculate_current_rate(elapsed)
            progress_callback(int(elapsed), self.punch_count, current_rate_display)
            time.sleep(0.1)

        result_callback(self._calculate_results())

    def _calculate_current_rate(self, elapsed: float) -> float:
        if elapsed <= 0:
            return 0.0
        return (self.punch_count / elapsed) * 60.0

    def _window_rate(self, start_s: float, end_s: float) -> float:
        punches_in_window = sum(1 for timestamp in self.punch_times if start_s <= timestamp <= end_s)
        duration_min = max((end_s - start_s) / 60.0, 1e-6)
        return punches_in_window / duration_min

    def _calculate_results(self) -> Dict[str, float | int]:
        average_rate = (self.punch_count / max(self.duration, 1)) * 60.0
        first_30_rate = self._window_rate(0.0, min(30.0, float(self.duration)))
        last_30_start = max(0.0, float(self.duration) - 30.0)
        last_30_rate = self._window_rate(last_30_start, float(self.duration))

        fatigue_percentage = 0.0
        if first_30_rate > 0:
            fatigue_percentage = max(0.0, ((first_30_rate - last_30_rate) / first_30_rate) * 100.0)

        rate_component = min(70.0, (average_rate / 120.0) * 70.0)
        fatigue_component = max(0.0, 30.0 - (fatigue_percentage * 0.75))
        stamina_score = int(round(min(100.0, rate_component + fatigue_component)))

        result = StaminaResult(
            total_punches=self.punch_count,
            average_rate=round(average_rate, 2),
            first_30_rate=round(first_30_rate, 2),
            last_30_rate=round(last_30_rate, 2),
            stamina_score=stamina_score,
            fatigue_percentage=round(fatigue_percentage, 2),
            duration=self.duration,
        )
        return result.to_dict()
