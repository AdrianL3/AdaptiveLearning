import { Link } from 'react-router-dom';
import logo from '../NavigationLogo.png';
const Public = () => {
    const content = (
        <section className="public">
            <nav className="navbar">
                <div className="logo-section">
                    <img src={logo} alt="Master IQ Logo" className="logo" />
                    <div className="site-title">
                        <span className="site-name">MASTER</span>
                        <span className="site-sub">IQ</span>
                    </div>
                </div>
                <div className="nav-links">
                    <Link to="/" className="nav-btn">Home</Link>
                    <Link to="/modules" className="nav-btn">Modules</Link>
                    <Link to="/profile" className="nav-btn">Profile</Link>
                    <Link to="/" className="nav-btn">Login</Link>
                    <Link to="/" className="nav-btn">Signup</Link>
                </div>
            </nav>
        </section>

    )
    return content
}
export default Public