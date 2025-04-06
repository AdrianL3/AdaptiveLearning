// src/features/auth/Login.js
import React, { useState } from 'react';
import { signInWithEmailAndPassword } from 'firebase/auth';
import { auth } from './firebase';
import { useNavigate } from 'react-router-dom';
import Navbar from '../../components/Navbar';  // Import Navbar component

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const signIn = async (e) => {
        e.preventDefault();
        try {
            await signInWithEmailAndPassword(auth, email, password);
            navigate('/dash');  // Redirect to dash on success
        } catch (error) {
            const errorCode = error.code;

            if (errorCode === 'auth/wrong-password') {
                setError('Incorrect password. Please try again.');
            } else if (error.code === 'auth/user-not-found') {
                setError('No user found with this email. Please sign up.');
            } else {
                setError(error.message); // Display error from Firebase
            }
        }
    };

    return (
        <>
            <Navbar />  {/* Navbar component displayed at the top */}
            <div className="login-container">
                <form onSubmit={signIn} className="form-box">
                    {error && <p className="error-text">{error}</p>}
                    <div className="input-field">
                        <label>Email</label>
                        <input
                            type="email"
                            placeholder="Enter your email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </div>

                    <div className="input-field">
                        <label>Password</label>
                        <input
                            type="password"
                            placeholder="Enter your password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>

                    <div className="button-group">
                        <button type="submit" className="primary-btn">Sign In</button>
                    </div>

                    <div className="text-link">
                        <a href="/forgot-password">Forgot password?</a>
                    </div>
                </form>
            </div>
        </>
    );
};

export default Login;
