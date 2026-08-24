import { apiFetch } from './client'
import type { HistoryItem } from '../types'
export const getHistory = () => apiFetch<HistoryItem[]>('/api/history')
