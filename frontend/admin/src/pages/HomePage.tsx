import { useQuery } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import {
  Package,
  UtensilsCrossed,
  LayoutDashboard,
  TrendingUp,
  Plus,
  ArrowRight,
  ChefHat,
  DollarSign,
  ShoppingCart,
  Clock,
  Wallet
} from 'lucide-react'
import { Link } from 'react-router-dom'
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts'
import { useProductos } from '../hooks/useProductos'
import { useCategorias } from '../hooks/useCategorias'
import { useIngredientes } from '../hooks/useIngredientes'
import { estadisticasApi } from '../services/api'
import { Card } from '../components/common/Card'
import { Button } from '../components/common/Button'
import { formatCurrency } from '../utils/format'

const PIE_COLORS = ['#f59e0b', '#3b82f6', '#f97316', '#10b981', '#ef4444']
const ESTADO_LABELS: Record<string, string> = {
  PENDIENTE: 'Pendiente', CONFIRMADO: 'Confirmado', EN_PREP: 'En Preparación',
  ENTREGADO: 'Entregado', CANCELADO: 'Cancelado',
}

function getMesActual() {
  const d = new Date()
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-01`
}

function getSemanaRange() {
  const hoy = new Date()
  const inicio = new Date(hoy)
  inicio.setDate(inicio.getDate() - 7)
  return { desde: inicio.toISOString().split('T')[0], hasta: hoy.toISOString().split('T')[0] }
}

export function HomePage() {
  const { data: productos } = useProductos()
  const { data: categorias } = useCategorias()
  const { data: ingredientes } = useIngredientes()

  const { data: resumen } = useQuery({
    queryKey: ['estadisticas', 'resumen'],
    queryFn: estadisticasApi.resumen,
  })

  const { desde, hasta } = getSemanaRange()
  const { data: ventas } = useQuery({
    queryKey: ['estadisticas', 'ventas', desde, hasta],
    queryFn: () => estadisticasApi.ventas(desde, hasta),
  })

  const { data: productosTop } = useQuery({
    queryKey: ['estadisticas', 'productos-top'],
    queryFn: () => estadisticasApi.productosTop(5),
  })

  const { data: pedidosPorEstado } = useQuery({
    queryKey: ['estadisticas', 'pedidos-por-estado'],
    queryFn: estadisticasApi.pedidosPorEstado,
  })

  const { data: ingresosFP } = useQuery({
    queryKey: ['estadisticas', 'ingresos'],
    queryFn: () => estadisticasApi.ingresos(getMesActual()),
  })

  const masCaro = productos?.reduce((prev, current) => (prev.precio_base > current.precio_base) ? prev : current, productos[0])

  const kpis = [
    { label: 'Ventas Hoy', value: formatCurrency(Number(resumen?.ventas_hoy) || 0), icon: DollarSign, color: 'text-emerald-500', bg: 'bg-emerald-500/10' },
    { label: 'Ticket Promedio', value: formatCurrency(Number(resumen?.ticket_promedio) || 0), icon: Wallet, color: 'text-indigo-500', bg: 'bg-indigo-500/10' },
    { label: 'Pedidos Activos', value: resumen?.pedidos_activos ?? 0, icon: ShoppingCart, color: 'text-amber-500', bg: 'bg-amber-500/10' },
    { label: 'Total del Mes', value: formatCurrency(Number(resumen?.total_mes_actual) || 0), icon: TrendingUp, color: 'text-primary', bg: 'bg-primary/10' },
  ]

  const stats = [
    { label: 'Productos', value: productos?.length || 0, icon: UtensilsCrossed, color: 'text-primary', bg: 'bg-primary/10' },
    { label: 'Categorías', value: categorias?.length || 0, icon: LayoutDashboard, color: 'text-amber-500', bg: 'bg-amber-500/10' },
    { label: 'Ingredientes', value: ingredientes?.length || 0, icon: Package, color: 'text-emerald-500', bg: 'bg-emerald-500/10' },
  ]

  return (
    <div className="space-y-10">
      {/* Hero */}
      <section className="relative overflow-hidden rounded-[2rem] bg-slate-900 px-8 py-12 text-white shadow-2xl">
        <div className="absolute top-0 right-0 -translate-y-1/2 translate-x-1/4 opacity-10">
          <ChefHat size={320} />
        </div>
        <div className="relative z-10 max-w-2xl">
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
            <span className="inline-block px-4 py-1.5 rounded-full bg-primary/20 text-primary text-xs font-bold uppercase tracking-widest mb-4">
              Panel de Control
            </span>
            <h1 className="text-4xl md:text-5xl font-display font-bold leading-tight mb-4">
              Bienvenido, <span className="text-primary">Admin Gourmet</span>.
            </h1>
            <p className="text-slate-400 text-lg mb-8 leading-relaxed">
              Hoy es un gran día para innovar en la cocina. Mirá cómo van tus números y empezá a crear nuevas experiencias gastronómicas.
            </p>
            <div className="flex flex-wrap gap-4">
              <Link to="/productos">
                <Button size="lg" icon={Plus}>Nuevo Producto</Button>
              </Link>
              <Link to="/ingredientes">
                <Button variant="secondary" size="lg" className="bg-white/10 border-white/20 text-white hover:bg-white/20">
                  Ver Despensa
                </Button>
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* KPI Cards */}
      <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {kpis.map((kpi, index) => (
          <Card key={kpi.label} className="group">
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: index * 0.05 }}
              className="flex items-center gap-4"
            >
              <div className={`w-12 h-12 rounded-2xl ${kpi.bg} ${kpi.color} flex items-center justify-center transition-transform group-hover:scale-110`}>
                <kpi.icon size={24} />
              </div>
              <div className="min-w-0">
                <p className="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wider truncate">{kpi.label}</p>
                <p className="text-xl font-display font-bold text-slate-900 dark:text-white">{kpi.value}</p>
              </div>
            </motion.div>
          </Card>
        ))}
      </section>

      {/* Charts Row 1: Ventas LineChart + Productos Top BarChart */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <h3 className="text-lg font-bold font-display text-slate-900 dark:text-white mb-4">Ventas (últimos 7 días)</h3>
          <ResponsiveContainer width="100%" height={260}>
            <LineChart data={ventas}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey="periodo" tick={{ fontSize: 11 }} stroke="#94a3b8" />
              <YAxis tick={{ fontSize: 11 }} stroke="#94a3b8" />
              <Tooltip formatter={(v: number) => formatCurrency(v)} />
              <Line type="monotone" dataKey="total_ventas" stroke="#6366f1" strokeWidth={2} dot={{ r: 3 }} />
            </LineChart>
          </ResponsiveContainer>
        </Card>

        <Card>
          <h3 className="text-lg font-bold font-display text-slate-900 dark:text-white mb-4">Top 5 Productos</h3>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={productosTop} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis type="number" tick={{ fontSize: 11 }} stroke="#94a3b8" />
              <YAxis dataKey="nombre" type="category" width={100} tick={{ fontSize: 11 }} stroke="#94a3b8" />
              <Tooltip formatter={(v: number) => `${v} vendidos`} />
              <Bar dataKey="cantidad_vendida" fill="#f97316" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>
      </div>

      {/* Charts Row 2: PieChart estados + Ingresos BarChart */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <h3 className="text-lg font-bold font-display text-slate-900 dark:text-white mb-4">Pedidos por Estado</h3>
          <ResponsiveContainer width="100%" height={260}>
            <PieChart>
              <Pie
                data={pedidosPorEstado?.map(p => ({ ...p, name: ESTADO_LABELS[p.estado_codigo] || p.estado_codigo }))}
                dataKey="cantidad"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={90}
                label={({ name, cantidad }: { name: string; cantidad: number }) => `${name}: ${cantidad}`}
              >
                {pedidosPorEstado?.map((_, i) => (
                  <Cell key={i} fill={PIE_COLORS[i % PIE_COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </Card>

        <Card>
          <h3 className="text-lg font-bold font-display text-slate-900 dark:text-white mb-4">Ingresos por Forma de Pago (Mes)</h3>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={ingresosFP} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis type="number" tick={{ fontSize: 11 }} stroke="#94a3b8" />
              <YAxis dataKey="forma_pago_codigo" type="category" width={120} tick={{ fontSize: 11 }} stroke="#94a3b8" />
              <Tooltip formatter={(v: number) => formatCurrency(v)} />
              <Bar dataKey="total" fill="#10b981" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>
      </div>

      {/* Stats Grid */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {stats.map((stat, index) => (
          <Card key={stat.label} className="group">
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: index * 0.1 }}
              className="flex items-center gap-5"
            >
              <div className={`w-14 h-14 rounded-2xl ${stat.bg} ${stat.color} flex items-center justify-center transition-transform group-hover:scale-110`}>
                <stat.icon size={28} />
              </div>
              <div>
                <p className="text-sm font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wider">{stat.label}</p>
                <p className="text-3xl font-display font-bold text-slate-900 dark:text-white">{stat.value}</p>
              </div>
            </motion.div>
          </Card>
        ))}
      </section>

      {/* Highlights & Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <Card noPadding className="overflow-hidden h-full">
          <div className="p-6 border-b border-slate-100 dark:border-slate-800">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-display font-bold text-slate-900 dark:text-white flex items-center gap-2">
                <TrendingUp size={20} className="text-primary" />
                Producto Destacado
              </h2>
            </div>
          </div>
          {masCaro ? (
            <div className="p-8 flex flex-col items-center text-center space-y-4">
              <div className="w-20 h-20 bg-amber-100 dark:bg-amber-900/30 text-amber-600 rounded-3xl flex items-center justify-center shadow-inner">
                <UtensilsCrossed size={40} />
              </div>
              <div>
                <h3 className="text-2xl font-bold text-slate-900 dark:text-white">{masCaro.nombre}</h3>
                <p className="text-slate-500 dark:text-slate-400 mt-1">{masCaro.categorias?.[0]?.nombre || 'General'}</p>
              </div>
              <div className="px-6 py-2 rounded-2xl bg-slate-50 dark:bg-slate-902 text-accent font-display font-bold text-2xl">
                {formatCurrency(Number(masCaro.precio_base) || 0)}
              </div>
              <p className="text-sm text-slate-400">Es el producto de mayor valor en tu carta actual.</p>
              <Link to={`/productos/${masCaro.id}`} className="pt-4">
                <Button variant="ghost" icon={ArrowRight}>Ver Detalles</Button>
              </Link>
            </div>
          ) : (
            <div className="p-12 text-center text-slate-400">No hay productos para destacar aún.</div>
          )}
        </Card>

        <section className="space-y-6">
          <h2 className="text-xl font-display font-bold text-slate-900 dark:text-white px-2">Acciones Rápidas</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <Link to="/categorias">
              <Card className="hover:border-primary/50 transition-colors h-full flex items-center gap-4 group">
                <div className="p-3 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 group-hover:bg-primary/10 group-hover:text-primary transition-colors">
                  <LayoutDashboard size={20} />
                </div>
                <span className="font-semibold text-slate-700 dark:text-slate-200">Gestionar Categorías</span>
              </Card>
            </Link>
            <Link to="/ingredientes">
              <Card className="hover:border-amber-500/50 transition-colors h-full flex items-center gap-4 group">
                <div className="p-3 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 group-hover:bg-amber-500/10 group-hover:text-amber-500 transition-colors">
                  <Package size={20} />
                </div>
                <span className="font-semibold text-slate-700 dark:text-slate-200">Control de Insumos</span>
              </Card>
            </Link>
          </div>

          <Card className="bg-primary/5 border-primary/10 p-8 flex flex-col items-center text-center space-y-4">
            <ChefHat size={48} className="text-primary" />
            <h3 className="text-lg font-bold text-slate-900 dark:text-white">¿Todo listo para el servicio?</h3>
            <p className="text-sm text-slate-600 dark:text-slate-400">Recordá revisar que todos los ingredientes estén actualizados antes de abrir el salón.</p>
          </Card>
        </section>
      </div>
    </div>
  )
}
