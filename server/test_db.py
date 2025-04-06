import json
from db import (
    init_db,
    import_questions,
    get_question_by_difficulty,
    check_answer,
    update_user_progress,
    get_user_progress,
    create_user,
    get_user
)

def test_question_cycle():
    print("Initializing database...\n")
    init_db()
    import_questions()
    
    # Start with difficulty 1
    user_id = "test_user"
    topic = "Algebra"
    difficulty = 1
    
    print("1. Getting initial question...")
    question = get_question_by_difficulty(topic, difficulty)
    if not question:
        print("No questions found at any difficulty level!")
        return
    print("Question JSON:")
    print(json.dumps(question, indent=2))
    
    print("\n2. Checking answer...")
    user_answer = "B"  # Simulate user answering incorrectly
    is_correct, correct_answer = check_answer(question["question_number"], user_answer)
    print(f"User answer: {user_answer}")
    print(f"Correct answer: {correct_answer}")
    print(f"Is correct: {is_correct}")
    
    print("\n3. Updating user progress...")
    new_difficulty = update_user_progress(user_id, topic, difficulty, is_correct)
    print(f"New difficulty: {new_difficulty}")
    
    print("\n4. Getting next question with updated difficulty...")
    next_question = get_question_by_difficulty(topic, new_difficulty)
    if not next_question:
        print("No questions found at new difficulty level!")
        return
    print("Next Question JSON:")
    print(json.dumps(next_question, indent=2))
    
    print("\nFinal User Progress:")
    progress = get_user_progress(user_id)
    print(json.dumps(progress, indent=2))

def test_user_progress():
    print("Initializing database...\n")
    init_db()
    import_questions()
    
    # Create a test user with Firebase UID
    firebase_uid = "test_user_123"
    print("1. Creating test user...")
    success = create_user(firebase_uid)
    print(f"User creation {'successful' if success else 'failed'}")
    
    # Get initial user state
    print("\n2. Initial user state:")
    user = get_user(firebase_uid)
    print(json.dumps(user, indent=2))
    
    # Test progress in different topics
    print("\n3. Testing progress updates across topics...")
    topics = [
        "Algebra",
        "Data Analysis, Statistics, and Probability",
        "Geometry"
    ]
    
    for topic in topics:
        print(f"\nTesting {topic}:")
        # Get a question at current difficulty
        current_difficulty = user["topic_difficulties"][topic]
        question = get_question_by_difficulty(topic, current_difficulty)
        if question:
            print(f"Got question {question['question_number']} at difficulty {question['difficulty']}")
            print(f"User's current difficulty: {current_difficulty}")
            
            # Simulate correct answer
            is_correct, _ = check_answer(question["question_number"], question["correct_answer"])
            new_difficulty = update_user_progress(firebase_uid, topic, question["difficulty"], is_correct)
            print(f"Answered correctly, new difficulty: {new_difficulty}")
            
            # Get another question at higher difficulty
            higher_difficulty = min(current_difficulty + 1, 7)
            question = get_question_by_difficulty(topic, higher_difficulty)
            if question:
                print(f"\nGot harder question {question['question_number']} at difficulty {question['difficulty']}")
                is_correct, _ = check_answer(question["question_number"], question["correct_answer"])
                new_difficulty = update_user_progress(firebase_uid, topic, question["difficulty"], is_correct)
                print(f"Answered correctly, new difficulty: {new_difficulty}")
    
    # Get final user state
    print("\n4. Final user state:")
    user = get_user(firebase_uid)
    print(json.dumps(user, indent=2))

if __name__ == "__main__":
    test_user_progress() 