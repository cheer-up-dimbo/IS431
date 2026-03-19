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

## BoxBunny GUI — Integration Guide

This guide is for groupmates who need to connect their subsystem to the GUI. One section per role. Each section tells you what the GUI already does, what state it's in, what you need to implement on your side, and how to test the connection.

---

## 1. Robot Arms

### 1.1 What the GUI does

The robot arms are active in two modes:

- **Sparring mode**: The arms throw punches continuously throughout each round. The punch sequence is generated by a Markov chain weighted by the chosen boxing style (Pressure Fighter, Counter Puncher, Infighter, Out-Boxer, Balanced) and the user's historical weakness profile built from past CV data.
- **Combo Drill mode** (Beginner / Intermediate / Advanced / Self-Select): The arms loop the current displayed combo for the full duration of each round so the user can mirror it.

In both modes the arms pause during rest periods and stop cleanly when a session ends or is stopped early.

### 1.2 GUI-side status

Fully implemented. `sparring/robot_interface.py` contains placeholder `print` functions. Every call site is wired:

| Call | When it fires |
| --- | --- |
| `set_speed(speed)` | Once, at session start |
| `send_round_start()` | Start of every round |
| `send_punch(punch)` | Each individual punch in the sequence |
| `send_round_stop()` | End of every round (natural finish, stop button, or session end) |

### 1.3 What you need to implement

Open `sparring/robot_interface.py` and replace the `print` statements with real `pyserial` serial writes. **Do not change any function signatures.** The file has clear comments showing exactly what to replace.

```python
# Current placeholder — replace this body only:
def send_punch(punch: str) -> None:
    print(f"[ROBOT] Punch: {punch}")
```

```python
# After your change:
import serial
_port = serial.Serial('/dev/ttyUSB0', <baud_rate>)

def send_punch(punch: str) -> None:
    _port.write(f"PUNCH:{punch}\n".encode())
```

### 1.4 Interface contract

`set_speed(speed: str)` — called once before the session starts.

| Value | Intra-punch gap | Inter-combo gap |
| --- | --- | --- |
| `"slow"` | 0.8 s | 2.0 s |
| `"medium"` | 0.5 s | 1.5 s |
| `"fast"` | 0.3 s | 1.0 s |

Send this as a serial message so the arms can adjust their movement speed accordingly.

`send_punch(punch: str)` — one call per punch, gaps handled by the GUI's background thread.

| Code | Punch | Code | Punch |
| --- | --- | --- | --- |
| `"1"` | Jab | `"2"` | Cross |
| `"3"` | Lead hook | `"4"` | Rear hook |
| `"5"` | Lead uppercut | `"6"` | Rear uppercut |
| `"3b"` | Lead hook to body | `"2b"` | Cross to body |

**Serial port:** `/dev/ttyUSB0` on Jetson Nano. Baud rate: confirm with groupmate.

`send_round_start()` / `send_round_stop()` — signal the arms that a round has begun or ended. Use these to reset arm state between rounds.

### 1.5 How to test without the arms connected

Run the GUI normally. All robot signals currently print to console. Start a sparring session or a combo drill session and watch the terminal — you should see the correct sequence of:

```console
[ROBOT] Speed: medium
[ROBOT] Round started
[ROBOT] Punch: 1
[ROBOT] Punch: 2
[ROBOT] Punch: 3
...
[ROBOT] Round stopped
```

---

## 2. Computer Vision (CV)

### 2.1 What the GUI does

After every sparring session, the GUI writes a trigger file and then waits for CV to return a punch detection result. The GUI uses that data to build a **weakness profile** per user — which punch types they land least — and biases the robot's next sparring session sequence to attack those weaknesses more. The profile improves with every session.

### 2.2 GUI-side status

Fully implemented. `SparProcessingPage` in `sparring/spar_pages.py` handles the trigger write, polling, and timeout. `sparring/sparring_database.py` handles parsing the result and updating the weakness profile.

### 2.3 What you need to implement

A watcher that monitors the `GUI/users/` directory for trigger files, runs the CV pipeline when one appears, and writes the result back. The GUI does not call any CV function directly — **all communication is file-based**.

Suggested structure:

```python
# cv_watcher.py
def start_watching(users_dir: str) -> None:
    """Poll all subdirectories of users_dir every second for spar_trigger.json."""
    ...
```

### 2.4 Interface contract

GUI writes → `GUI/users/<username>/spar_trigger.json`

```json
{
  "username": "zakir",
  "session_id": null,
  "timestamp": "2026-03-19T14:32:00.123456"
}
```

Written immediately when the final sparring round ends.

CV writes back → `GUI/users/<username>/spar_cv_output.txt`

```text
jab,cross,jab,lead_hook,cross,rear_hook,jab,jab,cross
```

Comma-separated punch labels in chronological order. Write only when processing is fully complete — the GUI reads the file the moment it appears.

