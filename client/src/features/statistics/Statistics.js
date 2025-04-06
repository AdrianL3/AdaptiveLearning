import React, { useState, useEffect } from 'react';
import './Statistics.css';

const Statistics = () => {
    const [userData, setUserData] = useState(null);

    useEffect(() => {
        // Get user data from localStorage
        const storedUser = localStorage.getItem('user');
        if (storedUser) {
            const user = JSON.parse(storedUser);
            setUserData(user);
            console.log('User data loaded:', user);
        }
    }, []);

    if (!userData) {
        return <div>Loading user data...</div>;
    }

    return (
        <div className="statistics-container">
            <h2>Your Progress</h2>
            <div className="difficulty-levels">
                <div className="difficulty-card">
                    <h3>Overall Difficulty</h3>
                    <div className="difficulty-bar">
                        <div 
                            className="difficulty-fill" 
                            style={{ width: `${(userData.overall_difficulty / 7) * 100}%` }}
                        >
                            Level {userData.overall_difficulty}
                        </div>
                    </div>
                </div>

                <div className="difficulty-card">
                    <h3>Number Properties</h3>
                    <div className="difficulty-bar">
                        <div 
                            className="difficulty-fill" 
                            style={{ width: `${(userData.number_properties_difficulty / 7) * 100}%` }}
                        >
                            Level {userData.number_properties_difficulty}
                        </div>
                    </div>
                </div>

                <div className="difficulty-card">
                    <h3>Data Analysis</h3>
                    <div className="difficulty-bar">
                        <div 
                            className="difficulty-fill" 
                            style={{ width: `${(userData.data_analysis_difficulty / 7) * 100}%` }}
                        >
                            Level {userData.data_analysis_difficulty}
                        </div>
                    </div>
                </div>

                <div className="difficulty-card">
                    <h3>Measurement</h3>
                    <div className="difficulty-bar">
                        <div 
                            className="difficulty-fill" 
                            style={{ width: `${(userData.measurement_difficulty / 7) * 100}%` }}
                        >
                            Level {userData.measurement_difficulty}
                        </div>
                    </div>
                </div>

                <div className="difficulty-card">
                    <h3>Algebra</h3>
                    <div className="difficulty-bar">
                        <div 
                            className="difficulty-fill" 
                            style={{ width: `${(userData.algebra_difficulty / 7) * 100}%` }}
                        >
                            Level {userData.algebra_difficulty}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Statistics;
