import { useState, useEffect } from 'react'
import { Navigate, Outlet, useLocation } from 'react-router-dom'
import { isAuthenticated } from '../api/auth'
import { getProfile } from '../api/profile'
import { ProfileProvider } from '../context/ProfileContext'

export default function ProtectedRoute() {
  const location = useLocation()
  const [checked, setChecked] = useState(false)
  const [profileComplete, setProfileComplete] = useState(false)

  useEffect(() => {
    if (!isAuthenticated()) { setChecked(true); return }
    getProfile()
      .then(p => { setProfileComplete(!!p.display_name); setChecked(true) })
      .catch(() => { setChecked(true) })
  }, [])

  if (!isAuthenticated()) return <Navigate to="/login" replace />
  if (!checked) return null

  if (!profileComplete && location.pathname !== '/profile') {
    return <Navigate to="/profile" replace />
  }

  return (
    <ProfileProvider initialComplete={profileComplete}>
      <Outlet />
    </ProfileProvider>
  )
}
