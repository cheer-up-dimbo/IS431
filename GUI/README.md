# BoxBunny — Boxing Training GUI

## 1. Overview

BoxBunny is an interactive boxing training system built with PySide6 for a Jetson Nano–based embedded platform with a 1024×600 touchscreen. The GUI manages the full training loop: combo curriculum drills (Beginner / Intermediate / Advanced / Self-Select), multi-round sparring sessions against a robot arm opponent, three fitness performance tests (power, stamina, reaction time), per-user progress tracking, history review, and AI-assisted coaching feedback. Hardware integration points include Arduino-based punch sensors, physical navigation buttons, and a file-based interface to a computer-vision punch-detection pipeline.

---

## 2. Prerequisites

### Platform

- Target: Jetson Nano (Ubuntu), 1024×600 touchscreen
- Development: Windows 10/11 (tested)

### Python

- Python 3.9 or later

### Required packages

No `requirements.txt` — install manually:

```bash
pip install PySide6 opencv-python numpy ultralytics pyserial anthropic
```

| Package | Purpose |
| --- | --- |
| `PySide6` | Qt 6 GUI framework |
| `opencv-python` | Webcam capture for reaction test |
| `numpy` | Numerical ops (pose estimation) |
| `ultralytics` | YOLO11 pose estimation model |
| `pyserial` | Arduino serial communication |
| `anthropic` | Claude API for AI coaching chat |

### Hardware (optional)

- Arduino with punch force sensors (power and stamina tests)
- Arduino with three navigation buttons (UP/ENTER/DOWN — whole-app navigation)
- Webcam (reaction time test)

---

## 3. Setup & Run

```bash
# 1. Clone and enter the GUI directory
cd GUI

# 2. Create and activate a virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux / Jetson:
source .venv/bin/activate

# 3. Install dependencies
pip install PySide6 opencv-python numpy ultralytics pyserial anthropic

# 4. Configure environment
cp .env.example .env
# Edit .env — set ARDUINO_BUTTON_PORT and any other values you need.
# Add ANTHROPIC_API_KEY=sk-ant-... manually if you want AI chat features.

# 5. Set up the shared combo database (auto-runs on first login, but can be run manually)
python setup/setup_combo_database.py --db-path data/combos.db --force

# 6. Place the YOLO pose model at the repo-root models/ directory
#    models/yolo11s-pose.pt

# 7. Run
python main_gui.py
```

---

## 4. Project Structure

```text
GUI/
├── main_gui.py                   # Main entry point; all page classes and MainWindow
├── placeholders.py               # Shared scoring/feedback helper
├── performance_database.py       # Per-user SQLite DB for power/stamina/reaction history
├── users.csv                     # User credentials (username, SHA-256 hash, level, progress)
├── .env                          # Runtime config (not committed — copy from .env.example)
├── .env.example                  # Template for .env
│
├── core/                         # Shared config, constants, navigation mixin
│   ├── config.py                 # TrainingConfig dataclass and AppState singleton
│   ├── constants.py              # PageIndex (44 entries) and ButtonStyle stylesheet strings
│   ├── navigation.py             # ButtonNavigationMixin — keyboard/Arduino focus cycling
│   └── tooltip.py                # attach_tooltip() helper
│
├── sparring/                     # Multi-round sparring flow and robot interface
│   ├── spar_pages.py             # 8 page classes: StyleSelect → RoundConfig → Countdown →
│   │                             #   Session → Rest → Processing → Result → SparHistory
│   ├── combo_pools.py            # Markov-chain transition matrices for 5 boxing styles
│   ├── sequence_generator.py     # Generates punch sequences using style matrices + weakness bias
│   ├── robot_interface.py        # Stub serial interface: set_speed, send_punch, round signals
│   ├── sparring_database.py      # SQLite logging for sessions and weakness profiles
│   └── __init__.py
│
├── proficiency/                  # Post-signup proficiency assessment
│   ├── proficiency_pages.py      # ProficiencyChecklistPage and ProficiencyResultPage
│   └── __init__.py
│
├── combo_curriculum/             # Combo database and progression logic
│   ├── curriculum.py             # ComboCurriculum class — SQLite-backed combo manager
│   ├── action_recognition_placeholder.py  # Stub for future CV action recognition
│   ├── docs/                     # Scoring, progression, and progress documentation
│   ├── examples/                 # Usage examples
│   ├── tests/                    # pytest test suite (5 files)
│   └── __init__.py
│
├── power/
│   └── power_runner.py           # Arduino serial protocol for punch force measurement
│
├── stamina/
│   └── stamina_runner.py         # Timed punch endurance test; Arduino or simulated mode
│
├── reaction_time/
│   └── reaction_time_runner.py   # YOLO11 pose + webcam reaction timing
│
├── utils/
│   ├── user_management.py        # users.csv CRUD: load, save, hash, level, progress helpers
│   └── __init__.py
│
├── arduino/
│   └── button_navigation/
│       └── button_navigation.ino # 3-button navigation firmware (UP/ENTER/DOWN)
│
├── setup/
│   ├── setup_combo_database.py   # Orchestrates schema + populate + verify for combos.db
│   ├── create_database_schema.py # Creates SQLite schema
│   └── populate_combos.py        # Inserts all 50 Beginner/Intermediate/Advanced combos
│
├── scripts/                      # Dev/debug scripts (verify imports, inspect DB, smoke tests)
│
├── data/
│   └── combos.db                 # Shared fallback combo template database
│
├── users/                        # Per-user directories created automatically at first login
│   └── <username>/
│       ├── combos.db
│       ├── performance_history.db
│       └── spar_trigger.json     # Written by GUI after each sparring session (CV trigger)
│
├── training_history/             # CSV training session logs: training_<username>.csv
└── training_history_archive/     # Archived training CSVs (timestamped copies)
```

