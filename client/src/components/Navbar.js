import { Link } from 'react-router-dom';
import logo from '../NavigationLogo.png';  // Make sure the path to your logo is correct

const Navbar = () => {
    return (
        <nav className="navbar" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            {/* Logo Section (on the left) */}
            <div className="logo-section">
                <img src={logo} alt="Master IQ Logo" className="logo" />
            </div>

            {/* Centered Section (Question and Signup Button) */}
            <div className="nav-links" style={{ display: 'flex', justifyContent: 'center', flex: 1 }}>
                <p style={{ marginRight: '10px', fontSize: '1.5rem' }}>Don't have an account?</p>
                <Link to="/signup" className="nav-btn">
                    Signup
                </Link>
            </div>
        </nav>
    );
}

export default Navbar;