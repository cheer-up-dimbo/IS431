"""
Usage examples for the Combo Curriculum Engine.

This script demonstrates how to integrate the curriculum engine with
the boxing training GUI.
"""

from combo_curriculum import ComboCurriculum, create_mock_analytics


def example_basic_usage():
    """Basic usage example: initialize, get combo, update score."""
    print("=" * 60)
    print("EXAMPLE 1: Basic Usage")
    print("=" * 60)
    
    # Initialize curriculum with sample data
    curriculum = ComboCurriculum('demo_combos.xlsx', create_sample_data=True)
    
    # Get statistics
    stats = curriculum.get_stats('Beginner')
    print(f"\nBeginner Combos:")
    print(f"  Total: {stats.total_combos}")
    print(f"  New: {stats.new_combos}")
    print(f"  Learning: {stats.learning_combos}")
    print(f"  Review: {stats.review_combos}")
    
    # Get next combo to train
    combo = curriculum.get_next_combo(difficulty='Beginner')
    
    if combo:
        print(f"\n📋 Next Combo: {combo['combo_name']}")
        print(f"   Sequence: {combo['combo_sequence']}")
        print(f"   Mastery: {combo['mastery_score']:.1f}/5.0")
        print(f"   Attempts: {combo['total_attempts']}")
        
        # Simulate training with good performance
        analytics = create_mock_analytics(
            accuracy=0.85,
            timing=0.88,
            form_score=0.82,
            completions=7
        )
        
        print(f"\n📊 Training Analytics:")
        print(f"   Accuracy: {analytics['accuracy']:.0%}")
        print(f"   Timing: {analytics['timing']:.0%}")
        print(f"   Form: {analytics['form_score']:.0%}")
        print(f"   Completions: {analytics['combo_completion']}")
        
        # Update score
        curriculum.update_score(combo['combo_id'], analytics)
        
        # Check updated stats
        updated_stats = curriculum.get_combo_stats(combo['combo_id'])
        print(f"\n✅ Updated Mastery: {updated_stats['mastery_score']:.1f}/5.0")


def example_full_session():
    """Example of a full training session with multiple intervals."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Full Training Session")
    print("=" * 60)
    
    curriculum = ComboCurriculum('demo_combos.xlsx')
    
    # Simulate a 5-round training session
    difficulty = 'Beginner'
    num_intervals = 5
    recent_combos = []
    
    print(f"\nStarting {num_intervals}-interval session at {difficulty} level\n")
    
    for interval_num in range(1, num_intervals + 1):
        print(f"--- Interval {interval_num} ---")
        
        # Get next combo (avoiding recent ones)
        combo = curriculum.get_next_combo(
            difficulty=difficulty,
            exclude_recent=recent_combos[-3:]  # Don't repeat last 3
        )
        
        if not combo:
            print("No combos available!")
            break
        
        print(f"Training: {combo['combo_name']} ({combo['combo_sequence']})")
        print(f"Current mastery: {combo['mastery_score']:.1f}/5.0")
        
        # Simulate varying performance
        import random
        base_performance = random.uniform(0.65, 0.95)
        analytics = create_mock_analytics(
            accuracy=base_performance,
            timing=base_performance + random.uniform(-0.1, 0.1),
            form_score=base_performance + random.uniform(-0.15, 0.05),
            completions=int(base_performance * 10)
        )
        
        # Update score
        curriculum.update_score(combo['combo_id'], analytics)
        
        # Track recent combos
        recent_combos.append(combo['combo_id'])
        
        print()
    
    # Final statistics
    print("=" * 60)
    print("SESSION COMPLETE")
    print("=" * 60)
    stats = curriculum.get_stats(difficulty)
    print(f"\nFinal Stats:")
    print(f"  Average Mastery: {stats.average_mastery:.2f}/5.0")
    print(f"  Learning: {stats.learning_combos}")
    print(f"  Overdue: {stats.overdue_combos}")


def example_gui_integration():
    """Example showing how to integrate with TechCorrSessionPage."""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: GUI Integration Pattern")
    print("=" * 60)
    
    print("""
# In TechCorrSessionPage.__init__():

from combo_curriculum import ComboCurriculum

