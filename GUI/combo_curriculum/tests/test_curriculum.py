"""
Test script for ComboCurriculum class

This script demonstrates basic usage of the ComboCurriculum class
for querying boxing combos from the database.
"""

import sys
import os

# Add parent directory to path to import combo_curriculum
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from combo_curriculum import ComboCurriculum


def main():
    """Test the ComboCurriculum class with basic queries."""
    
    # Assuming combos.db is in the setup folder
    db_path = os.path.join(os.path.dirname(__file__), "..", "setup", "combos.db")
    
    print("=" * 60)
    print("Testing ComboCurriculum Class")
    print("=" * 60)
    print()
    
    # Test with context manager (recommended)
    try:
        with ComboCurriculum(db_path) as curriculum:
            
            # Test 1: Get beginner combos
            print("Test 1: Getting Beginner combos...")
            print("-" * 60)
            beginner_combos = curriculum.get_combos_by_difficulty("Beginner")
            print(f"Found {len(beginner_combos)} beginner combos")
            if beginner_combos:
                print(f"First combo: {beginner_combos[0]['combo_name']}")
                print(f"  ID: {beginner_combos[0]['combo_id']}")
                print(f"  Sequence: {beginner_combos[0]['combo_sequence']}")
            print()
            
            # Test 2: Get intermediate combos
            print("Test 2: Getting Intermediate combos...")
            print("-" * 60)
            intermediate_combos = curriculum.get_combos_by_difficulty("Intermediate")
            print(f"Found {len(intermediate_combos)} intermediate combos")
            if intermediate_combos:
                print(f"First combo: {intermediate_combos[0]['combo_name']}")
            print()
            
            # Test 3: Get advanced combos
            print("Test 3: Getting Advanced combos...")
            print("-" * 60)
            advanced_combos = curriculum.get_combos_by_difficulty("Advanced")
            print(f"Found {len(advanced_combos)} advanced combos")
            if advanced_combos:
                print(f"First combo: {advanced_combos[0]['combo_name']}")
            print()
            
            # Test 4: Query specific combo by ID
            print("Test 4: Querying specific combo by ID...")
            print("-" * 60)
            combo = curriculum.get_combo_by_id("beginner_001")
            if combo:
                print(f"Combo ID: {combo['combo_id']}")
                print(f"Name: {combo['combo_name']}")
                print(f"Sequence: {combo['combo_sequence']}")
                print(f"Difficulty: {combo['difficulty_level']}")
                print(f"Mastery Score: {combo['mastery_score']}")
                print(f"Total Attempts: {combo['total_attempts']}")
            else:
                print("Combo not found!")
            print()
            
            # Test 5: Query non-existent combo
            print("Test 5: Querying non-existent combo...")
            print("-" * 60)
            combo = curriculum.get_combo_by_id("invalid_999")
            if combo:
                print("Combo found (unexpected!)")
            else:
                print("Combo not found (expected)")
            print()
            
    except Exception as e:
        print(f"Error during testing: {e}")
        return 1
    
    print("=" * 60)
    print("All tests completed successfully!")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
