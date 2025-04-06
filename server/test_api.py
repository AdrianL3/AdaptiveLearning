import pytest
import requests
import json
from fastapi.testclient import TestClient
from api import app, RATE_LIMIT, RATE_LIMIT_WINDOW
import sqlite3
import os
import time

# Test client
client = TestClient(app)

# Test database setup
def setup_module(module):
    """Set up test database."""
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            firebase_uid TEXT UNIQUE,
            username TEXT,
            difficulty INTEGER DEFAULT 1
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            question_number INTEGER PRIMARY KEY,
            topic TEXT,
            difficulty INTEGER,
            correct_answer TEXT,
            image_path TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            topic TEXT,
            difficulty INTEGER,
            last_answer_correct BOOLEAN,
            last_updated TIMESTAMP,
            UNIQUE(user_id, topic)
        )
    ''')
    
    # Insert test data
    cursor.execute('''
        INSERT INTO questions (question_number, topic, difficulty, correct_answer, image_path)
        VALUES (1, 'Algebra', 1, 'A', 'images/1.png')
    ''')
    
    conn.commit()
    conn.close()

def teardown_module(module):
    """Clean up test database."""
    if os.path.exists('test.db'):
        os.remove('test.db')

# Mock Firebase token
MOCK_TOKEN = "mock_token"
MOCK_UID = "test_user_123"

# Test cases
def test_create_user():
    """Test user creation endpoint."""
    response = client.post(
        "/users",
        json={"username": "test_user", "difficulty": 1},
        headers={"Authorization": f"Bearer {MOCK_TOKEN}"}
    )
    assert response.status_code == 201
    assert response.json() == {"message": "User created successfully"}

def test_get_current_user():
    """Test getting current user information."""
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {MOCK_TOKEN}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["firebase_uid"] == MOCK_UID
    assert data["username"] == "test_user"

def test_get_question():
    """Test getting a question."""
    response = client.get(
        "/questions?topic=Algebra&difficulty=1",
        headers={"Authorization": f"Bearer {MOCK_TOKEN}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["topic"] == "Algebra"
    assert data["difficulty"] == 1
    assert data["correct_answer"] == "A"

def test_check_answer():
    """Test checking an answer."""
    response = client.post(
        "/questions/1/check",
        json={"answer": "A"},
        headers={"Authorization": f"Bearer {MOCK_TOKEN}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["is_correct"] is True
    assert data["correct_answer"] == "A"

def test_update_progress():
    """Test updating user progress."""
    response = client.post(
        "/progress",
        json={
            "topic": "Algebra",
            "difficulty": 2,
            "last_answer_correct": True
        },
        headers={"Authorization": f"Bearer {MOCK_TOKEN}"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Progress updated successfully"}

def test_get_progress():
    """Test getting user progress."""
    response = client.get(
        "/progress",
        headers={"Authorization": f"Bearer {MOCK_TOKEN}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "Algebra" in data
    assert data["Algebra"]["difficulty"] == 2
    assert data["Algebra"]["last_answer_correct"] is True

# Error cases
def test_invalid_topic():
    """Test getting a question with invalid topic."""
    response = client.get(
        "/questions?topic=Invalid&difficulty=1",
        headers={"Authorization": f"Bearer {MOCK_TOKEN}"}
    )
    assert response.status_code == 400

def test_invalid_difficulty():
    """Test getting a question with invalid difficulty."""
    response = client.get(
        "/questions?topic=Algebra&difficulty=8",
        headers={"Authorization": f"Bearer {MOCK_TOKEN}"}
    )
    assert response.status_code == 400

def test_invalid_answer():
    """Test checking an invalid answer."""
    response = client.post(
        "/questions/1/check",
        json={"answer": "E"},
        headers={"Authorization": f"Bearer {MOCK_TOKEN}"}
    )
    assert response.status_code == 422

def test_unauthorized_access():
    """Test accessing endpoints without authorization."""
    response = client.get("/users/me")
    assert response.status_code == 401

# Middleware tests
def test_content_type_validation():
    """Test content type validation middleware."""
    response = client.post(
        "/users",
        data="invalid data",
        headers={
            "Authorization": f"Bearer {MOCK_TOKEN}",
            "Content-Type": "text/plain"
        }
    )
    assert response.status_code == 415
    assert response.json()["detail"] == "Content-Type must be application/json"

def test_rate_limiting():
    """Test rate limiting middleware."""
    # Make requests up to the limit
    for _ in range(RATE_LIMIT):
        response = client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {MOCK_TOKEN}"}
        )
        assert response.status_code == 200
    
    # Next request should be rate limited
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {MOCK_TOKEN}"}
    )
    assert response.status_code == 429
    assert response.json()["detail"] == "Rate limit exceeded"
    
    # Wait for rate limit window to reset
    time.sleep(RATE_LIMIT_WINDOW)
    
    # Should be able to make requests again
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {MOCK_TOKEN}"}
    )
    assert response.status_code == 200

def test_cors_headers():
    """Test CORS headers."""
    response = client.options(
        "/users/me",
        headers={
            "Authorization": f"Bearer {MOCK_TOKEN}",
            "Origin": "http://localhost:3000"
        }
    )
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
    assert "access-control-allow-methods" in response.headers
    assert "access-control-allow-headers" in response.headers
    assert "access-control-max-age" in response.headers

if __name__ == "__main__":
    pytest.main([__file__]) 