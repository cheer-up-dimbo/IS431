# Combo Curriculum Module

Python module for managing and querying boxing combination curriculum from SQLite database.

## Project Structure

```
combo_curriculum/
├── __init__.py                          # Package initialization, exports main classes/functions
├── curriculum.py                        # ComboCurriculum class - main database interface
├── action_recognition_placeholder.py   # Placeholder for action recognition (returns 3.0)
├── README.md                            # This file - main documentation
│
├── docs/                                # Detailed documentation
│   ├── README.md                       # Documentation index
│   ├── USER_PROGRESS.md                # User level and progress system
│   ├── SCORING_SYSTEM.md               # Scoring and mastery methodology
│   └── PROGRESSION_INTEGRATION.md      # Integration guide for main GUI
│
├── tests/                               # Test suite
│   ├── README.md                       # Testing documentation
│   ├── test_curriculum.py              # Basic database operation tests
│   ├── test_scoring.py                 # Scoring and progression tests
│   ├── test_progress.py                # Progress tracking tests
│   ├── test_progression.py             # Level-up eligibility tests
│   └── test_action_recognition.py      # Placeholder function tests
│
└── examples/                            # Usage examples
    ├── README.md                       # Examples documentation
    ├── example_training_flow.py        # Complete training session workflow
    └── user_progress_example.py        # User dashboard and progress tracking
```

## Database Structure

**File:** `combos.db` (located in `setup/` folder)

**Tables:**
- `combos`: Main combo data (combo_id, combo_name, combo_sequence, difficulty_level, mastery_score, total_attempts, last_trained_timestamp, created_date)
- `performance_history`: Performance tracking (id, combo_id, timestamp, performance_score)

**Combo Library:**
- 15 Beginner combos (IDs: beginner_001 to beginner_015)
- 20 Intermediate combos (IDs: intermediate_001 to intermediate_020)
- 15 Advanced combos (IDs: advanced_001 to advanced_015)

## Usage

### Action Recognition Placeholder

For testing the progression system without the ML model:

```python
from combo_curriculum import get_performance_score, USE_ACTION_RECOGNITION

# Check if real model is enabled
print(f"Using real model: {USE_ACTION_RECOGNITION}")  # False

# Get a placeholder score for testing
score = get_performance_score()
print(f"Score: {score}/5.0")  # Always returns 3.0

# When ML model is ready:
# 1. Set USE_ACTION_RECOGNITION = True in action_recognition_placeholder.py
# 2. Implement the model in get_performance_score()
# 3. Pass real video_path and combo_id
score = get_performance_score(
    video_path="recordings/session_001.mp4",
    combo_id="beginner_001"
)
```

### Basic Database Operations

```python
from combo_curriculum import ComboCurriculum

# Initialize with database path
curriculum = ComboCurriculum("setup/combos.db")

# Get all combos for a difficulty level
beginner_combos = curriculum.get_combos_by_difficulty("Beginner")
intermediate_combos = curriculum.get_combos_by_difficulty("Intermediate")
advanced_combos = curriculum.get_combos_by_difficulty("Advanced")

# Query a specific combo
combo = curriculum.get_combo_by_id("beginner_001")
if combo:
    print(f"Combo: {combo['combo_name']}")
    print(f"Sequence: {combo['combo_sequence']}")

# Get next combo for sequential progression
next_combo = curriculum.get_next_combo("Beginner")
if next_combo:
    print(f"Practice this combo: {next_combo['combo_name']}")
    
    # After training, update the score (0-5 from action recognition)
    performance_score = 4.2  # From your ML model
    curriculum.update_score(next_combo['combo_id'], performance_score)

# Close connection when done
curriculum.close()

# Or use context manager (recommended)
with ComboCurriculum("setup/combos.db") as curriculum:
    # Get next combo to practice
    next_combo = curriculum.get_next_combo("Beginner")
    
    if next_combo:
        # User practices the combo
        # Action recognition model scores the performance
        score = 4.5  # Score from 0-5
        
        # Update database with new score
        curriculum.update_score(next_combo['combo_id'], score)
        
        # Check if combo is now mastered
        updated_combo = curriculum.get_combo_by_id(next_combo['combo_id'])
        if updated_combo['total_attempts'] >= 5 and updated_combo['mastery_score'] >= 0.6:
            print(f"Mastered {updated_combo['combo_name']}!")
            
            # Get next combo in sequence
            next_up = curriculum.get_next_combo("Beginner")
            if next_up:
                print(f"Moving to: {next_up['combo_name']}")
            else:
                print("All Beginner combos mastered! 🎉")
    # Connection automatically closed
```

