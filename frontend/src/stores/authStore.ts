import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { API_URL } from '@/config'

interface User {
  id: string
  email: string
  first_name: string
  last_name: string
  display_name: string | null
  user_type: 'job_seeker' | 'employer' | 'admin'
  is_active: boolean
  created_at: string
  updated_at: string
}

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
  rememberMe: boolean
  login: (email: string, password: string, remember?: boolean) => Promise<'admin' | 'employer' | 'job_seeker' | string>
  register: (data: RegisterData) => Promise<void>
  logout: () => void
  setUser: (user: User | null) => void
  setToken: (token: string | null) => void
  setError: (error: string | null) => void
  forgotPassword: (email: string) => Promise<void>
  resetPassword: (token: string, newPassword: string) => Promise<void>
}

interface RegisterData {
  email: string
  password: string
  first_name: string
  last_name: string
  display_name?: string
  user_type: 'job_seeker' | 'employer'
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,
      rememberMe: false,

      setUser: (user) => {
        set({ user, isAuthenticated: !!user })
      },

      setToken: (token) => {
        set({ token })
      },

      setError: (error) => {
        set({ error })
      },

      login: async (email: string, password: string, remember = false): Promise<'admin' | 'employer' | 'job_seeker' | string> => {
        try {
          set({ isLoading: true, error: null })
          
          const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
              username: email,
              password: password,
            }),
          })

          if (!response.ok) {
            const error = await response.json()
            throw new Error(error.detail || 'Login failed')
          }

          const data = await response.json()
          const user = data.user
          set({
            token: data.access_token,
            user: user,
            isAuthenticated: true,
            error: null,
            rememberMe: remember,
          })

          // Check both is_superuser and user_type for admin
          if (user.is_superuser && user.user_type === 'admin') {
            return 'admin'
          }

          return user.user_type
        } catch (error) {
          set({ error: error instanceof Error ? error.message : 'Login failed' })
          throw error
        } finally {
          set({ isLoading: false })
        }
      },

      register: async (data: RegisterData) => {
        try {
          set({ isLoading: true, error: null })
          
          const response = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
          })

          if (!response.ok) {
            const error = await response.json()
            throw new Error(error.detail || 'Registration failed')
          }

          const responseData = await response.json()
          set({
            token: responseData.access_token,
            user: responseData.user,
            isAuthenticated: true,
            error: null,
          })
        } catch (error) {
          set({ error: error instanceof Error ? error.message : 'Registration failed' })
        } finally {
          set({ isLoading: false })
        }
      },

      forgotPassword: async (email: string) => {
        try {
          set({ isLoading: true, error: null })
          
          const response = await fetch(`${API_URL}/auth/forgot-password`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email }),
          })

          if (!response.ok) {
            const error = await response.json()
            throw new Error(error.detail || 'Failed to send reset email')
          }
        } catch (error) {
          set({ error: error instanceof Error ? error.message : 'Failed to send reset email' })
          throw error
        } finally {
          set({ isLoading: false })
        }
      },

      resetPassword: async (token: string, newPassword: string) => {
        try {
          set({ isLoading: true, error: null })
          
          const response = await fetch(`${API_URL}/auth/reset-password`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ token, new_password: newPassword }),
          })

          if (!response.ok) {
            const error = await response.json()
            throw new Error(error.detail || 'Failed to reset password')
          }
        } catch (error) {
          set({ error: error instanceof Error ? error.message : 'Failed to reset password' })
          throw error
        } finally {
          set({ isLoading: false })
        }
      },

      logout: () => {
        set({
          user: null,
          token: null,
          isAuthenticated: false,
          error: null,
          rememberMe: false,
        })
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        token: state.token,
        user: state.user,
        isAuthenticated: state.isAuthenticated,
        rememberMe: state.rememberMe,
      }),
    }
  )
)

export default useAuthStore 