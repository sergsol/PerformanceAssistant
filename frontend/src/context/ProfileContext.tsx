import { createContext, useContext, useState, ReactNode } from 'react'

interface ProfileCtx {
  profileComplete: boolean
  markProfileComplete: () => void
}

const Ctx = createContext<ProfileCtx>({ profileComplete: false, markProfileComplete: () => {} })
export const useProfileCtx = () => useContext(Ctx)

export function ProfileProvider({ children, initialComplete }: { children: ReactNode; initialComplete: boolean }) {
  const [profileComplete, setProfileComplete] = useState(initialComplete)
  return (
    <Ctx.Provider value={{ profileComplete, markProfileComplete: () => setProfileComplete(true) }}>
      {children}
    </Ctx.Provider>
  )
}
