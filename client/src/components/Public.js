import { Link } from 'react-router-dom';
import logo from '../NavigationLogo.png';
const Public = () => {
    const content = (
        <section className="public">
        <nav className="navbar">
            <div className="logo-section">
                <img src={logo} alt="Master IQ Logo" className="logo" />
            </div>
            <div className="nav-links">
                <Link to="/login" className="nav-btn">Login</Link>
                <Link to="/signup" className="nav-btn">Signup</Link>
            </div>
        </nav>

        {/* Centered Welcome Section */}
        <div className="welcome-container">
            <img src={logo} alt="Master IQ Logo" className="center-logo" />
            <h2 className="subtitle">Build your Foundation</h2>

            <div className="welcome-text">
                <p><strong>Welcome to MasterIQ</strong> you're about to begin a personalized learning experience designed to help you truly understand and  master the material- not just memorize it.</p>
                <p>Here’s how it works:</p>
                <ul>
                    <li><strong>Adaptive difficulty:</strong> Get a question right, and we’ll raise the challenge to keep you sharp.</li>
                    <li><strong>Supportive review:</strong> Get one wrong, and we’ll adjust with easier questions to reinforce your understanding.</li>
                    <li><strong>Track your progress:</strong> See how your mastery improves over time with real feedback.</li>
                </ul>
            </div>
        </div>
    </section>

    )
    return content
}
export default Public