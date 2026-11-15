import { apiFetch } from './client'
import type { AssessResult, AssessInput } from '../types'

// No account needed: the role/level key and optional context travel with the request.
export const assess = (input: AssessInput) =>
  apiFetch<AssessResult>('/api/assess', { method: 'POST', body: JSON.stringify(input) })
