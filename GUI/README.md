# Boxing Training GUI Application

A comprehensive PySide6-based GUI application for boxing training with user progression, combo curriculum management, real-time performance tracking, and YOLO-based reaction time measurement.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [How It Works](#how-it-works)
- [User Progression System](#user-progression-system)
- [Feature Documentation](#feature-documentation)
- [Architecture](#architecture)
- [Modules](#modules)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

---

## Features

### 👤 User Management & Progression
- **Login/Signup System**: Secure user authentication with password hashing
- **User Levels**: Beginner → Intermediate → Advanced progression
- **Progress Tracking**: Combo mastery percentage and training history
- **Level-Based Access**: Training modes unlock as users advance
- **Admin Panel**: User management with level/progress overview

### 🥊 Combo Curriculum System
- **50 Punch Combinations**: 15 Beginner, 20 Intermediate, 15 Advanced
- **Sequential Progression**: Practice combos in order until mastered
- **Mastery Tracking**: Average of last 5 training sessions
- **Automatic Level-Up**: Advance when all combos at current level are mastered
- **Performance Database**: SQLite database tracking all training history

### 🎯 Training Modes
- **Technique Training**: Level-based punch combination practice
- **Self-Select**: Custom sequence creation (available to all levels)
- **Sparring Mode**: Unlocked at Intermediate level
- **Configurable Parameters**: Rounds (1-12), speed (25%-100%), work/rest time

### ⚡ Performance Testing
- **Reaction Time**: YOLO pose estimation detecting punch response time
- **Power Testing**: Accelerometer-based punch force measurement (m/s²)
- **Stamina Testing**: Endurance drills (instructions only)

### 📊 Progress & Analytics
- **Training History**: Track all training sessions per user
- **Mastery Scores**: Combo-level performance tracking (0-5 scale)
- **Progress Dashboard**: User management page shows level and progress
- **Automatic Updates**: Progress updates after each session

---

## Installation

### Prerequisites
- Python 3.8+
- Virtual Environment (recommended)
- Webcam (for reaction time testing)
- Serial accelerometer sensor (optional, for power testing)

### Step 1: Setup Virtual Environment

```bash
cd GUI
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually install:

```bash
pip install PySide6>=6.0.0
pip install opencv-python>=4.5.0
pip install numpy>=1.20.0
pip install ultralytics>=8.0.0
pip install pyserial  # Optional, for power sensor
```

### Step 3: Setup Combo Database

**Required for training modes to work:**

```bash
cd setup
python setup_combo_database.py
```

This creates `setup/combos.db` with:
- 15 Beginner combos
- 20 Intermediate combos  
- 15 Advanced combos
- Empty performance history

### Step 4: Verify YOLO Model

Ensure the YOLO pose model is present:

```
../models/yolo11s-pose.pt
```

If not available, it will be automatically downloaded on first use.

### Step 5: Run the Application

```bash
python main_gui.py
```

---

## Project Structure

```
GUI/
├── main_gui.py                      # Main application (4235 lines)
├── users.csv                        # User database (username, password_hash, level, progress)
├── README.md                        # This file
│
├── combo_curriculum/                # Combo curriculum module
│   ├── curriculum.py                # ComboCurriculum class - database interface
│   ├── action_recognition_placeholder.py  # Placeholder (returns 3.0)
│   ├── docs/                        # Detailed documentation
│   ├── tests/                       # Test suite (6 test scripts)
│   └── examples/                    # Usage examples
│
├── setup/                           # Database setup scripts
│   ├── setup_combo_database.py     # Run this first! Creates combos.db
│   ├── create_database_schema.py   # Schema definition
│   └── populate_combos.py          # Populates 50 combos
│
├── power/                           # Power measurement module
│   ├── __init__.py
│   └── power_runner.py             # Serial accelerometer interface
│
└── reaction_time/                   # Reaction time module
    ├── __init__.py
    ├── reaction_time_runner.py     # YOLO-based reaction measurement
    └── cv_sample.py                # Standalone testing script
```

---

## Quick Start

### First Time Setup

1. **Create combo database:**
   ```bash
   cd setup
   python setup_combo_database.py
   ```

2. **Run application:**
   ```bash
   python main_gui.py
   ```

3. **Create user account:**
   - Click "Sign Up"
   - Enter username and password
   - New users start at Beginner level with 0% progress

4. **Start training:**
   - Login → Training → Punch Combinations
   - Only Beginner and Self-Select available initially
   - Complete training sessions to progress
├── main_gui.py              # Main application entry point and all UI pages
├── json_reader.py           # JSON configuration/data handling utilities
├── power/
│   ├── __init__.py
│   └── power_runner.py      # Punch force measurement via serial sensor
├── reaction_time/
│   ├── __init__.py
│   ├── reaction_time_runner.py  # YOLO-based reaction time measurement
│   └── cv_sample.py         # Standalone testing script (optional)
└── README.md                # This file
```

---

## How It Works

### Application Flow

```
┌─────────────┐
│ Login/Signup│
└──────┬──────┘
       │
       v
┌─────────────┐
│  Homepage   │──────┬──────────┬─────────────┐
└─────────────┘      │          │             │
                     v          v             v
              ┌─────────┐  ┌──────────┐  ┌────────┐
              │Training │  │Performance│  │ Others │
              └────┬────┘  └─────┬────┘  └────────┘
                   │             │
        ┌──────────┼──────┐      │
        v          v      v      v
   ┌─────────┐ ┌─────┐ ┌────┐ ┌──────────┐
   │  Punch  │ │Spar │ │Self│ │ Reaction │
   │  Combos │ │Mode │ │Sel.│ │  Power   │
   └────┬────┘ └──┬──┘ └─┬──┘ └───┬──────┘
        │         │      │        │
        v         v      v        v
   Parameters → Countdown → Training/Testing → Results
```

### User Progression Flow

```
1. New User Created
   ├─ Level: Beginner
   ├─ Progress: 0%
   └─ Access: Beginner combos + Self-Select

2. Training Session
   ├─ User selects next combo (e.g., "beginner_001")
   ├─ Performs combo during training
   ├─ [Placeholder] Score = 3.0/5.0 (fixed for now)
   └─ Score recorded in database

3. Progress Calculation
   ├─ Last 5 scores averaged per combo
   ├─ Mastery threshold: Beginner=3.0, Intermediate/Advanced=4.0
   ├─ Combo mastered if: attempts ≥5 AND avg_score ≥threshold
   └─ Progress = (mastered_combos / total_combos) × 100%

4. Level-Up Check (After Each Session)
   ├─ Check if ALL combos at current level mastered
   ├─ If yes → Advance to next level
   ├─ Beginner→Intermediate: Unlocks Intermediate combos + Sparring
   └─ Intermediate→Advanced: Unlocks Advanced combos

5. Repeat until Advanced level mastery
```

---

## User Progression System

### User Data Structure (users.csv)

```csv
username,password_hash,level,progress
john_doe,<sha256_hash>,Beginner,23.5
jane_smith,<sha256_hash>,Intermediate,60.0
pro_boxer,<sha256_hash>,Advanced,100.0
```

**Fields:**
- `username`: Unique identifier
- `password_hash`: SHA-256 hashed password
- `level`: Current user level (Beginner/Intermediate/Advanced)
- `progress`: Mastery percentage at current level (0-100%)

### Level Requirements

| Level | Combos | Mastery Threshold | Unlock Requirements |
|-------|--------|-------------------|---------------------|
| **Beginner** | 15 combos | ≥3.0/5.0 (60%) | Starting level |
| **Intermediate** | 20 combos | ≥4.0/5.0 (80%) | ALL 15 Beginner combos mastered |
| **Advanced** | 15 combos | ≥4.0/5.0 (80%) | ALL 20 Intermediate combos mastered |

**Mastery Criteria:**
- Combo must have ≥5 training attempts
- Average score of last 5 sessions ≥ threshold
- Both conditions must be met

### Access Control

#### Beginner Users Can Access:
- ✅ Beginner punch combinations
- ✅ Self-Select (custom sequences)
- ❌ Intermediate combos (locked)
- ❌ Advanced combos (locked)
- ❌ Sparring mode (locked)

#### Intermediate Users Can Access:
- ✅ All Beginner combos
- ✅ Intermediate punch combinations
- ✅ Self-Select
- ✅ Sparring mode
- ❌ Advanced combos (locked)

#### Advanced Users Can Access:
- ✅ All punch combinations (Beginner/Intermediate/Advanced)
- ✅ Self-Select
- ✅ Sparring mode

### Progress Calculation

**Formula:**
```python
progress = (mastered_combos / total_combos_at_level) × 100%

# Example: Beginner with 4 out of 15 combos mastered
progress = (4 / 15) × 100 = 26.7%
```

**Automatic Updates:**
- Progress recalculated after every training session
- Level-up triggered when progress reaches 100%
- New level resets progress to 0%

---

## Feature Documentation

### 1. Login & User Management

**How It Works:**

1. **Sign Up**
   ```
   User Action: Enter username + password
   System:
   1. Check if username exists
   2. Hash password with SHA-256
   3. Create user: level=Beginner, progress=0
   4. Save to users.csv
   5. Login automatically
   ```

2. **Login**
   ```
   User Action: Enter credentials
   System:
   1. Hash entered password
   2. Compare with stored hash
   3. Load user level and progress
   4. Navigate to Homepage
   ```

3. **User Management Page** (accessible from Others)
   ```
   Display Table:
   ┌──────────┬──────────────┬──────────┬──────────────────┬─────────┐
   │ Username │ Level        │ Progress │ Training Sessions│ Actions │
   ├──────────┼──────────────┼──────────┼──────────────────┼─────────┤
   │ john_doe │ Beginner     │ 23.5%    │ 8                │ Delete  │
   │ jane_doe │ Intermediate │ 60.0%    │ 24               │ Delete  │
   └──────────┴──────────────┴──────────┴──────────────────┴─────────┘
   
   Features:
   - View all users and their progress
   - See training session count
   - Delete users (admin function)
   - Back to homepage
   ```

**Code Location:** `LoginPage`, `UserManagementPage` in main_gui.py

---

### 2. Combo Curriculum & Training

**How It Works:**

#### Database Structure (combos.db)

**Tables:**
1. `combos` - Main combo data
   ```sql
   combo_id (TEXT)          -- e.g., "beginner_001", "intermediate_015"
   combo_name (TEXT)        -- e.g., "Jab-Cross", "Hook-Uppercut"
   combo_sequence (TEXT)    -- Human-readable name
   difficulty_level (TEXT)  -- "Beginner", "Intermediate", "Advanced"
   mastery_score (REAL)     -- Average of last 5 sessions (0-1 scale)
   total_attempts (INTEGER) -- Number of training sessions
   last_trained_timestamp   -- ISO timestamp of last session
   created_date            -- ISO timestamp of combo creation
   ```

2. `performance_history` - Training session records
   ```sql
   id (INTEGER)             -- Auto-increment primary key
   combo_id (TEXT)          -- Foreign key to combos table
   timestamp (TEXT)         -- ISO timestamp of training session
   performance_score (REAL) -- Score from 0-5 (5 being perfect)
   ```

#### Training Flow

```
1. User Opens Training
   └─ System checks user level

2. PunchCombinationPage Loads
   ├─ Buttons dynamically enabled/disabled based on level:
   │  ├─ Beginner: Enabled
   │  ├─ Intermediate: Enabled if level ≥ Intermediate
   │  ├─ Advanced: Enabled if level = Advanced
   │  └─ Self-Select: Always enabled
   
3. User Selects Difficulty
   └─ Navigate to TechCorrParametersPage

4. Configure Parameters
   ├─ Rounds (1-12)
   ├─ Speed (25%, 50%, 75%, 100%)
   ├─ Work Time (e.g., "3:00")
   └─ Rest Time (e.g., "1:00")

5. Countdown (5 seconds)
   └─ "Wear Gloves!" message

6. Training Session Begins
   ├─ Display: Round X of Y
   ├─ Timer: Work time countdown
   ├─ [Placeholder] User performs combo
   ├─ [Future] Action recognition scores performance
   └─ Rest period after each round

7. Session Ends
   ├─ [Placeholder] Score = 3.0/5.0 (fixed)
   ├─ Update combo database:
   │  ├─ Insert score into performance_history
   │  ├─ Calculate average of last 5 scores
   │  ├─ Update mastery_score in combos table
   │  └─ Increment total_attempts
   ├─ Check level-up eligibility
   └─ Update user progress in users.csv

8. Results Display
   └─ Show session summary
```

#### Sequential Combo Progression

**How get_next_combo() Works:**

```python
# System selects next combo to practice
next_combo = curriculum.get_next_combo("Beginner")

# Returns first combo that is NOT mastered:
# - total_attempts < 5, OR
# - mastery_score < threshold

# Example sequence for Beginner:
# 1. beginner_001 (Jab-Cross) → Practice until mastered
# 2. beginner_002 (Jab-Jab-Cross) → Next in line
# 3. ... continue through beginner_015
# 4. When all mastered → Level up to Intermediate
```

**Mastery Determination:**
```python
is_mastered = (total_attempts >= 5) AND (mastery_score >= threshold)

# Thresholds:
# Beginner: 3.0/5.0 = 0.6
# Intermediate: 4.0/5.0 = 0.8
# Advanced: 4.0/5.0 = 0.8
```

**Code Location:** 
- `PunchCombinationPage` in main_gui.py
- `combo_curriculum/curriculum.py` - Database operations
- `combo_curriculum/action_recognition_placeholder.py` - Scoring (placeholder)

---

### 3. Performance Testing: Reaction Time

**How It Works:**

```
1. User Clicks "Reaction Time" from Performance Page
   └─ Navigate to ReactionInstructionsPage

2. ReactionInstructionsPage
   ├─ Display instructions: "Stand 2-3 feet from camera"
   ├─ User clicks "Start"
   └─ Navigate to ReactionTestPage

3. ReactionTestPage - Red Screen Phase
   ├─ Display: "Setting up camera and pose detection..."
   ├─ Background thread starts:
   │  ├─ Initialize webcam (cv2.VideoCapture)
   │  ├─ Load YOLO11s pose model
   │  ├─ Run 10 warmup frames for stability
   │  └─ Signal: Initialization complete
   ├─ Random delay: 5-8 seconds
   └─ When ready → Turn green

4. ReactionTestPage - Green Screen Phase
   ├─ Display: "PUNCH NOW!" in large text
   ├─ Background thread continues:
   │  ├─ Capture 5 frames to stabilize pose
   │  ├─ Store baseline keypoint positions
   │  ├─ Monitor for motion in each frame:
   │  │  ├─ Detect 17 body keypoints (COCO format)
   │  │  ├─ Calculate Euclidean distance moved
   │  │  ├─ If distance > threshold (20px default):
   │  │  │  └─ PUNCH DETECTED!
   │  │  └─ Record reaction time
   │  └─ Timeout after 2.5 seconds
   └─ Navigate to ReactionResultPage

5. ReactionResultPage
   ├─ Display results:
   │  ├─ Success: "Reaction Time: XXX ms"
   │  ├─ Too Soon: "You moved before green!"
   │  ├─ Timeout: "No punch detected in 2.5s"
   │  └─ Error: Show error message
   └─ Options: View History / Restart / Back
```

**YOLO Pose Detection:**

```
Frame Processing:
1. Capture frame from webcam
2. Run YOLO11s pose estimation
3. Detect 17 keypoints:
   [0:Nose, 1:L-Eye, 2:R-Eye, 3:L-Ear, 4:R-Ear,
    5:L-Shoulder, 6:R-Shoulder, 7:L-Elbow, 8:R-Elbow,
    9:L-Wrist, 10:R-Wrist, 11:L-Hip, 12:R-Hip,
    13:L-Knee, 14:R-Knee, 15:L-Ankle, 16:R-Ankle]

Motion Detection:
distances = []
for each keypoint:
    dist = sqrt((x_current - x_baseline)² + (y_current - y_baseline)²)
    distances.append(dist)

total_motion = sum(distances)
if total_motion > motion_threshold:
    PUNCH DETECTED!
```

**Threading Model:**
```
Main Thread (UI)           Worker Thread (QThread)
     │                            │
     ├─ Show red screen          │
     ├─ Start init thread ──────>│
     │                            ├─ Open camera
     │                            ├─ Load YOLO model
     │                            ├─ Warmup frames
     │<─ Signal: Ready ───────────┤
     ├─ Turn green               │
     ├─ Start measure thread ───>│
     │                            ├─ Stabilize pose
     │                            ├─ Monitor motion
     │                            ├─ Detect punch
     │<─ Signal: Result ──────────┤
     ├─ Show result page         │
     └─ Cleanup camera ──────────>│
```

**Configuration:**
```python
ReactionTimeRunner(
    camera_index=0,              # Webcam device (0, 1, 2...)
    confidence_threshold=0.3,    # YOLO confidence (0-1)
    motion_threshold=20.0        # Pixel distance for punch
)
```

**Code Location:**
- `ReactionTestPage`, `ReactionResultPage` in main_gui.py
- `reaction_time/reaction_time_runner.py` - Core logic
- `reaction_time/cv_sample.py` - Standalone testing

---

### 4. Performance Testing: Power Measurement

**How It Works:**

```
1. User Clicks "Power" from Performance Page
   └─ Navigate to PowerInstructionsPage

2. PowerInstructionsPage
   ├─ Display instructions: "Connect sensor to COM port"
   ├─ User clicks "Start"
   └─ Navigate to Countdown (5 seconds)

3. PowerPunchPage
   ├─ Display: "PUNCH THE BAG!"
   ├─ Background thread:
   │  ├─ Open serial port (default: COM12, 115200 baud)
   │  ├─ Read accelerometer data from sensor
   │  ├─ Parse format: "Total_Accel:XX.XX"
   │  ├─ Detect punch if acceleration > threshold (35.0 m/s²)
   │  ├─ Track peak acceleration
   │  ├─ Debounce (300ms) to prevent double-counting
   │  └─ Collect 10 punches or timeout (120s)
   └─ Navigate to PowerResultPage

4. PowerResultPage
   ├─ Display: "Peak Force: XX.XX m/s²"
   ├─ Convert to human-readable (optional)
   └─ Options: Restart / Back
```

**Serial Data Flow:**
```
Accelerometer Sensor → Serial Port (COM12) → Python
                                              │
                      "Total_Accel:45.23"    │
                      "Total_Accel:12.87"    │
                      "Total_Accel:89.45" ←─ PUNCH! (>35.0)
                                              │
                                              ├─ Record: 89.45
                                              └─ Update peak if higher
```

**Debouncing Logic:**
```python
last_punch_time = None
debounce_ms = 300

while measuring:
    if acceleration > threshold:
        current_time = time_ms()
        if last_punch_time is None or (current_time - last_punch_time) > debounce_ms:
            # Valid punch!
            record_punch(acceleration)
            last_punch_time = current_time
        else:
            # Too soon, ignore (debounce)
            continue
```

**Configuration:**
```python
measure_peak(
    port="COM12",           # Serial port (check Device Manager)
    baud=115200,           # Sensor baud rate
    threshold=35.0,        # Punch detection threshold (m/s²)
    max_punches=10,        # Number of punches to collect
    debounce_ms=300,       # Minimum time between punches
    max_duration_s=120.0   # Timeout (seconds)
)
```

**Code Location:**
- `PowerPunchPage`, `PowerResultPage` in main_gui.py
- `power/power_runner.py` - Serial communication logic

---

### 5. Self-Select Mode (Custom Sequences)

**How It Works:**

```
1. User Opens Training → Punch Combinations → Self-Select
   └─ Navigate to SelfSelectSequencePage

2. SelfSelectSequencePage
   ├─ Display input field for custom sequence
   ├─ User enters: "Jab-Cross-Hook-Uppercut"
   ├─ Click "Add Sequence"
   ├─ Sequence added to training_config.custom_sequences[]
   └─ Can add multiple sequences

3. Start Training
   ├─ Configure parameters (rounds, speed, time)
   ├─ Training session displays custom sequences
   └─ User trains with their own combinations

4. Custom Sequences
   ├─ NOT saved to combo database
   ├─ NOT tracked for mastery/progress
   ├─ Just for practice
   └─ Cleared when session ends
```

**Features:**
- Available to ALL user levels (Beginner/Intermediate/Advanced)
- No restrictions on sequence content
- Multiple sequences can be added
- Used for creative practice outside structured curriculum

**Code Location:** `TechniquesPage`, `TrainingConfig.custom_sequences` in main_gui.py

---

### 6. Sparring Mode

**How It Works:**

```
1. User Opens Training → Sparring
   ├─ Check user level
   ├─ If Beginner: Button disabled (locked)
   └─ If Intermediate/Advanced: Navigate to SparPage

2. SparPage
   ├─ Configure parameters
   ├─ Select opponent style (optional):
   │  ├─ Pressure Fighter
   │  ├─ Counter Puncher
   │  ├─ Balanced Boxer
   │  ├─ Out Boxer
   │  └─ Random
   └─ Start training session

3. Training Session
   ├─ Display round/timer as usual
   ├─ [Future] AI opponent patterns
   ├─ [Future] Adaptive difficulty
   └─ Track performance

4. Results
   └─ Show session summary
```

**Unlock Requirement:**
- User must be at Intermediate level or higher
- Unlocked automatically when user advances from Beginner

**Code Location:** `SparPage`, `TrainingPage.showEvent()` in main_gui.py

---

**Code Location:** `SparPage`, `TrainingPage.showEvent()` in main_gui.py

---

## Architecture

### Application Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Main GUI (PySide6)                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │          QMainWindow (Application Shell)              │  │
│  │  ┌────────────────────────────────────────────────┐  │  │
│  │  │      QStackedWidget (Page Container)           │  │  │
│  │  │  ┌──────────┐  ┌──────────┐  ┌──────────┐    │  │  │
│  │  │  │ Login    │  │ HomePage │  │ Training │    │  │  │
│  │  │  │ Page (0) │  │  Page (2)│  │ Page (3) │... │  │  │
│  │  │  └──────────┘  └──────────┘  └──────────┘    │  │  │
│  │  └────────────────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────────────┘ │
└───────┬─────────────────────────────┬───────────────┬─────┘
        │                             │               │
        v                             v               v
┌──────────────┐           ┌──────────────┐  ┌──────────────┐
│  Users.csv   │           │ Combos.db    │  │ Worker       │
│              │           │              │  │ Threads      │
│ - username   │           │ Tables:      │  │              │
│ - pass_hash  │           │ - combos     │  │ - Camera     │
│ - level      │           │ - perf_hist  │  │ - YOLO       │
│ - progress   │           │              │  │ - Serial     │
└──────────────┘           └──────────────┘  └──────────────┘
```

### Threading Model

The application uses **Qt threads (QThread)** to prevent UI blocking during heavy operations:

```
Main Thread (QMainWindow)
    │
    ├─ UI Rendering (always responsive)
    ├─ Page Navigation (instant)
    ├─ Button Clicks (immediate)
    └─ Signal/Slot Processing
    
Worker Threads (QThread)
    │
    ├─ Reaction Time Thread
    │  ├─ Camera initialization
    │  ├─ YOLO pose inference (~100-150ms/frame)
    │  ├─ Motion detection
    │  └─ Emit signal → Main thread updates UI
    │
    ├─ Power Measurement Thread  
    │  ├─ Serial port communication
    │  ├─ Data parsing
    │  ├─ Peak tracking
    │  └─ Emit signal → Main thread shows results
    │
    └─ Training Session Thread (future)
       ├─ Video recording
       ├─ Action recognition
       └─ Emit signal → Update progress
```

**Why Threading?**
- ❌ **Without threads**: UI freezes during camera/YOLO operations
- ✅ **With threads**: UI remains responsive, user can cancel operations

### Data Flow

```
User Input (Button Click)
    ↓
Main Thread (validate input)
    ↓
Create Worker Thread
    ↓
Worker Thread runs (camera, YOLO, serial, etc.)
    ↓
Emit Signal with result
    ↓
Main Thread receives signal (via Qt event loop)
    ↓
Update UI (show results, navigate page)
```

**Example: Reaction Time Flow**
```python
# Main thread
def on_start_clicked(self):
    self.status_label.setText("Setting up camera...")
    # Don't block here!
    
    # Create worker thread
    self.init_thread = InitializationThread()
    self.init_thread.finished_signal.connect(self.on_initialization_done)
    self.init_thread.start()  # Runs in background
    
# Worker thread (background)
class InitializationThread(QThread):
    finished_signal = Signal(bool, str)
    
    def run(self):
        success, error = rt_runner.initialize_camera_and_model()
        self.finished_signal.emit(success, error)  # Send back to main

# Main thread receives result
def on_initialization_done(self, success, error):
    if success:
        self.turn_green()  # Update UI
    else:
        self.show_error(error)  # Update UI
```

---

## Modules

### 1. main_gui.py (4235 lines)

**Core Classes:**

#### TrainingConfig (Dataclass)
```python
@dataclass
class TrainingConfig:
    rounds: int = 12
    time_minutes: int = 3
    time_seconds: int = 0
    rest_minutes: int = 1
    rest_seconds: int = 0
    speed: str = "100%"
    difficulty: Optional[str] = None
    battle_style: Optional[str] = None
    custom_sequences: List[str] = field(default_factory=list)
```
- Stores all training parameters
- Methods: `get_time_str()`, `set_time_from_str()`, `to_dict()`, `reset()`

#### PageIndex (Constants)
```python
class PageIndex:
    LOGIN = 0
    SIGNUP = 1
    HOMEPAGE = 2
    USER_MANAGEMENT = 3
    TRAINING = 4
    TECHNIQUES = 5
    PUNCH_COMBINATIONS = 6
    # ... total 23 pages
```

#### Page Classes
All pages inherit from `QWidget` and follow this pattern:
```python
class SomePage(QWidget):
    def __init__(self, stacked_widget, main_window=None):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.main_window = main_window
        self.setup_ui()
        
    def setup_ui(self):
        # Create layout and widgets
        pass
        
    def on_button_clicked(self):
        # Navigate or perform action
        self.stacked_widget.setCurrentIndex(PageIndex.NEXT_PAGE)
```

**Key Pages:**

| Page | Purpose | Key Methods |
|------|---------|-------------|
| LoginPage | User authentication | `on_login_clicked()`, `hash_password()` |
| Homepage | Main menu | Navigation buttons to Training/Performance/Others |
| PunchCombinationPage | Select difficulty | `showEvent()` - enables/disables based on level |
| TechCorrSessionPage | Active training | `start_training()`, `timer callbacks` |
| ReactionTestPage | Reaction measurement | `start_test()`, `go_green()`, threading |
| PowerPunchPage | Power measurement | `start_punch_test()`, `on_punch_detected()` |

---

### 2. combo_curriculum/ Module

Complete documentation: [combo_curriculum/README.md](combo_curriculum/README.md)

**Main Components:**

#### ComboCurriculum Class
```python
from combo_curriculum import ComboCurriculum

with ComboCurriculum("setup/combos.db") as curriculum:
    # Get next combo to practice
    next_combo = curriculum.get_next_combo("Beginner")
    
    # Record training score
    curriculum.update_score("beginner_001", 4.2)
    
    # Get progress statistics
    progress = curriculum.get_level_progress("Beginner")
    
    # Check if user can level up
    can_advance = curriculum.check_progression_eligibility("Beginner")
```

**Key Methods:**
- `get_combos_by_difficulty(difficulty)` - Get all combos at a level
- `get_next_combo(difficulty)` - Sequential progression
- `update_score(combo_id, score)` - Record session, calculate mastery
- `get_combo_stats(combo_id)` - Detailed combo statistics
- `get_level_progress(difficulty)` - Overall level statistics
- `check_progression_eligibility(difficulty)` - Can user level up?
- `get_next_difficulty(difficulty)` - Get next level name

#### Action Recognition Placeholder
```python
from combo_curriculum import get_performance_score, USE_ACTION_RECOGNITION

# Currently returns fixed 3.0 for testing
score = get_performance_score()  # 3.0

# Future: When USE_ACTION_RECOGNITION = True
score = get_performance_score(
    video_path="recording.mp4",
    combo_id="beginner_001"
)  # Real score from ML model
```

---

### 3. reaction_time/ Module

#### ReactionTimeRunner Class
```python
from reaction_time import reaction_time_runner as rt

# Initialize
runner = rt.ReactionTimeRunner(
    camera_index=0,
    confidence_threshold=0.3,
    motion_threshold=20.0
)

# Use
success, error = runner.initialize_camera_and_model()
if success:
    result = runner.measure_reaction_time()
    print(f"Reaction: {result.reaction_ms}ms")
runner.cleanup()
```

**ReactionResult Dataclass:**
```python
@dataclass
class ReactionResult:
    success: bool
    reaction_ms: Optional[float] = None
    status: Optional[str] = None  # "too_soon", "timeout", "error"
    error_message: Optional[str] = None
```

**Key Features:**
- YOLO11s pose estimation (17 keypoints)
- Motion detection via Euclidean distance
- Timeout: 2.5 seconds
- Warmup: 10 frames for stable detection

---

### 4. power/ Module

#### measure_peak() Function
```python
from power import power_runner

peak_force = power_runner.measure_peak(
    port="COM12",
    baud=115200,
    threshold=35.0,
    max_punches=10,
    debounce_ms=300,
    max_duration_s=120.0
)

print(f"Peak force: {peak_force} m/s²")
```

**Features:**
- Serial communication with accelerometer
- Peak tracking across multiple punches
- Debouncing (default 300ms)
- Timeout protection

---

### 5. setup/ Module

**Database Setup Scripts:**

1. `setup_combo_database.py` - **Run this first!**
   - Creates combos.db
   - Calls create_database_schema.py
   - Calls populate_combos.py
   - One-command setup

2. `create_database_schema.py`
   - Creates SQLite tables
   - Tables: combos, performance_history

3. `populate_combos.py`
   - Inserts 50 combos:
     - 15 Beginner (beginner_001 to beginner_015)
     - 20 Intermediate (intermediate_001 to intermediate_020)
     - 15 Advanced (advanced_001 to advanced_015)

---

## Configuration

### Reaction Time Settings

**In reaction_time_runner.py:**
```python
ReactionTimeRunner(
    camera_index=0,              # Webcam device (0, 1, 2...)
    confidence_threshold=0.3,    # YOLO confidence (0.0-1.0)
    motion_threshold=20.0        # Pixel distance for punch detection
)
```

**Tuning:**
- **Too many "Too Soon" errors?** → Increase `motion_threshold` to 25.0 or 30.0
- **Missing punches?** → Decrease `motion_threshold` to 15.0
- **Poor pose detection?** → Increase lighting, check camera position

### Power Measurement Settings

**In power_runner.py:**
```python
measure_peak(
    port="COM12",           # Serial port (check Device Manager)
    baud=115200,           # Match sensor baud rate
    threshold=35.0,        # Punch detection threshold (m/s²)
    max_punches=10,        # Punches to collect
    debounce_ms=300        # Min time between punches
)
```

**Finding COM Port (Windows):**
```powershell
Get-WmiObject Win32_SerialPort | Select-Object Name, DeviceID
```

### User Progression Settings

**Mastery Thresholds** (in combo_curriculum/curriculum.py):
```python
# Beginner threshold
threshold_beginner = 3.0 / 5.0  # 60%

# Intermediate/Advanced threshold  
threshold_higher = 4.0 / 5.0  # 80%
```

**Level-Up Requirements** (in combo_curriculum/curriculum.py):
```python
# Beginner → Intermediate
# ALL 15 combos: total_attempts >= 5 AND mastery_score >= 0.6

# Intermediate → Advanced
# ALL 20 combos: total_attempts >= 5 AND mastery_score >= 0.8
```

---
└── SparPage (12) or BattlePage (13)
```

Configuration: Rounds → Speed → Time → Rest → Countdown (9) → Training Session (10)

### 3. Performance Testing Flow

```
PerformancePage (14)
├── Power: Instructions (15) → Test (16) → Results (17)
├── Reaction: Instructions (19) → Test (20) → Results (21)
└── Stamina: Instructions (18)
```

#### Reaction Test Sequence

```
1. ReactionInstructionsPage (19)
   ↓ [Start]
2. CountdownPage (9) [optional - can skip on restart]
   ↓ [Countdown completes]
3. ReactionTestPage (20)
   ├─ Red screen: "Setting up camera..."
   ├─ Initialization in background thread
   ├─ Turn green after 5-8 second delay
   ├─ Measurement in background thread
   ↓
4. ReactionResultPage (21)
   ├─ Display reaction time (milliseconds)
   ├─ Or error status (Too Soon / Timeout)
   └─ Options: History / Restart / Back
```

#### Power Test Sequence

```
1. PowerInstructionsPage (15)
   ↓ [Start]
2. CountdownPage (9)
   ↓ [Countdown completes]
3. PowerPunchPage (16)
   ├─ Connect to serial sensor
   ├─ Listen for punch impacts
   ├─ Measure peak force
   ↓
4. PowerResultPage (17)
   ├─ Display peak punch force (m/s²)
   └─ Options: Restart / Back
```

---

## Configuration

### Training Config

Edit parameters in **ReactionInstructionsPage** or programmatically:

```python
config = TrainingConfig()
config.rounds = 5
config.set_time_from_str("3:30")
config.speed = "75%"
config.difficulty = "Advanced"
```

### Reaction Time Settings

Adjust in **ReactionTimeRunner**:

```python
runner = ReactionTimeRunner(
    camera_index=0,              # Change camera if multiple available
    confidence_threshold=0.3,    # Lower = more sensitive (0.0-1.0)
    motion_threshold=20.0        # Lower = more sensitive, higher = less false positives
)
```

**Tuning Tips**:
- **Too many "Too Soon"?**: Increase `motion_threshold` (e.g., 25.0)
- **Missing punches?**: Decrease `motion_threshold` (e.g., 15.0)
- **Poor pose detection?**: Improve lighting, increase `confidence_threshold`

### Power Measurement Settings

Edit in **PowerPunchPage**:

```python
power_runner.measure_peak(
    port="COM12",           # Check Device Manager for correct port
    baud=115200,           # Match your sensor's baud rate
    threshold=35.0,        # Punch detection threshold (m/s²)
    max_punches=10,        # How many punches to measure
    debounce_ms=300        # Time between punches (prevents double-counting)
)
```

**Serial Port Detection** (Windows):
```powershell
Get-WmiObject Win32_SerialPort | Select-Object Name, DeviceID
```

---

## Troubleshooting

### Reaction Time Issues

#### "Too Soon" on Every Attempt
- **Cause**: Pose detection instability or sensitive motion threshold
- **Fix**: 
  - Increase `motion_threshold` from 20.0 to 25.0 or 30.0
  - Ensure good lighting
  - Stand at proper distance (2-3 feet from camera)

#### "Timeout" on Valid Punches
- **Cause**: Motion threshold too high or slow punch
- **Fix**: 
  - Decrease `motion_threshold` to 15.0
  - Punch faster/sharper
  - Check camera FPS (should be 30+)

#### Camera Not Opening
- **Cause**: Camera in use, wrong index, or permission issue
- **Fix**:
  - Close other camera apps
  - Try different `camera_index` (0, 1, 2...)
  - Check camera permissions in Windows Settings

#### Model Not Found
- **Error**: `Model file not found at: ../models/yolo11s-pose.pt`
- **Fix**: 
  - Download model: https://github.com/ultralytics/assets/releases/
  - Place in `../models/` folder
  - Or let YOLO auto-download (requires internet)

### Power Measurement Issues

#### Serial Port Not Found
- **Error**: `Failed to open serial port`
- **Fix**:
  - Verify sensor is connected
  - Check port name in Device Manager
  - Update port in code (e.g., "COM3" instead of "COM12")
  - Ensure only one app is using the port

#### No Data from Sensor
- **Cause**: Wrong baud rate or data format
- **Fix**:
  - Check sensor documentation for correct baud rate
  - Verify data format matches: `Total_Accel:XX.XX`
  - Test with serial monitor first

#### PySerial Import Error
- **Fix**: `pip install pyserial`

### GUI Issues

#### Buttons Not Responsive
- **Cause**: Worker thread blocking
- **Fix**: Check that all heavy operations run in QThread (not main thread)

#### Page Navigation Fails
- **Cause**: PageIndex out of range or widget not added
- **Fix**: Verify all pages are added to stacked_widget in correct order

#### Countdown Skips
- **Cause**: Timer not stopped properly
- **Fix**: Ensure `green_timer.stop()` is called before `start()`

---

## Development

### Adding New Pages

1. Create new class inheriting from `QWidget`
2. Add `PageIndex` constant
3. Instantiate and add to `stacked_widget` in main window
4. Connect navigation buttons to `setCurrentIndex()`

Example:
```python
class NewPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        # ... setup UI ...
    
    def on_button_clicked(self):
        self.stacked_widget.setCurrentIndex(PageIndex.HOMEPAGE)
```

### Running Tests

For reaction time module:
```bash
cd reaction_time
python cv_sample.py --motion-threshold 20.0 --camera 0
```

### Debugging

Enable debug output:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## Troubleshooting

### 1. Camera Issues

**Symptom**: "Failed to initialize camera" during reaction test

**Possible Causes:**
- Another application is using the webcam (Teams, Zoom, Skype, etc.)
- Wrong camera index
- Missing camera drivers

**Solutions:**

1. **Close other camera applications:**
   ```powershell
   # Check processes using camera
   Get-Process | Where-Object {$_.ProcessName -match "zoom|teams|skype"}
   ```

2. **Try different camera index:**
   ```python
   # In reaction_time_runner.py (line ~40)
   ReactionTimeRunner(camera_index=1)  # Default is 0
   ```

3. **Verify camera detection:**
   ```bash
   python -c "import cv2; print('Working' if cv2.VideoCapture(0).read()[0] else 'Failed')"
   ```

4. **Check OpenCV installation:**
   ```bash
   pip show opencv-python
   # Reinstall if needed
   pip install --upgrade opencv-python
   ```

---

### 2. Serial Port Issues

**Symptom**: "Failed to open port COM12" during power test

**Possible Causes:**
- Arduino/sensor not connected
- Wrong COM port
- Port already in use (Arduino IDE Serial Monitor)
- Missing USB drivers

**Solutions:**

1. **Find correct COM port (Windows):**
   ```powershell
   Get-WmiObject Win32_SerialPort | Select-Object Name, DeviceID
   # Example output: USB Serial Device (COM12)
   ```

   Device Manager → Ports (COM & LPT) → Note the COM number

2. **Update port in power_runner.py:**
   ```python
   # Line ~80
   measure_peak(port="COM3")  # Change COM12 to your port
   ```

3. **Close Arduino IDE Serial Monitor:**
   - Only ONE program can use the COM port at a time
   - Close Serial Monitor before running power test

4. **Check sensor connection:**
   ```bash
   # Test with Arduino IDE Serial Monitor first
   # Open Arduino IDE → Tools → Serial Monitor → Set baud to 115200
   # You should see: Total_Accel:XX.XX
   ```

5. **Install CH340/FTDI drivers:**
   - Some Arduino clones need CH340 drivers
   - Download: [CH340 Drivers](https://sparks.gogo.co.nz/ch340.html)

---

### 3. Reaction Time Issues

**Symptom**: "Too soon! No movement detected"

**Cause:** Punching before screen turns green OR motion threshold too high

**Solutions:**

1. **Wait for green screen:**
   - Do NOT punch during red screen
   - Only punch when screen turns GREEN and shows "PUNCH NOW!"

2. **Lower motion threshold (if punches not detected):**
   ```python
   # In reaction_time_runner.py (line ~40)
   ReactionTimeRunner(motion_threshold=15.0)  # Default: 20.0
   ```

**Symptom**: "Timeout! No punch detected within 2.5 seconds"

**Cause:** Motion threshold too high OR punching too slowly

**Solutions:**

1. **Decrease motion threshold:**
   ```python
   ReactionTimeRunner(motion_threshold=15.0)  # More sensitive
   ```

2. **Punch more forcefully:**
   - Ensure full arm extension
   - Stand closer to camera (1-2 meters)

3. **Check camera positioning:**
   - Camera should see full upper body
   - Ensure good lighting
   - Avoid backlit positions (window behind you)

4. **Check YOLO model confidence:**
   ```python
   ReactionTimeRunner(confidence_threshold=0.2)  # Default: 0.3 (lower = more detections)
   ```

---

### 4. Database Issues

**Symptom**: "No such table: combos" or "Database not found"

**Cause:** Database not initialized

**Solution:**

```bash
cd setup
python setup_combo_database.py
# Output: Database setup complete! combos.db created with 50 combos.
```

**Symptom**: "UNIQUE constraint failed: performance_history.id"

**Cause:** Database corruption or duplicate IDs

**Solution:**

```bash
# Backup existing database
cd setup
copy combos.db combos_backup.db

# Recreate database
python setup_combo_database.py
```

---

### 5. User Login Issues

**Symptom**: "User not found" even though user exists

**Cause:** `users.csv` corruption or format issue

**Solution:**

1. **Check users.csv format:**
   ```csv
   username,password_hash,level,progress
   testuser,5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8,Beginner,0.0
   ```

2. **Ensure no extra spaces or tabs:**
   ```bash
   # Remove trailing whitespace
   (Get-Content users.csv) | ForEach-Object { $_.TrimEnd() } | Set-Content users.csv
   ```

**Symptom**: Cannot create new user (no Sign Up page)

**Solution:**
- Sign Up is only accessible from Login page
- Click "Sign Up" button on Login page (PageIndex.SIGNUP = 1)

---

### 6. Button Disabled Issues

**Symptom**: "Intermediate" or "Advanced" buttons are greyed out in Punch Combinations

**Cause:** This is EXPECTED behavior for user progression

**Explanation:**
- Beginners can only access "Beginner" and "Self-Select"
- Must complete ALL 15 beginner combos with score ≥3.0 to unlock Intermediate
- Must complete ALL 20 intermediate combos with score ≥4.0 to unlock Advanced

**Check your level:**
1. Go to "Manage Users" from Login/Homepage
2. Find your username in the table
3. Check "Level" and "Progress (%)" columns
4. If progress < 80%, you cannot level up yet

**Force level-up (for testing):**
```python
# Manually edit users.csv
testuser,password_hash,Intermediate,0.0  # Change Beginner → Intermediate
```

---

### 7. YOLO Model Issues

**Symptom**: "Model file not found: models/yolo11s-pose.pt"

**Cause:** YOLO weights not downloaded

**Solution:**

```bash
# Download YOLO11s-pose model
cd models
# Visit: https://github.com/ultralytics/ultralytics
# Or use ultralytics CLI:
yolo pose predict model=yolo11s-pose.pt source=0  # Downloads automatically
```

**Symptom**: Slow YOLO inference (>300ms per frame)

**Solutions:**

1. **Use GPU acceleration:**
   ```bash
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
   ```

2. **Lower camera resolution:**
   ```python
   # In reaction_time_runner.py after cap.open()
   cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
   cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
   ```

3. **Check CPU usage:**
   - Close other applications
   - YOLO inference is CPU-intensive without GPU

---

### 8. Threading Issues

**Symptom**: UI freezes during reaction/power test

**Cause:** Worker thread not properly created or signals not connected

**Solution:**

1. **Check thread initialization:**
   ```python
   # In ReactionTestPage (line ~450)
   self.measure_thread = MeasurementThread()
   self.measure_thread.finished_signal.connect(self.on_measurement_completed)
   self.measure_thread.start()  # Must call .start()
   ```

2. **Verify QThread import:**
   ```python
   from PySide6.QtCore import QThread, Signal
   ```

3. **Check for blocking calls in main thread:**
   ```python
   # ❌ BAD (blocks UI)
   result = rt_runner.measure_reaction_time()  
   
   # ✅ GOOD (non-blocking)
   thread = MeasurementThread()
   thread.start()
   ```

---

### 9. Module Import Errors

**Symptom**: "ModuleNotFoundError: No module named 'combo_curriculum'"

**Cause:** Not running from correct directory or PYTHONPATH not set

**Solution:**

```bash
# Ensure you're in the GUI/ directory
cd GUI
python main_gui.py

# Or set PYTHONPATH (if running from elsewhere)
$env:PYTHONPATH = "C:\path\to\IS431\GUI"
python main_gui.py
```

**Symptom**: "ImportError: cannot import name 'ComboCurriculum'"

**Cause:** `combo_curriculum/__init__.py` not exporting correctly

**Solution:**

Check `combo_curriculum/__init__.py` contains:
```python
from .curriculum import ComboCurriculum
from .action_recognition_placeholder import get_performance_score, USE_ACTION_RECOGNITION

__all__ = [
    'ComboCurriculum',
    'get_performance_score',
    'USE_ACTION_RECOGNITION'
]
```

---

### 10. Performance Issues

**Symptom**: Application feels slow or laggy

**Solutions:**

1. **Close background applications:**
   - OBS, video editors, browsers with many tabs
   - Free up RAM (recommended: 8GB+)

2. **Reduce YOLO inference frequency:**
   ```python
   # In measure_reaction_time(), add frame skipping
   if frame_count % 2 == 0:  # Process every 2nd frame
       results = model(frame)
   ```

3. **Lower video quality:**
   ```python
   cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
   cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
   ```

4. **Check disk space:**
   - SQLite needs disk space for database operations
   - Ensure at least 1GB free space

---

### 11. Common Error Messages

| Error Message | Meaning | Solution |
|---------------|---------|----------|
| "Failed to initialize camera" | Camera already in use or not detected | Close other camera apps, check device index |
| "Failed to open port COMxx" | Serial port in use or wrong port | Close Arduino IDE, verify COM port |
| "No such table: combos" | Database not initialized | Run `setup_combo_database.py` |
| "UNIQUE constraint failed" | Database corruption | Recreate database or restore backup |
| "Model file not found" | YOLO weights missing | Download yolo11s-pose.pt to models/ |
| "Too soon! No movement detected" | Punched before green screen | Wait for green, or lower motion threshold |
| "Timeout! No punch detected" | Punch not detected or too slow | Punch harder, check camera position |
| "User not found" | User doesn't exist in users.csv | Check CSV format, create user via Sign Up |

---

---

## License

This project is part of IS431 (CDE4301) at NUS.

---

## Support

For issues or questions:
1. Check **Troubleshooting** section
2. Review console output for error messages
3. Test standalone modules (`cv_sample.py` for reaction time)
4. Check camera/sensor hardware connections
