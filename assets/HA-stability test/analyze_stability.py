import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.signal import butter, filtfilt, find_peaks

# Configuration
FILES = [
    "IMU_Data_1776246174280_base.csv",
    "IMU_Data_1776247701045_circular.csv",
    "IMU_Data_1776248084423_steel tube.csv",
    "IMU_Data_1776248507888_top steel tube.csv"
]
LABELS = ["Level 1: Base (15.2cm)", "Level 2: Circular Plate (20.8cm)", 
          "Level 3: Bottom Tube (46.0cm)", "Level 4: Top Tube (106.0cm)"]

def butter_lowpass_filter(data, cutoff, fs, order=4):
    """Applies a low-pass filter to remove high-frequency electrical noise."""
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return filtfilt(b, a, data)

plt.figure(figsize=(15, 10))

script_dir = os.path.dirname(os.path.abspath(__file__))

for i, (file, label) in enumerate(zip(FILES, LABELS)):
    try:
        # Load data
        file_path = os.path.join(script_dir, file)
        df = pd.read_csv(file_path)
        
        # Calculate time vector (assuming ms timestamps)
        if 'time_ms' in df.columns:
            t = (df['time_ms'] - df['time_ms'].iloc[0]) / 1000.0 
        else:
            t = np.linspace(0, len(df)/100.0, len(df)) # Fallback assumption 100Hz
            
        fs = 1.0 / np.mean(np.diff(t)) # Calculate actual sampling frequency
        
        # 1. Calculate L2 Norm Magnitude (Vibration/Shock)
        # Removes 1g gravity baseline to show pure dynamic impact
        accel_mag = np.sqrt(df['ax']**2 + df['ay']**2 + df['az']**2)
        accel_mag_filtered = butter_lowpass_filter(accel_mag, cutoff=15.0, fs=fs)
        dynamic_shock = accel_mag_filtered - np.mean(accel_mag_filtered[:100]) # Zero the baseline
        
        # 2. Calculate Sway (Tilt Angle in degrees) using Low-Passed Accel Vectors
        # High-frequency is punch shock; low-frequency is the structural sway/tilt
        ax_lp = butter_lowpass_filter(df['ax'], cutoff=0.5, fs=fs)
        ay_lp = butter_lowpass_filter(df['ay'], cutoff=0.5, fs=fs)
        az_lp = butter_lowpass_filter(df['az'], cutoff=0.5, fs=fs)
        
        # Absolute tilt from baseline gravity vector (immune to IMU mounting orientation)
        g_vec = np.array([np.mean(ax_lp[:100]), np.mean(ay_lp[:100]), np.mean(az_lp[:100])])
        g_vec = g_vec / np.linalg.norm(g_vec)
        
        accel_vecs = np.column_stack((ax_lp, ay_lp, az_lp))
        norms = np.linalg.norm(accel_vecs, axis=1, keepdims=True)
        accel_vecs_normalized = accel_vecs / np.where(norms == 0, 1, norms)
        
        dot_products = np.clip(np.sum(accel_vecs_normalized * g_vec, axis=1), -1.0, 1.0)
        sway_angle = np.degrees(np.arccos(dot_products))
        
        # Plot Dynamic Shock (Vibration)
        plt.subplot(2, 2, 1)
        plt.plot(t, dynamic_shock, label=label, alpha=0.8)
        plt.title("Impact Vibration (Acceleration L2 Norm)")
        plt.ylabel("Acceleration (g)")
        plt.xlabel("Time (s)")
        plt.legend()
        
        # Plot Sway (Tilt Angle)
        plt.subplot(2, 2, 2)
        plt.plot(t, sway_angle, label=label, alpha=0.8)
        plt.title("Structural Sway (Angular Deflection)")
        plt.ylabel("Sway Angle (Degrees)")
        plt.xlabel("Time (s)")
        plt.legend()

    except Exception as e:
        print(f"Could not process {file}: {e}")

plt.tight_layout()
plt.show()
