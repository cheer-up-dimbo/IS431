# Boxing Training GUI (PySide6)

A touchscreen-first boxing training interface built with PySide6 for the BoxBunny project.

This GUI integrates:
- combo curriculum training,
- performance testing (Power / Stamina / Reaction),
- per-user progress tracking,
- and hardware/CV integration points.

---

## What’s New (Current GUI)

The GUI has been updated with the following major changes:

1. **Automatic navigation stack**
   - Centralized navigation with `navigate_to()` / `navigate_back()`.
   - Back button behavior now follows real page history instead of hardcoded return pages.

2. **Per-user combo database**
   - Each user gets their own `combos.db` at:
     - `GUI/users/<username>/combos.db`
   - Database is initialized automatically on first use.

3. **Unified per-user performance history database**
   - Power, Stamina, and Reaction test results are stored in:
     - `GUI/users/<username>/performance_history.db`
   - Includes latest-vs-average summary helpers for trend display.

4. **Arduino multi-mode protocol with fallback**
   - Supports command-based modes (`MODE:POWER`, `MODE:STAMINA`, etc.).
   - Falls back to legacy streaming behavior if firmware does not support mode commands.

5. **Expanded user progress pages**
   - Added overview and detailed combo progress pages.
   - Progress and mastery are tracked with difficulty-aware thresholds.

6. **AI feedback plumbing (template-based now, LLM-ready path included)**
   - Feedback data formatting and combo-result pages are integrated.
   - `ComboLLMChatPage` exists behind app state configuration.

---

## Key Features

### User & Session Management
- Login/Signup with SHA-256 password hashing.
- User records in `GUI/users.csv`.
- User management page for viewing/deleting accounts.

### Combo Curriculum Training
- 50 combos total:
  - 15 Beginner
  - 20 Intermediate
  - 15 Advanced
- Group-based progression by difficulty.
- Mastery based on average recent performance and attempts.
- Self-select sequence mode and spar/battle entry flows.

### Performance Testing
- **Power**: serial-based punch power workflow.
- **Stamina**: timed punch endurance workflow (Arduino + simulation path).
- **Reaction**: camera + YOLO pose-based reaction timing.
- Consolidated performance history page with per-test filtering and trends.

### Self-Select Sequence with Unified Button Navigation
- Custom punch sequence creation interface with 5-sequence management.
- All input buttons (numpad 1-6, defense moves, backspace, confirm, back, next) support:
  - **Unified styling** with standardized focus highlighting (green border).
  - **Keyboard focus** support for seamless navigation via up/down keys.
  - **Arduino physical button integration** enabling up/down/enter cycling without touching the screen.
  - **Flexible sizing** that adapts to grid layout constraints while maintaining visual consistency.
- Manages up to 9 moves per sequence; supports editing and reordering via sequence list controls.
- Full integration with combo training workflow for custom difficulty progression.

### UI / Architecture
- Single `QStackedWidget` app with indexed pages.
- Shared `AppState` (`core/config.py`) for training/session configuration.
- Shared page constants in `core/constants.py`.

---

## Project Structure

```text
GUI/
├── main_gui.py
├── README.md
├── users.csv
├── performance_database.py
├── placeholders.py
│
├── core/
│   ├── __init__.py
│   ├── config.py
│   └── constants.py
│
├── utils/
│   ├── __init__.py
│   └── user_management.py
│
├── combo_curriculum/
│   ├── __init__.py
│   ├── curriculum.py
│   ├── action_recognition_placeholder.py
│   ├── docs/
│   ├── examples/
│   └── tests/
│
├── power/
│   └── power_runner.py
├── stamina/
│   └── stamina_runner.py
├── reaction_time/
│   └── reaction_time_runner.py
│
├── setup/
│   ├── setup_combo_database.py
│   ├── create_database_schema.py
│   ├── populate_combos.py
│   └── combos.db
│
├── users/
├── training_history/
└── training_history_archive/
```

---

## Prerequisites

- Python 3.9+
- Windows/Linux with camera access (for reaction test)
- Optional Arduino + sensor setup (for hardware power/stamina path)

Python packages used by the GUI include:
- `PySide6`
- `opencv-python`
- `numpy`
- `ultralytics`
- `pyserial`

