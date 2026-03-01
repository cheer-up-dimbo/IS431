# Level Progression Integration Guide

This guide shows how to integrate the progression checking methods with the main GUI to automatically level up users.

## Progression Rules

### Beginner → Intermediate
**Requirement:** ALL 15 Beginner combos must have:
- `total_attempts >= 5` AND
- `mastery_score >= 0.6` (3.0/5.0)

### Intermediate → Advanced
**Requirement:** ALL 20 Intermediate combos must have:
- `total_attempts >= 5` AND
- `mastery_score >= 0.8` (4.0/5.0)

### Advanced
No next level. This is the highest difficulty.

## Methods

### `check_progression_eligibility(current_difficulty)`
Checks if user has mastered ALL combos at current level.

```python
from combo_curriculum import ComboCurriculum

with ComboCurriculum("setup/combos.db") as curriculum:
    # Check if user can advance
    can_advance = curriculum.check_progression_eligibility("Beginner")
    
    if can_advance:
        print("User is ready to level up!")
```

**Returns:** `bool`
- `True` - User has mastered all combos at current level
- `False` - User still needs to practice more combos

### `get_next_difficulty(current_difficulty)`
Returns the next difficulty level.

```python
next_level = curriculum.get_next_difficulty("Beginner")
# Returns: "Intermediate"

next_level = curriculum.get_next_difficulty("Intermediate")
# Returns: "Advanced"

next_level = curriculum.get_next_difficulty("Advanced")
# Returns: None
```

## Integration with main_gui.py

### After Each Training Session

After a training session ends and the score is recorded:

```python
from combo_curriculum import ComboCurriculum

def on_training_complete(username, combo_id, performance_score):
    """Called when user completes a training session."""
    
    # 1. Update combo score in database
    with ComboCurriculum("setup/combos.db") as curriculum:
        curriculum.update_score(combo_id, performance_score)
        
        # 2. Get user's current level
        current_level = get_user_level(username)
        
        # 3. Check if user is eligible to level up
        if curriculum.check_progression_eligibility(current_level):
            # User has mastered all combos at current level!
            next_level = curriculum.get_next_difficulty(current_level)
            
            if next_level:
                # Level up the user
                set_user_level(username, next_level)
                
                # Show congratulations message
                show_level_up_notification(username, current_level, next_level)
                
        # 4. Update user's progress percentage
        progress = curriculum.get_level_progress(current_level)
        percentage = (progress['mastered_combos'] / progress['total_combos']) * 100
        update_user_progress(username, percentage)
```

### Level Up Notification

Display a congratulations message when user levels up:

```python
def show_level_up_notification(username, old_level, new_level):
    """Display level up message to user."""
    
    message = f"""
    🎉 CONGRATULATIONS {username}! 🎉
    
    You've mastered all {old_level} combos!
    
    You've been promoted to: {new_level}
    
    New features unlocked:
    - Access to {new_level} punch combinations
    {f'- Sparring mode enabled' if new_level in ['Intermediate', 'Advanced'] else ''}
    
    Keep up the great work! 🥊
    """
    
    # Show in a message box or notification
    QMessageBox.information(None, "Level Up!", message)
```

### Progress Tracking

Update progress percentage automatically:

```python
def calculate_user_progress_from_combos(username, db_path="setup/combos.db"):
    """Calculate user's progress percentage based on combo mastery."""
    
    user_level = get_user_level(username)
    
    with ComboCurriculum(db_path) as curriculum:
        progress = curriculum.get_level_progress(user_level)
        
        total = progress['total_combos']
        mastered = progress['mastered_combos']
        
        if total > 0:
            percentage = (mastered / total) * 100
            return round(percentage, 1)
        
    return 0.0
```

### User Dashboard

Display detailed progress information:

