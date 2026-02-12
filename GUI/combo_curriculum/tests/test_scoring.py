"""
Test script for update_score and get_next_combo methods

This demonstrates the new scoring and progression functionality.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from combo_curriculum import ComboCurriculum


def test_update_score_and_progression():
    """Test the update_score and get_next_combo methods."""
    
    # Path to database
    db_path = os.path.join(os.path.dirname(__file__), "..", "setup", "combos.db")
    
    if not os.path.exists(db_path):
        print(f"Database not found at: {db_path}")
        print("Skipping tests.")
        return
    
    print("=" * 70)
    print("Testing update_score and get_next_combo")
    print("=" * 70)
    print()
    
    with ComboCurriculum(db_path) as curriculum:
        
        # Test 1: Get next combo to practice (Beginner)
        print("Test 1: Get next combo to practice")
        print("-" * 70)
        next_combo = curriculum.get_next_combo("Beginner")
        if next_combo:
            print(f"Next combo to practice:")
            print(f"  ID: {next_combo['combo_id']}")
            print(f"  Name: {next_combo['combo_name']}")
            print(f"  Sequence: {next_combo['combo_sequence']}")
            print(f"  Current mastery: {next_combo['mastery_score']:.3f}")
            print(f"  Total attempts: {next_combo['total_attempts']}")
            
            combo_to_practice = next_combo['combo_id']
        else:
            print("All Beginner combos are mastered!")
            combo_to_practice = "beginner_001"  # Use first combo for demo
        print()
        
        # Test 2: Simulate training sessions with varying scores
        print("Test 2: Simulate 5 training sessions")
        print("-" * 70)
        test_scores = [2.5, 3.0, 3.5, 4.0, 4.2]  # Scores from 0-5
        
        for i, score in enumerate(test_scores, 1):
            print(f"Session {i}: Recording score {score:.1f}...")
            success = curriculum.update_score(combo_to_practice, score)
            if success:
                print(f"  ✓ Score recorded successfully")
            else:
                print(f"  ✗ Failed to record score")
        print()
        
        # Test 3: Check updated combo status
        print("Test 3: Check updated combo status")
        print("-" * 70)
        combo = curriculum.get_combo_by_id(combo_to_practice)
        if combo:
            print(f"Combo: {combo['combo_name']}")
            print(f"  Mastery score: {combo['mastery_score']:.3f} (avg of last 5)")
            print(f"  Total attempts: {combo['total_attempts']}")
            print(f"  Last trained: {combo['last_trained_timestamp']}")
            
            # Check if mastered (Beginner threshold = 0.6)
            if combo['total_attempts'] >= 5 and combo['mastery_score'] >= 0.6:
                print(f"  ✓ MASTERED! (threshold: 0.6 for Beginner)")
            else:
                print(f"  ✗ Not yet mastered (need 5+ attempts and 0.6+ mastery)")
        print()
        
        # Test 4: Get next combo after practicing current one
        print("Test 4: Get next combo to practice now")
        print("-" * 70)
        next_combo = curriculum.get_next_combo("Beginner")
        if next_combo:
            print(f"Next combo:")
            print(f"  ID: {next_combo['combo_id']}")
            print(f"  Name: {next_combo['combo_name']}")
            print(f"  Mastery: {next_combo['mastery_score']:.3f}")
            print(f"  Attempts: {next_combo['total_attempts']}")
        else:
            print("All Beginner combos are mastered! 🎉")
        print()
        
        # Test 5: Test different difficulty thresholds
        print("Test 5: Check thresholds for different difficulty levels")
        print("-" * 70)
        difficulties = ["Beginner", "Intermediate", "Advanced"]
        thresholds = {
            "Beginner": 3.0 / 5.0,      # 0.6
            "Intermediate": 4.0 / 5.0,  # 0.8
            "Advanced": 4.0 / 5.0       # 0.8
        }
        
        for diff in difficulties:
            next_combo = curriculum.get_next_combo(diff)
            print(f"{diff}:")
            print(f"  Mastery threshold: {thresholds[diff]:.1f} ({thresholds[diff] * 5:.1f}/5.0)")
            if next_combo:
                print(f"  Next combo: {next_combo['combo_id']} - {next_combo['combo_name']}")
            else:
                print(f"  All {diff} combos mastered!")
        print()
    
    print("=" * 70)
    print("All tests completed!")
    print("=" * 70)


def simulate_user_progression():
    """Simulate a user progressing through combos sequentially."""
    
    db_path = os.path.join(os.path.dirname(__file__), "..", "setup", "combos.db")
    
    if not os.path.exists(db_path):
        print(f"Database not found: {db_path}")
        return
    
    print()
    print("=" * 70)
    print("Simulating User Progression (Sequential Combo Practice)")
    print("=" * 70)
    print()
    
    with ComboCurriculum(db_path) as curriculum:
        difficulty = "Beginner"
        combo_count = 0
        
        print(f"Starting {difficulty} progression...")
        print()
        
        # Practice first 3 combos in sequence
        for _ in range(3):
            # Get next combo
            next_combo = curriculum.get_next_combo(difficulty)
            
            if not next_combo:
                print("All combos mastered!")
                break
            
            combo_count += 1
            print(f"Combo {combo_count}: {next_combo['combo_id']} - {next_combo['combo_name']}")
            print(f"  Current: {next_combo['total_attempts']} attempts, {next_combo['mastery_score']:.3f} mastery")
            
            # Simulate 5 training sessions with improving scores
            scores = [2.0, 2.5, 3.0, 3.5, 4.0]
            print(f"  Training sessions: {scores}")
            
            for score in scores:
                curriculum.update_score(next_combo['combo_id'], score)
            
            # Check final status
            updated = curriculum.get_combo_by_id(next_combo['combo_id'])
            print(f"  After training: {updated['total_attempts']} attempts, {updated['mastery_score']:.3f} mastery")
            
            if updated['mastery_score'] >= 0.6:
                print(f"  ✓ MASTERED!")
            else:
                print(f"  Need more practice (threshold: 0.6)")
            print()
    
    print("=" * 70)
    print("Progression simulation complete!")
    print("=" * 70)


if __name__ == "__main__":
    test_update_score_and_progression()
    simulate_user_progression()
