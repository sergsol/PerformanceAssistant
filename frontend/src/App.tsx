import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Home from './pages/Home'
import Assess from './pages/Assess'
import { SelectionProvider } from './context/SelectionContext'

export default function App() {
  return (
    <SelectionProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/assess" element={<Assess />} />
          {/* Accounts were removed: send old /login, /register, /profile, /history links to the start. */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </SelectionProvider>
  )
}
