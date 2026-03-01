# Examples

This directory contains example scripts demonstrating how to use the Combo Curriculum module in real-world scenarios.

## Example Files

### `example_training_flow.py`
**Complete training session workflow demonstration**

Shows the entire flow of a training session from start to finish:
1. Get next combo to practice with `get_next_combo()`
2. User performs the combo (video recording simulation)
3. Action recognition scores the performance with `get_performance_score()`
4. Update database with score using `update_score()`
5. Display session results and statistics
6. Check overall level progress
7. Check for level-up eligibility with `check_progression_eligibility()`
8. Display level-up notification if eligible

**Run:** `python combo_curriculum/examples/example_training_flow.py`

**Key Concepts Demonstrated:**
- Using the action recognition placeholder (returns 3.0)
- Complete training session lifecycle
- Progress tracking after each session
- Automatic level-up checking
- Integration with user management system

**Use Case:** Reference implementation for integrating combo curriculum into main GUI's training flow.

---

### `user_progress_example.py`
**User progress dashboard and tracking**

Demonstrates how to display comprehensive user progress information:
- Current level and progress percentage
- Combo mastery breakdown by difficulty
- Visual progress bars and statistics
- Next combo recommendations
- Time-based progress tracking
- Multi-user progress comparison

**Run:** `python combo_curriculum/examples/user_progress_example.py`

**Key Concepts Demonstrated:**
- Using `get_level_progress()` for statistics
- Using `get_combo_stats()` for individual combo details
- Calculating progress percentages
- Generating visual progress indicators
- User dashboard UI data preparation

**Use Case:** Reference for creating user progress dashboards and training summaries in the GUI.

---

## Running Examples

From the `GUI` directory:

```bash
# Training flow example
python combo_curriculum/examples/example_training_flow.py

# User progress example
python combo_curriculum/examples/user_progress_example.py
```

Or run from the examples directory:

```bash
cd combo_curriculum/examples
python example_training_flow.py
python user_progress_example.py
```

## Integration Guide

These examples show how to integrate the combo curriculum into your main application:

### 1. After Training Session

```python
from combo_curriculum import (
    ComboCurriculum,
    get_performance_score,
    integrate_score_after_training
)

# In your training completion handler
def on_training_complete(username, combo_id, video_path):
    with ComboCurriculum("setup/combos.db") as curriculum:
        # Get score from action recognition
        score = get_performance_score(video_path, combo_id)
        
        # Update database
        curriculum.update_score(combo_id, score)
        
        # Check for level-up
        current_level = get_user_level(username)
        if curriculum.check_progression_eligibility(current_level):
            next_level = curriculum.get_next_difficulty(current_level)
            if next_level:
                set_user_level(username, next_level)
                show_level_up_notification(username, next_level)
```

### 2. User Progress Dashboard

```python
from combo_curriculum import ComboCurriculum

def show_user_dashboard(username):
    user_level = get_user_level(username)
    
    with ComboCurriculum("setup/combos.db") as curriculum:
        progress = curriculum.get_level_progress(user_level)
        
        # Display statistics
        print(f"Mastered: {progress['mastered_combos']}/{progress['total_combos']}")
        print(f"In Progress: {progress['in_progress_combos']}")
        print(f"Struggling: {progress['struggling_combos']}")
```

### 3. Next Combo Selection

```python
from combo_curriculum import ComboCurriculum

def start_training_session(user_level):
    with ComboCurriculum("setup/combos.db") as curriculum:
        next_combo = curriculum.get_next_combo(user_level)
        
        if next_combo:
            # Show combo to user
            display_combo(next_combo['combo_name'], next_combo['combo_sequence'])
        else:
            # All combos mastered
            show_level_complete_message()
```

## Database Requirement

All examples require the combo database to be set up:

```bash
cd GUI/setup
python setup_combo_database.py
```

This creates `setup/combos.db` with:
- 15 Beginner combos
- 20 Intermediate combos
- 15 Advanced combos

## Next Steps

After reviewing these examples:

1. **Integrate into main GUI** - Use these patterns in `main_gui.py`
2. **Implement ML model** - Replace action recognition placeholder
3. **Add UI components** - Create progress bars, stats displays, notifications
4. **Test with real users** - Validate progression system with actual training data
