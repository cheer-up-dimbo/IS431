# Test Suite

This directory contains all test scripts for the Combo Curriculum module.

## Test Files

### `test_curriculum.py`
Tests basic database operations:
- Database connection
- Querying combos by difficulty level
- Retrieving specific combo by ID
- Database schema validation

**Run:** `python -m combo_curriculum.tests.test_curriculum`

### `test_scoring.py`
Tests the scoring and progression system:
- Recording performance scores
- Calculating mastery from last 5 sessions
- Sequential combo progression with `get_next_combo()`
- Mastery threshold validation

**Run:** `python -m combo_curriculum.tests.test_scoring`

### `test_progress.py`
Tests progress tracking and statistics:
- `get_combo_stats()` - Individual combo statistics
- `get_level_progress()` - Overall level progress
- Combo categorization (mastered/in-progress/struggling)
- Progress dashboard generation

**Run:** `python -m combo_curriculum.tests.test_progress`

### `test_progression.py`
Tests level progression eligibility:
- `check_progression_eligibility()` - Validate level-up requirements
- `get_next_difficulty()` - Next level lookup
- Progression simulation across levels
- Requirement validation (15 Beginner, 20 Intermediate, 15 Advanced)

**Run:** `python -m combo_curriculum.tests.test_progression`

### `test_action_recognition.py`
Tests action recognition placeholder:
- `get_performance_score()` placeholder function
- `USE_ACTION_RECOGNITION` flag testing
- Integration workflow testing
- Future implementation documentation

**Run:** `python -m combo_curriculum.tests.test_action_recognition`

## Running All Tests

From the `GUI` directory:

```bash
# Run all tests
python -m combo_curriculum.tests.test_curriculum
python -m combo_curriculum.tests.test_scoring
python -m combo_curriculum.tests.test_progress
python -m combo_curriculum.tests.test_progression
python -m combo_curriculum.tests.test_action_recognition
```

Or run them directly:

```bash
cd combo_curriculum/tests
python test_curriculum.py
python test_scoring.py
python test_progress.py
python test_progression.py
python test_action_recognition.py
```

## Test Database

All tests use the database located at:
```
GUI/setup/combos.db
```

Make sure to run `setup/setup_combo_database.py` first if the database doesn't exist.

## Test Coverage

- ✅ Database queries and connections
- ✅ Score recording and mastery calculation
- ✅ Sequential combo progression
- ✅ Progress tracking and statistics
- ✅ Level progression eligibility
- ✅ Action recognition placeholder
- 🔄 Integration with main GUI (manual testing required)
- 🔄 Real action recognition model (to be implemented)
