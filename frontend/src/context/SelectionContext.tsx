import { createContext, useContext, useState, ReactNode } from 'react'

export interface Selection {
  /** Scorecard key, e.g. "senior_qa" */
  scorecardKey: string
  company: string
  techContext: string
}

interface Ctx {
  selection: Selection | null
  setSelection: (s: Selection | null) => void
}

const STORAGE_KEY = 'pa.selection'
const Context = createContext<Ctx>({ selection: null, setSelection: () => {} })
export const useSelection = () => useContext(Context)

function load(): Selection | null {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY)
    return raw ? (JSON.parse(raw) as Selection) : null
  } catch {
    return null
  }
}

// The choice lives only in this browser tab (sessionStorage): no account, nothing stored server-side.
export function SelectionProvider({ children }: { children: ReactNode }) {
  const [selection, setState] = useState<Selection | null>(load)
  function setSelection(s: Selection | null) {
    setState(s)
    try {
      if (s) sessionStorage.setItem(STORAGE_KEY, JSON.stringify(s))
      else sessionStorage.removeItem(STORAGE_KEY)
    } catch { /* storage unavailable: keep in memory only */ }
  }
  return <Context.Provider value={{ selection, setSelection }}>{children}</Context.Provider>
}
