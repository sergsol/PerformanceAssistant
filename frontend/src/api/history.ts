import { fetchWithRetry, ApiError } from './client'
import type { HistoryItem } from '../types'
export const getHistory = () => fetchWithRetry<HistoryItem[]>('/api/history')
