import { NavLink, useLocation, useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import {
  ChefHat,
  ShoppingCart,
  ListOrdered,
  LogOut,
  User,
  UserCircle
} from 'lucide-react'
import { useCartStore } from '../../store/useCartStore'
import { useAuthStore } from '../../store/useAuthStore'

interface LayoutProps {
  children: React.ReactNode
}

export function MainLayout({ children }: LayoutProps) {
  const location = useLocation()
  const navigate = useNavigate()
  const { items } = useCartStore()
  const { isAuthenticated, logout } = useAuthStore()
  
  const cartItemCount = items.reduce((acc, item) => acc + item.cantidad, 0)

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 dark:bg-slate-920">
      <header className="sticky top-0 z-50 bg-white/80 dark:bg-slate-900/80 backdrop-blur-md border-b border-slate-200 dark:border-slate-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-20">
            <NavLink to="/" className="flex items-center gap-3 group">
              <div className="w-12 h-12 bg-primary/10 dark:bg-primary/20 rounded-xl flex items-center justify-center text-primary group-hover:scale-105 transition-transform">
                <ChefHat size={28} strokeWidth={2.5} />
              </div>
              <div>
                <h1 className="text-2xl font-display font-bold text-slate-900 dark:text-white leading-tight">
                  UTN Gourmet
                </h1>
                <p className="text-xs text-slate-500 font-medium tracking-wide uppercase">
                  Tienda Online
                </p>
              </div>
            </NavLink>

            <div className="flex items-center gap-4">
              {isAuthenticated ? (
                <>
                  <NavLink
                    to="/mis-pedidos"
                    className={({ isActive }) => `
                      flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium transition-all duration-200
                      ${isActive
                        ? 'bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-white'
                        : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800/50'
                      }
                    `}
                  >
                    <ListOrdered size={20} />
                    <span className="hidden sm:inline">Mis Pedidos</span>
                  </NavLink>

                  <NavLink
                    to="/mi-perfil"
                    className={({ isActive }) => `
                      flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium transition-all duration-200
                      ${isActive
                        ? 'bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-white'
                        : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800/50'
                      }
                    `}
                  >
                    <UserCircle size={20} />
                    <span className="hidden sm:inline">Mi Perfil</span>
                  </NavLink>

                  <button
                    onClick={handleLogout}
                    className="flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium text-red-600 hover:bg-red-50 dark:hover:bg-red-500/10 transition-colors"
                  >
                    <LogOut size={20} />
                    <span className="hidden sm:inline">Salir</span>
                  </button>
                </>
              ) : (
                <NavLink
                  to="/login"
                  className="flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors"
                >
                  <User size={20} />
                  <span className="hidden sm:inline">Ingresar</span>
                </NavLink>
              )}

              <div className="w-px h-8 bg-slate-200 dark:bg-slate-800 mx-2" />

              <NavLink
                to="/carrito"
                className="relative flex items-center justify-center w-12 h-12 rounded-xl bg-primary text-white hover:bg-primary-dark transition-colors shadow-lg shadow-primary/30 hover:shadow-primary/50 hover:-translate-y-0.5 duration-200"
              >
                <ShoppingCart size={22} />
                {cartItemCount > 0 && (
                  <span className="absolute -top-2 -right-2 w-6 h-6 flex items-center justify-center bg-red-500 text-white text-xs font-bold rounded-full border-2 border-white dark:border-slate-900">
                    {cartItemCount}
                  </span>
                )}
              </NavLink>
            </div>
          </div>
        </div>
      </header>

      <main className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 lg:py-12">
        <AnimatePresence mode="wait">
          <motion.div
            key={location.pathname}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.2 }}
          >
            {children}
          </motion.div>
        </AnimatePresence>
      </main>
    </div>
  )
}
