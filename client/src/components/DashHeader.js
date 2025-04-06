import { Link } from 'react-router-dom';
import logo from '../NavigationLogo.png'; // Ensure the path is correct

const DashHeader = () => {
    const content = (
        <header className="dash-header">
            <section className="public">
                <nav className="navbar">
                    <div className="logo-section">
                        <a href="/"><img src={logo} alt="Master IQ Logo" className="logo" /> </a>
                    </div>
                    <div className="nav-links">
                        <Link to="/" className="nav-btn">Home</Link>
                        <Link to="/modules" className="nav-btn">Modules</Link>
                        <Link to="/dash" className="nav-btn">Profile</Link>
                    </div>
                </nav>
            </section>
        </header>
    )

    return content
}
export default DashHeader