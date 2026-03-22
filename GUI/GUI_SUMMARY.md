# GUI Folder Summary — BoxBunny Boxing Training System

## Overview

The `GUI/` folder contains the full application stack for **BoxBunny**, an interactive boxing training system built with **PySide6 (Qt)**. The application guides users through structured boxing training modes, physical fitness tests, and AI-assisted combo review. Hardware integration includes Arduino-based button navigation and force-sensing punch pads.

---

## Folder Structure

```
GUI/
├── main_gui.py                  # Main application entry point (~5500+ lines)
├── placeholders.py              # Shared feedback/scoring helper
├── performance_database.py      # SQLite DB for power/stamina/reaction history
├── users.csv                    # User credentials (username, SHA-256 hash, level, progress)
├── .env / .env.example          # Environment config (API keys, feature flags)
│
├── core/                        # Shared config, constants, navigation mixin
├── sparring/                    # Sparring mode pages and logic
├── combo_curriculum/            # Combo database manager and curriculum logic
├── power/                       # Power punch measurement (Arduino serial)
├── stamina/                     # Stamina endurance test runner
├── reaction_time/               # Reaction time runner (YOLO pose estimation)
├── utils/                       # User management utilities
├── arduino/                     # Arduino firmware for button navigation
├── setup/                       # Database initialisation scripts
├── scripts/                     # Dev/debug scripts
├── data/                        # Shared combos.db
├── users/                       # Per-user databases (combos, stamina, performance)
├── training_history/            # CSV training session logs
└── training_history_archive/    # Archived training logs
```

---

## Technology Stack

| Layer | Technology |
|---|---|
| GUI Framework | PySide6 (Qt for Python) |
| Database | SQLite3 (per-user and shared) |
| Hardware comms | pyserial (Arduino serial) |
| Computer Vision | OpenCV + YOLO (ultralytics) — reaction time |
| LLM integration | API key via `.env` (combo chat feature) |
| User auth | SHA-256 password hashing, CSV storage |

---

## Core Modules (`core/`)

### `config.py`
- **`TrainingConfig`** — dataclass holding all session parameters: rounds, work time, rest time, speed (25–100%), difficulty, battle style, and custom punch sequences.
- **`AppState`** — central singleton-style state manager; all pages read/write training config through this object. Also holds `cv_enabled` and `ai_chat_enabled` flags.

### `constants.py`
- **`PageIndex`** — 42 named integer constants for `QStackedWidget` page navigation (e.g., `HOMEPAGE=0`, `SPAR_RESULT=39`).
- **`ButtonStyle`** — static Qt stylesheet strings for all button variants (Primary/Back/Info in Large/Medium/Small sizes, plus special selection button styles).

### `navigation.py`
- **`ButtonNavigationMixin`** — mixin for any page class that needs keyboard and Arduino navigation. Manages focus cycling (Up/Down arrows or `BTN1`/`BTN3`), enter-to-click, and a green glow `QGraphicsDropShadowEffect` on the focused button.

---

## Main Application (`main_gui.py`)

Entry point. Creates a `QApplication` + `QMainWindow` containing a `QStackedWidget` with all 40 pages instantiated at startup. Handles:
- Arduino serial thread (reads `BTN1_PRESS` / `BTN2_PRESS` / `BTN3_PRESS` from COM port)
- `.env` file loading
- Per-user combo database initialisation on first login
- Global `navigate_to()` helper patched onto `QWidget`

### Pages defined in `main_gui.py`

