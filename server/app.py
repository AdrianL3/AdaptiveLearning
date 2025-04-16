from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from db import (
    init_db,
    import_questions,
    get_question_by_difficulty,
    get_user_progress,
    update_user_progress,
    check_answer
)
import os
import sqlite3

app = Flask(__name__)

# Configure CORS
CORS(app, 
     resources={r"/api/*": {
         "origins": ["http://localhost:3000"],
         "methods": ["GET", "POST", "OPTIONS"],
         "allow_headers": ["Content-Type", "Authorization"],
         "supports_credentials": True,
         "expose_headers": ["Content-Type", "Authorization"]
     }})

# Initialize database and import questions
init_db()
import_questions()

# Serve static files (question images)
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/questions', methods=['GET'])
def get_question():
    topic = request.args.get('topic')
    auth_header = request.headers.get('Authorization')
    
    '''
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Unauthorized'}), 401
        
    user_id = auth_header.split(' ')[1]  # Extract token from Bearer header
    
    if not topic:
        return jsonify({'error': 'Topic is required'}), 400
    '''
    
    question = get_question_by_difficulty(topic="Data Analysis, Statistics, and Probability", difficulty=5)
    if not question:
        return jsonify({'error': 'No questions available'}), 404
        
    # Add the full URL to the image path
    question['image_url'] = f"http://localhost:64000/static/{question['image_url']}"
    
    # Remove the correct answer from the response
    correct_answer = question.pop('correct_answer')
    return jsonify(question)

@app.route('/api/questions/answer', methods=['POST'])
def check_question_answer():
    data = request.json
    question_number = data.get('question_id')
    answer = data.get('answer')
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Unauthorized'}), 401
        
    user_id = auth_header.split(' ')[1]  # Extract token from Bearer header
    
    if not all([question_number, answer]):
        return jsonify({'error': 'Missing required fields'}), 400
        
    is_correct, correct_answer = check_answer(question_number, answer)
    
    # Get the topic from the question
    question = get_question_by_difficulty(user_id, None)  # Get any question to get topic
    if question:
        new_difficulty = update_user_progress(user_id, question['topic'], is_correct)
    
    return jsonify({
        'correct': is_correct,
        'correct_answer': correct_answer,
        'new_difficulty': new_difficulty
    })

@app.route('/api/questions/topics', methods=['GET'])
def get_topics():
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Unauthorized'}), 401
        
    # Get unique topics from the database
    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT topic FROM questions")
    topics = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(topics)

@app.route('/api/users/progress', methods=['GET'])
def get_user_progress_endpoint():
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Unauthorized'}), 401
        
    user_id = auth_header.split(' ')[1]  # Extract token from Bearer header
    progress = get_user_progress(user_id)
    return jsonify(progress)

if __name__ == '__main__':
    app.run(port=64000, debug = True)



    