# Combo Database Setup - Instructions

This folder contains scripts to set up the combo curriculum database on your Jetson.

## Files Included

1. **setup_combo_database.py** - Main setup script (run this one)
2. **create_database_schema.py** - Creates database structure (called by setup script)
3. **populate_combos.py** - Populates combo data (called by setup script)

## Combo Library Summary

**Total: 50 combos**
- Beginner: 15 combos (single punches + 2-punch combos)
- Intermediate: 20 combos (3-punch combos, body shots, basic defense)
- Advanced: 15 combos (4-6 punch combos, complex defense patterns)

**Notation System:**
- `1-6` = Jab, Cross, Lead Hook, Rear Hook, Lead Uppercut, Rear Uppercut
- `1b-6b` = Same punches to the body
- `slip` = Slip (head movement)
- `block` = Block (defensive arms up)

**Examples:**
- Beginner: `1-2` (Jab-Cross)
- Intermediate: `1-2-3` (Jab-Cross-Lead Hook), `1-slip-2` (Jab-Slip-Cross)
- Advanced: `1-2-3-2-6` (Jab-Cross-Lead Hook-Cross-Rear Uppercut)

---

## Setup on Jetson (Ubuntu 22.04)

### Prerequisites

Python 3 is already installed on Ubuntu 22.04. SQLite comes built-in with Python.

Verify:
```bash
python3 --version
# Should show Python 3.8 or higher

python3 -c "import sqlite3; print('SQLite available')"
# Should print: SQLite available
```

### Installation Steps

#### 1. Clone your repository (if using Git)

```bash
cd ~
git clone https://github.com/yourusername/boxing-robot.git
cd boxing-robot/setup
```

Or if files are already on Jetson, navigate to the setup folder:
```bash
cd /path/to/setup/folder
```

#### 2. Run the setup script

**Basic usage (creates combos.db in current directory):**
```bash
python3 setup_combo_database.py
```

**With custom location:**
```bash
python3 setup_combo_database.py --db-path /opt/boxing_robot/data/combos.db
```

**Force reset without confirmation:**
```bash
python3 setup_combo_database.py --force
```

#### 3. Expected output

```
======================================================================
BOXING COMBO CURRICULUM - DATABASE SETUP
======================================================================

Step 1: Creating database schema...
  ✓ Tables created: combos, performance_history
  ✓ Indexes created: 6 indexes for query optimization

Step 2: Populating combo library...
  ✓ Inserted 50 combos

Step 3: Verifying database...
  ✓ All combos initialized correctly

  Combo counts by difficulty:
    Beginner     : 15 combos
    Intermediate : 20 combos
    Advanced     : 15 combos
    Total        : 50 combos

======================================================================
✓ SETUP COMPLETE
======================================================================

Database location: /home/user/combos.db
Database size: 45.0 KB

Next steps:
  1. Your application can now load combos from this database
  2. Test database access: sqlite3 combos.db "SELECT COUNT(*) FROM combos;"
  3. Run your training application
```

---

## Verification

### Manual verification using SQLite command line:

```bash
# Open database
sqlite3 combos.db

# Check total combos
SELECT COUNT(*) FROM combos;
-- Expected: 50

# Check by difficulty
SELECT difficulty_level, COUNT(*) FROM combos GROUP BY difficulty_level;
-- Expected:
-- Beginner|15
-- Intermediate|20
-- Advanced|15

# View first 5 beginner combos
SELECT combo_name, combo_sequence FROM combos WHERE difficulty_level = 'Beginner' LIMIT 5;
-- Expected:
-- Jab|1
-- Cross|2
-- Lead Hook|3
-- etc.

# Verify all untrained
SELECT COUNT(*) FROM combos WHERE total_attempts > 0;
-- Expected: 0

# Exit
.quit
```

### Python verification:

```python
import sqlite3

conn = sqlite3.connect('combos.db')
cursor = conn.cursor()

# Check total
cursor.execute("SELECT COUNT(*) FROM combos")
print(f"Total combos: {cursor.fetchone()[0]}")  # Should be 50

# Check a specific combo
cursor.execute("SELECT * FROM combos WHERE combo_id = 'beginner_007'")
row = cursor.fetchone()
print(f"Jab-Cross combo: {row}")

conn.close()
```

