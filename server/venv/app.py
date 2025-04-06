import random
from PIL import Image
import os

questions = {
    1: [{"question": "What is 2 + 2?", "options": ["3", "4", "5", "6"], "answer": "4"}],
    2: [{"question": "What is 5 * 2?", "options": ["7", "10", "12", "15"], "answer": "10"}],
    3: [{"question": "What is 12 / 3?", "options": ["2", "4", "6", "3"], "answer": "4"}],
    4: [{"question": "Solve for x: x + 5 = 12", "options": ["6", "7", "8", "9"], "answer": "7"}],
    5: [{"question": "What is the square root of 81?", "options": ["7", "8", "9", "10"], "answer": "9"}],
    6: [{"question": "What is 15% of 200?", "options": ["25", "30", "35", "40"], "answer": "30"}],
    7: [{"question": "Derivative of x^2?", "options": ["x", "2x", "x^2", "1"], "answer": "2x"}]
}

# Used to avoid repetition
used_questions = {level: set() for level in questions.keys()}

difficulty = 4
max_difficulty = 7
min_difficulty = 1
history = []

print("📊 Welcome to the Adaptive Math Quiz (Beta)!")
print("Answer the questions. Difficulty adjusts as you go.\n")

def display_question(q):
    if isinstance(q["question"], str) and q["question"].lower().endswith(('.png', '.jpg', '.jpeg')):
        if os.path.exists(q["question"]):
            img = Image.open(q["question"])
            img.show()  # Opens image in default viewer
            print("[🖼️ Image question opened in viewer]")
        else:
            print(f"[❌ Image not found: {q['question']}]")
    else:
        print(q["question"])

while True:
    current_questions = questions[difficulty]

    # Filter out used questions
    available = [i for i in range(len(current_questions)) if i not in used_questions[difficulty]]
    if available:
        q_index = random.choice(available)
    else:
        # All used: allow repetition
        q_index = random.randint(0, len(current_questions) - 1)

    used_questions[difficulty].add(q_index)
    question = current_questions[q_index]

    print(f"\n📈 Difficulty Level {difficulty}")
    display_question(question)
    for idx, option in enumerate(question["options"]):
        print(f"{idx + 1}. {option}")

    try:
        choice = int(input("Your choice (1-4): ")) - 1
        user_answer = question["options"][choice]
    except (ValueError, IndexError):
        print("❌ Invalid input. Try again.\n")
        continue

    if user_answer == question["answer"]:
        print("✅ Correct!\n")
        history.append((difficulty, True))
        difficulty = min(difficulty + 1, max_difficulty)
    else:
        print(f"❌ Incorrect. The correct answer was {question['answer']}.\n")
        history.append((difficulty, False))
        difficulty = max(difficulty - 1, min_difficulty)

    # Check for mastery
    recent_hard = [res for lvl, res in history if lvl >= 6]
    if len(recent_hard) >= 6:
        accuracy = sum(res for res in recent_hard) / len(recent_hard)
        if accuracy >= 0.75:
            print(f"🎉 Mastery achieved! Accuracy at hard levels: {accuracy * 100:.0f}%")
            break



    