| Page | Description |
|---|---|
| `LoginPage` | Username/password login, account creation |
| `UserManagementPage` | View/delete users, stamina history table |
| `OthersPage` | Settings hub: AI chat toggle, CV toggle, performance tests |
| `PerformancePage` | Hub for power, stamina, reaction tests |
| `PerformanceHistoryPage` | Tabbed history view for all three test types |
| `PowerInstructionsPage` | Pre-test instructions for power punch |
| `PowerPunchPage` | Live power punch test (Arduino or simulated) |
| `PowerResultPage` | Display peak/average power and punch count |
| `StaminaInstructionsPage` | Pre-test instructions for stamina test |
| `StaminaTestPage` | Live 2-minute stamina test with countdown |
| `StaminaResultPage` | Display score, fatigue %, punch rate |
| `StaminaHistoryPage` | Historical stamina results table |
| `ReactionInstructionsPage` | Instructions for YOLO-based reaction test |
| `ReactionTestPage` | Live reaction time measurement with camera |
| `ReactionResultPage` | Display reaction time result |
| `TrainingPage` | Top-level training mode menu |
| `TechniquesPage` | Technique selection (Beginner/Intermediate/Advanced/Self-Select) |
| `PunchCombinationPage` | Browse and select combos from curriculum |
| `BasicParametersPage` | Configure rounds, time, rest, speed before session |
| `RoundSelectionPage` | Grid selector for number of rounds (1–12) |
| `SpeedSelectionPage` | Speed selector (25%/50%/75%/100%) |
| `TimeSelectionPage` | Work time selector |
| `RestSelectionPage` | Rest time selector |
| `CountdownPage` | 5-second countdown before training session |
| `TrainingSessionPage` | Live training session: combo display, round timer, rest timer |
| `SelfSelectSequencePage` | Build a custom punch sequence from punch buttons |
| `SparPage` | Sparring mode entry page |
| `BattleStyleDescriptionPage` | Descriptions of each boxing style |
| `ComboLLMChatPage` | AI chat for feedback on combo performance |
| `ComboResultsPage` | Results after completing a combo |
| `UserComboProgressPage` | Per-combo mastery progress table |
| `UserProgressOverviewPage` | Overview of level progress and group completion |

---

## Sparring Module (`sparring/`)

Implements a full multi-round sparring flow against a robot arm.

| File | Purpose |
|---|---|
| `spar_pages.py` | 7 page classes: Style Select → Round Config → Countdown → Session → Rest → Processing → Result |
| `combo_pools.py` | Markov-chain transition matrices for 5 boxing styles: Pressure Fighter, Counter Puncher, Infighter, Out-Boxer, Balanced Boxer |
| `sequence_generator.py` | Generates a full session combo sequence using style matrices |
| `robot_interface.py` | Placeholder serial interface: `send_punch()`, `send_round_start()`, `send_round_stop()` |
| `sparring_database.py` | SQLite logging for sparring session results |
| `__init__.py` | Package exports |

### Boxing Styles (Markov chain)
Each style defines a transition probability matrix over punch types:
`1`=jab, `2`=cross, `3`=lead hook, `4`=rear hook, `5`=lead uppercut, `6`=rear uppercut, `3b`=lead body hook, `2b`=cross to body.

---

## Combo Curriculum (`combo_curriculum/`)

| File | Purpose |
|---|---|
| `curriculum.py` | `ComboCurriculum` class — SQLite-backed combo manager with difficulty groups |
| `action_recognition_placeholder.py` | Stub for future CV-based action recognition |
| `__init__.py` | Exports `ComboCurriculum` and helper functions |
| `examples/` | Usage examples for training flow and progress tracking |
| `tests/` | 5 pytest test files covering curriculum, scoring, progression, progress |
| `docs/` | Markdown docs: scoring system, progression, user progress |

### Difficulty Groups
- **Beginner**: Single punches, 2-punch combos with jab, other 2-punch combos (15 combos)
- **Intermediate**: 3-punch combos, body shots, defense, advanced patterns (20 combos)
- **Advanced**: Long combinations, complex defense, counter punching (15 combos)

---

## Fitness Test Modules

### `power/power_runner.py`
- Communicates with Arduino over serial to measure punch force.
- Supports two protocol modes: command-based (`MODE:CONTINUOUS`) and streaming.
- Returns `RESULT:PEAK:<value>,AVG:<value>,COUNT:<count>`.

### `stamina/stamina_runner.py`
- `StaminaRunner` — runs a 2-minute punch endurance test.
- Computes: total punches, average rate, first-30s vs last-30s rate, fatigue %, stamina score.
- Arduino or simulated mode (`USE_ARDUINO = False` by default).

### `reaction_time/reaction_time_runner.py`
- `ReactionTimeRunner` — uses YOLO11 pose estimation (`yolo11s-pose.pt`) + OpenCV webcam.
- Displays a random-delay cue then measures time to first detected arm movement.
- Returns `ReactionResult` (success, reaction_ms, status).

---

## Performance Database (`performance_database.py`)

Per-user SQLite database at `users/<username>/performance_history.db`.

Tables:
- `power_tests` — timestamp, peak_power, average_power, total_punches
- `stamina_tests` — timestamp, total_punches, rates, score, fatigue_percentage, duration
- `reaction_tests` — timestamp, reaction_time, accuracy, total_attempts

