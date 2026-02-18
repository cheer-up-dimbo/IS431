#!/usr/bin/env python3
"""
Complete setup script for boxing combo curriculum database.

This is the main script you run on the Jetson to set up the combo database.
It creates the schema, populates combos, and verifies everything worked.

Usage:
    python3 setup_combo_database.py
    
With custom path:
    python3 setup_combo_database.py --db-path /opt/boxing_robot/data/combos.db
    
Force reset (no confirmation):
    python3 setup_combo_database.py --force
"""

import sqlite3
import argparse
import sys
from datetime import datetime
from pathlib import Path


def create_schema(db_path):
    """Create database schema (tables and indexes)."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create combos table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS combos (
            combo_id TEXT PRIMARY KEY,
            combo_name TEXT NOT NULL,
            combo_sequence TEXT NOT NULL,
            difficulty_level TEXT NOT NULL CHECK(difficulty_level IN ('Beginner', 'Intermediate', 'Advanced')),
            mastery_score REAL DEFAULT 0.0 CHECK(mastery_score >= 0.0 AND mastery_score <= 5.0),
            total_attempts INTEGER DEFAULT 0 CHECK(total_attempts >= 0),
            last_trained_timestamp TEXT,
            due_date TEXT,
            ease_factor REAL DEFAULT 2.0 CHECK(ease_factor >= 1.3 AND ease_factor <= 2.5),
            interval_days REAL DEFAULT 0.0 CHECK(interval_days >= 0.0),
            consecutive_successes INTEGER DEFAULT 0 CHECK(consecutive_successes >= 0),
            created_date TEXT NOT NULL,
            last_updated TEXT
        )
    ''')
    
    # Create performance history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS performance_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            combo_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            performance_score REAL CHECK(performance_score >= 0.0 AND performance_score <= 5.0),
            accuracy REAL CHECK(accuracy >= 0.0 AND accuracy <= 1.0),
            timing REAL CHECK(timing >= 0.0 AND timing <= 1.0),
            form_score REAL CHECK(form_score >= 0.0 AND form_score <= 1.0),
            combo_completion INTEGER CHECK(combo_completion >= 0),
            FOREIGN KEY (combo_id) REFERENCES combos(combo_id) ON DELETE CASCADE
        )
    ''')
    
    # Create indexes
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_difficulty ON combos(difficulty_level)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_due_date ON combos(due_date)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_mastery ON combos(mastery_score)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_attempts ON combos(total_attempts)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_performance_combo ON performance_history(combo_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_performance_timestamp ON performance_history(timestamp)')
    
    conn.commit()
    conn.close()


def populate_combos(db_path):
    """Insert all 50 combos into the database."""
    
    # Full combo library
    combos = [
        # BEGINNER (15)
        ("beginner_001", "Jab", "1", "Beginner"),
        ("beginner_002", "Cross", "2", "Beginner"),
        ("beginner_003", "Lead Hook", "3", "Beginner"),
        ("beginner_004", "Rear Hook", "4", "Beginner"),
        ("beginner_005", "Lead Uppercut", "5", "Beginner"),
        ("beginner_006", "Rear Uppercut", "6", "Beginner"),
        ("beginner_007", "Jab-Cross", "1-2", "Beginner"),
        ("beginner_008", "Jab-Lead Hook", "1-3", "Beginner"),
        ("beginner_009", "Jab-Rear Hook", "1-4", "Beginner"),
        ("beginner_010", "Jab-Lead Uppercut", "1-5", "Beginner"),
        ("beginner_011", "Jab-Rear Uppercut", "1-6", "Beginner"),
        ("beginner_012", "Double Jab", "1-1", "Beginner"),
        ("beginner_013", "Cross-Lead Hook", "2-3", "Beginner"),
        ("beginner_014", "Cross-Rear Uppercut", "2-6", "Beginner"),
        ("beginner_015", "Lead Hook-Cross", "3-2", "Beginner"),
        
        # INTERMEDIATE (20)
        ("intermediate_001", "Jab-Cross-Lead Hook", "1-2-3", "Intermediate"),
        ("intermediate_002", "Jab-Cross-Rear Uppercut", "1-2-6", "Intermediate"),
        ("intermediate_003", "Double Jab-Cross", "1-1-2", "Intermediate"),
        ("intermediate_004", "Jab-Lead Hook-Cross", "1-3-2", "Intermediate"),
        ("intermediate_005", "Jab-Lead Uppercut-Cross", "1-5-2", "Intermediate"),
        ("intermediate_006", "Jab-Cross-Lead Uppercut", "1-2-5", "Intermediate"),
        ("intermediate_007", "Jab-Rear Hook-Cross", "1-4-2", "Intermediate"),
        ("intermediate_008", "Triple Jab", "1-1-1", "Intermediate"),
        ("intermediate_009", "Jab-Body Cross-Lead Hook", "1-2b-3", "Intermediate"),
        ("intermediate_010", "Jab-Body Lead Hook-Head Hook", "1-3b-3", "Intermediate"),
        ("intermediate_011", "Jab-Cross-Body Rear Hook", "1-2-4b", "Intermediate"),
        ("intermediate_012", "Jab-Slip-Cross", "1-slip-2", "Intermediate"),
        ("intermediate_013", "Jab-Block-Cross-Lead Hook", "1-block-2-3", "Intermediate"),
        ("intermediate_014", "Slip-Jab-Cross", "slip-1-2", "Intermediate"),
        ("intermediate_015", "Block-Cross-Lead Hook", "block-2-3", "Intermediate"),
        ("intermediate_016", "Slip-Cross-Lead Uppercut", "slip-2-5", "Intermediate"),
        ("intermediate_017", "Cross-Lead Hook-Cross", "2-3-2", "Intermediate"),
        ("intermediate_018", "Cross-Lead Hook-Rear Uppercut", "2-3-6", "Intermediate"),
        ("intermediate_019", "Lead Hook-Cross-Lead Hook", "3-2-3", "Intermediate"),
        ("intermediate_020", "Cross-Body Lead Hook-Cross", "2-3b-2", "Intermediate"),
        
        # ADVANCED (15)
        ("advanced_001", "Jab-Cross-Lead Hook-Cross", "1-2-3-2", "Advanced"),
        ("advanced_002", "Jab-Cross-Lead Hook-Cross-Rear Uppercut", "1-2-3-2-6", "Advanced"),
        ("advanced_003", "Double Jab-Cross-Lead Hook", "1-1-2-3", "Advanced"),
        ("advanced_004", "Jab-Body Cross-Lead Hook-Cross", "1-2b-3-2", "Advanced"),
        ("advanced_005", "Jab-Lead Uppercut-Cross-Rear Uppercut", "1-5-2-6", "Advanced"),
        ("advanced_006", "Jab-Slip-Cross-Block-Lead Hook", "1-slip-2-block-3", "Advanced"),
        ("advanced_007", "Jab-Cross-Slip-Lead Hook-Cross", "1-2-slip-3-2", "Advanced"),
        ("advanced_008", "Jab-Block-Cross-Lead Hook-Rear Uppercut", "1-block-2-3-6", "Advanced"),
        ("advanced_009", "Slip-Jab-Cross-Lead Hook", "slip-1-2-3", "Advanced"),
        ("advanced_010", "Block-Cross-Slip-Lead Hook-Cross", "block-2-slip-3-2", "Advanced"),
        ("advanced_011", "Slip-Cross-Lead Hook-Rear Uppercut", "slip-2-3-6", "Advanced"),
        ("advanced_012", "Block-Jab-Slip-Cross-Lead Hook", "block-1-slip-2-3", "Advanced"),
        ("advanced_013", "Cross-Lead Hook-Cross-Rear Hook", "2-3-2-4", "Advanced"),
        ("advanced_014", "Lead Hook-Body Cross-Lead Uppercut-Cross", "3-2b-5-2", "Advanced"),
        ("advanced_015", "Cross-Body Lead Hook-Slip-Cross-Lead Hook", "2-3b-slip-2-3", "Advanced"),
    ]
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    created_date = datetime.now().isoformat()
    inserted = 0
    
    for combo_id, combo_name, combo_sequence, difficulty in combos:
        try:
            cursor.execute('''
                INSERT INTO combos (
                    combo_id, combo_name, combo_sequence, difficulty_level,
                    mastery_score, total_attempts, ease_factor, interval_days,
                    consecutive_successes, created_date
                ) VALUES (?, ?, ?, ?, 0.0, 0, 2.0, 0.0, 0, ?)
            ''', (combo_id, combo_name, combo_sequence, difficulty, created_date))
            inserted += 1
        except sqlite3.IntegrityError:
            pass  # Already exists
    
    conn.commit()
    conn.close()
    
    return inserted


def verify_database(db_path):
    """Verify database was set up correctly."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    
    if 'combos' not in tables or 'performance_history' not in tables:
        return False, "Missing required tables"
    
    # Check combo counts
    cursor.execute("SELECT difficulty_level, COUNT(*) FROM combos GROUP BY difficulty_level")
    results = dict(cursor.fetchall())
    
    cursor.execute("SELECT COUNT(*) FROM combos")
    total = cursor.fetchone()[0]
    
    # Check initial state
    cursor.execute("SELECT COUNT(*) FROM combos WHERE mastery_score = 0.0 AND total_attempts = 0")
    untrained = cursor.fetchone()[0]
    
    conn.close()
    
    if total != 50:
        return False, f"Expected 50 combos, found {total}"
    
    if untrained != total:
        return False, "Some combos have non-zero initial state"
    
    return True, results