```python
def show_user_dashboard(username):
    """Display user progress dashboard."""
    
    user_level = get_user_level(username)
    
    with ComboCurriculum("setup/combos.db") as curriculum:
        # Get overall progress for current level
        progress = curriculum.get_level_progress(user_level)
        
        print(f"\n{'='*60}")
        print(f"USER DASHBOARD: {username}")
        print(f"{'='*60}")
        print(f"Current Level: {user_level}")
        print(f"\nProgress at {user_level} Level:")
        print(f"  Mastered:    {progress['mastered_combos']}/{progress['total_combos']}")
        print(f"  In Progress: {progress['in_progress_combos']}")
        print(f"  Struggling:  {progress['struggling_combos']}")
        
        # Calculate percentage
        percentage = (progress['mastered_combos'] / progress['total_combos']) * 100
        print(f"\nCompletion: {percentage:.1f}%")
        
        # Progress bar
        filled = int(percentage / 5)  # 20 blocks for 100%
        bar = '█' * filled + '░' * (20 - filled)
        print(f"[{bar}]")
        
        # Check if eligible for level up
        if curriculum.check_progression_eligibility(user_level):
            next_level = curriculum.get_next_difficulty(user_level)
            if next_level:
                print(f"\n✅ Ready to advance to {next_level}!")
            else:
                print(f"\n🏆 All combos mastered! You're at the highest level!")
        else:
            remaining = progress['total_combos'] - progress['mastered_combos']
            print(f"\n📝 Master {remaining} more combos to level up")
```

### Automatic Progress Update

Call this after every training session:

```python
def auto_check_and_update_progress(username):
    """Automatically check and update user progress after training."""
    
    current_level = get_user_level(username)
    
    with ComboCurriculum("setup/combos.db") as curriculum:
        # Update progress percentage
        progress = curriculum.get_level_progress(current_level)
        percentage = (progress['mastered_combos'] / progress['total_combos']) * 100
        update_user_progress(username, percentage)
        
        # Check for level up
        if curriculum.check_progression_eligibility(current_level):
            next_level = curriculum.get_next_difficulty(current_level)
            
            if next_level:
                # Automatic level up
                set_user_level(username, next_level)
                
                # Reset progress for new level
                update_user_progress(username, 0.0)
                
                # Show notification
                show_level_up_notification(username, current_level, next_level)
                
                return True  # Level up occurred
    
    return False  # No level up
```

## Complete Training Flow Example

```python
class TrainingSession:
    def __init__(self, username):
        self.username = username
        self.db_path = "setup/combos.db"
    
    def start_session(self):
        """Start a new training session."""
        user_level = get_user_level(self.username)
        
        with ComboCurriculum(self.db_path) as curriculum:
            # Get next combo to practice
            next_combo = curriculum.get_next_combo(user_level)
            
            if next_combo:
                print(f"Practice: {next_combo['combo_name']}")
                print(f"Sequence: {next_combo['combo_sequence']}")
                return next_combo
            else:
                print("All combos at this level are mastered!")
                return None
    
    def complete_session(self, combo_id, performance_score):
        """Complete training session and update progress."""
        
        with ComboCurriculum(self.db_path) as curriculum:
            # 1. Record the score
            curriculum.update_score(combo_id, performance_score)
            
            # 2. Get updated stats
            stats = curriculum.get_combo_stats(combo_id)
            print(f"\nSession Results:")
            print(f"  Score: {performance_score}/5.0")
            print(f"  Average (last 5): {stats['average_score']:.2f}/5.0")
            print(f"  Total Sessions: {stats['total_attempts']}")
            print(f"  Mastered: {stats['is_mastered']}")
            
            # 3. Check for level up
            current_level = get_user_level(self.username)
            leveled_up = auto_check_and_update_progress(self.username)
            
            if leveled_up:
                new_level = get_user_level(self.username)
                print(f"\n🎉 LEVEL UP: {current_level} → {new_level}")
            
            # 4. Show next combo
            next_combo = curriculum.get_next_combo(get_user_level(self.username))
            if next_combo:
                print(f"\nNext: {next_combo['combo_name']}")

# Usage
session = TrainingSession("john_doe")
combo = session.start_session()
if combo:
    # User practices...
    # Action recognition scores performance...
    score = 4.5
    session.complete_session(combo['combo_id'], score)
```

## Summary

1. **After Training:** Call `update_score()` to record performance
2. **Check Eligibility:** Use `check_progression_eligibility()` to see if user can level up
3. **Level Up:** If eligible, use `get_next_difficulty()` and `set_user_level()`
4. **Update Progress:** Calculate percentage using `get_level_progress()`
5. **Notify User:** Show congratulations message and unlock new features
