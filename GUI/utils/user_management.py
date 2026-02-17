"""Utility functions for user management and progress tracking."""

import os
import csv
import hashlib


def get_users_csv_path():
    """Get the path to the users CSV file."""
    return os.path.join(os.path.dirname(__file__), "users.csv")


def hash_password(password: str) -> str:
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def load_users() -> dict:
    """Load users from CSV file. Returns dict of {username: {"password_hash": ..., "level": ..., "progress": ...}}."""
    users = {}
    csv_path = get_users_csv_path()
    if os.path.exists(csv_path):
        try:
            with open(csv_path, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    users[row['username']] = {
                        'password_hash': row['password_hash'],
                        'level': row.get('level', 'Beginner'),
                        'progress': float(row.get('progress', '0.0'))
                    }
        except Exception as e:
            print(f"Error loading users: {e}")
    return users


def save_users(users: dict) -> bool:
    """Save users dict to CSV file. Returns True on success."""
    csv_path = get_users_csv_path()
    try:
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['username', 'password_hash', 'level', 'progress'])
            writer.writeheader()
            for username, user_data in users.items():
                if isinstance(user_data, dict):
                    writer.writerow({
                        'username': username,
                        'password_hash': user_data['password_hash'],
                        'level': user_data.get('level', 'Beginner'),
                        'progress': user_data.get('progress', 0.0)
                    })
                else:
                    # Backward compatibility for old format
                    writer.writerow({
                        'username': username,
                        'password_hash': user_data,
                        'level': 'Beginner',
                        'progress': 0.0
                    })
        return True
    except Exception as e:
        print(f"Error saving users: {e}")
        return False


def get_user_level(username: str) -> str:
    """Get the current level of a user. Returns 'Beginner', 'Intermediate', or 'Advanced'."""
    users = load_users()
    if username in users:
        user_data = users[username]
        if isinstance(user_data, dict):
            return user_data.get('level', 'Beginner')
        return 'Beginner'
    return 'Beginner'


def set_user_level(username: str, level: str) -> bool:
    """Set the level of a user. Returns True on success."""
    if level not in ['Beginner', 'Intermediate', 'Advanced']:
        print(f"Invalid level: {level}")
        return False
    users = load_users()
    if username in users:
        users[username]['level'] = level
        return save_users(users)
    return False


def get_user_progress(username: str) -> float:
    """Get the current progress percentage of a user (0.0-100.0)."""
    users = load_users()
    if username in users:
        user_data = users[username]
        if isinstance(user_data, dict):
            return user_data.get('progress', 0.0)
        return 0.0
    return 0.0


def update_user_progress(username: str, progress: float) -> bool:
    """
    Update user's progress percentage and auto-level up if thresholds met.
    
    Progress thresholds:
    - Beginner -> Intermediate: 80% progress at Beginner level
    - Intermediate -> Advanced: 80% progress at Intermediate level
    
    Args:
        username: Username to update
        progress: Progress percentage (0.0-100.0)
    
    Returns:
        bool: True on success
    """
    users = load_users()
    if username not in users:
        return False
    
    # Clamp progress to 0-100
    progress = max(0.0, min(100.0, progress))
    
    current_level = users[username].get('level', 'Beginner')
    users[username]['progress'] = progress
    
    # Auto level-up logic
    if current_level == 'Beginner' and progress >= 80.0:
        users[username]['level'] = 'Intermediate'
        users[username]['progress'] = 0.0  # Reset progress for new level
        print(f"User {username} leveled up to Intermediate!")
    elif current_level == 'Intermediate' and progress >= 80.0:
        users[username]['level'] = 'Advanced'
        users[username]['progress'] = 0.0  # Reset progress for new level
        print(f"User {username} leveled up to Advanced!")
    
    return save_users(users)


def calculate_user_progress_from_combos(username: str, db_path: str) -> float:
    """
    Calculate user's progress based on combo mastery from database.
    
    Progress = (Average mastery score of all combos at current level) * 100
    
    Args:
        username: Username to calculate progress for
        db_path: Path to combos.db database
    
    Returns:
        float: Progress percentage (0.0-100.0)
    """
    try:
        import sys
        # Add combo_curriculum to path if not already there
        curriculum_path = os.path.join(os.path.dirname(__file__), '..', 'combo_curriculum')
        curriculum_path = os.path.abspath(curriculum_path)
        if curriculum_path not in sys.path:
            sys.path.insert(0, curriculum_path)
        
        from combo_curriculum import ComboCurriculum
        
        # Get user's current level
        level = get_user_level(username)
        
        # Query combos at that level
        with ComboCurriculum(db_path) as curriculum:
            combos = curriculum.get_combos_by_difficulty(level)
            
            if not combos:
                return 0.0
            
            # Calculate average mastery score
            total_mastery = sum(combo.get('mastery_score', 0.0) for combo in combos)
            avg_mastery = total_mastery / len(combos)
            
            # Convert to percentage (mastery_score is 0.0-1.0)
            progress = avg_mastery * 100.0
            
            return progress
    
    except Exception as e:
        print(f"Error calculating progress from combos: {e}")
        return 0.0


def get_training_csv_path(username: str):
    """Get the path to a user's training history CSV file."""
    return os.path.join(os.path.dirname(__file__), "..", f"training_{username}.csv")