def main():
    parser = argparse.ArgumentParser(
        description='Setup boxing combo curriculum database on Jetson'
    )
    parser.add_argument(
        '--db-path',
        default='combos.db',
        help='Database file path (default: combos.db in current directory)'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force reset without confirmation prompt'
    )
    
    args = parser.parse_args()
    
    db_file = Path(args.db_path)
    
    # Print header
    print()
    print("=" * 70)
    print("BOXING COMBO CURRICULUM - DATABASE SETUP")
    print("=" * 70)
    print()
    
    # Check if database already exists
    if db_file.exists() and not args.force:
        print(f"[WARNING] Database already exists at: {db_file.absolute()}")
        print()
        response = input("Reset and recreate database? (yes/no): ").strip().lower()
        
        if response != 'yes':
            print("\nSetup cancelled.")
            return 0
        
        # Backup existing database
        backup_path = db_file.parent / f"{db_file.stem}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        db_file.rename(backup_path)
        print(f"[OK] Backed up existing database to: {backup_path.name}")
        print()
    
    # Create parent directory if needed
    db_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # Step 1: Create schema
        print("Step 1: Creating database schema...")
        create_schema(args.db_path)
        print("  [OK] Tables created: combos, performance_history")
        print("  [OK] Indexes created: 6 indexes for query optimization")
        print()
        
        # Step 2: Populate combos
        print("Step 2: Populating combo library...")
        inserted = populate_combos(args.db_path)
        print(f"  [OK] Inserted {inserted} combos")
        print()
        
        # Step 3: Verify
        print("Step 3: Verifying database...")
        success, result = verify_database(args.db_path)
        
        if not success:
            print(f"  [FAILED] Verification failed: {result}")
            return 1
        
        print("  [OK] All combos initialized correctly")
        print()
        print("  Combo counts by difficulty:")
        for difficulty in ['Beginner', 'Intermediate', 'Advanced']:
            count = result.get(difficulty, 0)
            print(f"    {difficulty:12} : {count:2} combos")
        print(f"    {'Total':12} : {sum(result.values()):2} combos")
        print()
        
        # Success summary
        print("=" * 70)
        print("[SUCCESS] SETUP COMPLETE")
        print("=" * 70)
        print()
        print(f"Database location: {db_file.absolute()}")
        print(f"Database size: {db_file.stat().st_size / 1024:.1f} KB")
        print()
        print("Next steps:")
        print("  1. Your application can now load combos from this database")
        print("  2. Test database access: sqlite3", args.db_path, '"SELECT COUNT(*) FROM combos;"')
        print("  3. Run your training application")
        print()
        
        return 0
        
    except Exception as e:
        print(f"\n[ERROR] Setup failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
