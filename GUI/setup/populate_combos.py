#!/usr/bin/env python3
"""
Populate combo database with initial combo library.

This script inserts all 50 combos (15 Beginner, 20 Intermediate, 15 Advanced)
into the database. All combos start with mastery_score=0, total_attempts=0.

Usage:
    python3 populate_combos.py
    python3 populate_combos.py --db-path /custom/path/combos.db
"""

import sqlite3
import argparse
from datetime import datetime


# Complete combo library: (combo_id, combo_name, combo_sequence, difficulty_level)
COMBO_LIBRARY = [
    # ==================== BEGINNER (15 combos) ====================
    
    # Single Punches (6)
    ("beginner_001", "Jab", "1", "Beginner"),
    ("beginner_002", "Cross", "2", "Beginner"),
    ("beginner_003", "Lead Hook", "3", "Beginner"),
    ("beginner_004", "Rear Hook", "4", "Beginner"),
    ("beginner_005", "Lead Uppercut", "5", "Beginner"),
    ("beginner_006", "Rear Uppercut", "6", "Beginner"),
    
    # 2-Punch Combos Starting with Jab (6)
    ("beginner_007", "Jab-Cross", "1-2", "Beginner"),
    ("beginner_008", "Jab-Lead Hook", "1-3", "Beginner"),
    ("beginner_009", "Jab-Rear Hook", "1-4", "Beginner"),
    ("beginner_010", "Jab-Lead Uppercut", "1-5", "Beginner"),
    ("beginner_011", "Jab-Rear Uppercut", "1-6", "Beginner"),
    ("beginner_012", "Double Jab", "1-1", "Beginner"),
    
    # 2-Punch Combos Starting with Other Punches (3)
    ("beginner_013", "Cross-Lead Hook", "2-3", "Beginner"),
    ("beginner_014", "Cross-Rear Uppercut", "2-6", "Beginner"),
    ("beginner_015", "Lead Hook-Cross", "3-2", "Beginner"),
    
    # ==================== INTERMEDIATE (20 combos) ====================
    
    # 3-Punch Combos Starting with Jab (8)
    ("intermediate_001", "Jab-Cross-Lead Hook", "1-2-3", "Intermediate"),
    ("intermediate_002", "Jab-Cross-Rear Uppercut", "1-2-6", "Intermediate"),
    ("intermediate_003", "Double Jab-Cross", "1-1-2", "Intermediate"),
    ("intermediate_004", "Jab-Lead Hook-Cross", "1-3-2", "Intermediate"),
    ("intermediate_005", "Jab-Lead Uppercut-Cross", "1-5-2", "Intermediate"),
    ("intermediate_006", "Jab-Cross-Lead Uppercut", "1-2-5", "Intermediate"),
    ("intermediate_007", "Jab-Rear Hook-Cross", "1-4-2", "Intermediate"),
    ("intermediate_008", "Triple Jab", "1-1-1", "Intermediate"),
    
    # With Body Shots Starting with Jab (3)
    ("intermediate_009", "Jab-Body Cross-Lead Hook", "1-2b-3", "Intermediate"),
    ("intermediate_010", "Jab-Body Lead Hook-Head Hook", "1-3b-3", "Intermediate"),
    ("intermediate_011", "Jab-Cross-Body Rear Hook", "1-2-4b", "Intermediate"),
    
    # With Defense Starting with Jab (2)
    ("intermediate_012", "Jab-Slip-Cross", "1-slip-2", "Intermediate"),
    ("intermediate_013", "Jab-Block-Cross-Lead Hook", "1-block-2-3", "Intermediate"),
    
    # Starting with Defense (Counter Punching) (3)
    ("intermediate_014", "Slip-Jab-Cross", "slip-1-2", "Intermediate"),
    ("intermediate_015", "Block-Cross-Lead Hook", "block-2-3", "Intermediate"),
    ("intermediate_016", "Slip-Cross-Lead Uppercut", "slip-2-5", "Intermediate"),
    
    # Starting with Other Punches (4)
    ("intermediate_017", "Cross-Lead Hook-Cross", "2-3-2", "Intermediate"),
    ("intermediate_018", "Cross-Lead Hook-Rear Uppercut", "2-3-6", "Intermediate"),
    ("intermediate_019", "Lead Hook-Cross-Lead Hook", "3-2-3", "Intermediate"),
    ("intermediate_020", "Cross-Body Lead Hook-Cross", "2-3b-2", "Intermediate"),
    
    # ==================== ADVANCED (15 combos) ====================
    
    # Long Combos Starting with Jab (5)
    ("advanced_001", "Jab-Cross-Lead Hook-Cross", "1-2-3-2", "Advanced"),
    ("advanced_002", "Jab-Cross-Lead Hook-Cross-Rear Uppercut", "1-2-3-2-6", "Advanced"),
    ("advanced_003", "Double Jab-Cross-Lead Hook", "1-1-2-3", "Advanced"),
    ("advanced_004", "Jab-Body Cross-Lead Hook-Cross", "1-2b-3-2", "Advanced"),
    ("advanced_005", "Jab-Lead Uppercut-Cross-Rear Uppercut", "1-5-2-6", "Advanced"),
    
    # Complex Defense Starting with Jab (3)
    ("advanced_006", "Jab-Slip-Cross-Block-Lead Hook", "1-slip-2-block-3", "Advanced"),
    ("advanced_007", "Jab-Cross-Slip-Lead Hook-Cross", "1-2-slip-3-2", "Advanced"),
    ("advanced_008", "Jab-Block-Cross-Lead Hook-Rear Uppercut", "1-block-2-3-6", "Advanced"),
    
    # Counter Punching (Defense First) (4)
    ("advanced_009", "Slip-Jab-Cross-Lead Hook", "slip-1-2-3", "Advanced"),
    ("advanced_010", "Block-Cross-Slip-Lead Hook-Cross", "block-2-slip-3-2", "Advanced"),
    ("advanced_011", "Slip-Cross-Lead Hook-Rear Uppercut", "slip-2-3-6", "Advanced"),
    ("advanced_012", "Block-Jab-Slip-Cross-Lead Hook", "block-1-slip-2-3", "Advanced"),
    
    # Complex Patterns (3)
    ("advanced_013", "Cross-Lead Hook-Cross-Rear Hook", "2-3-2-4", "Advanced"),
    ("advanced_014", "Lead Hook-Body Cross-Lead Uppercut-Cross", "3-2b-5-2", "Advanced"),
    ("advanced_015", "Cross-Body Lead Hook-Slip-Cross-Lead Hook", "2-3b-slip-2-3", "Advanced"),
]


