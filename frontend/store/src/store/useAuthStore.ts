import { create } from 'zustand'

interface AuthState {
  isAuthenticated: boolean
  roles: string[]
  setAuth: (isAuthenticated: boolean, roles: string[]) => void
  logout: () => void
}

export const useAuthStore = create<AuthState>((set) => {
  const storedAuth = localStorage.getItem('auth')
  const initial = storedAuth ? JSON.parse(storedAuth) : { isAuthenticated: false, roles: [] }

  return {
    ...initial,
    setAuth: (isAuthenticated, roles) => {
      localStorage.setItem('auth', JSON.stringify({ isAuthenticated, roles }))
      set({ isAuthenticated, roles })
    },
    logout: () => {
      localStorage.removeItem('auth')
      set({ isAuthenticated: false, roles: [] })
    }
  }
})
