import serial
from datetime import datetime
import time

PORT = "COM4"      # adjust
BAUD = 115200
OUTFILE = "punch_log.csv"

with serial.Serial(PORT, BAUD, timeout=1) as ser, open(OUTFILE, "w", newline="") as f:
    time.sleep(0.5)  # wait for device to settle
    ser.reset_input_buffer()  # clear any stale data

    # Listen for the firmware prompt and answer Y
    prompt = ser.readline().decode(errors="ignore").strip()
    if prompt:
        print(prompt)
    ser.write(b"Y\n")  # auto-confirm logging; remove if you want to type manually

    # Read header from device, add date/time columns
    header = ser.readline().decode(errors="ignore").strip()
    if header:
        f.write("date,time," + header + "\n")

    while True:
        line = ser.readline().decode(errors="ignore").strip()
        if line:
            now = datetime.now()
            f.write(f"{now.date()},{now.strftime('%H:%M:%S')},{line}\n")
            f.flush()
