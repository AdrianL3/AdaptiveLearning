import { Link } from 'react-router-dom';
import logo from '../NavigationLogo.png'; // Ensure the path is correct

const DashHeader = () => {
    const content = (
        <header className="dash-header">
            <div className="dash-header__container">
                <Link to="/dash">
                    <a href="/dash"><img src={logo}></img></a>
                    <h1 className="dash-header__title">notes</h1>
                </Link>
                <nav className="dash-header__nav">
                    {/* add nav buttons later */}
                </nav>
            </div>
        </header>
    )

    return content
}
export default DashHeader