class TechCorrSessionPage(QWidget):
    def __init__(self, stacked_widget, app_state=None):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.app_state = app_state
        
        # Initialize curriculum engine
        self.curriculum = ComboCurriculum('data/combos.xlsx')
        self.current_combo_id = None
        self.recent_combos = []
        
        # ... rest of init
    
    def start_interval(self):
        '''Called when starting a new 25-second interval.'''
        
        # Get user's difficulty level
        difficulty = self.config.difficulty  # "Beginner", "Intermediate", "Advanced"
        
        # Get next combo (avoiding recent repeats)
        combo = self.curriculum.get_next_combo(
            difficulty=difficulty,
            exclude_recent=self.recent_combos[-5:]
        )
        
        if combo:
            # Display combo to user
            self.combo_name_label.setText(combo['combo_name'])
            self.combo_sequence_label.setText(combo['combo_sequence'])
            
            # Store for later update
            self.current_combo_id = combo['combo_id']
            
            # Track recency
            self.recent_combos.append(combo['combo_id'])
            
            # Start robot demonstration
            # self.robot_controller.demonstrate(combo['combo_sequence'])
        else:
            self.combo_name_label.setText("No combos available")
    
    def end_interval(self):
        '''Called when 25-second interval ends.'''
        
        # Get analytics from CV system
        # In v1, use placeholders until CV is integrated
        analytics = {
            'accuracy': 0.75,      # From CV: punch detection accuracy
            'timing': 0.80,        # From CV: rhythm consistency
            'form_score': 0.70,    # From CV: technique quality
            'combo_completion': 6  # From CV: complete reps counted
        }
        
        # Or if CV is available:
        # from cv_interface import get_cv_state
        # cv_data = get_cv_state()
        # analytics = {
        #     'accuracy': cv_data['accuracy'],
        #     'timing': cv_data['timing'],
        #     'form_score': cv_data['form_quality'],
        #     'combo_completion': cv_data['rep_count']
        # }
        
        # Update curriculum
        if self.current_combo_id:
            self.curriculum.update_score(self.current_combo_id, analytics)
            
            # Show feedback to user
            stats = self.curriculum.get_combo_stats(self.current_combo_id)
            self.show_feedback(stats['mastery_score'])
    
    def show_feedback(self, new_mastery):
        '''Display mastery update to user.'''
        feedback_text = f"Mastery: {new_mastery:.1f}/5.0"
        
        if new_mastery >= 4.0:
            feedback_text += " - Excellent! 🥊"
        elif new_mastery >= 3.0:
            feedback_text += " - Good progress! 💪"
        else:
            feedback_text += " - Keep practicing! 🥋"
        
        self.feedback_label.setText(feedback_text)
    """)


def example_statistics_and_analytics():
    """Example showing how to query and display statistics."""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Statistics and Analytics")
    print("=" * 60)
    
    curriculum = ComboCurriculum('demo_combos.xlsx')
    
    # Overall statistics
    print("\n📊 Overall Statistics:")
    for difficulty in ['Beginner', 'Intermediate', 'Advanced']:
        stats = curriculum.get_stats(difficulty)
        print(f"\n{difficulty}:")
        print(f"  Total: {stats.total_combos}")
        print(f"  New: {stats.new_combos} | Learning: {stats.learning_combos} | Review: {stats.review_combos}")
        print(f"  Average Mastery: {stats.average_mastery:.2f}/5.0")
    
    # Individual combo details
    print("\n📋 Sample Combo Details:")
    combo = curriculum.get_next_combo('Beginner')
    if combo:
        detailed_stats = curriculum.get_combo_stats(combo['combo_id'])
        print(f"\nCombo: {combo['combo_name']}")
        print(f"  Status: {'NEW' if detailed_stats['is_new'] else 'LEARNING' if detailed_stats['is_learning'] else 'REVIEW'}")
        print(f"  Mastery: {detailed_stats['mastery_score']:.1f}/5.0")
        print(f"  Total attempts: {detailed_stats['total_attempts']}")
        print(f"  Consecutive successes: {detailed_stats['consecutive_successes']}")
        if detailed_stats['recent_performance']:
            print(f"  Recent avg performance: {detailed_stats['recent_performance']:.0%}")


def example_difficulty_progression():
    """Example showing how a user might progress through difficulty levels."""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Difficulty Progression Pattern")
    print("=" * 60)
    
    print("""
Recommended progression pattern:

1. User starts at Beginner level
2. Train until average mastery reaches 3.5/5.0
3. Prompt user to try Intermediate level
4. Train Intermediate until average mastery reaches 3.5/5.0
5. Prompt user to try Advanced level

Implementation:

def should_suggest_level_up(curriculum, current_difficulty):
    '''Check if user is ready for next difficulty level.'''
    stats = curriculum.get_stats(current_difficulty)
    
    # Criteria for leveling up:
    # - Average mastery >= 3.5
    # - At least 80% of combos have been attempted
    # - Less than 20% overdue combos
    
    mastery_ready = stats.average_mastery >= 3.5
    experience_ready = (stats.new_combos / stats.total_combos) < 0.2
    maintenance_good = (stats.overdue_combos / stats.total_combos) < 0.2
    
    return mastery_ready and experience_ready and maintenance_good

# In your GUI:
def check_progression(self):
    if should_suggest_level_up(self.curriculum, self.current_difficulty):
        self.show_level_up_dialog()
    """)


def main():
    """Run all examples."""
    example_basic_usage()
    example_full_session()
    example_gui_integration()
    example_statistics_and_analytics()
    example_difficulty_progression()
    
    print("\n" + "=" * 60)
    print("All examples complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Install openpyxl: pip install openpyxl")
    print("2. Copy combo_curriculum/ folder to your project")
    print("3. Import in your GUI: from combo_curriculum import ComboCurriculum")
    print("4. Initialize in TechCorrSessionPage.__init__()")
    print("5. Call get_next_combo() and update_score() as shown above")


if __name__ == '__main__':
    main()
