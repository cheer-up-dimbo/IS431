# User Progress Integration Documentation

## Overview

The user progress system integrates combo mastery scores from the SQLite database with user levels and automatic advancement. Users start as Beginner and can progress to Intermediate and Advanced based on their combo mastery.

## User Data Structure

Each user has the following attributes stored in `users.csv`:

```csv
username,password_hash,level,progress
john_doe,<hash>,Beginner,45.5
jane_smith,<hash>,Intermediate,62.3
```

**Fields:**
- `username`: Unique username
- `password_hash`: SHA-256 hashed password
- `level`: Current skill level (Beginner, Intermediate, Advanced)
- `progress`: Progress percentage at current level (0.0-100.0)

## Level Progression System

### Advancement Thresholds

Users automatically level up when they reach **80% progress** at their current level:

- **Beginner → Intermediate**: 80% mastery of Beginner combos
- **Intermediate → Advanced**: 80% mastery of Intermediate combos
- **Advanced**: Final level (no further advancement)

### Progress Calculation

Progress is calculated as:
```
Progress = (Average mastery score of all combos at current level) × 100
```

Where:
- Mastery scores range from 0.0 to 1.0 in the database
- Progress is displayed as percentage (0.0% to 100.0%)

## Available Functions

### User Level Functions

```python
# Get user's current level
level = get_user_level(username)  # Returns: 'Beginner', 'Intermediate', or 'Advanced'

# Set user's level manually (rarely needed)
success = set_user_level(username, 'Intermediate')
```

### Progress Tracking Functions

```python
# Get current progress percentage
progress = get_user_progress(username)  # Returns: 0.0 to 100.0

# Update progress (with auto-level up)
success = update_user_progress(username, 75.5)

# Calculate progress from combo database
progress = calculate_user_progress_from_combos(username, 'setup/combos.db')
```

### Complete Sync Function

```python
# Sync user progress with database and auto-level up
from combo_curriculum.user_progress_example import sync_user_progress_with_database

result = sync_user_progress_with_database(username, db_path)
print(f"Level: {result['level']}, Progress: {result['progress']:.1f}%")
if result['leveled_up']:
    print(f"Leveled up from {result['old_level']} to {result['level']}!")
```

## Integration with Punch Combinations

### Access Restrictions

The `PunchCombinationPage` restricts button access based on user level:

- **Beginner users**: Can only select "Beginner" and "Self-Select"
- **Intermediate users**: Can only select "Intermediate"
- **Advanced users**: Can only select "Advanced"

### Sparring Access

The `TrainingPage` restricts sparring access:

- **Beginner**: No access to Sparring
- **Intermediate**: Can access Sparring (Battle mode)
- **Advanced**: Can access Sparring (Battle mode)

## User Management UI

The User Management page displays:

| Username | Level | Progress | Training Sessions | Actions |
|----------|-------|----------|-------------------|---------|
| john_doe | Beginner | 45.5% | 12 | Delete |
| jane_smith | Intermediate | 62.3% | 28 | Delete |

## Workflow Example

### New User Registration
1. User signs up → Created with level="Beginner", progress=0.0
2. User trains with Beginner combos
3. Combo mastery scores are stored in database
4. System calculates progress from mastery scores
5. At 80% progress → Auto-level up to Intermediate
6. Progress resets to 0.0 at new level
7. Process repeats for Intermediate → Advanced

### After Training Session

After each training session, sync user progress:

```python
# In your training completion code
def on_training_complete(username):
    # Update combo mastery in database (done by combo system)
    # ...
    
    # Sync user progress with database
    db_path = "setup/combos.db"
    result = sync_user_progress_with_database(username, db_path)
    
    # Show level-up notification if applicable
    if result['leveled_up']:
        show_notification(f"Congratulations! You've advanced to {result['level']}!")
    
    # Update UI to reflect new level/progress
    update_ui(result['level'], result['progress'])
```

## Testing the System

Run the test script:

```bash
python GUI/combo_curriculum/user_progress_example.py
```

This demonstrates:
- Getting user status
- Manual progress updates
- Automatic level-up
- Database synchronization

## Database Requirements

Ensure `combos.db` exists with:

```sql
-- combos table structure
CREATE TABLE combos (
    combo_id TEXT PRIMARY KEY,
    combo_name TEXT,
    combo_sequence TEXT,
    difficulty_level TEXT,
    mastery_score REAL,  -- 0.0 to 1.0
    total_attempts INTEGER,
    last_trained_timestamp TEXT,
    created_date TEXT
);
```

## Important Notes

1. **Progress resets** when leveling up (starts at 0% for new level)
2. **Level changes are automatic** when 80% threshold is reached
3. **Progress is per-level** (not cumulative across all levels)
4. **Advanced is the final level** (no further advancement)
5. **Mastery scores** must be updated in the database by the training system

## Future Enhancements

Potential additions:
- Manual level override by admin
- Progress history tracking
- Achievement badges at milestones
- Detailed progress reports per combo
- Recommended combos based on weaknesses