## Testing

All test scripts are located in the `tests/` directory. See [tests/README.md](tests/README.md) for detailed documentation.

**Run all tests:**

```bash
# From GUI directory
python combo_curriculum/tests/test_curriculum.py
python combo_curriculum/tests/test_scoring.py
python combo_curriculum/tests/test_progress.py
python combo_curriculum/tests/test_progression.py
python combo_curriculum/tests/test_action_recognition.py
```

**Or from the tests directory:**

```bash
cd combo_curriculum/tests
python test_curriculum.py
python test_scoring.py
python test_progress.py
python test_progression.py
python test_action_recognition.py
```

**What's tested:**
- ✅ Database queries and connections
- ✅ Score recording and mastery calculation
- ✅ Sequential combo progression with `get_next_combo()`
- ✅ Mastery thresholds for different difficulty levels
- ✅ Detailed combo statistics with `get_combo_stats()`
- ✅ Level-wide progress tracking with `get_level_progress()`
- ✅ Progression eligibility with `check_progression_eligibility()`
- ✅ Next difficulty level lookup with `get_next_difficulty()`
- ✅ Action recognition placeholder with `get_performance_score()`

## Examples

Usage examples are in the `examples/` directory. See [examples/README.md](examples/README.md) for detailed documentation.

**Run examples:**

```bash
# Complete training session workflow
python combo_curriculum/examples/example_training_flow.py

# User progress dashboard
python combo_curriculum/examples/user_progress_example.py
```

**What's demonstrated:**
- Complete training session lifecycle
- User progress tracking and dashboards
- Level-up checking and notifications
- Integration patterns for main GUI

## Class Methods

### ComboCurriculum Methods

### `__init__(db_path)`
Initialize and connect to database.

### `get_combos_by_difficulty(difficulty_level)`
Retrieve all combos for a specific difficulty level ("Beginner", "Intermediate", or "Advanced").
Returns list of combo dictionaries.

### `get_combo_by_id(combo_id)`
Query a specific combo by its ID (e.g., "beginner_001").
Returns combo dictionary or None if not found.

### `update_score(combo_id, score)`
Update combo performance after training session.

**Parameters:**
- `combo_id` - Combo identifier (e.g., "beginner_001")
- `score` - Performance score from action recognition model (0-5)

**Process:**
1. Inserts score into performance_history with timestamp
2. Gets last 5 scores for this combo
3. Calculates average of last 5 scores
4. Updates combos table:
   - Sets mastery_score = average of last 5 (normalized to 0-1)
   - Increments total_attempts by 1
   - Updates last_trained_timestamp

**Returns:** `bool` - True on success

```python
curriculum.update_score("beginner_001", 4.2)
```

### `get_next_combo(difficulty)`
Get the next combo that needs practice for sequential progression.

**Logic:**
- Returns first combo (by combo_id order) that is NOT mastered
- Not mastered = `total_attempts < 5` OR `mastery_score < threshold`
- Thresholds:
  - Beginner: 3.0/5.0 = 0.6
  - Intermediate/Advanced: 4.0/5.0 = 0.8

**Returns:** Combo dict with `{combo_id, combo_name, combo_sequence, mastery_score, total_attempts}` or None if all mastered

```python
next_combo = curriculum.get_next_combo("Beginner")
if next_combo:
    print(f"Practice: {next_combo['combo_name']}")
else:
    print("All combos mastered!")
```

