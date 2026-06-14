import { create } from 'zustand'
import { authApi } from '../services/api'

interface AuthState {
  isAuthenticated: boolean
  roles: string[]
  loading: boolean
  setAuth: (isAuthenticated: boolean, roles: string[]) => void
  logout: () => void
  initAuth: () => Promise<void>
}

export const useAuthStore = create<AuthState>(() => ({
  isAuthenticated: false,
  roles: [],
  loading: true,
  setAuth: (isAuthenticated, roles) => {
    useAuthStore.setState({ isAuthenticated, roles, loading: false })
  },
  logout: () => {
    useAuthStore.setState({ isAuthenticated: false, roles: [] })
  },
  initAuth: async () => {
    const ADMIN_ROLES = ['ADMIN', 'STOCK', 'PEDIDOS']
    try {
      const user = await authApi.me()
      const roles = user.roles.map(r => r.nombre)
      const hasAdminAccess = roles.some(r => ADMIN_ROLES.includes(r))
      if (hasAdminAccess) {
        useAuthStore.setState({ isAuthenticated: true, roles, loading: false })
      } else {
        await authApi.logout()
        useAuthStore.setState({ isAuthenticated: false, roles: [], loading: false })
      }
    } catch {
      useAuthStore.setState({ isAuthenticated: false, roles: [], loading: false })
    }
  },
}))
