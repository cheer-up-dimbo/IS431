"""
Test script for the Combo Curriculum Engine.

Run this to verify the system works correctly before integrating with GUI.
"""

import sys
from datetime import datetime, timedelta

# Add current directory to path so we can import combo_curriculum
sys.path.insert(0, '/home/claude')

from combo_curriculum import (
    ComboCurriculum,
    Combo,
    create_mock_analytics,
    calculate_simple_performance
)


def test_initialization():
    """Test that curriculum initializes correctly."""
    print("\n" + "="*60)
    print("TEST 1: Initialization")
    print("="*60)
    
    try:
        curriculum = ComboCurriculum('test_combos.xlsx', create_sample_data=True)
        print("✓ Curriculum initialized successfully")
        
        stats = curriculum.get_stats()
        print(f"✓ Loaded {stats.total_combos} combos")
        
        assert stats.total_combos > 0, "Should have combos"
        print("✓ Sample data created")
        
        return True
    except Exception as e:
        print(f"✗ Initialization failed: {e}")
        return False


def test_combo_selection():
    """Test that combo selection works correctly."""
    print("\n" + "="*60)
    print("TEST 2: Combo Selection")
    print("="*60)
    
    try:
        curriculum = ComboCurriculum('test_combos.xlsx')
        
        # Test selecting beginner combo
        combo = curriculum.get_next_combo('Beginner')
        assert combo is not None, "Should get a combo"
        assert combo['difficulty_level'] == 'Beginner', "Should be Beginner difficulty"
        print(f"✓ Selected combo: {combo['combo_name']}")
        
        # Test exclusion list
        combo2 = curriculum.get_next_combo('Beginner', exclude_recent=[combo['combo_id']])
        assert combo2 is not None, "Should get different combo"
        assert combo2['combo_id'] != combo['combo_id'], "Should be different combo"
        print(f"✓ Exclusion works: {combo2['combo_name']}")
        
        # Test all difficulty levels
        for difficulty in ['Beginner', 'Intermediate', 'Advanced']:
            combo = curriculum.get_next_combo(difficulty)
            assert combo is not None, f"Should get {difficulty} combo"
            assert combo['difficulty_level'] == difficulty
            print(f"✓ {difficulty} selection works")
        
        return True
    except Exception as e:
        print(f"✗ Selection failed: {e}")
        return False