### `get_combo_stats(combo_id)`
Get detailed statistics for a specific combo.

**Returns:** Dict with:
- `combo_name` - Name of the combo
- `combo_sequence` - Punch sequence
- `last_5_scores` - List of last 5 performance scores (0-5 scale)
- `average_score` - Average of last 5 scores (0-5 scale)
- `total_attempts` - Total number of training sessions
- `is_mastered` - True if >= 5 attempts AND >= threshold
- `threshold` - Mastery threshold (3.0 for Beginner, 4.0 for others)

```python
stats = curriculum.get_combo_stats("beginner_001")
print(f"Average: {stats['average_score']:.1f}/5.0")
print(f"Last 5: {stats['last_5_scores']}")
print(f"Mastered: {stats['is_mastered']}")
```

### `get_level_progress(difficulty)`
Get progress statistics for an entire difficulty level.

**Returns:** Dict with:
- `difficulty` - The difficulty level
- `total_combos` - Total number of combos at this level
- `mastered_combos` - Count of mastered combos (>= 5 attempts AND >= threshold)
- `in_progress_combos` - Count with < 5 attempts
- `struggling_combos` - Count with >= 5 attempts but below threshold

```python
progress = curriculum.get_level_progress("Beginner")
print(f"Mastered: {progress['mastered_combos']}/{progress['total_combos']}")
print(f"In Progress: {progress['in_progress_combos']}")
print(f"Struggling: {progress['struggling_combos']}")
```

### `check_progression_eligibility(current_difficulty)`
Check if user is eligible to progress to the next difficulty level.

**Progression Requirements:**
- Beginner → Intermediate: ALL 15 beginner combos have `total_attempts >= 5` AND `mastery_score >= 0.6` (3.0/5.0)
- Intermediate → Advanced: ALL 20 intermediate combos have `total_attempts >= 5` AND `mastery_score >= 0.8` (4.0/5.0)
- Advanced: Returns False (no next level)

**Returns:** `bool` - True if user meets criteria to level up, False otherwise

```python
# Check if user can advance from Beginner to Intermediate
if curriculum.check_progression_eligibility("Beginner"):
    next_level = curriculum.get_next_difficulty("Beginner")
    print(f"Ready to advance to {next_level}!")
    # Update user level in your system
else:
    print("Keep practicing to unlock Intermediate level")
```

### `get_next_difficulty(current_difficulty)`
Get the next difficulty level after the current one.

**Returns:** `str` or `None`
- "Beginner" → "Intermediate"
- "Intermediate" → "Advanced"
- "Advanced" → None

```python
next_level = curriculum.get_next_difficulty("Beginner")
print(f"Next level: {next_level}")  # Output: Intermediate

next_level = curriculum.get_next_difficulty("Advanced")
print(f"Next level: {next_level}")  # Output: None
```

### `close()`
Close database connection.

---

## Standalone Functions

### `get_performance_score(video_path=None, combo_id=None)`
Get performance score from action recognition model (currently a placeholder).

**Current Behavior (Placeholder):**
- Returns fixed score of 3.0 for testing
- Ignores video_path and combo_id parameters
- Controlled by `USE_ACTION_RECOGNITION = False` flag

**Future Implementation:**
When `USE_ACTION_RECOGNITION = True`:
- Will import and use real ML model from CV module
- Will process video_path through pose estimation
- Will compare performance to expected combo_id sequence
- Will return actual score based on technique accuracy

**Parameters:**
- `video_path` (str, optional): Path to training video recording
- `combo_id` (str, optional): Expected combo identifier

**Returns:** `float` - Score from 0.0 to 5.0

```python
from combo_curriculum import get_performance_score, USE_ACTION_RECOGNITION

# Current placeholder usage
score = get_performance_score()  # Returns 3.0
print(f"Score: {score}/5.0")

# Future real implementation (when USE_ACTION_RECOGNITION = True)
score = get_performance_score(
    video_path="recordings/session_001.mp4",
    combo_id="beginner_001"
)
```

