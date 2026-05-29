import { useState } from 'react'
import { Card } from '../components/common/Card'
import { useMovimientosStock } from '../hooks/useStock'
import { useIngredientes } from '../hooks/useIngredientes'
import { Package, ArrowDownRight, ArrowUpRight, Filter } from 'lucide-react'

export function StockPage() {
  const [filtroIngrediente, setFiltroIngrediente] = useState<number | undefined>()
  const { data: movimientos, isLoading, isError } = useMovimientosStock(filtroIngrediente)
  const { data: ingredientes } = useIngredientes()

  if (isLoading) return (
    <div className="flex flex-col items-center justify-center min-h-[400px] gap-4">
      <div className="w-12 h-12 border-4 border-primary/20 border-t-primary rounded-full animate-spin" />
      <p className="text-slate-500 font-medium italic">Revisando los libros de stock...</p>
    </div>
  )

  if (isError) return (
    <Card className="border-red-100 bg-red-50 dark:bg-red-900/10">
      <p className="text-red-600 dark:text-red-400 font-medium">Error al cargar el historial de stock.</p>
    </Card>
  )

  return (
    <div className="space-y-8">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-display font-bold text-slate-900 dark:text-white">Movimientos de Stock</h1>
          <p className="text-slate-500 dark:text-slate-400 mt-1">
            Auditoria completa de ingresos y egresos de ingredientes.
          </p>
        </div>
      </div>

      <div className="flex flex-col md:flex-row gap-4">
        <div className="relative min-w-[250px]">
          <label className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none">
            <Filter size={18} />
          </label>
          <select
            value={filtroIngrediente ?? ''}
            onChange={(e) => setFiltroIngrediente(e.target.value ? Number(e.target.value) : undefined)}
            className="w-full pl-11 pr-10 py-3 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl text-sm appearance-none focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all shadow-sm"
          >
            <option value="">Todos los ingredientes</option>
            {ingredientes?.map((ing) => (
              <option key={ing.id} value={ing.id}>{ing.nombre}</option>
            ))}
          </select>
        </div>
      </div>

      <Card noPadding className="overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead>
              <tr>
                <th className="premium-table-header w-32">Fecha y Hora</th>
                <th className="premium-table-header">Ingrediente</th>
                <th className="premium-table-header text-center">Tipo</th>
                <th className="premium-table-header text-right">Cantidad</th>
                <th className="premium-table-header">Motivo</th>
                <th className="premium-table-header">Usuario</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
              {movimientos?.map((mov) => (
                <tr key={mov.id} className="premium-table-row">
                  <td className="px-6 py-4">
                    <span className="text-xs font-medium text-slate-500">
                      {new Date(mov.created_at).toLocaleString('es-AR', { dateStyle: 'short', timeStyle: 'short' })}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <span className="font-semibold text-slate-900 dark:text-slate-200">{mov.ingrediente_nombre}</span>
                  </td>
                  <td className="px-6 py-4 text-center">
                    {mov.tipo === 'INGRESO' ? (
                      <span className="inline-flex items-center gap-1 bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400 text-[10px] uppercase font-bold tracking-widest px-2 py-1 rounded-full border border-green-200 dark:border-green-800">
                        <ArrowUpRight size={12} />
                        Ingreso
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1 bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400 text-[10px] uppercase font-bold tracking-widest px-2 py-1 rounded-full border border-red-200 dark:border-red-800">
                        <ArrowDownRight size={12} />
                        Egreso
                      </span>
                    )}
                  </td>
                  <td className="px-6 py-4 text-right">
                    <span className={`font-mono font-bold ${mov.tipo === 'INGRESO' ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'}`}>
                      {mov.tipo === 'INGRESO' ? '+' : '-'}{mov.cantidad}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <span className="text-slate-600 dark:text-slate-400">{mov.motivo}</span>
                  </td>
                  <td className="px-6 py-4">
                    <span className="text-slate-500 text-xs">{mov.usuario_nombre || 'Sistema'}</span>
                  </td>
                </tr>
              ))}
              {movimientos?.length === 0 && (
                <tr>
                  <td colSpan={6} className="px-6 py-20 text-center">
                    <div className="flex flex-col items-center gap-3">
                      <Package size={48} className="text-slate-200 dark:text-slate-700" />
                      <p className="text-slate-500 dark:text-slate-400 font-medium">No hay movimientos registrados.</p>
                    </div>
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  )
}
