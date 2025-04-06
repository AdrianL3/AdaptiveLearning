import { Navigate, useLocation } from 'react-router-dom';

const RequireAuth = ({ children }) => {
    const token = localStorage.getItem('token');
    const location = useLocation();

    console.log('RequireAuth check:', {
        hasToken: !!token,
        currentPath: location.pathname,
        from: location.state?.from
    });

    if (!token) {
        console.log('No token found, redirecting to login');
        return <Navigate to="/login" state={{ from: location }} replace />;
    }

    console.log('Token found, rendering protected content');
    return children;
};

export default RequireAuth; 