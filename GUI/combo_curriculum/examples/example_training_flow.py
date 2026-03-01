"""
Example: Complete Training Flow with Placeholder Score

This example demonstrates how to integrate the combo curriculum
and action recognition placeholder into a training session workflow.

This is what you'll implement in main_gui.py when the user
completes a training session.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from combo_curriculum import (
    ComboCurriculum,
    get_performance_score,
    integrate_score_after_training
)


def simulate_training_session(username: str, user_level: str):
    """
    Simulate a complete training session workflow.
    
    This demonstrates what happens when a user:
    1. Starts a training session
    2. Performs a combo
    3. Gets scored by action recognition
    4. Has their progress updated
    5. Checks if they leveled up
    
    Args:
        username: User's name
        user_level: Current user level (Beginner/Intermediate/Advanced)
    """
    print("=" * 70)
    print(f"TRAINING SESSION: {username} ({user_level})")
    print("=" * 70)
    print()
    
    db_path = os.path.join(os.path.dirname(__file__), '..', 'setup', 'combos.db')
    
    with ComboCurriculum(db_path) as curriculum:
        # STEP 1: Get next combo to practice
        print("Step 1: Get next combo to practice")
        print("-" * 70)
        
        next_combo = curriculum.get_next_combo(user_level)
        
        if not next_combo:
            print(f"✅ All {user_level} combos mastered!")
            print()
            
            # Check if user can level up
            if curriculum.check_progression_eligibility(user_level):
                next_level = curriculum.get_next_difficulty(user_level)
                if next_level:
                    print(f"🎉 READY TO LEVEL UP TO {next_level}!")
                else:
                    print("🏆 HIGHEST LEVEL ACHIEVED!")
            
            return
        
        print(f"Combo: {next_combo['combo_name']}")
        print(f"Sequence: {next_combo['combo_sequence']}")
        print(f"Current mastery: {next_combo['mastery_score']:.3f}")
        print(f"Attempts: {next_combo['total_attempts']}")
        print()
        
        # STEP 2: User performs the combo
        print("Step 2: User performs the combo")
        print("-" * 70)
        print("👊 Recording video...")
        print("👊 User performing combo...")
        video_path = f"recordings/{username}_{next_combo['combo_id']}_session.mp4"
        print(f"   Video saved: {video_path}")
        print()
        
        # STEP 3: Get performance score from action recognition
        print("Step 3: Action recognition scores the performance")
        print("-" * 70)
        
        # NOTE: Currently returns 3.0 (placeholder)
        # When ML model is ready, it will analyze video_path
        performance_score = get_performance_score(
            video_path=video_path,
            combo_id=next_combo['combo_id']
        )
        print()
        
        # STEP 4: Update database with score
        print("Step 4: Update database with score")
        print("-" * 70)
        
        curriculum.update_score(next_combo['combo_id'], performance_score)
        print()
        
        # STEP 5: Get updated stats
        print("Step 5: Display updated progress")
        print("-" * 70)
        
        stats = curriculum.get_combo_stats(next_combo['combo_id'])
        
        print(f"📊 Session Results:")
        print(f"   Score: {performance_score:.1f}/5.0")
        print(f"   Average (last 5): {stats['average_score']:.2f}/5.0")
        print(f"   Total attempts: {stats['total_attempts']}")
        print(f"   Threshold: {stats['threshold']}/5.0")
        print(f"   Mastered: {'✅ YES' if stats['is_mastered'] else '❌ Not yet'}")
        print()
        
        # STEP 6: Check overall level progress
        print("Step 6: Check overall level progress")
        print("-" * 70)
        
        progress = curriculum.get_level_progress(user_level)
        
        total = progress['total_combos']
        mastered = progress['mastered_combos']
        percentage = (mastered / total) * 100
        
        print(f"📈 {user_level} Level Progress:")
        print(f"   Mastered: {mastered}/{total} ({percentage:.1f}%)")
        print(f"   In Progress: {progress['in_progress_combos']}")
        print(f"   Struggling: {progress['struggling_combos']}")
        
        # Progress bar
        filled = int(percentage / 5)
        bar = '█' * filled + '░' * (20 - filled)
        print(f"   [{bar}]")
        print()
        
        # STEP 7: Check for level-up eligibility
        print("Step 7: Check for level-up eligibility")
        print("-" * 70)
        
        can_level_up = curriculum.check_progression_eligibility(user_level)
        
        if can_level_up:
            next_level = curriculum.get_next_difficulty(user_level)
            if next_level:
                print(f"🎉 CONGRATULATIONS!")
                print(f"   You've mastered all {user_level} combos!")
                print(f"   Ready to advance to: {next_level}")
                print()
                print(f"   New features unlocked:")
                print(f"   - Access to {next_level} punch combinations")
                if next_level in ['Intermediate', 'Advanced']:
                    print(f"   - Sparring mode enabled")
            else:
                print("🏆 CHAMPION!")
                print("   All combos at highest level mastered!")
        else:
            remaining = total - mastered
            print(f"📝 Keep training!")
            print(f"   Need to master {remaining} more combos to level up")
            
            # Show next combo
            next_up = curriculum.get_next_combo(user_level)
            if next_up:
                print(f"   Next: {next_up['combo_name']}")
        
        print()


def main():
    """Run example training sessions."""
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "TRAINING SESSION EXAMPLE" + " " * 29 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    # Example 1: Beginner user
    simulate_training_session("john_doe", "Beginner")
    
    print()
    print("=" * 70)
    print()
    
    # Show how to use the simpler integration helper
    print("ALTERNATIVE: Using Integration Helper")
    print("=" * 70)
    print()
    
    db_path = os.path.join(os.path.dirname(__file__), '..', 'setup', 'combos.db')
    
    with ComboCurriculum(db_path) as curriculum:
        next_combo = curriculum.get_next_combo("Beginner")
        
        if next_combo:
            # One-line integration
            result = integrate_score_after_training(
                curriculum,
                combo_id=next_combo['combo_id'],
                video_path=f"recordings/session.mp4"
            )
            
            if result['success']:
                print(f"✅ Training complete!")
                print(f"   Score: {result['score']:.1f}/5.0")
                print(f"   Average: {result['average_score']:.2f}/5.0")
                print(f"   Mastered: {result['is_mastered']}")
    
    print()
    print("=" * 70)
    print("✅ Example complete!")
    print()
    print("💡 Integration Tips:")
    print("   1. Call get_next_combo() when starting training")
    print("   2. Record video during training")
    print("   3. Call get_performance_score() to score video")
    print("   4. Call update_score() to save to database")
    print("   5. Call check_progression_eligibility() to check level-up")
    print("   6. Update user level in users.csv if eligible")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
