import { create } from "zustand"
import { persist } from "zustand/middleware"

export interface User {
  id: string
  name: string
  email: string
  user_type: "admin" | "employer" | "job_seeker"
}

interface AuthState {
  isAuthenticated: boolean
  user: User | null
  token: string | null
  userType: string | null
  isLoading: boolean
  login: (user: User, token: string) => void
  logout: () => void
  initialize: () => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      isAuthenticated: false,
      user: null,
      token: null,
      userType: null,
      isLoading: true,
      login: (user, token) =>
        set({
          isAuthenticated: true,
          user,
          token,
          userType: user.user_type,
          isLoading: false,
        }),
      logout: () =>
        set({
          isAuthenticated: false,
          user: null,
          token: null,
          isLoading: false,
        }),
      initialize: () => {
        const token = localStorage.getItem('auth-storage')
        if (token) {
          try {
            const { state } = JSON.parse(token)
            if (state.token) {
              set({
                isAuthenticated: true,
                user: state.user,
                token: state.token,
                isLoading: false,
              })
            } else {
              set({ isLoading: false })
            }
          } catch (error) {
            set({ isLoading: false })
          }
        } else {
          set({ isLoading: false })
        }
      },
    }),
    {
      name: "auth-storage",
    }
  )
) 