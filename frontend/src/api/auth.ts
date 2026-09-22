import { apiFetch } from './client'

interface TokenPair {
  access_token: string
  expires_in: number
  refresh_token: string
}

function getTokens(): { access: string | null; refresh: string | null } {
  return {
    access: localStorage.getItem('access_token'),
    refresh: localStorage.getItem('refresh_token'),
  }
}

function saveTokens(pair: TokenPair): void {
  localStorage.setItem('access_token', pair.access_token)
  localStorage.setItem('refresh_token', pair.refresh_token)
}

export async function register(email: string, password: string): Promise<void> {
  const pair = await apiFetch<TokenPair>('/api/auth/register', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  })
  saveTokens(pair)
}

export async function login(email: string, password: string): Promise<void> {
  const pair = await apiFetch<TokenPair>('/api/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  })
  saveTokens(pair)
}

export async function refreshAccessToken(): Promise<boolean> {
  const { refresh } = getTokens()
  if (!refresh) return false
  try {
    const pair = await apiFetch<TokenPair>('/api/auth/refresh', {
      method: 'POST',
      body: JSON.stringify({ refresh_token: refresh }),
    })
    saveTokens(pair)
    return true
  } catch {
    // Refresh failed — clear tokens and return false
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    return false
  }
}

export async function logout(): Promise<void> {
  const { refresh } = getTokens()
  if (refresh) {
    try {
      await fetch('/api/auth/revoke', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh_token: refresh }),
      })
    } catch {
      // Best-effort revoke; clear tokens anyway
    }
  }
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
}

export function isAuthenticated(): boolean {
  return !!localStorage.getItem('access_token')
}
