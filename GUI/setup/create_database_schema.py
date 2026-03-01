#!/usr/bin/env python3
"""
Create SQLite database schema for boxing combo curriculum.

This script creates the database structure (tables, indexes) but does not
populate it with combo data. Run this before populate_combos.py.

Usage:
    python3 create_database_schema.py
    python3 create_database_schema.py --db-path /custom/path/combos.db
"""

import sqlite3
import argparse
from pathlib import Path


def create_database(db_path='combos.db'):
    """Create SQLite database with proper schema for combo curriculum.
    
    Args:
        db_path: Path where database file will be created
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Convert to Path object for easier handling
        db_file = Path(db_path)
        
        # Create parent directory if it doesn't exist
        db_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Connect to database (creates file if doesn't exist)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create combos table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS combos (
                combo_id TEXT PRIMARY KEY,
                combo_name TEXT NOT NULL,
                combo_sequence TEXT NOT NULL,
                difficulty_level TEXT NOT NULL CHECK(difficulty_level IN ('Beginner', 'Intermediate', 'Advanced')),
                
                -- Learning state
                mastery_score REAL DEFAULT 0.0 CHECK(mastery_score >= 0.0 AND mastery_score <= 5.0),
                total_attempts INTEGER DEFAULT 0 CHECK(total_attempts >= 0),
                
                -- Scheduling information
                last_trained_timestamp TEXT,
                due_date TEXT,
                ease_factor REAL DEFAULT 2.0 CHECK(ease_factor >= 1.3 AND ease_factor <= 2.5),
                interval_days REAL DEFAULT 0.0 CHECK(interval_days >= 0.0),
                consecutive_successes INTEGER DEFAULT 0 CHECK(consecutive_successes >= 0),
                
                -- Metadata
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
                performance_score REAL CHECK(performance_score >= 0.0 AND performance_score <= 1.0),
                accuracy REAL CHECK(accuracy >= 0.0 AND accuracy <= 1.0),
                timing REAL CHECK(timing >= 0.0 AND timing <= 1.0),
                form_score REAL CHECK(form_score >= 0.0 AND form_score <= 1.0),
                combo_completion INTEGER CHECK(combo_completion >= 0),
                FOREIGN KEY (combo_id) REFERENCES combos(combo_id) ON DELETE CASCADE
            )
        ''')
        
        # Create indexes for faster queries
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_difficulty ON combos(difficulty_level)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_due_date ON combos(due_date)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_mastery ON combos(mastery_score)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_attempts ON combos(total_attempts)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_performance_combo ON performance_history(combo_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_performance_timestamp ON performance_history(timestamp)')
        
        conn.commit()
        conn.close()
        
        print(f"✓ Database schema created successfully")
        print(f"  Location: {db_file.absolute()}")
        print(f"  Tables: combos, performance_history")
        print(f"  Indexes: 6 indexes created for query optimization")
        
        return True
        
    except sqlite3.Error as e:
        print(f"✗ Database error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


def verify_schema(db_path='combos.db'):
    """Verify that database schema was created correctly.
    
    Args:
        db_path: Path to database file
        
    Returns:
        True if schema is valid, False otherwise
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check that tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = [row[0] for row in cursor.fetchall()]
        
        required_tables = ['combos', 'performance_history']
        for table in required_tables:
            if table not in tables:
                print(f"✗ Missing table: {table}")
                return False
        
        print(f"✓ Schema verification passed")
        print(f"  Tables found: {', '.join(tables)}")
        
        # Check combos table structure
        cursor.execute("PRAGMA table_info(combos)")
        columns = [row[1] for row in cursor.fetchall()]
        print(f"  Combos table columns: {len(columns)}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"✗ Verification failed: {e}")
        return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Create SQLite database schema for combo curriculum'
    )
    parser.add_argument(
        '--db-path',
        default='combos.db',
        help='Path to database file (default: combos.db)'
    )
    parser.add_argument(
        '--verify',
        action='store_true',
        help='Verify schema after creation'
    )
    
    args = parser.parse_args()
    
    print("="*60)
    print("COMBO CURRICULUM - DATABASE SCHEMA CREATION")
    print("="*60)
    print()
    
    # Create schema
    success = create_database(args.db_path)
    
    # Verify if requested
    if success and args.verify:
        print()
        verify_schema(args.db_path)
    
    print()
    if success:
        print("✓ Schema creation complete")
        print("  Next step: Run populate_combos.py to add combo data")
    else:
        print("✗ Schema creation failed")
        exit(1)
