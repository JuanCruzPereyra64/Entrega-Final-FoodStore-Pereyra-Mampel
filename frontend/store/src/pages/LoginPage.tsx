import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { authApi } from '../services/api'
import { useAuthStore } from '../store/useAuthStore'
import { Button } from '../components/common/Button'

export function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const setAuth = useAuthStore(s => s.setAuth)
  const navigate = useNavigate()

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const res = await authApi.login({ email, password })
      setAuth(true, res.rol, res.access_token)
      navigate('/')
    } catch (err: any) {
      setError(err.message || 'Error al iniciar sesión')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-[80vh] flex items-center justify-center">
      <div className="w-full max-w-md bg-white dark:bg-slate-900 p-8 rounded-3xl shadow-xl border border-slate-100 dark:border-slate-800">
        <h1 className="text-3xl font-bold font-display text-center mb-8">Food Store</h1>
        {error && <div className="bg-red-50 text-red-600 p-4 rounded-xl mb-6 text-sm">{error}</div>}
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-semibold mb-2 ml-1">Email</label>
            <input
              type="email"
              required
              className="w-full bg-slate-50 dark:bg-slate-800 border-none rounded-2xl px-4 py-3 focus:ring-2 focus:ring-primary/20"
              value={email}
              onChange={e => setEmail(e.target.value)}
            />
          </div>
          <div>
            <label className="block text-sm font-semibold mb-2 ml-1">Contraseña</label>
            <input
              type="password"
              required
              className="w-full bg-slate-50 dark:bg-slate-800 border-none rounded-2xl px-4 py-3 focus:ring-2 focus:ring-primary/20"
              value={password}
              onChange={e => setPassword(e.target.value)}
            />
          </div>
          <Button type="submit" className="w-full py-4" isLoading={loading}>
            Ingresar
          </Button>
          <div className="pt-4 flex flex-col items-center gap-3 border-t border-slate-100 dark:border-slate-800">
            <button
              type="button"
              onClick={() => { setEmail('test@test.com'); setPassword('Test12345!'); }}
              className="text-xs font-semibold text-slate-400 hover:text-primary transition-colors"
            >
              Autocompletar Cliente (Demo)
            </button>
            <p className="text-sm text-slate-500">
              ¿No tenés cuenta?{' '}
              <Link to="/register" className="font-semibold text-primary hover:underline">
                Registrate
              </Link>
            </p>
          </div>
        </form>
      </div>
    </div>
  )
}
