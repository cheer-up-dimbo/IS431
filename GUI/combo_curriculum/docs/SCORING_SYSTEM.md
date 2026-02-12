# Scoring and Sequential Progression System

## Overview

The `ComboCurriculum` class now supports:
1. **Score tracking** - Record performance scores after each training session
2. **Sequential progression** - Automatically determine the next combo to practice
3. **Mastery calculation** - Average of last 5 sessions (not all-time)
4. **Level-appropriate thresholds** - Different mastery requirements per difficulty

## New Methods

### 1. `update_score(combo_id, score)`

Records a training session score and updates mastery level.

**Score Range:** 0-5 (from action recognition model)

**Process:**
1. Insert score into `performance_history` table with timestamp
2. Retrieve last 5 scores for this combo
3. Calculate average of last 5 (or fewer if < 5 sessions)
4. Update `combos` table:
   - `mastery_score` = average / 5.0 (normalized to 0-1)
   - `total_attempts` += 1
   - `last_trained_timestamp` = now

**Example:**
```python
# User just completed beginner_001 with score 4.2/5.0
curriculum.update_score("beginner_001", 4.2)

# After 5 sessions with scores [3.0, 3.5, 4.0, 4.2, 4.5]:
# mastery_score = (3.0 + 3.5 + 4.0 + 4.2 + 4.5) / 5 / 5.0 = 0.78
```

### 2. `get_next_combo(difficulty)`

Returns the next combo that needs practice in sequential order.

**Mastery Criteria:**
- **Beginner:** 5+ attempts AND 0.6+ mastery (3.0/5.0)
- **Intermediate:** 5+ attempts AND 0.8+ mastery (4.0/5.0)
- **Advanced:** 5+ attempts AND 0.8+ mastery (4.0/5.0)

**Logic:**
1. Get all combos for difficulty level
2. Sort by `combo_id` (ensures sequential order)
3. Return FIRST combo where `attempts < 5` OR `mastery < threshold`
4. If all mastered, return `None`

**Example:**
```python
next_combo = curriculum.get_next_combo("Beginner")

if next_combo:
    print(f"Practice: {next_combo['combo_name']}")
    # User practices combo
    # Action recognition scores performance
    score = 4.5  # From ML model
    curriculum.update_score(next_combo['combo_id'], score)
else:
    print("All Beginner combos mastered! Ready for Intermediate!")
```

## Integration with User Progression

### Workflow

```
User logs in → Get user level → Get next combo for that level
    ↓
User practices combo → Action recognition scores it
    ↓
Update combo score → Recalculate mastery
    ↓
Check if combo mastered → Get next combo in sequence
    ↓
If all combos mastered → Calculate user progress
    ↓
If progress >= 80% → Auto level-up user
    ↓
Resume with next difficulty level
```

### Complete Integration Example

```python
from combo_curriculum import ComboCurriculum
from GUI.main_gui import (
    get_user_level,
    update_user_progress,
    calculate_user_progress_from_combos
)

username = "john_doe"
db_path = "setup/combos.db"

with ComboCurriculum(db_path) as curriculum:
    # 1. Get user's current level
    level = get_user_level(username)  # e.g., "Beginner"
    
    # 2. Get next combo to practice
    next_combo = curriculum.get_next_combo(level)
    
    if next_combo:
        print(f"Practice: {next_combo['combo_name']}")
        
        # 3. User practices combo
        # Action recognition model scores the performance
        performance_score = 4.2  # From ML model (0-5)
        
        # 4. Record the score
        curriculum.update_score(next_combo['combo_id'], performance_score)
        
        # 5. Check if combo is now mastered
        updated = curriculum.get_combo_by_id(next_combo['combo_id'])
        threshold = 0.6 if level == "Beginner" else 0.8
        
        if updated['total_attempts'] >= 5 and updated['mastery_score'] >= threshold:
            print(f"✓ Mastered {updated['combo_name']}!")
            
            # 6. Check if all combos at this level are mastered
            next_up = curriculum.get_next_combo(level)
            if next_up is None:
                print(f"All {level} combos mastered!")
                
                # 7. Calculate user progress and potentially level up
                progress = calculate_user_progress_from_combos(username, db_path)
                update_user_progress(username, progress)
                
                new_level = get_user_level(username)
                if new_level != level:
                    print(f"🎉 Leveled up to {new_level}!")
    else:
        # All combos at current level are mastered
        print(f"All {level} combos completed! Calculating progress...")
        progress = calculate_user_progress_from_combos(username, db_path)
        update_user_progress(username, progress)
```

## Mastery Score Calculation

### Why Last 5 Sessions?

Using the last 5 sessions (instead of all-time average):
- ✅ Reflects current skill level
- ✅ Adapts to improvement over time
- ✅ Ignores early learning struggles
- ✅ Reasonable sample size

### Example Progression

**Combo: beginner_001 "Jab-Cross"**

| Session | Score | Last 5 Avg | Mastery | Attempts | Status |
|---------|-------|------------|---------|----------|--------|
| 1       | 2.0   | 2.0        | 0.40    | 1        | Learning |
| 2       | 2.5   | 2.25       | 0.45    | 2        | Learning |
| 3       | 3.0   | 2.50       | 0.50    | 3        | Improving |
| 4       | 3.5   | 2.75       | 0.55    | 4        | Improving |
| 5       | 4.0   | 3.00       | **0.60**| 5        | **MASTERED** ✓ |
| 6       | 4.2   | 3.44       | 0.69    | 6        | Refined |
| 7       | 4.5   | 3.84       | 0.77    | 7        | Expert |

After session 5: mastery = 0.60 ≥ 0.60 (Beginner threshold) → **MASTERED**

Next sessions improve mastery further, but combo is already considered mastered.

## Database Schema Details

### performance_history table

```sql
CREATE TABLE performance_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    combo_id TEXT,
    timestamp TEXT,  -- ISO format: 2026-02-12T14:30:45.123456
    performance_score REAL  -- 0.0 to 5.0
);
```

### Query for Last 5 Scores

```sql
SELECT performance_score
FROM performance_history
WHERE combo_id = ?
ORDER BY timestamp DESC
LIMIT 5
```

Returns most recent 5 scores in descending order (newest first).

## Testing

Run the comprehensive test:
```bash
python GUI/combo_curriculum/test_scoring.py
```

This demonstrates:
- Recording scores with `update_score()`
- Sequential progression with `get_next_combo()`
- Mastery calculation from last 5 sessions
- Different thresholds for difficulty levels
- Complete user progression simulation

## Important Notes

1. **Mastery = average of LAST 5 sessions only** (not all-time)
2. **Normalized to 0-1 scale** (score/5.0) for storage
3. **Sequential order enforced** by `combo_id` sorting
4. **Thresholds differ by level:**
   - Beginner: 3.0/5.0 = 0.6
   - Intermediate: 4.0/5.0 = 0.8
   - Advanced: 4.0/5.0 = 0.8
5. **Both conditions required for mastery:** 5+ attempts AND score ≥ threshold
6. **Timestamps in ISO format** for consistency and timezone support

## Future Enhancements

Potential additions:
- Adjustable mastery thresholds per combo
- Difficulty scaling based on user performance
- Combo recommendations based on weak areas
- Performance analytics and trends
- Time-based retention tracking
- Combo similarity clustering for targeted practice
