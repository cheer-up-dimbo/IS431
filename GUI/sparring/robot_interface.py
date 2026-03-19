"""
Placeholder serial communication interface for the boxing robot.

This module provides functions to send signals to the robot. Currently, all functions
are placeholders that print to the console. In the real implementation, these functions
will use a serial communication library (e.g., `pyserial`) to send signals to the robot.

To implement real serial communication:
- Use the `pyserial` library.
- Configure the serial port (e.g., `COM3` on Windows, `/dev/ttyUSB0` on Linux).
- Define the signal format (e.g., ASCII strings, binary data).
- Replace the `print` statements with `serial.write` or equivalent.
"""

_speed: str = "medium"


def set_speed(speed: str) -> None:
    """Set the robot arm speed. Valid values: 'slow', 'medium', 'fast'."""
    global _speed
    _speed = speed
    print(f"[ROBOT] Speed: {speed}")


def get_intra_gap() -> float:
    """Return intra-combo gap (seconds between punches within a combo)."""
    if _speed == "slow":
        return 0.8
    if _speed == "fast":
        return 0.3
    return 0.5  # medium (default)


def get_inter_gap() -> float:
    """Return inter-combo gap (seconds between combos)."""
    if _speed == "slow":
        return 2.0
    if _speed == "fast":
        return 1.0
    return 1.5  # medium (default)


def send_punch(punch: str) -> None:
    """
    Sends a single punch signal to the robot.

    Args:
        punch: A string representing the punch (e.g., "1", "2", "3b").

    Placeholder implementation: prints the punch to the console.
    """
    print(f"[ROBOT] Punch: {punch}")

def send_round_start() -> None:
    """
    Signals the robot that a round has begun.

    Placeholder implementation: prints a round start message to the console.
    """
    print("[ROBOT] Round started")

def send_round_stop() -> None:
    """
    Signals the robot that a round has ended.

    Placeholder implementation: prints a round stop message to the console.
    """
    print("[ROBOT] Round stopped")