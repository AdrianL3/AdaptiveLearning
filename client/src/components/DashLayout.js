import { Outlet } from 'react-router-dom';
import DashHeader from './DashHeader';
import DashFooter from './DashFooter';

const DashLayout = () => {
    return (
        <div className="dash-container">
            <DashHeader />
            <div className="dash">
                <Outlet />
            </div>
            <DashFooter />
        </div>
    )
}

export default DashLayout