> Note: There is currently no dedicated `requirements.txt` in `GUI/`. Install the packages manually in your environment.

---

## Setup

From the repository root:

```bash
cd GUI
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install PySide6 opencv-python numpy ultralytics pyserial
```

### Database setup

`main_gui.py` auto-runs combo DB setup when needed. You can also run it manually:

```bash
python setup/setup_combo_database.py --db-path data/combos.db --force
```

---

## Run

```bash
cd GUI
python main_gui.py
```

---

## Data Storage

### User accounts
- `GUI/users.csv`

### Combo training DB
- Shared template DB: `GUI/data/combos.db`
- Per-user DBs (auto-created): `GUI/users/<username>/combos.db`

### Performance history DB
- Per-user DB (auto-created): `GUI/users/<username>/performance_history.db`
- Tables:
  - `power_tests`
  - `stamina_tests`
  - `reaction_tests`

### Training CSV logs
- `GUI/training_history/training_<username>.csv`

---

## Hardware / CV Notes

### Arduino protocol behavior
- GUI first probes command-based protocol support.
- If available, it uses explicit mode commands and structured responses.
- If unavailable, it falls back to legacy streaming mode.

### Arduino physical-button navigation (new)
- Upload sketch: `GUI/arduino/button_navigation/button_navigation.ino`
- Wiring: buttons on pins `2` (UP), `4` (ENTER), `7` (DOWN) using `INPUT_PULLUP` to GND.
- Arduino sends serial commands at `115200`: `BTN1_PRESS`, `BTN2_PRESS`, `BTN3_PRESS`.
- Python listener in `main_gui.py` runs in background thread and maps to Up/Down/Enter navigation.
- Optional config via `.env` (copy from `GUI/.env.example`):
   - `ARDUINO_BUTTONS_ENABLED=true|false`
   - `ARDUINO_BUTTON_PORT=COM3` (recommended on Windows)
   - `ARDUINO_BUTTON_BAUD=115200`
   - `ARDUINO_BUTTON_DEBOUNCE_MS=120`
   - `ARDUINO_BUTTON_TIMEOUT_SEC=0.05`
   - `ARDUINO_BUTTON_STARTUP_DELAY_SEC=1.2`
   - `ARDUINO_BUTTON_RECONNECT_SEC=2.0`
   - `ARDUINO_BUTTONS_SUSPEND_DURING_TESTS=true`
   - `ARDUINO_BUTTON_WATCHDOG_MS=5000`
- You can also set COM port directly in app: `Others` → dropdown (`Auto Detect` or COMx) → `Apply Arduino Port`.
- The dropdown refreshes each time `Others` opens, so newly plugged USB serial devices appear without restarting the app.
- If exactly one Arduino-like serial device is detected and no fixed port is configured, the app auto-applies that port.
- Button listener is temporarily suspended on serial-heavy Power/Stamina test pages to avoid COM-port contention, then resumed automatically.
- `Others` page shows live listener state (`connected`, `starting`, `reconnecting`, `suspended`, `disabled`).
- A watchdog auto-restarts the listener thread if it stops unexpectedly.

### Reaction-time model path
- Expected YOLO model file:
  - `models/yolo11s-pose.pt` (repo root `models/` folder)

---

## Main Pages (High-Level)

The app includes pages for:
- Login, Home, Training, Techniques
- Parameter selection (round/time/rest/speed)
- Countdown + Training Session
- Self-select sequences, Spar, Battle
- Power/Stamina/Reaction test flows and result pages
- Performance history
- User management, user combo progress, user progress overview
- Combo results + LLM chat page scaffold

---

## GUI Architecture & Developer Guide

This section explains how the GUI is built so a new developer can understand, modify, or extend it without prior knowledge of the codebase.

### Framework

The app uses **PySide6** (the official Python binding for Qt 6). All widgets, layouts, signals, and event handling come from PySide6:

```python
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                               QLabel, QStackedWidget, QHBoxLayout, QLineEdit)
from PySide6.QtCore import Qt, QTimer
```

### Main Window & Page System

The entire app lives inside a single `MainWindow(QWidget)` that holds one `QStackedWidget`. Each screen the user sees is a separate `QWidget` added to the stack. The visible page is controlled by its integer index:

