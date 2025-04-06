# Adaptive Learning Backend

This is the backend service for the Adaptive Learning system, built with FastAPI and Firebase Authentication.

## Features

- Firebase Authentication integration
- Question management
- User progress tracking
- Adaptive difficulty adjustment
- RESTful API endpoints
- Database migrations
- Comprehensive testing

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up Firebase:
   - Create a Firebase project
   - Download the service account key (firebase-credentials.json)
   - Place it in the server directory

3. Initialize the database:
   ```bash
   python migrations.py
   ```

4. Run the development server:
   ```bash
   uvicorn api:app --reload
   ```

## API Documentation

Once the server is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints

### User Management
- `POST /users` - Create a new user
- `GET /users/me` - Get current user information

### Questions
- `GET /questions` - Get a question by topic and difficulty
- `POST /questions/{question_number}/check` - Check if an answer is correct

### Progress
- `POST /progress` - Update user progress
- `GET /progress` - Get user progress for all topics

## Testing

Run the test suite:
```bash
pytest test_api.py
```

## Database Migrations

The system uses a simple migration system to manage database schema changes. To run migrations:

```bash
python migrations.py
```

Current migrations:
1. Initial schema (users, questions, user_progress tables)
2. Add indexes for better performance
3. Add question metadata (description, explanation, tags)

## Environment Variables

Create a `.env` file in the server directory with the following variables:

```env
DATABASE_URL=sqlite:///adaptive_learning.db
ENVIRONMENT=development
```

## Security

- All endpoints require Firebase authentication
- CORS is configured to allow specific origins
- Input validation is implemented for all requests
- Error handling is in place for various scenarios

## Development

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the development server with hot reload:
   ```bash
   uvicorn api:app --reload
   ```

## Production Deployment

1. Set environment variables:
   ```bash
   export ENVIRONMENT=production
   ```

2. Run the production server:
   ```bash
   uvicorn api:app --host 0.0.0.0 --port 8000
   ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 