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
