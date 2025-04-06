import sqlite3
import os
from datetime import datetime

def get_db_version(db_path):
    """Get current database version."""
    if not os.path.exists(db_path):
        return 0
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT version FROM schema_version")
        version = cursor.fetchone()[0]
    except sqlite3.OperationalError:
        version = 0
    
    conn.close()
    return version

def set_db_version(db_path, version):
    """Set database version."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schema_version (
            version INTEGER PRIMARY KEY,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("DELETE FROM schema_version")
    cursor.execute("INSERT INTO schema_version (version) VALUES (?)", (version,))
    
    conn.commit()
    conn.close()

def migrate(db_path):
    """Run database migrations."""
    current_version = get_db_version(db_path)
    
    # Migration 1: Initial schema
    if current_version < 1:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                firebase_uid TEXT UNIQUE,
                username TEXT,
                difficulty INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create questions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                question_number INTEGER PRIMARY KEY,
                topic TEXT,
                difficulty INTEGER,
                correct_answer TEXT,
                image_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create user_progress table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                topic TEXT,
                difficulty INTEGER,
                last_answer_correct BOOLEAN,
                last_updated TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, topic)
            )
        ''')
        
        conn.commit()
        conn.close()
        set_db_version(db_path, 1)
        print("Migration 1 completed: Initial schema created")
    
    # Migration 2: Add indexes
    if current_version < 2:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Add indexes for better query performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_questions_topic_difficulty ON questions(topic, difficulty)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_progress_user_id ON user_progress(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_progress_topic ON user_progress(topic)')
        
        conn.commit()
        conn.close()
        set_db_version(db_path, 2)
        print("Migration 2 completed: Indexes added")
    
    # Migration 3: Add question metadata
    if current_version < 3:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Add metadata columns to questions table
        cursor.execute('ALTER TABLE questions ADD COLUMN description TEXT')
        cursor.execute('ALTER TABLE questions ADD COLUMN explanation TEXT')
        cursor.execute('ALTER TABLE questions ADD COLUMN tags TEXT')
        
        conn.commit()
        conn.close()
        set_db_version(db_path, 3)
        print("Migration 3 completed: Question metadata added")

if __name__ == "__main__":
    db_path = "adaptive_learning.db"
    migrate(db_path)
    print(f"Database migration completed. Current version: {get_db_version(db_path)}") 