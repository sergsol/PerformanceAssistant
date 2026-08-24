import { useState, useEffect } from 'react'
import { Navigate, Outlet, useLocation } from 'react-router-dom'
import { isAuthenticated } from '../api/auth'
import { getProfile } from '../api/profile'
import { ProfileProvider, useProfileCtx } from '../context/ProfileContext'

function ProfileGuard() {
  const { profileComplete } = useProfileCtx()
  const { pathname } = useLocation()
  if (!profileComplete && pathname !== '/profile') {
    return <Navigate to="/profile" replace />
  }
  return <Outlet />
}

export default function ProtectedRoute() {
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

  return (
    <ProfileProvider initialComplete={profileComplete}>
      <ProfileGuard />
    </ProfileProvider>
  )
}
