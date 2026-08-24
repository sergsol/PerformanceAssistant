import { useState, FormEvent } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { register, isAuthenticated } from '../api/auth'
import { ApiError } from '../api/client'

export default function Register() {
  const navigate = useNavigate()
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  if (isAuthenticated()) {
    navigate('/')
    return null
  }

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault()
    const fd = new FormData(e.currentTarget)
    setLoading(true); setError('')
    try {
      await register(fd.get('email') as string, fd.get('password') as string)
      navigate('/profile')
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Something went wrong')
    } finally { setLoading(false) }
  }

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center px-4">
      <div className="w-full max-w-sm">
        <p className="text-2xl font-semibold text-center mb-1">Performance Assistant</p>
        <p className="text-sm text-slate-500 text-center mb-6">AI-powered performance self-assessment</p>
        <h1 className="text-xl font-medium mb-4">Create account</h1>
        {error && <p className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-3 py-2 mb-3">{error}</p>}
        <form onSubmit={handleSubmit} className="space-y-3">
          <input name="email" type="email" placeholder="name@company.com" required
            className="w-full border border-slate-300 rounded-lg px-3 py-3 text-base bg-white" />
          <input name="password" type="password" placeholder="Password" required
            className="w-full border border-slate-300 rounded-lg px-3 py-3 text-base bg-white" />
          <button disabled={loading}
            className="w-full bg-slate-900 text-white rounded-lg px-4 py-3 text-base font-medium disabled:opacity-60">
            {loading ? 'Creating account…' : 'Register'}
          </button>
        </form>
        <p className="text-sm text-slate-600 mt-4 text-center">Have an account? <Link to="/login" className="underline">Log in</Link></p>
      </div>
    </div>
  )
}
