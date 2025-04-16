# db.py
import sqlite3
import random
import csv
import os
import hashlib
from typing import Dict, Optional, Tuple

# Get the absolute path to the server directory
SERVER_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(SERVER_DIR, "adaptive_learning.db")
CSV_FILE = os.path.join(SERVER_DIR, "data", "questionsData.csv")

def init_db():
    """Initialize the database with required tables."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Drop existing tables if they exist
        cursor.execute('DROP TABLE IF EXISTS user_progress')
        cursor.execute('DROP TABLE IF EXISTS users')
        cursor.execute('DROP TABLE IF EXISTS questions')
        
        # Create questions table
        cursor.execute('''
            CREATE TABLE questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_number INTEGER NOT NULL,
                question_text TEXT NOT NULL,
                option_a TEXT NOT NULL,
                option_b TEXT NOT NULL,
                option_c TEXT NOT NULL,
                option_d TEXT NOT NULL,
                option_e TEXT NOT NULL,
                correct_answer TEXT NOT NULL,
                difficulty INTEGER NOT NULL,
                topic TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create users table with both overall and topic-specific difficulties
        cursor.execute('''
            CREATE TABLE users (
                firebase_uid TEXT PRIMARY KEY,
                username TEXT NOT NULL,
                overall_difficulty INTEGER DEFAULT 1,
                number_properties_difficulty INTEGER DEFAULT 1,
                data_analysis_difficulty INTEGER DEFAULT 1,
                measurement_difficulty INTEGER DEFAULT 1,
                algebra_difficulty INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create user progress table
        cursor.execute('''
            CREATE TABLE user_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                question_id INTEGER NOT NULL,
                is_correct BOOLEAN NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(firebase_uid),
                FOREIGN KEY (question_id) REFERENCES questions(id)
            )
        ''')
        
        conn.commit()
        print("Database initialized successfully!")
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

def get_db():
    """Get a database connection."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def create_user(firebase_uid: str) -> bool:
    """
    Create a new user in our local database using their Firebase UID.
    Returns True if successful, False if user already exists.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
        INSERT INTO users (
            firebase_uid,
            username,
            difficulty
        ) VALUES (?, ?, 1)
        """, (firebase_uid,))
        
        # Initialize user_progress for each topic
        topics = [
            "Algebra",
            "Data Analysis, Statistics, and Probability",
            "Geometry",
            "Measurement",
            "Number Properties and Operations"
        ]
        
        for topic in topics:
            cursor.execute("""
            INSERT INTO user_progress (user_id, topic, difficulty)
            VALUES (?, ?, 1)
            """, (firebase_uid, topic))
        
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_or_create_user(firebase_uid: str) -> Dict:
    """
    Get user information or create a new user if they don't exist.
    Returns the user's information.
    """
    user = get_user(firebase_uid)
    if not user:
        create_user(firebase_uid)
        user = get_user(firebase_uid)
    return user

def get_user(username: str) -> Optional[Dict]:
    """
    Get user information including overall and topic-specific difficulties.
    Returns None if user doesn't exist.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT 
        username,
        difficulty,
        created_at
    FROM users 
    WHERE username = ?
    """, (username,))
    
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {
            "username": user[0],
            "difficulty": user[1],
            "created_at": user[2]
        }
    return None

