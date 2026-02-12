"""
User Progress Integration Example

This script demonstrates how to integrate the combo curriculum with user
progress tracking and automatic level advancement.

Usage examples for updating user progress based on combo mastery.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import user management functions
from GUI.main_gui import (
    get_user_level,
    get_user_progress,
    update_user_progress,
    calculate_user_progress_from_combos
)


def sync_user_progress_with_database(username: str, db_path: str = None):
    """
    Synchronize user's progress with their combo mastery from database.
    
    This function:
    1. Calculates the user's progress based on combo mastery scores
    2. Updates the user's progress in the CSV file
    3. Automatically levels up the user if they meet the threshold (80%)
    
    Args:
        username: Username to update
        db_path: Path to combos.db (defaults to setup/combos.db)
    
    Returns:
        dict: Status information with level and progress
    
    Example:
        >>> result = sync_user_progress_with_database("john_doe")
        >>> print(f"Level: {result['level']}, Progress: {result['progress']:.1f}%")
    """
    if db_path is None:
        # Default to setup/combos.db
        db_path = os.path.join(
            os.path.dirname(__file__),
            "..", "setup", "combos.db"
        )
    
    # Get current status
    old_level = get_user_level(username)
    
    # Calculate progress from database
    progress = calculate_user_progress_from_combos(username, db_path)
    
    # Update user progress (this will auto-level up if threshold met)
    success = update_user_progress(username, progress)
    
    # Get new status
    new_level = get_user_level(username)
    new_progress = get_user_progress(username)
    
    result = {
        'success': success,
        'username': username,
        'old_level': old_level,
        'level': new_level,
        'progress': new_progress,
        'leveled_up': old_level != new_level
    }
    
    return result


def manual_update_user_progress(username: str, progress: float):
    """
    Manually update a user's progress percentage.
    
    Useful for testing or manual adjustments. The system will still
    auto-level up if the progress meets the threshold (80%).
    
    Args:
        username: Username to update
        progress: Progress percentage (0.0-100.0)
    
    Returns:
        dict: Status information
    
    Example:
        >>> result = manual_update_user_progress("jane_doe", 85.0)
        >>> if result['leveled_up']:
        >>>     print(f"Leveled up to {result['level']}!")
    """
    old_level = get_user_level(username)
    
    # Update progress
    success = update_user_progress(username, progress)
    
    # Get new status
    new_level = get_user_level(username)
    new_progress = get_user_progress(username)
    
    return {
        'success': success,
        'username': username,
        'old_level': old_level,
        'level': new_level,
        'progress': new_progress,
        'leveled_up': old_level != new_level
    }


def get_user_status(username: str):
    """
    Get current status of a user.
    
    Args:
        username: Username to query
    
    Returns:
        dict: User status information
    """
    level = get_user_level(username)
    progress = get_user_progress(username)
    
    # Calculate how much more progress needed for next level
    remaining = 80.0 - progress if progress < 80.0 else 0.0
    
    return {
        'username': username,
        'level': level,
        'progress': progress,
        'remaining_to_level_up': remaining,
        'can_level_up': progress >= 80.0 and level != 'Advanced'
    }


# Example usage
if __name__ == "__main__":
    print("=" * 70)
    print("User Progress Integration Examples")
    print("=" * 70)
    print()
    
    # Example 1: Check user status
    print("Example 1: Get user status")
    print("-" * 70)
    username = "test_user"
    status = get_user_status(username)
    print(f"Username: {status['username']}")
    print(f"Level: {status['level']}")
    print(f"Progress: {status['progress']:.1f}%")
    print(f"Remaining to level up: {status['remaining_to_level_up']:.1f}%")
    print()
    
    # Example 2: Manually update progress
    print("Example 2: Manual progress update")
    print("-" * 70)
    result = manual_update_user_progress(username, 75.0)
    print(f"Old Level: {result['old_level']}")
    print(f"New Level: {result['level']}")
    print(f"Progress: {result['progress']:.1f}%")
    print(f"Leveled Up: {result['leveled_up']}")
    print()
    
    # Example 3: Level up by reaching 80%
    print("Example 3: Level up by reaching threshold")
    print("-" * 70)
    result = manual_update_user_progress(username, 85.0)
    print(f"Old Level: {result['old_level']}")
    print(f"New Level: {result['level']}")
    print(f"Progress: {result['progress']:.1f}%")
    print(f"Leveled Up: {result['leveled_up']}")
    if result['leveled_up']:
        print(f"🎉 Congratulations! Leveled up to {result['level']}!")
    print()
    
    # Example 4: Sync with database (requires combos.db)
    print("Example 4: Sync with combo database")
    print("-" * 70)
    db_path = os.path.join(os.path.dirname(__file__), "..", "setup", "combos.db")
    if os.path.exists(db_path):
        result = sync_user_progress_with_database(username, db_path)
        print(f"Username: {result['username']}")
        print(f"Level: {result['level']}")
        print(f"Progress: {result['progress']:.1f}%")
        print(f"Synced from database successfully!")
    else:
        print(f"Database not found at: {db_path}")
        print("Skipping database sync example.")
    print()
    
    print("=" * 70)
    print("Examples completed!")
    print("=" * 70)
