import { create } from 'zustand'

interface AuthState {
  isAuthenticated: boolean
  roles: string[]
  token: string | null
  setAuth: (isAuthenticated: boolean, roles: string[], token: string) => void
  logout: () => void
}

const stored = localStorage.getItem('store_auth')
const initial = stored ? JSON.parse(stored) : { isAuthenticated: false, roles: [], token: null }

export const useAuthStore = create<AuthState>(() => ({
  ...initial,
  setAuth: (isAuthenticated, roles, token) => {
    localStorage.setItem('store_auth', JSON.stringify({ isAuthenticated, roles, token }))
    useAuthStore.setState({ isAuthenticated, roles, token })
  },
  logout: () => {
    localStorage.removeItem('store_auth')
    useAuthStore.setState({ isAuthenticated: false, roles: [], token: null })
  },
}))
