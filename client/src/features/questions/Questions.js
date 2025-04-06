import React, { useState, useEffect } from 'react';
import './Questions.css';
import { getQuestion, checkAnswer } from '../api';

const Questions = () => {
    const [currentQuestion, setCurrentQuestion] = useState(null);
    const [selectedAnswer, setSelectedAnswer] = useState('');
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState('');
    const [feedback, setFeedback] = useState('');

    useEffect(() => {
        fetchQuestion();
    }, []);

    const fetchQuestion = async () => {
        try {
            setIsLoading(true);
            setError('');
            setFeedback('');
            
            // Get question based on user's current difficulty
            const response = await getQuestion();
            setCurrentQuestion(response.data);
        } catch (err) {
            console.error('Error fetching question:', err);
            setError('Failed to load question. Please try again.');
        } finally {
            setIsLoading(false);
        }
    };

    const handleAnswerSubmit = async (e) => {
        e.preventDefault();
        if (!selectedAnswer) {
            setError('Please select an answer');
            return;
        }

        try {
            setError('');
            setFeedback('');

            // Get user data from localStorage
            const userData = JSON.parse(localStorage.getItem('user'));
            if (!userData) {
                throw new Error('User data not found');
            }

            // Submit answer
            const response = await checkAnswer(currentQuestion.question_number, selectedAnswer);

            // Update user data in localStorage
            const updatedUserData = {
                ...userData,
                overall_difficulty: response.data.new_difficulty,
                [currentQuestion.topic.toLowerCase() + '_difficulty']: response.data.new_difficulty
            };
            localStorage.setItem('user', JSON.stringify(updatedUserData));

            // Show feedback
            setFeedback(response.data.is_correct ? 'Correct!' : 'Incorrect. Try again!');
            
            // Fetch new question after a delay
            setTimeout(fetchQuestion, 2000);
        } catch (err) {
            console.error('Error submitting answer:', err);
            setError('Failed to submit answer. Please try again.');
        }
    };

    if (isLoading) {
        return <div className="loading">Loading question...</div>;
    }

    if (error) {
        return <div className="error">{error}</div>;
    }

    if (!currentQuestion) {
        return <div>No question available</div>;
    }

    return (
        <div className="questions-container">
            <div className="question-card">
                <h2>Question</h2>
                <div className="question-image">
                    <img 
                        src={currentQuestion.image_url} 
                        alt="Question" 
                        onError={(e) => {
                            e.target.onerror = null;
                            e.target.src = '/placeholder-image.png';
                        }}
                    />
                </div>
                <form onSubmit={handleAnswerSubmit}>
                    <div className="options-container">
                        {['A', 'B', 'C', 'D', 'E'].map((option) => (
                            <div key={option} className="option">
                                <input
                                    type="radio"
                                    id={`option-${option}`}
                                    name="answer"
                                    value={option}
                                    checked={selectedAnswer === option}
                                    onChange={(e) => setSelectedAnswer(e.target.value)}
                                />
                                <label htmlFor={`option-${option}`}>
                                    {currentQuestion[`option_${option.toLowerCase()}`]}
                                </label>
                            </div>
                        ))}
                    </div>
                    <button 
                        type="submit" 
                        className="submit-button"
                        disabled={!selectedAnswer}
                    >
                        Submit Answer
                    </button>
                </form>
                {feedback && (
                    <div className={`feedback ${feedback.includes('Correct') ? 'correct' : 'incorrect'}`}>
                        {feedback}
                    </div>
                )}
            </div>
        </div>
    );
};

export default Questions;