```python
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Boxing Training App")
        self.setFixedSize(1024, 600)         # Fixed for 7-inch touchscreen

        self.stacked_widget = QStackedWidget()
        self.app_state = AppState()          # Shared config object

        # Create page instances — each receives stacked_widget so it can navigate
        self.homepage = Homepage(self.stacked_widget)
        self.training_page = TrainingPage(self.stacked_widget)
        # ... more pages ...

        # Register pages — order determines index (0, 1, 2, ...)
        self.stacked_widget.addWidget(self.homepage)         # index 0
        self.stacked_widget.addWidget(self.training_page)    # index 1
        # ... more addWidget calls ...
```

Page indices are defined as named constants in `core/constants.py` so you never use raw numbers:

```python
# core/constants.py
class PageIndex:
    HOMEPAGE = 0
    TRAINING = 1
    TECHNIQUES = 2
    PUNCH_COMBINATIONS = 3
    BASIC_PARAMETERS = 4
    # ... 40 pages total
```

### Creating a New Page

Every page is a class that inherits from both `ButtonNavigationMixin` and `QWidget`. The mixin provides standardized button styling, keyboard/Arduino navigation, and the `navigate_to()` helper:

```python
from core.navigation import ButtonNavigationMixin
from core import PageIndex, ButtonStyle

class MyNewPage(ButtonNavigationMixin, QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget    # Required for navigation

        # 1. Create a layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        # 2. Create widgets
        title = QLabel("My Page Title")
        title.setStyleSheet("font-size: 30px; font-weight: bold;")

        action_btn = QPushButton("Do Something")
        back_btn = QPushButton("Back")

        # 3. Style buttons with centralized ButtonStyle constants
        action_btn.setStyleSheet(ButtonStyle.PRIMARY_MEDIUM)   # Green
        back_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)        # Red

        # 4. Wire button clicks to handler methods
        action_btn.clicked.connect(self.on_action_clicked)
        back_btn.clicked.connect(self.on_back_clicked)

        # 5. Add widgets to layout
        layout.addWidget(title)
        layout.addWidget(action_btn, alignment=Qt.AlignCenter)
        layout.addWidget(back_btn, alignment=Qt.AlignCenter)
        self.setLayout(layout)

    def on_action_clicked(self):
        print("Action triggered")
        self.navigate_to(PageIndex.TRAINING)   # Switch to Training page

    def on_back_clicked(self):
        self.navigate_to(PageIndex.HOMEPAGE)   # Switch to Homepage
```

To register the new page, add it in `MainWindow.__init__`:

```python
# In MainWindow.__init__:
self.my_new_page = MyNewPage(self.stacked_widget)
self.stacked_widget.addWidget(self.my_new_page)   # Gets next available index

# Add matching constant in core/constants.py:
# MY_NEW_PAGE = 40
```

### Button Clicks & Callbacks

PySide6 uses Qt's **signal/slot** pattern. Every `QPushButton` has a `clicked` signal. You connect it to any Python callable:

```python
# Direct method reference
btn.clicked.connect(self.on_btn_clicked)

# Lambda for passing arguments
btn.clicked.connect(lambda: self.handle_choice("Option A"))

# Lambda with default arg (important inside loops to capture loop variable)
for i, label in enumerate(["Beginner", "Intermediate", "Advanced"]):
    btn = QPushButton(label)
    btn.clicked.connect(lambda checked, arg=label: self.on_difficulty_clicked(arg))
```

> **Important:** Inside a loop, always use `lambda checked, arg=val: ...` with a default argument. Without it, all lambdas would capture the final loop value.

### Navigation

Navigation between pages is handled by two mechanisms:

**1. Page-level `navigate_to()`** — provided by `ButtonNavigationMixin`. Each page calls `self.navigate_to(PageIndex.SOME_PAGE)` which delegates to `MainWindow.navigate_to()`:

```python
# Inside any page class:
def on_training_clicked(self):
    self.navigate_to(PageIndex.TRAINING)    # Switches the visible page
```

**2. `MainWindow.navigate_to()` and `navigate_back()`** — manages a navigation stack for proper back-button behavior:

