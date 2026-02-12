"""
Test script for level progression checking methods.

Demonstrates:
- check_progression_eligibility() - Check if user can advance to next level
- get_next_difficulty() - Get the next difficulty level
"""

import sys
import os

# Add parent directory to path to import combo_curriculum
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from combo_curriculum import ComboCurriculum


def test_progression_checking():
    """Test progression eligibility checking."""
    print("=" * 70)
    print("LEVEL PROGRESSION ELIGIBILITY TEST")
    print("=" * 70)
    
    # Use the setup database
    db_path = os.path.join(os.path.dirname(__file__), '..', 'setup', 'combos.db')
    
    with ComboCurriculum(db_path) as curriculum:
        # Test for each difficulty level
        for difficulty in ["Beginner", "Intermediate", "Advanced"]:
            print(f"\n📊 {difficulty} Level Status:")
            print("-" * 70)
            
            # Get level progress
            progress = curriculum.get_level_progress(difficulty)
            print(f"Total Combos: {progress['total_combos']}")
            print(f"Mastered: {progress['mastered_combos']}")
            print(f"In Progress: {progress['in_progress_combos']}")
            print(f"Struggling: {progress['struggling_combos']}")
            
            # Check progression eligibility
            can_progress = curriculum.check_progression_eligibility(difficulty)
            print(f"\n✅ Can advance? {can_progress}")
            
            if can_progress:
                next_level = curriculum.get_next_difficulty(difficulty)
                if next_level:
                    print(f"🎉 Ready to advance to: {next_level}")
                else:
                    print("🏆 Highest level achieved! All combos mastered!")
            else:
                # Show what's needed for progression
                remaining = progress['total_combos'] - progress['mastered_combos']
                threshold = 3.0 if difficulty == "Beginner" else 4.0
                print(f"📝 Need to master {remaining} more combos (threshold: {threshold}/5.0)")
                
                next_level = curriculum.get_next_difficulty(difficulty)
                if next_level:
                    print(f"🎯 Next goal: {next_level} level")


def test_next_difficulty():
    """Test get_next_difficulty() helper method."""
    print("\n" + "=" * 70)
    print("DIFFICULTY PROGRESSION MAPPING")
    print("=" * 70)
    
    db_path = os.path.join(os.path.dirname(__file__), '..', 'setup', 'combos.db')
    
    with ComboCurriculum(db_path) as curriculum:
        levels = ["Beginner", "Intermediate", "Advanced"]
        
        for level in levels:
            next_level = curriculum.get_next_difficulty(level)
            if next_level:
                print(f"{level:15} → {next_level}")
            else:
                print(f"{level:15} → None (Max Level)")


def simulate_progression():
    """Simulate a user progressing through levels."""
    print("\n" + "=" * 70)
    print("USER PROGRESSION SIMULATION")
    print("=" * 70)
    
    db_path = os.path.join(os.path.dirname(__file__), '..', 'setup', 'combos.db')
    
    with ComboCurriculum(db_path) as curriculum:
        # Simulate mastering beginner combos
        print("\n📚 Training Beginner combos...")
        
        beginner_combos = curriculum.get_combos_by_difficulty("Beginner")
        print(f"Found {len(beginner_combos)} Beginner combos")
        
        # Train first 3 combos to mastery
        for i, combo in enumerate(beginner_combos[:3], 1):
            print(f"\n  Combo {i}: {combo['combo_name']}")
            
            # Simulate 5 training sessions with good scores
            for session in range(5):
                score = 3.5 + (session * 0.3)  # Improving scores
                curriculum.update_score(combo['combo_id'], score)
                print(f"    Session {session + 1}: {score:.1f}/5.0")
            
            # Check stats after training
            stats = curriculum.get_combo_stats(combo['combo_id'])
            print(f"    Average: {stats['average_score']:.2f}/5.0")
            print(f"    Mastered: {stats['is_mastered']}")
        
        # Check progression eligibility
        print("\n" + "-" * 70)
        print("Checking progression eligibility...")
        
        progress = curriculum.get_level_progress("Beginner")
        print(f"\nBeginner Progress: {progress['mastered_combos']}/{progress['total_combos']} mastered")
        
        can_progress = curriculum.check_progression_eligibility("Beginner")
        if can_progress:
            print("✅ Ready to advance to Intermediate!")
        else:
            remaining = progress['total_combos'] - progress['mastered_combos']
            print(f"❌ Need to master {remaining} more combos to advance")
            print(f"   Currently mastered: {progress['mastered_combos']}")
            print(f"   In progress: {progress['in_progress_combos']}")
            print(f"   Struggling: {progress['struggling_combos']}")


if __name__ == "__main__":
    test_progression_checking()
    test_next_difficulty()
    simulate_progression()
    
    print("\n" + "=" * 70)
    print("✅ All progression tests completed!")
    print("=" * 70)
