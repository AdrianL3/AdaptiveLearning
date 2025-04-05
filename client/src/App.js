import { Routes, Route } from 'react-router-dom'
import './App.css';
import Layout from './components/Layout';
import Public from './components/Public';
import Login from './features/auth/Login';
import DashLayout from './components/DashLayout';
import Welcome from './features/auth/Welcome';
import Questions from './features/questions/QuestionsList';
import Statistics from './features/statistics/StatisticsList';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Public />} />
        <Route path="login" element={<Login />} />

        <Route path="dash" element={<DashLayout />}>
          <Route index element={<Welcome />} />
          <Route path="questions" element={<Questions />} />
          <Route path="statistics" element={<Statistics />} />
        </Route>
      </Route>
    </Routes>
  );
}

export default App;