```python
# In MainWindow:
def navigate_to(self, page_index: int):
    self.stacked_widget.setCurrentIndex(page_index)  # Show the target page

def navigate_back(self):
    if self.navigation_stack:
        previous = self.navigation_stack.pop()       # Pop last page from history
        self.stacked_widget.setCurrentIndex(previous)
    else:
        self.stacked_widget.setCurrentIndex(PageIndex.MAIN_MENU)
```

### Data Flow: AppState

Pages share data through a single `AppState` object (defined in `core/config.py`). It holds a `TrainingConfig` dataclass with all training parameters:

```python
# core/config.py
class AppState:
    def __init__(self):
        self.config = TrainingConfig()     # rounds, speed, time, difficulty, etc.
        self.previous_page = PageIndex.HOMEPAGE
        self.ai_chat_enabled = False

    def update_rounds(self, rounds):       # Setter methods for each parameter
        self.config.rounds = rounds

    def update_difficulty(self, difficulty):
        self.config.difficulty = difficulty

    def get_config(self):                  # Read current config
        return self.config
```

Pages receive `app_state` in their constructor and use it to read/write shared training parameters:

```python
class BasicParametersPage(ButtonNavigationMixin, QWidget):
    def __init__(self, stacked_widget, app_state=None):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.app_state = app_state      # Shared state object

    def on_round_selected(self, value):
        self.app_state.update_rounds(value)    # Write to shared state

    def start_training(self):
        config = self.app_state.get_config()   # Read from shared state
        print(f"Starting {config.rounds} rounds at {config.difficulty}")
```

### Layout & Styling

**Layouts** — Qt provides layout managers that arrange widgets automatically:

```python
# Vertical stack (most common for page content)
layout = QVBoxLayout()
layout.setAlignment(Qt.AlignCenter)
layout.setSpacing(20)                          # Pixels between widgets
layout.setContentsMargins(50, 50, 50, 50)      # Left, Top, Right, Bottom
layout.addWidget(some_button)
layout.addStretch()                            # Flexible space

# Horizontal row (for side-by-side buttons)
row = QHBoxLayout()
row.addWidget(back_btn)
row.addWidget(next_btn)
layout.addLayout(row)                          # Nest layouts

# Grid (for numpad-style grids)
grid = QGridLayout()
grid.addWidget(btn, row=0, col=0)              # Position by row/col
```

**Button Styling** — The `ButtonStyle` class in `core/constants.py` provides pre-built Qt stylesheets:

```python
# core/constants.py — available styles:
ButtonStyle.PRIMARY_LARGE    # Green, large (main actions like "Start")
ButtonStyle.PRIMARY_MEDIUM   # Green, medium
ButtonStyle.BACK_LARGE       # Red, large (back/cancel actions)
ButtonStyle.BACK_MEDIUM      # Red, medium
ButtonStyle.INFO_SMALL       # Blue (informational/secondary)
ButtonStyle.HOME_LARGE       # Green, homepage-sized

# Usage:
btn.setStyleSheet(ButtonStyle.PRIMARY_MEDIUM)
```

Custom inline styles use Qt's CSS subset:

```python
label.setStyleSheet("font-size: 28px; font-weight: bold; color: #333;")
btn.setStyleSheet("""
    QPushButton {
        font-size: 18px;
        background-color: #2196F3;
        color: white;
        border-radius: 8px;
    }
    QPushButton:hover { background-color: #1976D2; }
    QPushButton:focus {
        border: 6px solid #00ff00;          /* Green border for Arduino nav */
        background-color: #2d5016;
    }
""")
```

### Arduino Physical Button Navigation

The `ButtonNavigationMixin` provides a `setup_navigation()` method that registers buttons for keyboard and Arduino cycling. When the Arduino sends UP/DOWN/ENTER over serial, the focused button changes with a visible green glow effect:

```python
class MyPage(ButtonNavigationMixin, QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        btn_a = QPushButton("Option A")
        btn_b = QPushButton("Option B")
        back_btn = QPushButton("Back")

        # ... set styles and connect clicks ...

        self.setLayout(layout)

        # Register buttons for Arduino up/down/enter navigation
        self.setup_navigation([btn_a, btn_b, back_btn])
```