Accepted labels: `jab`, `cross`, `lead_hook`, `rear_hook`, `lead_upper`, `rear_upper`

Timing:

- The GUI polls for `spar_cv_output.txt` every second with a **120-second timeout**
- If the file does not appear in time, the GUI skips analysis and continues without CV data
- The GUI deletes both files automatically after reading

CV toggle: If the user has CV disabled in the Others page, `spar_trigger.json` is never written. Your watcher will never trigger.

### 2.5 How to test without the full CV pipeline

While the GUI is on the Processing screen (spinning "Analysing..." state), manually write a `spar_cv_output.txt` file into `GUI/users/<username>/`:

```bash
echo "jab,cross,jab,lead_hook,cross" > GUI/users/testuser/spar_cv_output.txt
```

The GUI should read it within one second and navigate to the results page showing the punch breakdown.

---

## 3. Arduino (Performance Pages)

### 3.1 What the GUI does

The Arduino powers three things:

1. **Power test** — measures peak and average punch force across 10 punches (`PowerPunchPage`)
2. **Stamina test** — counts punches over 2 minutes and calculates fatigue rate (`StaminaPage`)
3. **Physical button navigation** — Up / Down / Enter buttons work throughout the entire app

Reaction test uses the YOLO camera, not Arduino — already fully implemented and no action needed.

### 3.2 GUI-side status

- Power test: fully implemented in `power/power_runner.py`, wired into `PowerPunchPage`
- Stamina test: implemented in `stamina/stamina_runner.py`, Arduino mode off by default
- Button navigation: fully implemented, background thread runs automatically

Both Power and Stamina read port and baud from `GUI/.env`.

### 3.3 What you need to do

1\. Set your port in `GUI/.env`:

```env
ARDUINO_BUTTON_PORT=COM3          # Windows
# ARDUINO_BUTTON_PORT=/dev/ttyACM0  # Jetson Nano
ARDUINO_BUTTON_BAUD=115200
```

2\. Enable stamina Arduino mode when firmware is ready:

```env
STAMINA_USE_ARDUINO=true
```

3\. Flash the correct firmware. The button navigation sketch is at `GUI/arduino/button_navigation/button_navigation.ino`.

### 3.4 Interface contract

Button navigation — Arduino sends these strings at 115200 baud:

| Message | Button | GPIO pin |
| --- | --- | --- |
| `BTN1_PRESS` | Up | 2 |
| `BTN2_PRESS` | Enter | 4 |
| `BTN3_PRESS` | Down | 7 |

Wiring: INPUT_PULLUP to GND on each pin.

Power test — Arduino sends after 10 punches:

```text
RESULT:PEAK:<value>,AVG:<value>,COUNT:<count>
```

Supports command-based protocol (`MODE:CONTINUOUS` → `OK:...`) with streaming fallback. See `power/power_runner.py` for full protocol detail.

Stamina test — Arduino sends punch detection events during the 2-minute window. See `stamina/stamina_runner.py` → `_measure_with_arduino()` for the expected message format.

Port conflict handling: The GUI automatically suspends the button navigation listener when entering a Power or Stamina test page and resumes it when leaving — so the same Arduino and port can be shared across all three uses.

### 3.5 How to test without Arduino

The GUI runs fully without Arduino connected:

- Stamina defaults to simulated mode (`STAMINA_USE_ARDUINO=false`)
- Power test will fail gracefully with an error message if the port is unavailable
- Button navigation is silently skipped if no port is found

---

## 4. AI Chat / LLM

### 4.1 What the GUI does

Two places use AI coaching feedback, both gated behind the **AI Chat toggle** in the Others page:

- **Combo drill result**: After a combo drill session with AI Chat enabled, the user lands on a chat page (`ComboLLMChatPage`) that sends an initial assessment of their performance score and combo and lets them ask follow-up questions.
- **Sparring result**: After a sparring session with AI Chat enabled, the results page shows an AI-generated coaching paragraph based on the session's punch count, most-used punch, and fighting style.

Both calls use `claude-haiku-4-5` with a boxing coach system prompt.

### 4.2 GUI-side status

Fully implemented. API calls are non-blocking (QThread workers). Falls back to hardcoded responses if `ANTHROPIC_API_KEY` is not set or is invalid — the app never crashes.

### 4.3 What you need to do

Add your API key to `GUI/.env`:

```env
ANTHROPIC_API_KEY=sk-ant-...
```

No code changes needed. That's it.

### 4.4 Interface contract

None — this integration is entirely self-contained within the GUI. The GUI calls the Anthropic API directly.

### 4.5 How to test

1. Toggle **AI Chat: On** in the Others page
2. Complete a combo drill session (any difficulty) or a sparring session
3. On the result page, the feedback area should briefly show "Thinking..." (combo chat) or "Analysing your session..." (sparring), then update with a real coaching response

If you see a generic hardcoded response instead, the API key is missing or invalid — check `GUI/.env` and restart the app.
