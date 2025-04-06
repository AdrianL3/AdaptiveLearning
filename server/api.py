from fastapi import FastAPI, HTTPException, Depends, Query, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator
import firebase_admin
from firebase_admin import credentials, auth
from firebase_admin import exceptions as firebase_exceptions
import sqlite3
import logging
import os
from datetime import datetime
from db import (
    create_user,
    get_user,
    get_question_by_difficulty,
    check_answer,
    update_user_progress,
    get_user_progress
)
import time
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Rate limiting configuration
RATE_LIMIT = 100  # requests per minute
RATE_LIMIT_WINDOW = 60  # seconds

# Request tracking
request_counts = {}

# Request validation middleware
class RequestValidationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Log request
        logger.info(f"Request: {request.method} {request.url.path}")
        
        # Validate content type for POST requests
        if request.method == "POST":
            content_type = request.headers.get("content-type", "")
            if not content_type.startswith("application/json"):
                return JSONResponse(
                    status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                    content={"detail": "Content-Type must be application/json"}
                )
        
        # Process request
        response = await call_next(request)
        return response

# Rate limiting middleware
class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Get user ID from token
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                decoded_token = auth.verify_id_token(token)
                user_id = decoded_token['uid']
                
                # Get current timestamp
                current_time = time.time()
                
                # Initialize user's request count if not exists
                if user_id not in request_counts:
                    request_counts[user_id] = {
                        'count': 0,
                        'window_start': current_time
                    }
                
                # Reset counter if window has passed
                if current_time - request_counts[user_id]['window_start'] > RATE_LIMIT_WINDOW:
                    request_counts[user_id] = {
                        'count': 0,
                        'window_start': current_time
                    }
                
                # Check rate limit
                if request_counts[user_id]['count'] >= RATE_LIMIT:
                    return JSONResponse(
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        content={"detail": "Rate limit exceeded"}
                    )
                
                # Increment request count
                request_counts[user_id]['count'] += 1
                
            except Exception as e:
                logger.warning(f"Rate limit check failed: {str(e)}")
        
        # Process request
        response = await call_next(request)
        return response

# Initialize Firebase Admin
try:
    cred = credentials.Certificate(json.loads(os.getenv('FIREBASE_SERVICE_ACCOUNT')))
    firebase_admin.initialize_app(cred)
    logger.info("Firebase Admin initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Firebase Admin: {str(e)}")
    raise

# Initialize FastAPI app with middleware
app = FastAPI(
    title="Adaptive Learning API",
    description="API for adaptive learning system with Firebase authentication",
    version="1.0.0",
    middleware=[
        Middleware(RequestValidationMiddleware),
        Middleware(RateLimitMiddleware)
    ]
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Constants
VALID_TOPICS = ["Algebra", "Geometry", "Calculus", "Statistics"]
MIN_DIFFICULTY = 1
MAX_DIFFICULTY = 7

# Pydantic models for request validation
class UserCreate(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    difficulty: int = Field(default=1, ge=1, le=7)

class CheckAnswerRequest(BaseModel):
    answer: str = Field(..., description="User's answer (A, B, C, or D)")
    
    @field_validator('answer')
    def validate_answer(cls, v):
        if v.upper() not in ['A', 'B', 'C', 'D']:
            raise ValueError('Answer must be A, B, C, or D')
        return v.upper()

class UpdateProgressRequest(BaseModel):
    topic: str = Field(..., description="Topic name")
    difficulty: int = Field(..., description="Current difficulty level")
    last_answer_correct: bool = Field(..., description="Whether the last answer was correct")
    
    @field_validator('topic')
    def validate_topic(cls, v):
        if v not in VALID_TOPICS:
            raise ValueError(f'Topic must be one of: {", ".join(VALID_TOPICS)}')
        return v
    
    @field_validator('difficulty')
    def validate_difficulty(cls, v):
        if not MIN_DIFFICULTY <= v <= MAX_DIFFICULTY:
            raise ValueError(f'Difficulty must be between {MIN_DIFFICULTY} and {MAX_DIFFICULTY}')
        return v

# Error handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logger.warning(f"Validation error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": str(exc)}
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    logger.warning(f"HTTP error: {str(exc)}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(sqlite3.Error)
async def database_exception_handler(request, exc):
    logger.error(f"Database error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Database operation failed"}
    )

@app.exception_handler(firebase_exceptions.FirebaseError)
async def firebase_exception_handler(request, exc):
    logger.error(f"Firebase error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": "Authentication failed"}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred"}
    )

# Dependency for Firebase authentication
async def verify_token(authorization: str = Depends(lambda x: x.headers.get("Authorization"))):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header"
        )
    
    token = authorization.split(" ")[1]
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        logger.error(f"Token verification failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

# Database connection
def get_db():
    conn = sqlite3.connect('adaptive_learning.db')
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

# API endpoints
@app.post("/api/users", status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    token: Dict[str, Any] = Depends(verify_token),
    db: sqlite3.Connection = Depends(get_db)
):
    """Create a new user in the database."""
    try:
        logger.info(f"Received create user request for Firebase UID: {token['uid']}")
        logger.info(f"User data: username={user.username}, difficulty={user.difficulty}")
        
        # Verify token is valid
        if not token or 'uid' not in token:
            logger.error("Invalid token received")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token"
            )
        
        # Check if user already exists
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE firebase_uid = ?", (token['uid'],))
        existing_user = cursor.fetchone()
        
        if existing_user:
            logger.warning(f"User already exists with Firebase UID: {token['uid']}")
            return {"message": "User already exists", "uid": token['uid']}
        
        # Create new user
        cursor.execute(
            "INSERT INTO users (firebase_uid, username, difficulty) VALUES (?, ?, ?)",
            (token['uid'], user.username, user.difficulty)
        )
        db.commit()
        logger.info(f"User created successfully in database: {token['uid']}")
        return {"message": "User created successfully", "uid": token['uid']}
    except sqlite3.IntegrityError as e:
        logger.error(f"Database integrity error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )
    except sqlite3.Error as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        logger.error(f"Error type: {type(e)}")
        logger.error(f"Error args: {e.args}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

@app.get("/api/users/me")
async def get_current_user(
    token: Dict[str, Any] = Depends(verify_token),
    db: sqlite3.Connection = Depends(get_db)
):
    """Get current user's information."""
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE firebase_uid = ?", (token['uid'],))
        user = cursor.fetchone()
        if not user:
            logger.warning(f"User not found: {token['uid']}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return dict(user)
    except sqlite3.Error as e:
        logger.error(f"Database error while fetching user: {str(e)}")
        raise

@app.get("/api/questions")
async def get_question():
    """Get a random question based on the test user's difficulty level."""
    try:
        # Get test user from database
        user = get_user("testuser123")
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Test user not found"
            )
        
        # Get question based on test user's overall difficulty
        question = get_question_by_difficulty("Algebra", user["overall_difficulty"])
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No questions available"
            )
        
        return question
        
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error getting question: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get question"
        )