---

## Database Schema

### Combos Table

| Column | Type | Description |
|--------|------|-------------|
| combo_id | TEXT | Primary key (e.g., "beginner_001") |
| combo_name | TEXT | Human-readable name (e.g., "Jab-Cross") |
| combo_sequence | TEXT | Robot notation (e.g., "1-2") |
| difficulty_level | TEXT | "Beginner", "Intermediate", or "Advanced" |
| mastery_score | REAL | 0.0 to 5.0 (starts at 0.0) |
| total_attempts | INTEGER | Number of times trained (starts at 0) |
| last_trained_timestamp | TEXT | ISO datetime of last training |
| due_date | TEXT | ISO datetime when next review is due |
| ease_factor | REAL | 1.3 to 2.5 (starts at 2.0) |
| interval_days | REAL | Days until next review |
| consecutive_successes | INTEGER | Current success streak |
| created_date | TEXT | When combo was added to database |
| last_updated | TEXT | Last modification timestamp |

### Performance History Table

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Auto-incrementing primary key |
| combo_id | TEXT | Foreign key to combos table |
| timestamp | TEXT | When performance was recorded |
| performance_score | REAL | Aggregate score (0-1) |
| accuracy | REAL | Punch detection accuracy (0-1) |
| timing | REAL | Rhythm consistency (0-1) |
| form_score | REAL | Technique quality (0-1) |
| combo_completion | INTEGER | Number of complete reps |

---

## Troubleshooting

### Issue: "Permission denied"

**Solution:**
```bash
# Fix file permissions
chmod 644 combos.db

# Or move to user-writable location
mkdir -p ~/boxing_app/data
mv combos.db ~/boxing_app/data/
```

### Issue: "Database is locked"

**Solution:**
```bash
# Check if any process is using the database
lsof combos.db

# Close any open connections, then try again
```

### Issue: "Table already exists"

This is normal if you run setup twice. The script will ask if you want to reset.

**To force reset:**
```bash
python3 setup_combo_database.py --force
```

### Issue: Python import error

**Solution:**
```bash
# Verify Python 3 is installed
python3 --version

# Verify SQLite module
python3 -c "import sqlite3; print(sqlite3.version)"
```

---

## File Locations

### Recommended structure:

```
/home/user/boxing_app/
├── main_gui.py
├── combo_curriculum/
│   └── (curriculum engine - next step)
├── data/
│   └── combos.db          ← Database lives here
└── setup/
    ├── setup_combo_database.py
    ├── create_database_schema.py
    └── populate_combos.py
```

### Database file permissions:

```bash
# Should be readable/writable by app user
ls -l combos.db
# Expected: -rw-r--r-- user user ... combos.db

# Fix if needed:
chmod 644 combos.db
chown $USER:$USER combos.db
```

---

## Next Steps

After setup is complete:

1. ✅ Database created with 50 combos
2. ⏭️ Integrate curriculum engine (Python module that uses this database)
3. ⏭️ Connect to GUI (TechCorrSessionPage)
4. ⏭️ Test with placeholder analytics
5. ⏭️ Integrate CV system (when ready)

---

## Adding Custom Combos (Optional)

You can manually add combos to the database:

```sql
sqlite3 combos.db

INSERT INTO combos (
    combo_id, combo_name, combo_sequence, difficulty_level,
    mastery_score, total_attempts, ease_factor, interval_days,
    consecutive_successes, created_date
) VALUES (
    'custom_001',
    'My Custom Combo',
    '1-3-2-6',
    'Intermediate',
    0.0,
    0,
    2.0,
    0.0,
    0,
    datetime('now')
);

.quit
```

Or edit `populate_combos.py` and re-run the setup script.

---

## Support

For issues:
1. Check this README
2. Verify database with SQLite commands above
3. Check file permissions
4. Ensure Python 3.8+ is installed

Database size should be approximately 40-60 KB with 50 combos.
