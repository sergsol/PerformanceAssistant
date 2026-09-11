import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Profile from './pages/Profile'
import Assess from './pages/Assess'
import History from './pages/History'
import ProtectedRoute from './components/ProtectedRoute'
import { ProfileProvider } from './context/ProfileContext'

export default function App() {
  return (
    <ProfileProvider initialComplete={false}>
      <BrowserRouter>
        <Routes>
          <Route element={<ProtectedRoute />}>
            <Route path="/" element={<Assess />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/history" element={<History />} />
          </Route>
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </ProfileProvider>
  )
}
