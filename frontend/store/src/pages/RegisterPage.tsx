import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { authApi } from '../services/api'
import { useAuthStore } from '../store/useAuthStore'
import { Button } from '../components/common/Button'

export function RegisterPage() {
  const [form, setForm] = useState({ nombre: '', apellido: '', email: '', password: '', celular: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const setAuth = useAuthStore(s => s.setAuth)
  const navigate = useNavigate()

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    setForm(prev => ({ ...prev, [e.target.name]: e.target.value }))
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await authApi.register({
        nombre: form.nombre,
        apellido: form.apellido,
        email: form.email,
        password: form.password,
        celular: form.celular || undefined,
      })
      const res = await authApi.login({ email: form.email, password: form.password })
      setAuth(true, res.rol)
      navigate('/')
    } catch (err: any) {
      setError(err.message || 'Error al registrarse')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-[80vh] flex items-center justify-center">
      <div className="w-full max-w-md bg-white dark:bg-slate-900 p-8 rounded-3xl shadow-xl border border-slate-100 dark:border-slate-800">
        <h1 className="text-3xl font-bold font-display text-center mb-2">Crear cuenta</h1>
        <p className="text-center text-slate-500 text-sm mb-8">Registrate para hacer tus pedidos</p>

        {error && <div className="bg-red-50 text-red-600 p-4 rounded-xl mb-6 text-sm">{error}</div>}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-semibold mb-2 ml-1">Nombre</label>
              <input
                name="nombre"
                type="text"
                required
                className="w-full bg-slate-50 dark:bg-slate-800 border-none rounded-2xl px-4 py-3 focus:ring-2 focus:ring-primary/20"
                value={form.nombre}
                onChange={handleChange}
              />
            </div>
            <div>
              <label className="block text-sm font-semibold mb-2 ml-1">Apellido</label>
              <input
                name="apellido"
                type="text"
                required
                className="w-full bg-slate-50 dark:bg-slate-800 border-none rounded-2xl px-4 py-3 focus:ring-2 focus:ring-primary/20"
                value={form.apellido}
                onChange={handleChange}
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-semibold mb-2 ml-1">Email</label>
            <input
              name="email"
              type="email"
              required
              className="w-full bg-slate-50 dark:bg-slate-800 border-none rounded-2xl px-4 py-3 focus:ring-2 focus:ring-primary/20"
              value={form.email}
              onChange={handleChange}
            />
          </div>

          <div>
            <label className="block text-sm font-semibold mb-2 ml-1">Contraseña</label>
            <input
              name="password"
              type="password"
              required
              minLength={6}
              className="w-full bg-slate-50 dark:bg-slate-800 border-none rounded-2xl px-4 py-3 focus:ring-2 focus:ring-primary/20"
              value={form.password}
              onChange={handleChange}
            />
          </div>

          <div>
            <label className="block text-sm font-semibold mb-2 ml-1">Celular (opcional)</label>
            <input
              name="celular"
              type="tel"
              className="w-full bg-slate-50 dark:bg-slate-800 border-none rounded-2xl px-4 py-3 focus:ring-2 focus:ring-primary/20"
              value={form.celular}
              onChange={handleChange}
            />
          </div>

          <Button type="submit" className="w-full py-4 mt-2" isLoading={loading}>
            Crear cuenta
          </Button>

          <div className="pt-4 flex justify-center border-t border-slate-100 dark:border-slate-800">
            <p className="text-sm text-slate-500">
              ¿Ya tenés cuenta?{' '}
              <Link to="/login" className="font-semibold text-primary hover:underline">
                Iniciá sesión
              </Link>
            </p>
          </div>
        </form>
      </div>
    </div>
  )
}