`setup_navigation()` does the following automatically:
- Sets `Qt.StrongFocus` on each button
- Applies the page's `NAV_BUTTON_STYLE` (or the default `BUTTON_STYLE`)
- Installs an event filter for Up/Down/Enter key handling
- Adds a green glow effect (`QGraphicsDropShadowEffect`) to the focused button
- Focuses the first button on page show

You can customize sizing per page with class-level constants:

```python
class MyPage(ButtonNavigationMixin, QWidget):
    NAV_BUTTON_MIN_WIDTH = 300       # Override default 360
    NAV_BUTTON_MAX_WIDTH = 500       # Override default 420
    NAV_BUTTON_MIN_HEIGHT = 50       # Override default 65
    NAV_BUTTON_AUTOSIZE = True       # Allow buttons to grow beyond max width
    NAV_BUTTON_STYLE = "..."         # Override default button stylesheet
```

### Accessing Other Pages at Runtime

Sometimes a page needs to update another page's state. Use the `stacked_widget` to get a reference by index:

```python
# Get a reference to another page widget by its PageIndex
basic_page = self.stacked_widget.widget(PageIndex.BASIC_PARAMETERS)
basic_page.update_button_displays()   # Call any method on it

# Get the MainWindow from any page
main_window = self.window()
if hasattr(main_window, 'get_current_user'):
    username = main_window.get_current_user()
```

### Per-User Data Storage

Each user gets an isolated data directory at `GUI/users/<username>/`:

```python
# Database files are created automatically per user:
# GUI/users/<username>/combos.db            — combo training progress
# GUI/users/<username>/performance_history.db — power/stamina/reaction results

# Access pattern (from performance_database.py):
from performance_database import PerformanceDB
db = PerformanceDB(username)
db.save_power_result(peak_g=4.2, avg_power=3.1, punch_count=12)
results = db.get_power_history(limit=10)
```

### Summary: Adding a Feature End-to-End

1. **Add a `PageIndex` constant** in `core/constants.py`
2. **Create the page class** inheriting `(ButtonNavigationMixin, QWidget)` in `main_gui.py`
3. **Build the UI** in `__init__`: create layout → create widgets → style them → connect signals → add to layout → call `setup_navigation()`
4. **Instantiate the page** in `MainWindow.__init__` and `addWidget()` it to the stacked widget
5. **Wire navigation** from existing pages using `self.navigate_to(PageIndex.MY_NEW_PAGE)`
6. **Share data** via `self.app_state` or by accessing other pages through `self.stacked_widget.widget(PageIndex.X)`

---

## Development Notes

- Navigation is centralized in `MainWindow` and driven by page indices.
- `AppState` carries mutable training config between pages.
- Combo scoring currently uses placeholder integration via `placeholders.py` / `combo_curriculum` helper functions.
- Existing combo curriculum tests are under:
  - `GUI/combo_curriculum/tests/`

---

## Troubleshooting

1. **Camera fails to initialize**
   - Check camera permissions and index.
   - Ensure no other app is locking the webcam.

2. **Reaction model not found**
   - Ensure `models/yolo11s-pose.pt` exists at repo root.

3. **Serial/Arduino issues**
   - Verify COM port and baud settings.
   - For physical-button nav, set `ARDUINO_BUTTON_PORT` in `GUI/.env` if auto-detect picks wrong port.
   - Check firmware compatibility (command-based mode support).
   - The app should fallback to streaming mode if needed.

4. **User data not appearing as expected**
   - Check `GUI/users.csv`.
   - Check per-user DB files under `GUI/users/<username>/`.

---

## Maintainer Note

If you add new GUI pages or data tables, update this README section order:
1. What’s New
2. Project Structure
3. Data Storage
4. Main Pages


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
    _port.write(f"PUNCH:{punch}\n".encode())
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
> "In `main_gui.py`, in `PowerPunchPage`, replace placeholder measurement logic with real Arduino serial reads. The Arduino sends force data as `FORCE:<value>\n`. Read this in a QThread worker following the same pattern as `ReactionTestPage`, emit the value via a signal, and display it. Use the existing port from `os.getenv('ARDUINO_BUTTON_PORT')`."

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
