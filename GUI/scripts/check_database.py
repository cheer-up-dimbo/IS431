#!/usr/bin/env python3
"""Database diagnostic utility for checking database tables and content."""

import sqlite3
import os
import sys
from pathlib import Path

# Handle both GUI root and scripts/ execution
script_dir = os.path.dirname(os.path.abspath(__file__))
gui_dir = os.path.dirname(script_dir)
os.chdir(gui_dir)  # Change to GUI directory for relative paths to work


def check_database(db_path: str) -> dict:
    """
    Check database structure and content.
    
    Args:
        db_path: Path to the SQLite database file
        
    Returns:
        Dictionary with database info or error message
    """
    if not os.path.exists(db_path):
        return {"status": "error", "message": f"Database not found: {db_path}"}
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [t[0] for t in cursor.fetchall()]
        
        result = {
            "status": "success",
            "path": db_path,
            "tables": tables,
            "table_info": {}
        }
        
        # Get row counts for each table
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                result["table_info"][table] = {"row_count": count}
            except:
                result["table_info"][table] = {"row_count": "N/A"}
        
        conn.close()
        return result
    
    except Exception as e:
        return {"status": "error", "message": str(e)}


def main():
    """Check all combo databases."""
    print("=" * 70)
    print("DATABASE DIAGNOSTIC UTILITY")
    print("=" * 70)
    
    # Check setup database
    setup_db = "setup/combos.db"
    print(f"\n📊 Checking {setup_db}:")
    result = check_database(setup_db)
    
    if result["status"] == "success":
        print(f"  ✓ Database found")
        print(f"  Tables: {', '.join(result['tables']) if result['tables'] else 'None'}")
        for table, info in result["table_info"].items():
            count = info["row_count"]
            print(f"    - {table}: {count} rows")
    else:
        print(f"  ✗ {result['message']}")
    
    # Check root combos database (if exists - shouldn't)
    parent_db = "../combos.db"
    print(f"\n📊 Checking {parent_db}:")
    result = check_database(parent_db)
    
    if result["status"] == "success":
        print(f"  ⚠️ Database found (should be in setup/)")
        print(f"  Tables: {', '.join(result['tables']) if result['tables'] else 'None'}")
        for table, info in result["table_info"].items():
            count = info["row_count"]
            print(f"    - {table}: {count} rows")
    else:
        print(f"  ✓ Not found (correct)")
    
    print("\n" + "=" * 70)
    print("RECOMMENDATION:")
    print("  Database should be located at: GUI/setup/combos.db")
    print("  Make sure main_gui.py uses the correct path.")
    print("=" * 70)


if __name__ == "__main__":
    main()
