#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
import threading
import time
import json
import math
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class ArmNode(Node):
    def __init__(self):
        super().__init__('arm_gui_node_v2')
        self.pub_cmd = self.create_publisher(Float64MultiArray, 'motor_commands', 10)
        self.create_subscription(Float64MultiArray, 'motor_feedback', self.feedback_callback, 10)
        
        self.actual_p1 = 0.0
        self.actual_p2 = 0.0
        self.target_p1 = 0.0
        self.target_p2 = 0.0
        self.target_speed = 5.0
        self.motor_enabled = False
        self.rx_count = 0
        self.last_msg_time = 0
        
        self.running = True
        self.thread = threading.Thread(target=self.heartbeat_loop, daemon=True)
        self.thread.start()

    def feedback_callback(self, msg):
        self.last_msg_time = time.time()
        if len(msg.data) >= 2:
            self.actual_p1 = msg.data[0]
            self.actual_p2 = msg.data[1]
            self.rx_count = int(msg.data[2]) if len(msg.data) > 2 else 0

    def heartbeat_loop(self):
        while self.running and rclpy.ok():
            msg = Float64MultiArray()
            msg.data = [
                float(self.target_p1), float(self.target_p2), 
                float(self.target_speed), float(self.target_speed),
                1.0 if self.motor_enabled else 0.0
            ]
            self.pub_cmd.publish(msg)
            time.sleep(0.1) # 10Hz Heartbeat

    def set_targets(self, p1, p2, speed=None):
        self.target_p1 = p1
        self.target_p2 = p2
        if speed: self.target_speed = speed

    def shutdown(self):
        self.running = False
        self.thread.join()

