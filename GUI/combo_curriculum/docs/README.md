# Documentation

This directory contains detailed documentation for the Combo Curriculum module.

## Documentation Files

### `USER_PROGRESS.md`
**User Progress and Level System Documentation**

Explains the user progression system:
- User level structure (Beginner/Intermediate/Advanced)
- Progress tracking methodology
- How progress is calculated from combo mastery
- Integration with user management system
- CSV data structure for users.csv

**Topics Covered:**
- User data model
- Progress calculation formulas
- Level advancement criteria
- User management functions

---

### `SCORING_SYSTEM.md`
**Scoring and Mastery System Documentation**

Details the performance scoring system:
- Score scale (0-5 from action recognition)
- Mastery calculation using last 5 sessions
- Mastery thresholds by difficulty level
- Performance history tracking
- Database schema for performance_history table

**Topics Covered:**
- Score recording workflow
- Average calculation methodology
- Mastery determination logic
- Beginner: 3.0/5.0 (60%) threshold
- Intermediate/Advanced: 4.0/5.0 (80%) threshold

---

### `PROGRESSION_INTEGRATION.md`
**Level Progression Integration Guide**

Complete guide for integrating level progression into main GUI:
- Automatic level-up system
- Progression eligibility checking
- Level-up notifications
- User dashboard implementation
- Training session workflow

**Topics Covered:**
- Progression requirements (ALL combos mastered)
- Beginner → Intermediate (15 combos)
- Intermediate → Advanced (20 combos)
- Integration examples for main_gui.py
- Automatic progress updates
- User notifications

**Code Examples:**
- `on_training_complete()` workflow
- `show_level_up_notification()` implementation
- `auto_check_and_update_progress()` function
- Complete training session class

---

## Quick Reference

### User Progression Requirements

| Current Level | Next Level | Requirement |
|--------------|------------|-------------|
| Beginner | Intermediate | ALL 15 combos: attempts ≥ 5 AND score ≥ 0.6 (3.0/5.0) |
| Intermediate | Advanced | ALL 20 combos: attempts ≥ 5 AND score ≥ 0.8 (4.0/5.0) |
| Advanced | - | Highest level (no progression) |

### Scoring Scale

| Score Range | Rating | Description |
|-------------|--------|-------------|
| 4.0 - 5.0 | Excellent | Expert level technique |
| 3.0 - 3.9 | Good | Solid technique |
| 2.0 - 2.9 | Fair | Adequate but needs improvement |
| 1.0 - 1.9 | Poor | Significant improvement needed |
| 0.0 - 0.9 | Very Poor | Major technical issues |

### Key Methods

- `check_progression_eligibility(difficulty)` - Check if user can level up
- `get_next_difficulty(difficulty)` - Get next level name
- `update_score(combo_id, score)` - Record training score
- `get_level_progress(difficulty)` - Get overall level statistics

## Related Documentation

- [Main README](../README.md) - Module overview and API reference
- [Tests README](../tests/README.md) - Testing documentation
- [Examples README](../examples/README.md) - Usage examples

## Integration Workflow

For integrating into main GUI, follow this order:

1. **Read** `USER_PROGRESS.md` - Understand user level system
2. **Read** `SCORING_SYSTEM.md` - Understand scoring methodology
3. **Read** `PROGRESSION_INTEGRATION.md` - See complete integration examples
4. **Run** examples from `../examples/` - See working code
5. **Implement** in main_gui.py using provided code patterns
