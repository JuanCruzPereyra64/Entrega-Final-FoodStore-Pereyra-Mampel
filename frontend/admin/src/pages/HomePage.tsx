import { motion } from 'framer-motion'
import { 
  Package, 
  UtensilsCrossed, 
  LayoutDashboard, 
  TrendingUp, 
  Plus,
  ArrowRight,
  ChefHat
} from 'lucide-react'
import { Link } from 'react-router-dom'
import { useProductos } from '../hooks/useProductos'
import { useCategorias } from '../hooks/useCategorias'
import { useIngredientes } from '../hooks/useIngredientes'
import { Card } from '../components/common/Card'
import { Button } from '../components/common/Button'

export function HomePage() {
  const { data: productos } = useProductos()
  const { data: categorias } = useCategorias()
  const { data: ingredientes } = useIngredientes()

  const stats = [
    { label: 'Productos', value: productos?.length || 0, icon: UtensilsCrossed, color: 'text-primary', bg: 'bg-primary/10' },
    { label: 'Categorías', value: categorias?.length || 0, icon: LayoutDashboard, color: 'text-amber-500', bg: 'bg-amber-500/10' },
    { label: 'Ingredientes', value: ingredientes?.length || 0, icon: Package, color: 'text-emerald-500', bg: 'bg-emerald-500/10' },
  ]

  const masCaro = productos?.reduce((prev, current) => (prev.precio_base > current.precio_base) ? prev : current, productos[0])

  return (
    <div className="space-y-10">
      {/* Hero / Welcome Section */}
      <section className="relative overflow-hidden rounded-[2rem] bg-slate-900 px-8 py-12 text-white shadow-2xl">
        <div className="absolute top-0 right-0 -translate-y-1/2 translate-x-1/4 opacity-10">
          <ChefHat size={320} />
        </div>
        
        <div className="relative z-10 max-w-2xl">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
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
                ${masCaro.precio_base.toFixed(2)}
              </div>
              <p className="text-sm text-slate-400">Es el producto de mayor valor en tu carta actual.</p>
              <Link to={`/productos/${masCaro.id}`} className="pt-4">
                <Button variant="ghost" icon={ArrowRight}>Ver Detalles</Button>
              </Link>
            </div>
          ) : (
            <div className="p-12 text-center text-slate-400">
              No hay productos para destacar aún.
            </div>
          )}
        </Card>

        {/* Quick Actions / Shortcuts */}
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