def populate_database(db_path='combos.db'):
    """Insert all combos into the database.
    
    Args:
        db_path: Path to database file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        created_date = datetime.now().isoformat()
        
        # Track insertion statistics
        inserted_count = 0
        skipped_count = 0
        
        # Insert each combo
        for combo_id, combo_name, combo_sequence, difficulty in COMBO_LIBRARY:
            try:
                cursor.execute('''
                    INSERT INTO combos (
                        combo_id,
                        combo_name,
                        combo_sequence,
                        difficulty_level,
                        mastery_score,
                        total_attempts,
                        last_trained_timestamp,
                        due_date,
                        ease_factor,
                        interval_days,
                        consecutive_successes,
                        created_date,
                        last_updated
                    ) VALUES (?, ?, ?, ?, 0.0, 0, NULL, NULL, 2.0, 0.0, 0, ?, NULL)
                ''', (combo_id, combo_name, combo_sequence, difficulty, created_date))
                inserted_count += 1
            except sqlite3.IntegrityError:
                # Combo already exists (duplicate primary key)
                skipped_count += 1
        
        conn.commit()
        
        # Query final counts by difficulty
        cursor.execute('''
            SELECT difficulty_level, COUNT(*) 
            FROM combos 
            GROUP BY difficulty_level 
            ORDER BY 
                CASE difficulty_level 
                    WHEN 'Beginner' THEN 1 
                    WHEN 'Intermediate' THEN 2 
                    WHEN 'Advanced' THEN 3 
                END
        ''')
        results = cursor.fetchall()
        
        # Query total count
        cursor.execute("SELECT COUNT(*) FROM combos")
        total_count = cursor.fetchone()[0]
        
        conn.close()
        
        # Print results
        print(f"✓ Database population complete")
        print()
        print(f"Inserted: {inserted_count} combos")
        if skipped_count > 0:
            print(f"Skipped: {skipped_count} combos (already existed)")
        print()
        print("Combo counts by difficulty:")
        for difficulty, count in results:
            print(f"  {difficulty:12} : {count:2} combos")
        print(f"  {'Total':12} : {total_count:2} combos")
        
        return True
        
    except sqlite3.Error as e:
        print(f"✗ Database error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


def verify_combos(db_path='combos.db'):
    """Verify that all combos were inserted correctly.
    
    Args:
        db_path: Path to database file
        
    Returns:
        True if verification passed, False otherwise
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check total count
        cursor.execute("SELECT COUNT(*) FROM combos")
        total = cursor.fetchone()[0]
        
        if total != len(COMBO_LIBRARY):
            print(f"✗ Expected {len(COMBO_LIBRARY)} combos, found {total}")
            return False
        
        # Verify all have correct initial state
        cursor.execute('''
            SELECT COUNT(*) FROM combos 
            WHERE mastery_score = 0.0 
            AND total_attempts = 0 
            AND ease_factor = 2.0
        ''')
        untrained = cursor.fetchone()[0]
        
        if untrained != total:
            print(f"✗ Some combos have incorrect initial state")
            return False
        
        # Check for combos starting with Jab
        cursor.execute('''
            SELECT COUNT(*) FROM combos 
            WHERE combo_sequence LIKE '1%' OR combo_sequence LIKE '1-%'
        ''')
        jab_first = cursor.fetchone()[0]
        
        print(f"✓ Verification passed")
        print(f"  All {total} combos initialized correctly")
        print(f"  {jab_first} combos start with Jab ({jab_first*100//total}%)")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"✗ Verification failed: {e}")
        return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Populate combo database with initial combo library'
    )
    parser.add_argument(
        '--db-path',
        default='combos.db',
        help='Path to database file (default: combos.db)'
    )
    parser.add_argument(
        '--verify',
        action='store_true',
        help='Verify combos after population'
    )
    
    args = parser.parse_args()
    
    print("="*60)
    print("COMBO CURRICULUM - DATABASE POPULATION")
    print("="*60)
    print()
    
    # Populate database
    success = populate_database(args.db_path)
    
    # Verify if requested
    if success and args.verify:
        print()
        verify_combos(args.db_path)
    
    print()
    if success:
        print("✓ Population complete")
        print("  Database is ready for use")
    else:
        print("✗ Population failed")
        exit(1)