@app.post("/api/questions/{question_number}/check")
async def check_answer(
    question_number: int,
    request: CheckAnswerRequest,
    token: Dict[str, Any] = Depends(verify_token),
    db: sqlite3.Connection = Depends(get_db)
):
    """Check if the answer is correct."""
    try:
        cursor = db.cursor()
        cursor.execute("SELECT correct_answer FROM questions WHERE question_number = ?", (question_number,))
        question = cursor.fetchone()
        if not question:
            logger.warning(f"Question not found: {question_number}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question not found"
            )
        
        is_correct = question['correct_answer'] == request.answer
        logger.info(f"Answer checked for question {question_number}: {'correct' if is_correct else 'incorrect'}")
        return {
            "is_correct": is_correct,
            "correct_answer": question['correct_answer']
        }
    except sqlite3.Error as e:
        logger.error(f"Database error while checking answer: {str(e)}")
        raise

@app.post("/api/progress")
async def update_progress(
    request: UpdateProgressRequest,
    token: Dict[str, Any] = Depends(verify_token),
    db: sqlite3.Connection = Depends(get_db)
):
    """Update user's progress for a topic."""
    try:
        cursor = db.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO user_progress 
            (user_id, topic, difficulty, last_answer_correct, last_updated)
            VALUES (?, ?, ?, ?, ?)
            """,
            (token['uid'], request.topic, request.difficulty, request.last_answer_correct, datetime.now())
        )
        db.commit()
        logger.info(f"Progress updated for user {token['uid']} in topic {request.topic}")
        return {"message": "Progress updated successfully"}
    except sqlite3.Error as e:
        logger.error(f"Database error while updating progress: {str(e)}")
        raise

@app.get("/api/progress")
async def get_progress(
    token: Dict[str, Any] = Depends(verify_token),
    db: sqlite3.Connection = Depends(get_db)
):
    """Get user's progress for all topics."""
    try:
        cursor = db.cursor()
        cursor.execute(
            "SELECT topic, difficulty, last_answer_correct FROM user_progress WHERE user_id = ?",
            (token['uid'],)
        )
        progress = cursor.fetchall()
        if not progress:
            logger.info(f"No progress found for user {token['uid']}")
            return {}
        
        result = {}
        for row in progress:
            result[row['topic']] = {
                "difficulty": row['difficulty'],
                "last_answer_correct": bool(row['last_answer_correct'])
            }
        return result
    except sqlite3.Error as e:
        logger.error(f"Database error while fetching progress: {str(e)}")
        raise 