import { API_URL } from '@/config'
import { useAuthStore } from '@/stores/authStore'

export async function fetchWithAuth(url: string, options: RequestInit = {}) {
  const token = useAuthStore.getState().token

  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...options.headers,
  }

  const response = await fetch(`${API_URL}${url}`, {
    ...options,
    headers,
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'API request failed')
  }

  return response.json()
} 