"""
Test script for combo statistics and progress tracking methods

Demonstrates get_combo_stats() and get_level_progress() functionality.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from combo_curriculum import ComboCurriculum


def test_combo_stats():
    """Test the get_combo_stats method."""
    
    db_path = os.path.join(os.path.dirname(__file__), "..", "setup", "combos.db")
    
    if not os.path.exists(db_path):
        print(f"Database not found: {db_path}")
        return
    
    print("=" * 70)
    print("Testing get_combo_stats()")
    print("=" * 70)
    print()
    
    with ComboCurriculum(db_path) as curriculum:
        
        # Test 1: Get stats for a specific combo
        print("Test 1: Get stats for beginner_001")
        print("-" * 70)
        
        stats = curriculum.get_combo_stats("beginner_001")
        
        if stats:
            print(f"Combo: {stats['combo_name']}")
            print(f"Sequence: {stats['combo_sequence']}")
            print(f"Total Attempts: {stats['total_attempts']}")
            print(f"Last 5 Scores: {[f'{s:.1f}' for s in stats['last_5_scores']]}")
            print(f"Average Score: {stats['average_score']:.2f}/5.0")
            print(f"Threshold: {stats['threshold']:.1f}/5.0")
            print(f"Mastered: {'✓ Yes' if stats['is_mastered'] else '✗ No'}")
            
            if not stats['is_mastered']:
                if stats['total_attempts'] < 5:
                    remaining = 5 - stats['total_attempts']
                    print(f"  → Need {remaining} more attempt(s)")
                elif stats['average_score'] < stats['threshold']:
                    needed = stats['threshold'] - stats['average_score']
                    print(f"  → Need {needed:.1f} points to reach threshold")
        else:
            print("Combo not found!")
        
        print()
        
        # Test 2: Add some scores and check stats again
        print("Test 2: Add training scores and recheck")
        print("-" * 70)
        
        test_combo = "beginner_002"
        test_scores = [2.5, 3.0, 3.5, 4.0, 4.5]
        
        print(f"Training {test_combo} with scores: {test_scores}")
        
        for score in test_scores:
            curriculum.update_score(test_combo, score)
        
        print()
        
        # Get updated stats
        stats = curriculum.get_combo_stats(test_combo)
        
        if stats:
            print(f"Updated Stats for {stats['combo_name']}:")
            print(f"  Last 5 Scores: {[f'{s:.1f}' for s in stats['last_5_scores']]}")
            print(f"  Average: {stats['average_score']:.2f}/5.0")
            print(f"  Attempts: {stats['total_attempts']}")
            print(f"  Threshold: {stats['threshold']:.1f}/5.0")
            print(f"  Mastered: {'✓ Yes' if stats['is_mastered'] else '✗ No'}")
        
        print()
        
        # Test 3: Test with non-existent combo
        print("Test 3: Query non-existent combo")
        print("-" * 70)
        
        stats = curriculum.get_combo_stats("invalid_999")
        if stats:
            print("Found (unexpected!)")
        else:
            print("Not found (expected)")
        
        print()


def test_level_progress():
    """Test the get_level_progress method."""
    
    db_path = os.path.join(os.path.dirname(__file__), "..", "setup", "combos.db")
    
    if not os.path.exists(db_path):
        print(f"Database not found: {db_path}")
        return
    
    print("=" * 70)
    print("Testing get_level_progress()")
    print("=" * 70)
    print()
    
    with ComboCurriculum(db_path) as curriculum:
        
        # Test all difficulty levels
        difficulties = ["Beginner", "Intermediate", "Advanced"]
        expected_counts = {"Beginner": 15, "Intermediate": 20, "Advanced": 15}
        
        for difficulty in difficulties:
            print(f"{difficulty} Progress")
            print("-" * 70)
            
            progress = curriculum.get_level_progress(difficulty)
            
            print(f"Total Combos: {progress['total_combos']}")
            print(f"  Expected: {expected_counts[difficulty]}")
            
            mastered_pct = (progress['mastered_combos'] / progress['total_combos'] * 100) if progress['total_combos'] > 0 else 0
            
            print(f"\nProgress Breakdown:")
            print(f"  ✓ Mastered: {progress['mastered_combos']} ({mastered_pct:.1f}%)")
            print(f"  ⏳ In Progress: {progress['in_progress_combos']}")
            print(f"  ⚠ Struggling: {progress['struggling_combos']}")
            
            # Calculate completion percentage
            if progress['total_combos'] > 0:
                completion = (progress['mastered_combos'] / progress['total_combos']) * 100
                print(f"\nCompletion: {completion:.1f}%")
                
                # Progress bar
                bar_length = 30
                filled = int(bar_length * completion / 100)
                bar = "█" * filled + "░" * (bar_length - filled)
                print(f"[{bar}] {completion:.0f}%")
            
            print()


def demo_user_progress_dashboard():
    """Demonstrate a user progress dashboard using both methods."""
    
    db_path = os.path.join(os.path.dirname(__file__), "..", "setup", "combos.db")
    
    if not os.path.exists(db_path):
        print(f"Database not found: {db_path}")
        return
    
    print("=" * 70)
    print("User Progress Dashboard Demo")
    print("=" * 70)
    print()
    
    with ComboCurriculum(db_path) as curriculum:
        
        # Get overall progress
        print("OVERALL PROGRESS")
        print("=" * 70)
        
        total_mastered = 0
        total_combos = 0
        
        for difficulty in ["Beginner", "Intermediate", "Advanced"]:
            progress = curriculum.get_level_progress(difficulty)
            total_mastered += progress['mastered_combos']
            total_combos += progress['total_combos']
            
            completion = (progress['mastered_combos'] / progress['total_combos'] * 100) if progress['total_combos'] > 0 else 0
            
            print(f"{difficulty:12} | {progress['mastered_combos']:2}/{progress['total_combos']:2} mastered ({completion:5.1f}%) | "
                  f"{progress['in_progress_combos']:2} in progress | {progress['struggling_combos']:2} struggling")
        
        print("-" * 70)
        overall_completion = (total_mastered / total_combos * 100) if total_combos > 0 else 0
        print(f"{'TOTAL':12} | {total_mastered:2}/{total_combos:2} mastered ({overall_completion:5.1f}%)")
        print()
        
        # Get next combo to practice
        print("NEXT STEPS")
        print("=" * 70)
        
        for difficulty in ["Beginner", "Intermediate", "Advanced"]:
            next_combo = curriculum.get_next_combo(difficulty)
            
            if next_combo:
                stats = curriculum.get_combo_stats(next_combo['combo_id'])
                
                print(f"\n{difficulty}:")
                print(f"  Next: {stats['combo_name']}")
                print(f"  Sequence: {stats['combo_sequence']}")
                print(f"  Current: {stats['total_attempts']} attempts, avg {stats['average_score']:.1f}/5.0")
                print(f"  Target: {stats['threshold']:.1f}/5.0 with 5+ attempts")
                
                if stats['total_attempts'] > 0:
                    print(f"  Last 5 scores: {[f'{s:.1f}' for s in stats['last_5_scores']]}")
            else:
                print(f"\n{difficulty}: All combos mastered! 🎉")
        
        print()


if __name__ == "__main__":
    test_combo_stats()
    print()
    test_level_progress()
    print()
    demo_user_progress_dashboard()
    
    print("=" * 70)
    print("All tests completed!")
    print("=" * 70)
