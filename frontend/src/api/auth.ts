import { apiFetch } from './client'

interface TokenResponse { access_token: string }

export async function register(email: string, password: string): Promise<void> {
  const data = await apiFetch<TokenResponse>('/api/auth/register', {
    method: 'POST', body: JSON.stringify({ email, password }),
  })
  localStorage.setItem('token', data.access_token)
}

export async function login(email: string, password: string): Promise<void> {
  const data = await apiFetch<TokenResponse>('/api/auth/login', {
    method: 'POST', body: JSON.stringify({ email, password }),
  })
  localStorage.setItem('token', data.access_token)
}

export function logout(): void { localStorage.removeItem('token') }
export function isAuthenticated(): boolean { return !!localStorage.getItem('token') }
