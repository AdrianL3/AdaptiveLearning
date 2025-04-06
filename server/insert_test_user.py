import sqlite3
import os
from datetime import datetime

# Get the absolute path to the database file
SERVER_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(SERVER_DIR, 'adaptive_learning.db')

def insert_test_user():
    try:
        # Connect to the database
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Insert test user with both overall and topic-specific difficulties
        test_user = {
            'firebase_uid': 'test_user_123',
            'username': 'testuser',
            'overall_difficulty': 1,
            'number_properties_difficulty': 1,
            'data_analysis_difficulty': 1,
            'measurement_difficulty': 1,
            'algebra_difficulty': 1,
            'created_at': datetime.now().isoformat()
        }
        
        cursor.execute('''
            INSERT INTO users (
                firebase_uid, 
                username, 
                overall_difficulty,
                number_properties_difficulty,
                data_analysis_difficulty,
                measurement_difficulty,
                algebra_difficulty,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            test_user['firebase_uid'],
            test_user['username'],
            test_user['overall_difficulty'],
            test_user['number_properties_difficulty'],
            test_user['data_analysis_difficulty'],
            test_user['measurement_difficulty'],
            test_user['algebra_difficulty'],
            test_user['created_at']
        ))
        
        # Commit the changes
        conn.commit()
        print("Test user inserted successfully!")
        
        # Verify the insertion
        cursor.execute('SELECT * FROM users WHERE firebase_uid = ?', (test_user['firebase_uid'],))
        inserted_user = cursor.fetchone()
        print("\nInserted user details:")
        print(f"Firebase UID: {inserted_user[0]}")
        print(f"Username: {inserted_user[1]}")
        print(f"Overall Difficulty: {inserted_user[2]}")
        print(f"Number Properties Difficulty: {inserted_user[3]}")
        print(f"Data Analysis Difficulty: {inserted_user[4]}")
        print(f"Measurement Difficulty: {inserted_user[5]}")
        print(f"Algebra Difficulty: {inserted_user[6]}")
        print(f"Created At: {inserted_user[7]}")
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    insert_test_user() 