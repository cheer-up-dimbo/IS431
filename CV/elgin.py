import serial
import time
import collections
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# --- CONFIGURATION ---
SERIAL_PORT = 'COM10'  # Change this to your Arduino port (e.g., /dev/ttyACM0 on Mac/Linux)
BAUD_RATE = 115200
WINDOW_SIZE = 100     # Number of data points to show on graph
PUNCH_THRESHOLD = 35.0 # m/s^2

# Setup data buffers
data_x = collections.deque(maxlen=WINDOW_SIZE)
data_y = collections.deque([0.0] * WINDOW_SIZE, maxlen=WINDOW_SIZE)

# Initialize serial
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
    time.sleep(2) # Wait for Arduino reset
except Exception as e:
    print(f"Error connecting to serial: {e}")
    exit()

# Setup Plot
fig, ax = plt.subplots(figsize=(10, 6))
line, = ax.plot(np.arange(WINDOW_SIZE), data_y, color='#00ff00', linewidth=2)
ax.set_ylim(0, 160) # 16G is roughly 157 m/s^2
ax.set_title("Punch Impact Monitor", fontsize=16)
ax.set_ylabel("Force (m/s²)")
ax.grid(True, alpha=0.3)

# Text elements
peak_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=12, fontweight='bold')
punch_alert = ax.text(0.5, 0.5, '', transform=ax.transAxes, fontsize=50, 
                      color='red', ha='center', va='center', fontweight='black')

session_peak = 0.0
last_punch_time = 0

def update(frame):
    global session_peak, last_punch_time
    
    while ser.in_waiting:
        line_data = ser.readline().decode('utf-8', errors='ignore').strip()
        
        # Parse "Total_Accel:XX.XX" from your Arduino output
        if "Total_Accel:" in line_data:
            try:
                # Extract numerical value
                parts = line_data.split(',')
                for p in parts:
                    if "Total_Accel:" in p:
                        val = float(p.split(':')[1])
                        data_y.append(val)
                        
                        # Update Peak
                        if val > session_peak:
                            session_peak = val
                        
                        # Trigger Punch Visual
                        if val > PUNCH_THRESHOLD:
                            last_punch_time = time.time()
                            punch_alert.set_text("PUNCH!")
            except:
                continue

    # Update the graph line
    line.set_ydata(data_y)
    
    # Update peak label
    peak_text.set_text(f"Session Peak: {session_peak:.2f} m/s²")
    
    # Handle Fading Indicator
    elapsed = time.time() - last_punch_time
    if elapsed > 2.0: # Remove text after 2 seconds
        punch_alert.set_text("")
    elif elapsed > 0.5: # Start fading opacity (simulated by alpha)
        punch_alert.set_alpha(max(0, 1 - (elapsed - 0.5)))
    else:
        punch_alert.set_alpha(1.0)

    return line, peak_text, punch_alert

# Animation
ani = animation.FuncAnimation(fig, update, interval=20, blit=True, cache_frame_data=False)
plt.show()
ser.close()