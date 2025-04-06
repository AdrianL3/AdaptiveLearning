import axios from 'axios';

// Create axios instance with base URL
const api = axios.create({
    baseURL: 'http://localhost:64000',
    headers: {
        'Content-Type': 'application/json',
    }
});

// Request interceptor
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        console.error('Request error:', error);
        return Promise.reject(error);
    }
);

// Response interceptor
api.interceptors.response.use(
    (response) => {
        return response;
    },
    (error) => {
        console.error('Response error:', error);
        if (error.response) {
            console.error('Error response:', error.response.data);
            if (error.response.status === 401) {
                // Handle unauthorized access
                localStorage.removeItem('token');
                window.location.href = '/login';
            }
        }
        return Promise.reject(error);
    }
);

// User endpoints
export const createUser = async (userData) => {
    console.log('Creating user with data:', userData);
    return api.post('/api/users', userData);
};

export const getCurrentUser = async () => {
    console.log('Fetching current user');
    return api.get('/api/users/me');
};

// Question endpoints
export const getQuestion = async () => {
    console.log('Fetching question');
    return api.get('/api/questions');
};

export const checkAnswer = async (questionNumber, answer) => {
    console.log('Checking answer:', { questionNumber, answer });
    return api.post(`/api/questions/${questionNumber}/check`, { answer });
};

// Progress endpoints
export const updateProgress = async (progressData) => {
    console.log('Updating progress:', progressData);
    return api.post('/api/progress', progressData);
};

export const getProgress = async () => {
    console.log('Fetching progress');
    return api.get('/api/progress');
};

export default api; 