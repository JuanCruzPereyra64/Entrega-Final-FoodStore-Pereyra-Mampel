import { Navigate, useLocation, Outlet } from 'react-router-dom'
import { useAuthStore } from '../../store/useAuthStore'
import type { ReactNode } from 'react'

interface Props {
  children?: ReactNode
  allowedRoles: string[]
}

export const AuthGuard = ({ children, allowedRoles }: Props) => {
  const { isAuthenticated, roles } = useAuthStore()
  const location = useLocation()

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />
  }

  const hasPermission = roles.some((role) => allowedRoles.includes(role))

  if (!hasPermission) {
    return <Navigate to="/unauthorized" replace />
  }

  return children ? <>{children}</> : <Outlet />
}
