# Boxing Training GUI Application

A comprehensive PySide6-based GUI application for boxing training with real-time performance tracking, including reaction time measurement and punch force analysis.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Modules](#modules)
- [GUI Pages](#gui-pages)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

---

## Features

### 🥊 Training Modes
- **Technique Training**: Practice specific punch combinations
- **Spar Mode**: Interactive sparring practice with AI patterns
- **Battle Mode**: Realistic fight simulation with different opponent styles

### ⚡ Performance Testing
- **Power Testing**: Measure maximum punch force using accelerometer sensor
- **Reaction Time Testing**: YOLO-based pose estimation to detect punch response time
- **Stamina Training**: Endurance and speed drills

### ⚙️ Customization
- **Adjustable Timing**: Configure work/rest intervals per round
- **Speed Control**: Training speeds from 25% to 100%
- **Difficulty Levels**: Beginner to Advanced modes
- **Custom Punch Sequences**: Create and train custom combinations

### 📊 Results
- Real-time feedback on performance metrics
- Result history tracking
- Detailed performance analysis

---

## Installation

### Prerequisites
- Python 3.8+
- Virtual Environment (recommended)
- Webcam (for reaction time testing)
- Serial sensor (optional, for power testing)

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

### Step 3: Verify YOLO Model

Ensure the YOLO pose model is present:

```
../models/yolo11s-pose.pt
```

If not available, it will be automatically downloaded on first use.

### Step 4: Run the Application

```bash
python main_gui.py
```

---

## Project Structure

```
GUI/
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

## Quick Start

### Running the GUI

```bash
python main_gui.py
```

This will open the main application window.

### Testing Reaction Time (Standalone)

```bash
cd reaction_time
python cv_sample.py --motion-threshold 20.0
```

### Testing Power Measurement (Standalone)

Use the GUI's Power Testing feature to measure punch force from your sensor.

---

## Architecture

### Threading Model

The application uses **Qt threads** to prevent UI blocking:

```
┌─ Main UI Thread (QMainWindow)
│  ├─ Page Navigation (QStackedWidget)
│  └─ Signals/Slots for communication
│
├─ Worker Threads (QThread)
│  ├─ Reaction Time Measurement
│  └─ Power Measurement
│
└─ Backend Modules
   ├─ reaction_time_runner.py (YOLO inference)
   └─ power_runner.py (Serial communication)
```

### Data Flow

```
User Input (GUI)
    ↓
Worker Thread
    ↓
Backend Module (non-blocking)
    ↓
Qt Signal (result)
    ↓
UI Update (main thread)
    ↓
Result Display
```

### No UI Blocking
- All heavy operations (camera, YOLO inference, serial I/O) run in background threads
- GUI remains responsive during measurements
- Results sent back via Qt signals/slots

---

## Modules

### 1. **main_gui.py** (2899 lines)

Main application file containing:

#### Core Classes

- **TrainingConfig**: Dataclass for boxing training parameters
  - Rounds, timing, speed, difficulty, battle style
  - Methods: `get_time_str()`, `set_time_from_str()`, `to_dict()`, `reset()`

- **PageIndex**: Enum-like class defining all page indices
  - HOMEPAGE, TRAINING, TECHNIQUES, COUNTDOWN, etc.
  - Total: 23 distinct pages

- **ButtonStyle**: Centralized button styling
  - Predefined styles: PRIMARY, SECONDARY, BACK, INFO, etc.
  - Sizes: LARGE, MEDIUM, SMALL

#### Page Classes (QWidget)

| Page | Index | Purpose |
|------|-------|---------|
| **HomePage** | 0 | Main menu with training/performance options |
| **TrainingPage** | 1 | Training mode selection (Techniques, Spar) |
| **TechniquesPage** | 2 | Punch combination library |
| **PunchCombinationsPage** | 3 | List of punch combinations |
| **BasicParametersPage** | 4 | Configure rounds and difficulty |
| **RoundSelectionPage** | 5 | Select number of rounds (1-12) |
| **SpeedSelectionPage** | 6 | Select training speed (25%-100%) |
| **TimeSelectionPage** | 7 | Configure work time |
| **RestSelectionPage** | 8 | Configure rest time |
| **CountdownPage** | 9 | Countdown timer with "Wear Gloves" message |
| **TrainingSessionPage** | 10 | Active training timer |
| **SelfSelectSequencePage** | 11 | Custom punch sequence creation |
| **SparPage** | 12 | Spar training mode |
| **BattlePage** | 13 | Battle simulation mode |
| **PerformancePage** | 14 | Performance testing hub |
| **PowerInstructionsPage** | 15 | Power test instructions |
| **PowerPunchPage** | 16 | Power measurement screen |
| **PowerResultPage** | 17 | Display punch force results |
| **StaminaInstructionsPage** | 18 | Stamina test instructions |
| **ReactionInstructionsPage** | 19 | Reaction test instructions |
| **ReactionTestPage** | 20 | Red/green screen for reaction test |
| **ReactionResultPage** | 21 | Display reaction time results |
| **OthersPage** | 22 | Additional options |

#### Key Methods

- **ReactionTestPage**:
  - `start_test()`: Begin reaction test with camera setup
  - `go_green()`: Show "Punch Now!" and start measurement
  - `_start_initialization()`: Worker thread for camera/model init
  - `start_measurement()`: Worker thread for reaction detection

- **PowerPunchPage**:
  - `start_punch_test()`: Initialize power measurement
  - `on_punch_detected()`: Handle punch detection from sensor

### 2. **reaction_time/reaction_time_runner.py** (266 lines)

Backend for reaction time measurement using YOLO pose estimation.

#### ReactionResult (Dataclass)

```python
@dataclass
class ReactionResult:
    success: bool
    reaction_ms: Optional[float] = None
    status: Optional[str] = None  # "too_soon", "timeout", "error"
    error_message: Optional[str] = None
```

#### ReactionTimeRunner (Class)

**Initialization**:
```python
runner = ReactionTimeRunner(
    camera_index=0,              # Webcam device index
    confidence_threshold=0.3,    # YOLO confidence (0-1)
    motion_threshold=20.0        # Pixel distance for punch detection
)
```

**Key Methods**:

1. **initialize_camera_and_model()** → `(success: bool, error_msg: str | None)`
   - Loads YOLO11s pose estimation model
   - Opens camera with platform-specific settings
   - Runs 10 warmup frames for pose detector stability
   - Returns success status and error message if failed

2. **measure_reaction_time()** → `ReactionResult`
   - Assumes camera/model are initialized
   - Stabilizes pose detection (5 frames)
   - Listens for punch movement
   - Detects motion by comparing keypoint positions
   - Returns reaction time in milliseconds
   - Timeout: 2.5 seconds

3. **cleanup()** → Releases camera resources

**Global Functions** (for simple usage):

```python
success, error = reaction_time.initialize_camera_and_model()
result = reaction_time.measure_reaction_time()
reaction_time.cleanup()
```

#### How It Works

1. **Pose Detection**: YOLO11s detects 17 body keypoints (COCO format)
2. **Motion Calculation**: Euclidean distance between consecutive frame keypoints
3. **Punch Detection**: When motion exceeds threshold (default 20px), a punch is detected
4. **Timing**: Reaction time = elapsed time from function call to punch detection

#### Keypoint Indices (COCO-17)

```
0: Nose          1: L Eye         2: R Eye          3: L Ear          4: R Ear
5: L Shoulder    6: R Shoulder    7: L Elbow        8: R Elbow        9: L Wrist
10: R Wrist      11: L Hip        12: R Hip         13: L Knee        14: R Knee
15: L Ankle      16: R Ankle
```

### 3. **power/power_runner.py** (107 lines)

Backend for punch force measurement via accelerometer sensor.

#### measure_peak()

```python
def measure_peak(
    port: str = "COM12",           # Serial port
    baud: int = 115200,            # Baud rate
    threshold: float = 35.0,       # Acceleration threshold (m/s²)
    max_punches: int = 10,         # Number of punches to detect
    debounce_ms: int = 300,        # Minimum time between punches
    max_duration_s: Optional[float] = 120.0  # Timeout (seconds)
) -> float
```

**Returns**: Maximum acceleration detected (m/s²)

**Data Format**: Expects serial lines with format: `Total_Accel:XX.XX`

**Features**:
- Debouncing to prevent double-counting
- Timeout protection
- Peak tracking

---

## GUI Pages

### 1. Home Page (Index 0)

Main menu with three options:
- **Training**: Technique training, spar, and battle modes
- **Performance**: Power, reaction time, and stamina testing
- **Others**: Settings and additional options

### 2. Training Flow

```
TrainingPage (1)
├── TechniquesPage (2) → PunchCombinationsPage (3)
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

## Performance

### Reaction Time Measurement
- **Latency**: ~33ms per frame (30 FPS) for camera capture
- **YOLO Inference**: ~100-150ms per frame (GPU-accelerated)
- **Typical Reaction Time**: 150-500ms (human average)

### Power Measurement
- **Serial Read Rate**: 115200 baud ≈ 11,500 bytes/sec
- **Debounce**: 300ms default to prevent double-counting

### UI Responsiveness
- All operations run in background threads
- Main thread never blocked (responsive at all times)

---

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| PySide6 | ≥6.0.0 | GUI framework |
| ultralytics | ≥8.0.0 | YOLO pose detection |
| opencv-python | ≥4.5.0 | Video capture & processing |
| numpy | ≥1.20.0 | Numerical operations |
| pyserial | ≥3.5 | Serial sensor communication |

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