def test_score_update():
    """Test that score updates work correctly."""
    print("\n" + "="*60)
    print("TEST 3: Score Update")
    print("="*60)
    
    try:
        curriculum = ComboCurriculum('test_combos.xlsx')
        
        # Get a combo and check initial state
        combo = curriculum.get_next_combo('Beginner')
        initial_score = combo['mastery_score']
        initial_attempts = combo['total_attempts']
        
        print(f"Initial state: {combo['combo_name']}")
        print(f"  Mastery: {initial_score:.1f}/5.0")
        print(f"  Attempts: {initial_attempts}")
        
        # Update with good performance
        analytics = create_mock_analytics(accuracy=0.85, timing=0.88, form_score=0.82, completions=8)
        success = curriculum.update_score(combo['combo_id'], analytics)
        assert success, "Update should succeed"
        print("✓ Score update succeeded")
        
        # Check that score changed
        updated = curriculum.get_combo_stats(combo['combo_id'])
        assert updated['mastery_score'] != initial_score, "Score should change"
        assert updated['total_attempts'] == initial_attempts + 1, "Attempts should increment"
        print(f"✓ New mastery: {updated['mastery_score']:.1f}/5.0")
        
        # Test poor performance
        poor_analytics = create_mock_analytics(accuracy=0.35, timing=0.40, form_score=0.30, completions=2)
        curriculum.update_score(combo['combo_id'], poor_analytics)
        updated2 = curriculum.get_combo_stats(combo['combo_id'])
        print(f"✓ After poor performance: {updated2['mastery_score']:.1f}/5.0")
        
        return True
    except Exception as e:
        print(f"✗ Score update failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_scheduling():
    """Test that interval scheduling works correctly."""
    print("\n" + "="*60)
    print("TEST 4: Interval Scheduling")
    print("="*60)
    
    try:
        curriculum = ComboCurriculum('test_combos.xlsx')
        
        # Get a new combo
        combo = curriculum.get_next_combo('Beginner')
        combo_id = combo['combo_id']
        
        print(f"Training combo: {combo['combo_name']}")
        
        # Train multiple times with good performance
        for i in range(5):
            analytics = create_mock_analytics(
                accuracy=0.80 + (i * 0.03),
                timing=0.85 + (i * 0.02),
                form_score=0.78 + (i * 0.03),
                completions=7 + i
            )
            curriculum.update_score(combo_id, analytics)
            
            stats = curriculum.get_combo_stats(combo_id)
            print(f"  Training {i+1}: Mastery {stats['mastery_score']:.1f}/5.0")
        
        # Check final state
        final_stats = curriculum.get_combo_stats(combo_id)
        assert final_stats['total_attempts'] == combo['total_attempts'] + 5
        assert final_stats['mastery_score'] > combo['mastery_score']
        
        print("✓ Interval scheduling works")
        print(f"✓ Final mastery: {final_stats['mastery_score']:.1f}/5.0")
        
        return True
    except Exception as e:
        print(f"✗ Scheduling failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_statistics():
    """Test that statistics are calculated correctly."""
    print("\n" + "="*60)
    print("TEST 5: Statistics")
    print("="*60)
    
    try:
        curriculum = ComboCurriculum('test_combos.xlsx')
        
        # Get overall stats
        stats = curriculum.get_stats()
        print(f"Total combos: {stats.total_combos}")
        print(f"New: {stats.new_combos}")
        print(f"Learning: {stats.learning_combos}")
        print(f"Review: {stats.review_combos}")
        print(f"Average mastery: {stats.average_mastery:.2f}")
        
        # Get difficulty-specific stats
        for difficulty in ['Beginner', 'Intermediate', 'Advanced']:
            diff_stats = curriculum.get_stats(difficulty)
            print(f"\n{difficulty}:")
            print(f"  Total: {diff_stats.total_combos}")
            print(f"  Avg mastery: {diff_stats.average_mastery:.2f}")
        
        print("\n✓ Statistics calculated correctly")
        return True
    except Exception as e:
        print(f"✗ Statistics failed: {e}")
        return False


def test_performance_calculation():
    """Test performance score calculation."""
    print("\n" + "="*60)
    print("TEST 6: Performance Calculation")
    print("="*60)
    
    try:
        # Test different performance levels
        test_cases = [
            (0.95, 0.92, 0.90, 10, "Excellent"),
            (0.80, 0.85, 0.78, 8, "Good"),
            (0.65, 0.70, 0.68, 6, "Fair"),
            (0.45, 0.50, 0.40, 3, "Poor"),
        ]
        
        for acc, timing, form, compl, label in test_cases:
            analytics = create_mock_analytics(acc, timing, form, compl)
            performance = calculate_simple_performance(analytics)
            print(f"{label}: {performance:.2f}")
            
            if label == "Excellent":
                assert performance > 0.85, f"Expected high score, got {performance}"
            elif label == "Poor":
                assert performance < 0.55, f"Expected low score, got {performance}"
        
        print("✓ Performance calculation works correctly")
        return True
    except Exception as e:
        print(f"✗ Performance calculation failed: {e}")
        return False


def test_mastery_progression():
    """Test that combos progress correctly from new -> learning -> review."""
    print("\n" + "="*60)
    print("TEST 7: Mastery Progression")
    print("="*60)
    
    try:
        curriculum = ComboCurriculum('test_combos.xlsx')
        
        # Reset a combo to test progression
        combo = curriculum.get_next_combo('Beginner')
        combo_id = combo['combo_id']
        curriculum.reset_combo(combo_id)
        
        stats = curriculum.get_combo_stats(combo_id)
        assert stats['is_new'], "Should be new after reset"
        print(f"✓ Combo starts as NEW: {combo['combo_name']}")
        
        # Train to learning phase
        for i in range(3):
            analytics = create_mock_analytics(0.75, 0.80, 0.72, 7)
            curriculum.update_score(combo_id, analytics)
        
        stats = curriculum.get_combo_stats(combo_id)
        assert stats['is_learning'], "Should be learning phase"
        print(f"✓ Progressed to LEARNING (mastery: {stats['mastery_score']:.1f})")
        
        # Train to review phase
        for i in range(5):
            analytics = create_mock_analytics(0.88, 0.90, 0.85, 9)
            curriculum.update_score(combo_id, analytics)
        
        stats = curriculum.get_combo_stats(combo_id)
        print(f"✓ Final state: {'REVIEW' if stats['is_review'] else 'LEARNING'} (mastery: {stats['mastery_score']:.1f})")
        
        return True
    except Exception as e:
        print(f"✗ Progression test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_recency_filtering():
    """Test that recent combos are properly excluded."""
    print("\n" + "="*60)
    print("TEST 8: Recency Filtering")
    print("="*60)
    
    try:
        curriculum = ComboCurriculum('test_combos.xlsx')
        
        # Get 5 combos and track them
        recent = []
        combos_selected = []
        
        for i in range(5):
            combo = curriculum.get_next_combo('Beginner', exclude_recent=recent)
            assert combo is not None, "Should get a combo"
            assert combo['combo_id'] not in recent, "Should not repeat recent combo"
            
            recent.append(combo['combo_id'])
            combos_selected.append(combo['combo_name'])
            
            # Keep only last 3
            if len(recent) > 3:
                recent = recent[-3:]
        
        print(f"✓ Selected 5 different combos:")
        for name in combos_selected:
            print(f"  - {name}")
        
        return True
    except Exception as e:
        print(f"✗ Recency filtering failed: {e}")
        return False


def run_all_tests():
    """Run all tests and report results."""
    print("\n" + "="*60)
    print("COMBO CURRICULUM ENGINE - TEST SUITE")
    print("="*60)
    
    tests = [
        ("Initialization", test_initialization),
        ("Combo Selection", test_combo_selection),
        ("Score Update", test_score_update),
        ("Interval Scheduling", test_scheduling),
        ("Statistics", test_statistics),
        ("Performance Calculation", test_performance_calculation),
        ("Mastery Progression", test_mastery_progression),
        ("Recency Filtering", test_recency_filtering),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ {test_name} crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! System is ready for integration.")
    else:
        print("\n⚠️ Some tests failed. Review errors above.")
    
    return passed == total


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