### `integrate_score_after_training(curriculum, combo_id, video_path=None)`
Complete workflow helper that gets score and updates database.

**Parameters:**
- `curriculum`: ComboCurriculum instance
- `combo_id`: Combo identifier
- `video_path`: Video path (optional)

**Returns:** `dict` with:
- `success`: True/False
- `score`: Performance score (0-5)
- `average_score`: Average of last 5 sessions
- `total_attempts`: Total training sessions
- `is_mastered`: Mastery status
- `threshold`: Mastery threshold for combo's difficulty

```python
from combo_curriculum import ComboCurriculum, integrate_score_after_training

with ComboCurriculum("setup/combos.db") as curriculum:
    result = integrate_score_after_training(
        curriculum,
        combo_id="beginner_001",
        video_path="recordings/session.mp4"
    )
    
    if result['success']:
        print(f"Score: {result['score']:.1f}/5.0")
        print(f"Mastered: {result['is_mastered']}")
```

---

## Additional Resources

### 📚 Detailed Documentation
- [User Progress System](docs/USER_PROGRESS.md) - User levels, progress tracking, CSV structure
- [Scoring System](docs/SCORING_SYSTEM.md) - Performance scoring, mastery calculation, thresholds
- [Integration Guide](docs/PROGRESSION_INTEGRATION.md) - Complete guide for integrating into main GUI

### 🧪 Testing
- [Test Suite Documentation](tests/README.md) - Overview of all test scripts
- Run tests from `tests/` directory - See testing section above

### 💡 Examples
- [Examples Documentation](examples/README.md) - Overview of usage examples
- [Training Flow Example](examples/example_training_flow.py) - Complete training session workflow
- [User Progress Example](examples/user_progress_example.py) - Dashboard and progress tracking

### 🔧 Setup
Database setup is required before using the module:
```bash
cd GUI/setup
python setup_combo_database.py
```

This creates `setup/combos.db` with 50 total combos (15 Beginner, 20 Intermediate, 15 Advanced).

---

## Quick Start

1. **Setup database:**
   ```bash
   python setup/setup_combo_database.py
   ```

2. **Import and use:**
   ```python
   from combo_curriculum import ComboCurriculum, get_performance_score
   
   with ComboCurriculum("setup/combos.db") as curriculum:
       # Get next combo
       combo = curriculum.get_next_combo("Beginner")
       
       # Get score (placeholder: returns 3.0)
       score = get_performance_score()
       
       # Update database
       curriculum.update_score(combo['combo_id'], score)
       
       # Check progress
       progress = curriculum.get_level_progress("Beginner")
       print(f"Mastered: {progress['mastered_combos']}/{progress['total_combos']}")
   ```

3. **Run examples:**
   ```bash
   python combo_curriculum/examples/example_training_flow.py
   ```

4. **Run tests:**
   ```bash
   python combo_curriculum/tests/test_curriculum.py
   ```

---

## Project Status

| Component | Status | Notes |
|-----------|--------|-------|
| Database schema | ✅ Complete | 50 combos across 3 difficulty levels |
| ComboCurriculum class | ✅ Complete | All CRUD and query methods implemented |
| Scoring system | ✅ Complete | Last 5 sessions averaging |
| Progress tracking | ✅ Complete | `get_combo_stats()`, `get_level_progress()` |
| Level progression | ✅ Complete | `check_progression_eligibility()`, `get_next_difficulty()` |
| Action recognition | 🔄 Placeholder | Returns fixed 3.0, ready for ML model |
| Test suite | ✅ Complete | 5 test scripts covering all functionality |
| Documentation | ✅ Complete | README + 3 detailed docs + examples |
| GUI integration | 🔄 Pending | Ready to integrate with main_gui.py |

**Next Steps:**
1. Integrate combo curriculum into main GUI training flow
2. Implement real action recognition ML model
3. Create UI components for progress visualization
4. Add user notifications for level-ups and achievements


