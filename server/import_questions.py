import csv
import sqlite3
import os
from typing import Dict, List

DB_FILE = "questions.db"
CSV_FILE = "data/questionsData.csv"

def init_db():
    """Initialize the database with required tables."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create questions table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            question_number INTEGER PRIMARY KEY,
            correct_answer TEXT,
            difficulty INTEGER,
            topic TEXT
        )
    """)
    
    conn.commit()
    conn.close()

def parse_difficulty(diff_str: str) -> int:
    """Convert difficulty string to integer level (1-7)."""
    try:
        # First try to convert directly to integer
        diff = int(diff_str)
        # Ensure it's within our range
        return max(1, min(7, diff))
    except ValueError:
        # Map string difficulties to numeric levels
        diff_map = {
            "Very Easy": 1,
            "Easy": 2,
            "Moderate": 3,
            "Medium": 4,
            "Challenging": 5,
            "Hard": 6,
            "Very Hard": 7
        }
        return diff_map.get(diff_str, 4)  # Default to 4 (Medium) if unknown

def parse_answer(answer_str: str) -> str:
    """Parse the answer string (A, B, C, D, E) and return it."""
    if not answer_str:
        return ""
    return answer_str.strip().upper()

def import_questions():
    """Import questions from CSV into the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Clear existing questions
    cursor.execute("DELETE FROM questions")
    
    with open(CSV_FILE, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 6:  # Ensure row has enough columns including answer
                try:
                    question_number = int(row[1])
                    topic = row[3].strip()
                    difficulty = parse_difficulty(row[4].strip())
                    correct_answer = parse_answer(row[5])  # Get answer from column 6
                    
                    # Check if image exists
                    image_path = f"static/question {question_number}.png"
                    if not os.path.exists(image_path):
                        print(f"Warning: Image not found for question {question_number}")
                        continue
                    
                    # Insert question into database
                    cursor.execute("""
                        INSERT INTO questions (
                            question_number,
                            correct_answer,
                            difficulty,
                            topic
                        ) VALUES (?, ?, ?, ?)
                    """, (
                        question_number,
                        correct_answer,
                        difficulty,
                        topic
                    ))
                    
                except (ValueError, IndexError) as e:
                    print(f"Error processing row: {row}")
                    print(f"Error: {str(e)}")
                    continue
    
    conn.commit()
    conn.close()
    print("Question import completed!")

def main():
    """Main function to run the import process."""
    print("Initializing database...")
    init_db()
    
    print("Importing questions...")
    import_questions()
    
    print("Done!")

if __name__ == "__main__":
    main() 