---

## 5. Architecture Overview

### QStackedWidget page model

The entire application lives inside a single `MainWindow(QWidget)` that contains one `QStackedWidget`. Every screen is a `QWidget` subclass added to the stack at startup. Exactly one page is visible at a time, selected by its integer index.

All 44 pages are instantiated in `MainWindow.__init__()` before the window is shown. The order of `addWidget()` calls determines the index, which must match the constant defined in `core/constants.py`.

### AppState

`core/config.py` defines a `TrainingConfig` dataclass (rounds, work time, rest time, speed, difficulty, battle style, custom punch sequence) and an `AppState` object that wraps it. `AppState` is created once in `MainWindow` and passed to pages that need it. Pages write their selections back to `AppState` so downstream pages can read the fully configured session when training starts.

`AppState` also carries boolean flags:

- `cv_enabled` — whether to write the CV trigger file after sparring
- `ai_chat_enabled` — whether to call the Claude API for coaching feedback

### ButtonNavigationMixin

Every page class inherits from `(ButtonNavigationMixin, QWidget)`. The mixin provides:

- `self.navigate_to(page_index)` — delegates to `MainWindow.navigate_to()`, which calls `stacked_widget.setCurrentIndex()`
- `self.setup_navigation(buttons)` — registers a list of buttons for keyboard and Arduino cycling:
  - Sets `Qt.StrongFocus` on each button
  - Installs a key event filter for Up/Down/Enter
  - Applies a green `QGraphicsDropShadowEffect` to the focused button
  - Focuses the first button when the page is shown

### navigate_to() patch on QWidget

At startup, `MainWindow` monkey-patches `navigate_to()` onto `QWidget` itself so that any page can call `self.navigate_to(index)` without needing a direct reference to `MainWindow`.

### The SKIP_NAV_SETUP class attribute