def import_questions():
    """Import questions from CSV file into the database."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        with open(CSV_FILE, 'r', encoding='latin1') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header row
            
            for row in csv_reader:
                if len(row) >= 6 and any(row):  # Check if row has at least 6 columns and is not empty
                    try:
                        question_number = int(row[1])  # Question number is in column 2
                        topic = row[3]  # Topic is in column 4
                        difficulty = int(row[4]) if row[4].strip() else 1  # Difficulty is in column 5, default to 1 if empty
                        correct_answer = row[5]  # Answer is in column 6
                        
                        # Insert the question into the database
                        cursor.execute('''
                            INSERT INTO questions (
                                question_number, 
                                topic, 
                                difficulty, 
                                question_text, 
                                option_a, 
                                option_b, 
                                option_c, 
                                option_d, 
                                option_e,
                                correct_answer
                            )
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            question_number, 
                            topic, 
                            difficulty, 
                            row[2],  # Question text
                            'Option A',  # Placeholder options
                            'Option B',
                            'Option C',
                            'Option D',
                            'Option E',
                            correct_answer
                        ))
                        
                    except (ValueError, IndexError) as e:
                        if any(row):  # Only print error for non-empty rows
                            print(f"Error processing row: {row}")
                            print(f"Error details: {str(e)}")
                        continue
                        
        conn.commit()
        print("Questions imported successfully!")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        
    finally:
        conn.close()

CSV_FILE = 'data/questionsData.csv'

def get_question_by_difficulty(topic: str, difficulty: int) -> Optional[Dict]:
    """
    Get a random question for the given topic and difficulty level.
    Returns None if no questions are available.
    """
    #conn = sqlite3.connect(DB_FILE)
    #cursor = conn.cursor()
    
    """# Get a random question within the difficulty range
    cursor.execute()
    SELECT 
        question_number,
        question_text,
        option_a,
        option_b,
        option_c,
        option_d,
        option_e,
        correct_answer,
        difficulty,
        topic
    FROM questions 
    WHERE topic = ? 
    AND difficulty = ?
    ORDER BY RANDOM()
    LIMIT 1
     (topic, difficulty)) """
        
    questions = []

    # Read the CSV file
    with open(CSV_FILE, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['topic'] == topic and int(row['difficulty']) == difficulty:
                questions.append(row)
                
    #question = cursor.fetchone()
    #conn.close()
    
    if questions:
        question = random.choice(questions)
        return {
            'question_number': question['question_number'],
            'question_text': question['question_text'],
            'correct_answer': question['correct_answer'],
            'difficulty': question['difficulty'],
            'topic': question['topic'],
            'image_url': f'/static/{question["question_number"]}.png'  # Updated image path
        }
    return None

def check_answer(question_number: int, user_answer: str) -> Tuple[bool, str]:
    """
    Check if the user's answer is correct.
    Returns (is_correct, correct_answer).
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT correct_answer
        FROM questions
        WHERE question_number = ?
    """, (question_number,))
    
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        return False, ""
        
    correct_answer = result[0]
    return user_answer.upper() == correct_answer.upper(), correct_answer

def update_user_progress(user_id: str, topic: str, question_difficulty: int, is_correct: bool) -> int:
    """
    Update user's progress based on their answer.
    Only increments difficulty if the question was more difficult than current level.
    Updates both the user_progress table and the user's topic-specific and overall difficulties.
    Returns the new difficulty level.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Get current difficulty for the topic
    cursor.execute("""
        SELECT difficulty
        FROM user_progress
        WHERE user_id = ? AND topic = ?
    """, (user_id, topic))
    
    result = cursor.fetchone()
    current_difficulty = result[0] if result else 1
    
    # Calculate new difficulty
    if is_correct and question_difficulty >= current_difficulty:
        new_difficulty = min(current_difficulty + 1, 7)  # Cap at 7
    elif not is_correct:
        new_difficulty = max(current_difficulty - 1, 1)  # Minimum 1
    else:
        new_difficulty = current_difficulty  # Stay the same if correct but not challenging enough
    
    # Update user_progress table
    cursor.execute("""
        INSERT OR REPLACE INTO user_progress
        (user_id, topic, difficulty, last_answer_correct, last_updated)
        VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
    """, (user_id, topic, new_difficulty, is_correct))
    
    # Update topic-specific difficulty in users table
    cursor.execute(f"""
        UPDATE users 
        SET difficulty = ?
        WHERE username = ?
    """, (new_difficulty, user_id))
    
    conn.commit()
    conn.close()
    return new_difficulty

def get_user_progress(user_id: str) -> Dict:
    """
    Get all progress for a user.
    Returns a dictionary mapping topics to progress data.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT topic, difficulty, last_answer_correct
        FROM user_progress
        WHERE user_id = ?
    """, (user_id,))
    
    progress = {}
    for row in cursor.fetchall():
        progress[row[0]] = {
            "difficulty": row[1],
            "last_answer_correct": bool(row[2])
        }
    
    conn.close()
    return progress

def answer_question(difficulty: int, user_answer: str):
    """
    Check the answer for the question at the given difficulty level.
    Returns True if correct, False otherwise.
    """
    