---

## User Management (`utils/user_management.py`)

- `users.csv` stores: username, SHA-256 password hash, level (`Beginner`/`Intermediate`/`Advanced`), progress (float 0.0–1.0).
- Key functions: `load_users()`, `save_users()`, `hash_password()`, `get_user_level()`, `set_user_level()`, `get_user_progress()`, `update_user_progress()`, `calculate_user_progress_from_combos()`.

---

## Arduino Integration

### `arduino/button_navigation/button_navigation.ino`
3-button navigation firmware for GUI control without a touchscreen.

| Button | Pin | Action |
|---|---|---|
| BTN1 | D2 | UP — move focus up |
| BTN2 | D4 | ENTER — activate focused button |
| BTN3 | D7 | DOWN — move focus down |

- Baud rate: 115200
- Sends `BTN1_PRESS` / `BTN2_PRESS` / `BTN3_PRESS` over serial on press edge (debounced at 40 ms).

---

## Setup Scripts (`setup/`)

| Script | Purpose |
|---|---|
| `create_database_schema.py` | Creates SQLite schema for combos DB |
| `populate_combos.py` | Inserts all Beginner/Intermediate/Advanced combos |
| `setup_combo_database.py` | Orchestrates schema + populate + verify; called automatically on first login |

---

## Dev/Debug Scripts (`scripts/`)

| Script | Purpose |
|---|---|
| `verify_modules.py` | Checks all GUI package imports succeed |
| `check_database.py` | Inspects combos DB contents |
| `test_curriculum_flow.py` | End-to-end curriculum flow test |
| `test_training_session_phase1.py` | Phase 1 training session smoke test |

---

## Data Files

| Path | Contents |
|---|---|
| `data/combos.db` | Shared fallback combo database |
| `users/<username>/combos.db` | Per-user combo progress (mastery scores, attempt counts) |
| `users/<username>/stamina_history.db` | Per-user stamina test history |
| `users/<username>/performance_history.db` | Per-user power/stamina/reaction history |
| `users/<username>/spar_trigger.json` | Sparring session trigger state file |
| `users.csv` | All user accounts |
| `training_history/training_<username>.csv` | Active training session logs |
| `training_history_archive/` | Archived training CSVs by timestamp |
| `.env` | Runtime config: API keys, feature flags (not committed) |
| `.env.example` | Template for `.env` |

---

## Page Navigation Flow

```
LOGIN (22)
  └─> HOMEPAGE (0)
        ├─> TRAINING (1)
        │     └─> TECHNIQUES (2)
        │           └─> PUNCH_COMBINATIONS (3)
        │                 └─> BASIC_PARAMETERS (4)
        │                       ├─> ROUND_SELECTION (5)
        │                       ├─> SPEED_SELECTION (6)
        │                       ├─> TIME_SELECTION (7)
        │                       ├─> REST_SELECTION (8)
        │                       └─> COUNTDOWN (9)
        │                             └─> TRAINING_SESSION (10)
        │                                   └─> COMBO_RESULTS (26)
        │                                         └─> COMBO_LLM_CHAT (27)
        │
        ├─> SPAR (12)
        │     └─> SPAR_STYLE_SELECT (33)
        │           └─> SPAR_ROUND_CONFIG (34)
        │                 └─> SPAR_COUNTDOWN (35)
        │                       └─> SPAR_SESSION (36)
        │                             └─> SPAR_REST (37)
        │                                   └─> SPAR_PROCESSING (38)
        │                                         └─> SPAR_RESULT (39)
        │
        ├─> OTHERS (21)
        │     └─> PERFORMANCE (13)
        │           ├─> POWER: POWER_INSTRUCTIONS (14) -> POWER_PUNCH (15) -> POWER_RESULT (16)
        │           ├─> STAMINA: STAMINA_INSTRUCTIONS (17) -> STAMINA_TEST (28) -> STAMINA_RESULT (29)
        │           └─> REACTION: REACTION_INSTRUCTIONS (18) -> REACTION_TEST (19) -> REACTION_RESULT (20)
        │
        ├─> USER_MANAGEMENT (23)
        │     ├─> USER_COMBO_PROGRESS (24)
        │     └─> USER_PROGRESS_OVERVIEW (25)
        │
        └─> PROFICIENCY_CHECKLIST (40)   [post-signup only]
              └─> PROFICIENCY_RESULT (41)
                    └─> HOMEPAGE (0)
```
