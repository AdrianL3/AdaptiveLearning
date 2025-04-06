import { Routes, Route } from 'react-router-dom'
import './App.css';
import Layout from './components/Layout';
import Public from './components/Public';
import Login from './features/auth/Login';
import SignUp from './features/auth/SignUp';
import DashLayout from './components/DashLayout';
import Welcome from './features/auth/Welcome';
import Questions from './features/questions/Questions';
import Statistics from './features/statistics/Statistics';
//import RequireAuth from './features/auth/RequireAuth';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Public />} />
        
        {/* Public routes */}
        <Route path="login" element={<Login />} />
        <Route path="signup" element={<SignUp />} />

        {/* Protected routes */}
        <Route path="dash" element={
          //<RequireAuth>
          <DashLayout />
          //</RequireAuth> 
        }>
          <Route index element={<Welcome />} />
          <Route path="questions" element={<Questions />} />
          <Route path="statistics" element={<Statistics />} />
        </Route>
      </Route>
    </Routes>
  );
}

export default App;
