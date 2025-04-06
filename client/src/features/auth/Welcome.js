import { Link } from 'react-router-dom'
import { auth } from './firebase';
import { useEffect, useState } from 'react';

const Welcome = () => {
    const [user, setUser] = useState(null);
    useEffect(() => {
        const unsubscribe = auth.onAuthStateChanged((currentUser) => {
            setUser(currentUser);
        });
    
        return () => unsubscribe(); // cleanup
    }, []);
    

    const content = (
        <section className="profile">
            <div className="profile-section">
                <h1>Profile and Statistics</h1>

                <p>Unique User Id: {user?.uid || 'Loading...'}</p>
                <p>Email Address: {user?.email || 'Loading...'}</p>
                <p>Display Name: {user?.displayName || 'Not set'}</p>

            </div>
            <div className="mastery-section">
                <h2>Mastery Statistics</h2>
                <div className="mastery-stats">
                    <label for="algebra">Algebra</label>
                    <p><progress id="algebra" value="0" max="100"></progress></p>
                    <label for="dataAnalysis">Data Analysis, Statistics, and Probability</label>
                    <p><progress id="dataAnalysis" value="0" max="100"></progress></p>
                    <label for="geometry">Geometry</label>
                    <p><progress id="geometry" value="0" max="100"></progress></p>
                    <label for="measurement">Measurement</label>
                    <p><progress id="measurement" value="0" max="100"></progress></p>
                    <label for="numberProperties">Number Properties and Operations</label>
                    <p><progress id="numberProperties" value="0" max="100"></progress></p>               
                </div>

                <Link to="/modules" className="btn btn-primary">Continue Learning</Link>
            </div>
        </section>
    )

    return content
}
export default Welcome