class App:
    def __init__(self, root, node):
        self.root = root
        self.node = node
        self.root.title("Damiao Arm Controller (Pos-Speed Mode)")
        self.root.geometry("600x800") # Increased height
        self.sequence = [] 
        self.setup_ui()
        self.update_gui_loop()

    def setup_ui(self):
        # 1. System Status
        status_frame = ttk.LabelFrame(self.root, text="System Status", padding=10)
        status_frame.pack(fill="x", padx=10, pady=5)
        self.lbl_conn = ttk.Label(status_frame, text="DISCONNECTED", foreground="red", font=("Arial", 10, "bold"))
        self.lbl_conn.pack(side="left")
        self.lbl_rx = ttk.Label(status_frame, text="RX: 0")
        self.lbl_rx.pack(side="right")

        # 2. Manual Control
        ctrl_frame = ttk.LabelFrame(self.root, text="Manual Control", padding=10)
        ctrl_frame.pack(fill="x", padx=10, pady=5)
        
        btn_frame = ttk.Frame(ctrl_frame)
        btn_frame.pack(fill="x", pady=5)
        self.btn_enable = ttk.Button(btn_frame, text="ENABLE (Stiff)", command=lambda: self.set_enabled(True))
        self.btn_enable.pack(side="left", expand=True, fill="x", padx=5)
        self.btn_disable = ttk.Button(btn_frame, text="DISABLE (Coast)", command=lambda: self.set_enabled(False))
        self.btn_disable.pack(side="left", expand=True, fill="x", padx=5)

        self.lbl_pos = ttk.Label(ctrl_frame, text="Actual: M1=0.00 M2=0.00", font=("Courier", 12))
        self.lbl_pos.pack(pady=5)

        self.scale_m1 = tk.Scale(ctrl_frame, from_=-12.5, to=12.5, orient="horizontal", label="Motor 1", resolution=0.1)
        self.scale_m1.pack(fill="x")
        self.scale_m2 = tk.Scale(ctrl_frame, from_=-12.5, to=12.5, orient="horizontal", label="Motor 2", resolution=0.1)
        self.scale_m2.pack(fill="x")
        self.scale_speed = tk.Scale(ctrl_frame, from_=0.5, to=30.0, orient="horizontal", label="Speed (rad/s)", resolution=0.5)
        self.scale_speed.set(5.0)
        self.scale_speed.pack(fill="x")
        
        ttk.Button(ctrl_frame, text="Move to Sliders", command=self.send_sliders).pack(pady=10)

        # 3. Sequencer (Fixed Layout: Controls at bottom, List fills rest)
        seq_frame = ttk.LabelFrame(self.root, text="Sequencer", padding=10)
        seq_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # --- Bottom Controls (Packed FIRST with side='bottom') ---
        
        # Playback Controls
        play_frame = ttk.Frame(seq_frame)
        play_frame.pack(side="bottom", fill="x", pady=5)
        self.lbl_status = ttk.Label(play_frame, text="Ready", relief="sunken", anchor="center")
        self.lbl_status.pack(fill="x", pady=2)
        self.progress = ttk.Progressbar(play_frame, orient="horizontal", mode="determinate")
        self.progress.pack(fill="x", pady=2)
        self.btn_play = ttk.Button(play_frame, text="▶ PLAY SEQUENCE", command=self.play_sequence)
        self.btn_play.pack(fill="x", ipady=10)

        # IO Controls
        io_frame = ttk.Frame(seq_frame)
        io_frame.pack(side="bottom", fill="x", pady=5)
        ttk.Button(io_frame, text="Save", command=self.save_sequence).pack(side="left", fill="x", expand=True)
        ttk.Button(io_frame, text="Load", command=self.load_sequence).pack(side="left", fill="x", expand=True)

        # Editing Tools
        tool_frame = ttk.Frame(seq_frame)
        tool_frame.pack(side="bottom", fill="x", pady=5)
        ttk.Button(tool_frame, text="Record Point (Actual)", command=self.record_point).pack(side="left", padx=2, expand=True, fill="x")
        ttk.Button(tool_frame, text="Delete", command=self.delete_point).pack(side="left", padx=2)
        ttk.Button(tool_frame, text="Clear", command=self.clear_sequence).pack(side="left", padx=2)

        # Listbox (Packed LAST with expand=True)
        self.listbox = tk.Listbox(seq_frame, height=8)
        self.listbox.pack(side="top", fill="both", expand=True, padx=5, pady=5)

    def set_enabled(self, state):
        if state:
            self.node.set_targets(self.node.actual_p1, self.node.actual_p2)
            self.scale_m1.set(self.node.actual_p1)
            self.scale_m2.set(self.node.actual_p2)
        self.node.motor_enabled = state

    def send_sliders(self):
        self.node.set_targets(self.scale_m1.get(), self.scale_m2.get(), self.scale_speed.get())

    def record_point(self):
        self.sequence.append({
            "p1": self.node.actual_p1,
            "p2": self.node.actual_p2,
            "speed": self.scale_speed.get()
        })
        self.update_listbox()

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for i, s in enumerate(self.sequence):
            self.listbox.insert(tk.END, f"{i+1}: Pos({s['p1']:.2f}, {s['p2']:.2f}) Spd({s['speed']})")

    def delete_point(self):
        if self.listbox.curselection():
            del self.sequence[self.listbox.curselection()[0]]
            self.update_listbox()

    def clear_sequence(self):
        self.sequence = []
        self.update_listbox()

    def save_sequence(self):
        f = filedialog.asksaveasfilename(defaultextension=".json")
        if f:
            with open(f, 'w') as file: json.dump(self.sequence, file)

    def load_sequence(self):
        f = filedialog.askopenfilename()
        if f:
            with open(f, 'r') as file: self.sequence = json.load(file)
            self.update_listbox()

    def play_sequence(self):
        if not self.sequence:
            messagebox.showwarning("Empty Sequence", "Please record or load a sequence first!")
            return
        threading.Thread(target=self._play_logic, daemon=True).start()

    def _play_logic(self):
        self.btn_play.configure(state="disabled")
        self.set_enabled(True)
        self.lbl_status.configure(text="Moving to Start Position...", background="yellow")
        
        # Move to start
        start = self.sequence[0]
        self.node.set_targets(start['p1'], start['p2'], 2.0)
        if not self.wait_for_arrival(start['p1'], start['p2']):
             self.lbl_status.configure(text="Error: Could not reach start!", background="red")
             time.sleep(1)
             self.btn_play.configure(state="normal")
             return

        time.sleep(0.5)

        for i, step in enumerate(self.sequence):
            self.lbl_status.configure(text=f"Playing Step {i+1}/{len(self.sequence)}", background="#aaf")
            self.progress['value'] = ((i+1)/len(self.sequence))*100
            
            self.node.set_targets(step['p1'], step['p2'], step['speed'])
            
            # Wait until motors actually reach target
            if not self.wait_for_arrival(step['p1'], step['p2']):
                print(f"Warning: Step {i+1} timeout")
            
            time.sleep(0.1)

        self.lbl_status.configure(text="Sequence Complete", background="green")
        time.sleep(1.0)
        # Use a standard color name instead of Windows-specific "SystemButtonFace"
        self.lbl_status.configure(text="Ready", background="white")
        self.btn_play.configure(state="normal")
        self.progress['value'] = 0

    def wait_for_arrival(self, t1, t2):
        """Blocks until actual pos is close to target"""
        timeout = 8.0 
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            err1 = abs(self.node.actual_p1 - t1)
            err2 = abs(self.node.actual_p2 - t2)
            # Threshold 0.2 radians (~11 degrees)
            if err1 < 0.2 and err2 < 0.2:
                return True
            time.sleep(0.05)
        return False

    def update_gui_loop(self):
        if time.time() - self.node.last_msg_time < 1.0:
            self.lbl_conn.configure(text="CONNECTED", foreground="green")
        else:
            self.lbl_conn.configure(text="DISCONNECTED", foreground="red")
        
        self.lbl_rx.configure(text=f"RX: {self.node.rx_count}")
        self.lbl_pos.configure(text=f"Actual: M1={self.node.actual_p1:.2f}  M2={self.node.actual_p2:.2f}")
        self.root.after(100, self.update_gui_loop)

def main():
    rclpy.init()
    node = ArmNode()
    spin_thread = threading.Thread(target=rclpy.spin, args=(node,), daemon=True)
    spin_thread.start()
    
    root = tk.Tk()
    app = App(root, node)
    try:
        root.mainloop()
    finally:
        node.shutdown()
        rclpy.shutdown()
        spin_thread.join()

if __name__ == "__main__":
    main()