If a page sets `SKIP_NAV_SETUP = True` as a class attribute, `ButtonNavigationMixin` skips the automatic call to `setup_navigation()` when the page is shown. Use this on pages that manage their own button focus (e.g., grids where the mixin's linear cycling would not make sense) or pages with no navigable buttons.

### SKIP_NORMALIZE

If a page sets `SKIP_NORMALIZE = True`, the mixin skips overriding button `min-width`/`min-height` to its normalized defaults. Use this when a page's buttons intentionally differ from the standard navigation button size (e.g., the proficiency checklist option buttons).

---

## 6. Page Index Reference

| Index | PageIndex constant | Class | Description |
| --- | --- | --- | --- |
| 0 | `HOMEPAGE` | `Homepage` | Main menu with Training, Spar, History, User Management, and Others |
| 1 | `TRAINING` | `TrainingPage` | Top-level training mode menu |
| 2 | `TECHNIQUES` | `TechniquesPage` | Difficulty level selection (Beginner / Intermediate / Advanced / Self-Select) |
| 3 | `PUNCH_COMBINATIONS` | `PunchCombinationPage` | Browse and select a combo from the curriculum |
| 4 | `BASIC_PARAMETERS` | `BasicParametersPage` | Configure rounds, time, rest, speed before session |
| 5 | `ROUND_SELECTION` | `RoundSelectionPage` | Grid selector for number of rounds (1–12) |
| 6 | `SPEED_SELECTION` | `SpeedSelectionPage` | Speed selector (25% / 50% / 75% / 100%) |
| 7 | `TIME_SELECTION` | `TimeSelectionPage` | Work time per round selector |
| 8 | `REST_SELECTION` | `RestSelectionPage` | Rest time between rounds selector |
| 9 | `COUNTDOWN` | `CountdownPage` | 5-second countdown before training session starts |
| 10 | `TRAINING_SESSION` | `TrainingSessionPage` | Live combo display with round and rest timers |
| 11 | `SELF_SELECT_SEQUENCE` | `SelfSelectSequencePage` | Build a custom punch sequence (up to 9 moves, up to 5 sequences) |
| 12 | `SPAR` | `SparPage` | Sparring mode entry page |
| 13 | `PERFORMANCE` | `PerformancePage` | Hub for power, stamina, and reaction tests |
| 14 | `POWER_INSTRUCTIONS` | `PowerInstructionsPage` | Pre-test instructions for power punch test |
| 15 | `POWER_PUNCH` | `PowerPunchPage` | Live power punch test (Arduino or simulated) |
| 16 | `POWER_RESULT` | `PowerResultPage` | Display peak power, average power, punch count |
| 17 | `STAMINA_INSTRUCTIONS` | `StaminaInstructionsPage` | Pre-test instructions for stamina test |
| 18 | `REACTION_INSTRUCTIONS` | `ReactionInstructionsPage` | Instructions for YOLO reaction time test |
| 19 | `REACTION_TEST` | `ReactionTestPage` | Live reaction time measurement (webcam + YOLO) |
| 20 | `REACTION_RESULT` | `ReactionResultPage` | Display reaction time result |
| 21 | `OTHERS` | `OthersPage` | Settings hub: Arduino port, CV toggle, AI chat toggle |
| 22 | `LOGIN` | `LoginPage` | Username/password login and account creation |
| 23 | `USER_MANAGEMENT` | `UserManagementPage` | View/delete users, view stamina history table |
| 24 | `USER_COMBO_PROGRESS` | `UserComboProgressPage` | Per-combo mastery progress table |
| 25 | `USER_PROGRESS_OVERVIEW` | `UserProgressOverviewPage` | Level progress and group completion overview |
| 26 | `COMBO_RESULTS` | `ComboResultsPage` | Results after completing a combo drill session |
| 27 | `COMBO_LLM_CHAT` | `ComboLLMChatPage` | AI coaching chat for combo performance feedback |
| 28 | `STAMINA_TEST` | `StaminaTestPage` | Live 2-minute stamina test with countdown |
| 29 | `STAMINA_RESULT` | `StaminaResultPage` | Display score, fatigue %, punch rate |
| 30 | `STAMINA_HISTORY` | `StaminaHistoryPage` | Historical stamina results table |
| 31 | `PERFORMANCE_HISTORY` | `PerformanceHistoryPage` | Tabbed history view for power / stamina / reaction |
| 32 | `BATTLE_STYLE_DESC` | `BattleStyleDescriptionPage` | Descriptions of each boxing style |
| 33 | `SPAR_STYLE_SELECT` | `SparStyleSelectPage` | Boxing style selection for sparring session |
| 34 | `SPAR_ROUND_CONFIG` | `SparRoundConfigPage` | Configure rounds, round time, and rest time |
| 35 | `SPAR_COUNTDOWN` | `SparCountdownPage` | 5-second countdown before each sparring round |
| 36 | `SPAR_SESSION` | `SparSessionPage` | Live sparring round — timer, punch display, stop control |
| 37 | `SPAR_REST` | `SparRestPage` | Rest period between sparring rounds |
| 38 | `SPAR_PROCESSING` | `SparProcessingPage` | Polling screen while CV pipeline analyses session |
| 39 | `SPAR_RESULT` | `SparResultPage` | Sparring session summary with punch breakdown and AI feedback |
| 40 | `PROFICIENCY_CHECKLIST` | `ProficiencyChecklistPage` | 6-question background survey shown once after account creation |
| 41 | `PROFICIENCY_RESULT` | `ProficiencyResultPage` | Shows suggested level; user can override and confirm |
| 42 | `HISTORY_HUB` | `HistoryHubPage` | Central hub to navigate to all history views |
| 43 | `SPAR_HISTORY` | `SparHistoryPage` | Table of past sparring sessions |

---

## 7. Navigation Flow

```text
LOGIN (22)
  │
  ├─> [new account] ──> PROFICIENCY_CHECKLIST (40)
  │                           └─> PROFICIENCY_RESULT (41) ──> HOMEPAGE (0)
  │
  └─> [existing account] ──> HOMEPAGE (0)
        │
        ├─> TRAINING (1)
        │     └─> TECHNIQUES (2)
        │           └─> PUNCH_COMBINATIONS (3)
        │                 └─> BASIC_PARAMETERS (4)
        │                       ├─> ROUND_SELECTION (5) ──> BASIC_PARAMETERS
        │                       ├─> SPEED_SELECTION (6) ──> BASIC_PARAMETERS
        │                       ├─> TIME_SELECTION (7)  ──> BASIC_PARAMETERS
        │                       ├─> REST_SELECTION (8)  ──> BASIC_PARAMETERS
        │                       └─> COUNTDOWN (9)
        │                             └─> TRAINING_SESSION (10)
        │                                   └─> COMBO_RESULTS (26)
        │                                         └─> COMBO_LLM_CHAT (27) [if AI enabled]
        │
        ├─> SPAR (12)
        │     └─> SPAR_STYLE_SELECT (33)
        │           └─> BATTLE_STYLE_DESC (32) [info popup]
        │           └─> SPAR_ROUND_CONFIG (34)
        │                 └─> SPAR_COUNTDOWN (35)
        │                       └─> SPAR_SESSION (36)
        │                             └─> SPAR_REST (37)
        │                                   └─> [next round: SPAR_COUNTDOWN → SPAR_SESSION → SPAR_REST]
        │                                         └─> [final round done]
        │                                               └─> SPAR_PROCESSING (38)
        │                                                     └─> SPAR_RESULT (39)
        │
        ├─> OTHERS (21)
        │     └─> PERFORMANCE (13)
        │           ├─> Power:    POWER_INSTRUCTIONS (14) → POWER_PUNCH (15) → POWER_RESULT (16)
        │           ├─> Stamina:  STAMINA_INSTRUCTIONS (17) → STAMINA_TEST (28) → STAMINA_RESULT (29)
        │           └─> Reaction: REACTION_INSTRUCTIONS (18) → REACTION_TEST (19) → REACTION_RESULT (20)
        │
        ├─> HISTORY (42)  [HistoryHubPage]
        │     ├─> PERFORMANCE_HISTORY (31) filtered to Power
        │     ├─> PERFORMANCE_HISTORY (31) filtered to Stamina
        │     ├─> PERFORMANCE_HISTORY (31) filtered to Reaction
        │     ├─> USER_COMBO_PROGRESS (24)
        │     └─> SPAR_HISTORY (43)
        │
        └─> USER_MANAGEMENT (23)
              ├─> USER_COMBO_PROGRESS (24)
              └─> USER_PROGRESS_OVERVIEW (25)
```

Self-select sequence: `TECHNIQUES (2)` → `SELF_SELECT_SEQUENCE (11)` → `BASIC_PARAMETERS (4)`

Stamina history: reachable from `STAMINA_RESULT (29)` → `STAMINA_HISTORY (30)`.

---

## 8. Data Storage

### users.csv

One row per user. Fields:

| Column | Type | Description |
| --- | --- | --- |
| `username` | string | Login name (also used as directory name under `users/`) |
| `password_hash` | string | SHA-256 hex digest of the plaintext password |
| `level` | string | `Beginner`, `Intermediate`, or `Advanced` |
| `progress` | float | 0.0–1.0 overall progress within the current level |

### users/\<username\>/combos.db

Per-user SQLite database created at first login. Mirrors the shared `data/combos.db` schema but adds mastery scores and attempt counts per user. Managed by `combo_curriculum/curriculum.py`.

### users/\<username\>/performance_history.db

Per-user SQLite database. Contains five tables:

**`power_tests`** — one row per power test session

| Column | Type |
| --- | --- |
| `timestamp` | TEXT (ISO-8601) |
| `peak_power` | REAL |
| `average_power` | REAL |
| `total_punches` | INTEGER |

**`stamina_tests`** — one row per stamina test session

| Column | Type |
| --- | --- |
| `timestamp` | TEXT (ISO-8601) |
| `total_punches` | INTEGER |
| `average_rate` | REAL (punches/min) |
| `first_30s_rate` | REAL |
| `last_30s_rate` | REAL |
| `fatigue_percentage` | REAL |
| `score` | REAL |
| `duration` | INTEGER (seconds) |

**`reaction_tests`** — one row per reaction test session

| Column | Type |
| --- | --- |
| `timestamp` | TEXT (ISO-8601) |
| `reaction_time` | REAL (milliseconds) |
| `accuracy` | REAL |
| `total_attempts` | INTEGER |

**`sparring_sessions`** — one row per sparring session

| Column | Type |
| --- | --- |
| `id` | INTEGER PK |
| `timestamp` | TEXT (ISO-8601) |
| `style` | TEXT |
| `total_rounds` | INTEGER |
| `round_duration` | INTEGER (seconds) |
| `rest_duration` | INTEGER (seconds) |
| `cv_raw_output` | TEXT (raw comma-separated punch labels from CV) |
| `punch_counts` | TEXT (JSON dict: `{"jab": 5, "cross": 3, ...}`) |
| `notes` | TEXT |

**`sparring_weakness_profile`** — one row per user (upserted after each session)

| Column | Type |
| --- | --- |
| `username` | TEXT UNIQUE |
| `jab_freq` | REAL |
| `cross_freq` | REAL |
| `lead_hook_freq` | REAL |
| `rear_hook_freq` | REAL |
| `lead_upper_freq` | REAL |
| `rear_upper_freq` | REAL |
| `sessions_count` | INTEGER |
| `last_updated` | TEXT (ISO-8601) |

### training_history/training_\<username\>.csv

Append-only log of training session events (round start/stop, combo selection, timestamps). One file per user. Archived copies go to `training_history_archive/`.

### data/combos.db

Shared SQLite template database holding all 50 combos (15 Beginner, 20 Intermediate, 15 Advanced). Read-only at runtime; copied into per-user directories on first login.

### .env

Runtime configuration file. Copy `.env.example` to `.env` and edit. Keys defined in `.env.example`:

| Key | Default | Purpose |
| --- | --- | --- |
| `ARDUINO_BUTTONS_ENABLED` | `true` | Enable/disable physical button listener |
| `ARDUINO_BUTTON_PORT` | `COM3` | Serial port for navigation buttons. Leave empty to auto-detect |
| `ARDUINO_BUTTON_BAUD` | `115200` | Baud rate for button navigation Arduino |
| `ARDUINO_BUTTON_DEBOUNCE_MS` | `120` | Software debounce window in milliseconds |
| `ARDUINO_BUTTON_TIMEOUT_SEC` | `0.05` | Serial read timeout in seconds |
| `ARDUINO_BUTTON_STARTUP_DELAY_SEC` | `1.2` | Delay before first read after port opens |
| `ARDUINO_BUTTON_RECONNECT_SEC` | `2.0` | Retry interval when connection is lost |
| `ARDUINO_BUTTONS_SUSPEND_DURING_TESTS` | `true` | Suspend button listener during Power/Stamina tests to avoid port conflicts |
| `ARDUINO_BUTTON_WATCHDOG_MS` | `5000` | Auto-restart listener thread if it stops unexpectedly |
| `STAMINA_USE_ARDUINO` | `false` | Use Arduino for stamina punch counting (false = simulated) |

Key not in `.env.example` — add manually:

| Key | Purpose |
| --- | --- |
| `ANTHROPIC_API_KEY` | API key for Claude AI coaching chat (`sk-ant-...`). Leave unset to run without AI features |

---

## 9. Adding a New Page (Developer Guide)

### Step-by-step

**1. Add a `PageIndex` constant** in `core/constants.py`:

```python
class PageIndex:
    ...
    MY_NEW_PAGE = 44   # Next available index
```

**2. Create the page class** inheriting `(ButtonNavigationMixin, QWidget)`. Place it in `main_gui.py` or a dedicated module:

```python
from core.navigation import ButtonNavigationMixin
from core.constants import PageIndex, ButtonStyle
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

class MyNewPage(ButtonNavigationMixin, QWidget):

    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(60, 40, 60, 40)

        title = QLabel("My Page")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 30px; font-weight: bold; color: white;")

        action_btn = QPushButton("Do Something")
        action_btn.setStyleSheet(ButtonStyle.PRIMARY_MEDIUM)
        action_btn.clicked.connect(self._on_action)

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)
        back_btn.clicked.connect(self._on_back)

        layout.addWidget(title)
        layout.addWidget(action_btn, alignment=Qt.AlignCenter)
        layout.addWidget(back_btn, alignment=Qt.AlignCenter)
        self.setLayout(layout)

        # Register buttons for Arduino/keyboard navigation
        self.setup_navigation([action_btn, back_btn])

    def _on_action(self):
        self.navigate_to(PageIndex.SOME_OTHER_PAGE)

    def _on_back(self):
        self.navigate_to(PageIndex.HOMEPAGE)
```

**3. Instantiate in `MainWindow.__init__`** and add at the correct index:

```python
# In MainWindow.__init__:
self.my_new_page = MyNewPage(self.stacked_widget)
self.stacked_widget.addWidget(self.my_new_page)   # must become index 44
```

The index is determined by the order of `addWidget()` calls. Count them carefully to ensure they match the `PageIndex` constant.

**4. Wire navigation from an existing page** — in the page that should link to yours:

```python
some_btn.clicked.connect(lambda: self.navigate_to(PageIndex.MY_NEW_PAGE))
```

### SKIP_NAV_SETUP

Do not call `self.setup_navigation()` and set `SKIP_NAV_SETUP = True` when:

- The page uses a grid layout where linear focus cycling would be confusing
- The page has no buttons that need keyboard/Arduino navigation
- You are managing focus manually

```python
class MyGridPage(ButtonNavigationMixin, QWidget):
    SKIP_NAV_SETUP = True

    def __init__(self, stacked_widget):
        ...
        # setup_navigation() will NOT be called automatically
```

### Lambda capture bug inside loops

When creating buttons inside a loop and connecting each to a handler that uses the loop variable, you must use a default-argument capture:

```python
# WRONG — all buttons end up calling with the last value of label
for label in ["Beginner", "Intermediate", "Advanced"]:
    btn = QPushButton(label)
    btn.clicked.connect(lambda: self.on_level(label))   # captures by reference

# CORRECT — each lambda captures its own copy of label
for label in ["Beginner", "Intermediate", "Advanced"]:
    btn = QPushButton(label)
    btn.clicked.connect(lambda checked=False, lvl=label: self.on_level(lvl))
```

---

## 10. Integration Guide — Robot Arms

### Modes that use robot arms

- **Sparring mode**: The arms throw punches continuously throughout each round. The sequence is generated by a Markov chain weighted by the chosen boxing style and the user's historical weakness profile.
- **Combo drill mode** (all difficulty levels): The arms loop the current displayed combo for the full duration of each round so the user can mirror it.

In both modes the arms pause during rest periods and stop when the session ends or the user presses stop.

### Interface — sparring/robot_interface.py

Four functions are called by the GUI. All are currently stubs that print to console.

| Function | When it fires |
| --- | --- |
| `set_speed(speed: str)` | Once, immediately before the session loop starts |
| `send_round_start()` | Start of every round |
| `send_punch(punch: str)` | Each individual punch, with timing gaps handled by the GUI thread |
| `send_round_stop()` | End of every round — natural timeout, stop button, or session abort |

### Speed and timing

`set_speed()` receives one of three string values. The GUI reads the corresponding gap durations from `get_intra_gap()` and `get_inter_gap()` in the same module:

| Speed value | Intra-punch gap | Inter-combo gap |
| --- | --- | --- |
| `"slow"` | 0.8 s | 2.0 s |
| `"medium"` | 0.5 s | 1.5 s |
| `"fast"` | 0.3 s | 1.0 s |

### Punch codes

`send_punch()` receives a single string code:

| Code | Punch | Code | Punch |
| --- | --- | --- | --- |
| `"1"` | Jab | `"2"` | Cross |
| `"3"` | Lead hook | `"4"` | Rear hook |
| `"5"` | Lead uppercut | `"6"` | Rear uppercut |
| `"3b"` | Lead body hook | `"2b"` | Cross to body |

### What to implement

Open `sparring/robot_interface.py` and replace the `print` statement bodies with `pyserial` writes. **Do not change any function signatures or the `_speed` global logic.**

```python
# Current placeholder:
def send_punch(punch: str) -> None:
    print(f"[ROBOT] Punch: {punch}")

# Replace with:
import serial
_port = serial.Serial('/dev/ttyUSB0', 115200)  # configure port/baud as needed

def send_punch(punch: str) -> None:
    _port.write(f"PUNCH:{punch}\n".encode())
```

Apply the same pattern to `set_speed()`, `send_round_start()`, and `send_round_stop()`.

### Testing without robot hardware

Run the GUI normally. Start a sparring or combo drill session and watch the terminal. You should see output matching this pattern:

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

## 11. Integration Guide — Computer Vision (CV)

### What the CV integration does

After every sparring session, the GUI writes a trigger file and polls for a result. The returned data is parsed into a punch count dictionary, saved to the session record, and used to update a **weakness profile** — a rolling weighted average of which punch types the user lands least. The weakness profile biases the Markov chain for the next session, making the robot attack the user's weaker side more.

### Trigger file — written by GUI

Path: `GUI/users/<username>/spar_trigger.json`

```json
{
  "username": "zakir",
  "session_id": null,
  "timestamp": "2026-03-19T14:32:00.123456"
}
```

Written immediately when the final sparring round ends, before navigating to `SPAR_PROCESSING`. If CV is disabled in the Others page, this file is never written.

### Output file — written by CV

Path: `GUI/users/<username>/spar_cv_output.txt`

```text
jab,cross,jab,lead_hook,cross,rear_hook,jab,jab,cross
```

Comma-separated punch labels in chronological order. Write only when the full CV pipeline has finished — the GUI reads the file the moment it appears.

Accepted labels: `jab`, `cross`, `lead_hook`, `rear_hook`, `lead_upper`, `rear_upper`

The parser also accepts `hook` (mapped to `lead_hook`) and `uppercut` (mapped to `lead_upper`).

### Timeout behaviour

The GUI polls for `spar_cv_output.txt` every second with a **120-second timeout**. If the file does not appear within 120 seconds, the GUI skips analysis, saves the session with empty punch counts, and continues to the result page. Both files are deleted automatically after a successful read.

### Weakness profile

Stored in `sparring_weakness_profile` table in `users/<username>/performance_history.db`. One row per user, upserted after each session.

Update formula (in `sparring/sparring_database.py`, `update_weakness_profile()`):

```text
alpha    = min(0.4, sessions_count * 0.05)
new_freq = (1 - alpha) * old_freq + alpha * current_session_freq
```

On the first session, `sessions_count = 0`, so `alpha = 0` and the first session's frequencies are written directly. By session 8, alpha reaches its cap of 0.4 and the profile updates at full speed.

Bias application (in `sparring/sequence_generator.py`, `_apply_weakness_bias()`): the weakness profile frequencies are blended into the Markov transition matrix before generating the session sequence. Left-side punches (`1`, `3`, `5`) are biased by the user's frequency of landing right-side punches and vice versa — meaning if the user rarely lands jabs, the robot will throw more left-side punches at them.

To adjust bias strength, change either of these constants in `_apply_weakness_bias()`:

- The alpha cap: `min(0.4, ...)` — increase to allow stronger long-term bias
- The sessions multiplier: `sessions_count * 0.05` — increase to ramp up faster

### CV toggle

If the user disables CV in the Others page (`cv_enabled = False` on `AppState`), `spar_trigger.json` is never written and `SparProcessingPage` skips polling entirely, navigating directly to results.

### Testing without the CV pipeline

While the GUI is on the Processing screen, manually write the output file:

```bash
echo "jab,cross,jab,lead_hook,cross" > GUI/users/<username>/spar_cv_output.txt
```

The GUI reads it within one second and advances to the result page.

---

## 12. Integration Guide — Arduino (Performance Pages)

### What uses Arduino

| Feature | Module | Default mode |
| --- | --- | --- |
| Power punch test | `power/power_runner.py` | Requires Arduino |
| Stamina test | `stamina/stamina_runner.py` | Simulated (no Arduino) |
| Physical button navigation | `main_gui.py` background thread | Enabled if port is found |

Reaction test uses the YOLO webcam, not Arduino.

### Physical button navigation protocol

Upload `arduino/button_navigation/button_navigation.ino`. Arduino sends at 115200 baud on button press (debounced at 40 ms):

| Message | Button | GPIO pin | Action |
| --- | --- | --- | --- |
| `BTN1_PRESS` | UP | D2 | Move focus to previous button |
| `BTN2_PRESS` | ENTER | D4 | Click the focused button |
| `BTN3_PRESS` | DOWN | D7 | Move focus to next button |

Wiring: `INPUT_PULLUP` with button to GND on each pin.

### Power test serial protocol

Arduino sends after 10 punches:

```text
RESULT:PEAK:<value>,AVG:<value>,COUNT:<count>
```

The GUI first probes for command-based mode (`MODE:CONTINUOUS` → expects `OK:...`). If the firmware does not respond to commands, it falls back to legacy streaming mode. See `power/power_runner.py` for full detail.

### Stamina test serial protocol

Arduino sends punch detection events during the 2-minute window. Enable with `STAMINA_USE_ARDUINO=true` in `.env`. See `stamina/stamina_runner.py`, `_measure_with_arduino()`, for the expected message format.

### Port conflict handling

`ARDUINO_BUTTONS_SUSPEND_DURING_TESTS=true` in `.env` causes the button navigation listener to suspend automatically when the GUI enters a Power or Stamina test page, and resume automatically on exit. This allows the same physical Arduino and COM port to serve all three roles without conflicts.

### Port configuration

In `.env`:

```ini
ARDUINO_BUTTON_PORT=COM3          # Windows
ARDUINO_BUTTON_PORT=/dev/ttyACM0  # Jetson Nano
ARDUINO_BUTTON_BAUD=115200
```

Leave `ARDUINO_BUTTON_PORT` empty for auto-detection. The Others page also has a live COM port dropdown and Apply button; changing it there takes effect immediately without restarting.

### Testing without Arduino

The GUI runs fully without any Arduino:

- Stamina defaults to simulated mode (`STAMINA_USE_ARDUINO=false`)
- Power test fails gracefully with an error dialog if the port is unavailable
- Button navigation is silently skipped if no port is detected

---

## 13. Integration Guide — AI Chat (LLM)

### Where AI feedback appears

| Location | Condition |
| --- | --- |
| `ComboLLMChatPage` (27) | After a combo drill session, if AI Chat is enabled |
| `SparResultPage` (39) | Inline coaching paragraph, if AI Chat is enabled |

Both use `claude-haiku-4-5` with a boxing coach system prompt.

### Enabling AI features

1. Toggle **AI Chat: On** in the Others page (sets `AppState.ai_chat_enabled = True`)
2. Ensure `ANTHROPIC_API_KEY` is set in `GUI/.env`:

```ini
ANTHROPIC_API_KEY=sk-ant-api03-...
```

Restart the app after changing `.env`.

### Fallback behaviour

If `ANTHROPIC_API_KEY` is missing, empty, or returns an error, the GUI falls back to a hardcoded response string. The app never crashes. API calls run in QThread workers and do not block the UI.

### Testing AI features

1. Set `ANTHROPIC_API_KEY` in `.env`
2. Toggle AI Chat on in Others
3. Complete a combo drill or sparring session
4. The feedback area will briefly show "Thinking..." or "Analysing your session...", then update with a live Claude response

If you see a generic hardcoded response, the key is missing or invalid.

---

## 14. Troubleshooting

### Camera fails to initialize

- Check that no other application (Teams, OBS, etc.) holds the camera.
- Verify camera permissions on the OS.
- The reaction test defaults to camera index 0. If the system has multiple cameras, the wrong one may be selected — check `reaction_time/reaction_time_runner.py`.

### Reaction model not found (yolo11s-pose.pt)

- Place the model at `<repo_root>/models/yolo11s-pose.pt`.
- The path is relative to the repository root, not the `GUI/` directory.

### Serial / Arduino port issues

- Set `ARDUINO_BUTTON_PORT` explicitly in `.env` if auto-detection picks the wrong device.
- On Windows, check Device Manager for the correct COMx number.
- On Jetson Nano, the port is typically `/dev/ttyACM0` or `/dev/ttyUSB0`.
- If the button navigation listener shows `reconnecting` in the Others page status, the Arduino is connected but communication is failing — check the baud rate.
- If Power or Stamina tests fail, ensure `ARDUINO_BUTTONS_SUSPEND_DURING_TESTS=true` so the navigation listener releases the port before the test takes it.

### User data not appearing

- Confirm the username in `users.csv` exactly matches the subdirectory name under `users/`.
- Per-user databases are created on first login. If a user was added manually to `users.csv` without logging in, the databases will not exist yet.

### App crashes on startup

- Run `python scripts/verify_modules.py` to check all imports resolve.
- Ensure all pip packages are installed in the active virtual environment.
- If `.env` is missing, the app runs with defaults. If `.env` contains syntax errors, dotenv parsing may fail silently — check that key=value lines have no spaces around `=`.
- Missing `data/combos.db` causes a crash at first login. Run `python setup/setup_combo_database.py --db-path data/combos.db` to create it.

### CV pipeline timeout

- The GUI waits up to 120 seconds for `spar_cv_output.txt` to appear.
- If CV processing takes longer, the session is saved without punch breakdown data and the result page shows empty counts.
- To test the GUI without CV, manually write the output file while the Processing screen is shown (see Section 11).
- If CV is intentionally not running, disable it in the Others page so the trigger file is never written and the GUI skips polling entirely.
