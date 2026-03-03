import os

# Read the current README.md
readme_path = r"c:\Users\zakir\OneDrive - National University of Singapore\Desktop\NUS Semesters\Y4S1\CDE4301\IS431\GUI\README.md"

with open(readme_path, 'r', encoding='utf-8') as f:
    original_content = f.read()

# Append the integration guide
integration_guide = """

---

# BoxBunny GUI — Integration Guide

This guide covers how to integrate the placeholder systems in the GUI with real hardware and software, and how to import the entire GUI into a larger project.

---

## Table of Contents
1. [CV Integration](#1-cv-integration)
2. [Robot Arms Integration](#2-robot-arms-integration)
3. [Arduino Integration](#3-arduino-integration-performance-pages)
4. [Improving AI Chat](#4-improving-the-ai-chat-experience)
5. [Importing the GUI into Another Project](#5-importing-the-gui-into-another-project)

---

## 1. CV Integration

The CV system integrates with the GUI through a file-based handshake. The GUI writes a trigger file when a sparring session ends, the CV pipeline reads it, processes the video, and writes an output file that the GUI polls for.

### 1.1 What the GUI sends to CV

When a sparring session completes its final round, the GUI writes:

**Path:** `GUI/users/<username>/spar_trigger.json`

**Format:**
```json
{
  "username": "zakir",
  "session_id": null,
  "timestamp": "2025-03-01T14:32:00.123456"
}
```

The CV should watch for this file, begin processing the most recent recording when found, and use `username` to know where to write output.

### 1.2 What CV needs to output to the GUI

**Path:** `GUI/users/<username>/spar_cv_output.txt`

**Format:** Comma-separated punch labels in chronological order:
```
jab,cross,jab,lead_hook,cross,rear_hook,jab,jab,cross
```

**Accepted labels:** `jab`, `cross`, `lead_hook`, `rear_hook`, `lead_upper`, `rear_upper`

**Aliases auto-mapped by GUI:** `hook` → `lead_hook`, `uppercut` → `lead_upper`

Write the file only after processing is complete. The GUI reads it the moment it appears.

### 1.3 Timing

1. GUI writes `spar_trigger.json` → CV begins processing
2. CV finishes → CV writes `spar_cv_output.txt`
3. GUI detects file → reads → deletes both files → updates weakness profile

The GUI has a **120 second timeout** before skipping analysis.

### 1.4 CV Toggle

Go to **Others → CV: On/Off** to toggle CV processing. When disabled, the GUI skips polling entirely and proceeds with empty data after 1 second. This allows the GUI to run without CV hardware.

### 1.5 Copilot Prompts for CV Integration

**Update label parser:**
> "In `sparring/sparring_database.py`, update `_parse_cv_output` to handle these additional label aliases from our CV system: [list labels]. Map each to the canonical label (jab, cross, lead_hook, rear_hook, lead_upper, rear_upper)."

**Add timing data support:**
> "Update `spar_cv_output.txt` format to include timestamps per punch like `jab:0.1,cross:0.4`. Update `_parse_cv_output` in `sparring_database.py` to parse timestamps and extract opener patterns (first punch after a gap > 1.0 second)."

**Replace file polling with direct CV call:**
> "In `sparring/spar_pages.py`, in `SparProcessingPage._poll`, replace the file polling logic with a direct call to `[your CV module].process_session(username, trigger_data)` that returns the cv_raw string directly. Keep the timeout and skip logic unchanged."

---

## 2. Robot Arms Integration

### 2.1 Signals the Arms Receive

All signals are sent from `sparring/robot_interface.py`:

| Function | When Called | Current Behaviour |
|----------|-------------|-------------------|
| `send_round_start()` | Round begins | Prints `[ROBOT] Round started` |
| `send_punch(punch)` | Each punch | Prints `[ROBOT] Punch: <code>` |
| `send_round_stop()` | Round ends | Prints `[ROBOT] Round stopped` |

**Punch codes:**

| Code | Punch | Code | Punch |
|------|-------|------|-------|
| `"1"` | Jab | `"2"` | Cross |
| `"3"` | Lead hook | `"4"` | Rear hook |
| `"5"` | Lead uppercut | `"6"` | Rear uppercut |
| `"3b"` | Lead hook to body | `"2b"` | Cross to body |

**Timing constants in `robot_interface.py`:**
```python
INTRA_COMBO_GAP_S = 0.3   # between punches within a combo
INTER_COMBO_GAP_S = 1.0   # between combos
```

### 2.2 Replacing the Placeholder

Open `sparring/robot_interface.py`. The comment block at the top explains what to replace. Steps:

1. Install pyserial: `pip install pyserial`
2. Set your port (e.g. `/dev/ttyUSB0` on Jetson Nano)
3. Replace `print` statements with `serial.write()` calls

Example:
```python
import serial
_port = serial.Serial('/dev/ttyUSB0', 9600)

def send_punch(punch: str) -> None:
    _port.write(f"PUNCH:{punch}\\n".encode())
```

### 2.3 Copilot Prompts for Arms Integration

**Replace with pyserial:**
> "In `sparring/robot_interface.py`, replace the placeholder print statements with real pyserial communication. Port is `/dev/ttyUSB0`, baud rate is [your baud rate], signal format is [your format]. Keep function signatures unchanged."

**Add connection management:**
> "In `sparring/robot_interface.py`, add `connect()` and `disconnect()` functions. Add error handling so if the port is unavailable, all send functions fail silently with a warning."

**Wire speed parameter:**
> "In `sparring/robot_interface.py`, replace `INTRA_COMBO_GAP_S` and `INTER_COMBO_GAP_S` with a `set_speed(speed_percent: int)` function. At 100% speed: 0.3s intra, 1.0s inter. Scale linearly to 0.6s and 2.0s at 0%."

---

## 3. Arduino Integration (Performance Pages)

The Power, Stamina, and Reaction Time pages navigate to their test pages but hardware measurement logic is placeholder.

### 3.1 How Arduino Currently Connects

Managed through **Others page** — select port from dropdown, press Apply. Port is saved to `.env` and persisted. The `ArduinoButtonListener` background thread handles button events (up/down/enter) for keyboard navigation.

### 3.2 Copilot Prompt for Performance Page Integration

**Wire Arduino sensor data:**
> "In `main_gui.py`, in `PowerPunchPage`, replace placeholder measurement logic with real Arduino serial reads. The Arduino sends force data as `FORCE:<value>\\n`. Read this in a QThread worker following the same pattern as `ReactionTestPage`, emit the value via a signal, and display it. Use the existing port from `os.getenv('ARDUINO_BUTTON_PORT')`."

---

## 4. Improving the AI Chat Experience

The AI Chat toggle (Others → AI Chat: On/Off) switches result pages from `🥊 Feedback:` to `🤖 Coach Feedback:` prefix. To make this real AI coaching:

### 4.1 Copilot Prompt for Real AI Feedback

> "In `sparring/spar_pages.py`, in `SparResultPage.set_results`, when `ai_chat_enabled` is True, replace the hardcoded feedback string with a call to the Anthropic API. Send punch counts, most common punch, total punches, and style fought as context. System prompt: 'You are a boxing coach giving brief encouraging feedback after a sparring session. Keep it under 3 sentences.' Use the existing `combo_llm_chat_page` API call pattern."

---

## 5. Importing the GUI into Another Project

### 5.1 Folder Structure to Copy

Copy the entire `GUI/` folder as-is. Structure must be preserved:
```
GUI/
├── main_gui.py
├── core/
│   ├── config.py
│   ├── constants.py
│   └── navigation.py
├── sparring/
│   ├── __init__.py
│   ├── combo_pools.py
│   ├── sequence_generator.py
│   ├── robot_interface.py
│   ├── sparring_database.py
│   └── spar_pages.py
├── combo_curriculum/
├── users/
├── .env
└── requirements.txt
```

### 5.2 Install Dependencies
```bash
pip install PySide6 pyserial anthropic --break-system-packages
```

On Jetson Nano, also run:
```bash
export DISPLAY=:0
```

### 5.3 Running the GUI from Another Project
```python
import subprocess, sys, os

gui_path = os.path.join(os.path.dirname(__file__), 'GUI')
subprocess.Popen([sys.executable, 'main_gui.py'], cwd=gui_path)
```

### 5.4 File-Based Communication Interface

The GUI communicates with external systems through `GUI/users/<username>/`:

| File | Direction | Purpose |
|------|-----------|---------|
| `spar_trigger.json` | GUI → External | Session ended, CV should process |
| `spar_cv_output.txt` | External → GUI | CV punch detection results |
| `performance_history.db` | GUI internal | All user performance and sparring data |

### 5.5 Copilot Prompt for Wiring Integration Project to GUI

> "Create a `cv_watcher.py` module with a `start_watching(users_dir: str)` function that runs a background thread polling all subdirectories of `users_dir` every second for new `spar_trigger.json` files. When found, call our CV pipeline and write results to `spar_cv_output.txt` in the same directory."
"""

# Write the combined content
with open(readme_path, 'w', encoding='utf-8') as f:
    f.write(original_content)
    f.write(integration_guide)

print("✓ Integration guide successfully appended to README.md")
