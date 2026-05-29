import { useState, useMemo } from 'react'
import { useQuery } from '@tanstack/react-query'
import { pedidosApi } from '../services/api'
import { Card } from '../components/common/Card'
import { TrendingUp, DollarSign, Clock, LayoutDashboard, Filter } from 'lucide-react'
import { formatCurrency } from '../utils/format'

export function VentasPage() {
  const { data: pedidos, isLoading, isError } = useQuery({
    queryKey: ['pedidos'],
    queryFn: pedidosApi.getAll
  })

  const [filtroEstado, setFiltroEstado] = useState<string>('')

  // Cálculos de métricas
  const metricas = useMemo(() => {
    if (!pedidos) return { ingresosLiquidos: 0, aLiquidar: 0, cantidadVentas: 0, ticketPromedio: 0 }

    let liquidos = 0
    let aLiquidar = 0
    let cantEntregados = 0

    pedidos.forEach(p => {
      const totalNum = Number(p.total) || 0
      if (p.estado_codigo === 'ENTREGADO') {
        liquidos += totalNum
        cantEntregados++
      } else if (['EN_CAMINO', 'EN_PREP', 'CONFIRMADO'].includes(p.estado_codigo)) {
        aLiquidar += totalNum
      }
    })

    const ticketPromedio = cantEntregados > 0 ? liquidos / cantEntregados : 0

    return { ingresosLiquidos: liquidos, aLiquidar, cantidadVentas: cantEntregados, ticketPromedio }
  }, [pedidos])

  const listaFiltrada = useMemo(() => {
    if (!pedidos) return []
    // Por defecto mostramos todo lo que no sea CANCELADO ni PENDIENTE, a menos que se filtre
    let list = pedidos
    if (filtroEstado === 'A_LIQUIDAR') {
      list = pedidos.filter(p => ['EN_CAMINO', 'EN_PREP', 'CONFIRMADO'].includes(p.estado_codigo))
    } else if (filtroEstado) {
      list = pedidos.filter(p => p.estado_codigo === filtroEstado)
    } else {
      list = pedidos.filter(p => ['ENTREGADO', 'EN_CAMINO', 'EN_PREP', 'CONFIRMADO'].includes(p.estado_codigo))
    }
    // Ordenar por fecha descendente
    return list.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
  }, [pedidos, filtroEstado])

  const estadoBadge: Record<string, { label: string; className: string }> = {
    PENDIENTE:  { label: 'Pendiente',       className: 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400' },
    CONFIRMADO: { label: 'Confirmado',      className: 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400' },
    EN_PREP:    { label: 'En Preparación',  className: 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400' },
    EN_CAMINO:  { label: 'En Camino',       className: 'bg-indigo-100 text-indigo-700 dark:bg-indigo-900/30 dark:text-indigo-400' },
    ENTREGADO:  { label: 'Entregado',       className: 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400' },
    CANCELADO:  { label: 'Cancelado',       className: 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400' },
  }

  if (isLoading) return (
    <div className="flex flex-col items-center justify-center min-h-[400px] gap-4">
      <div className="w-12 h-12 border-4 border-primary/20 border-t-primary rounded-full animate-spin" />
      <p className="text-slate-500 font-medium italic">Calculando ingresos...</p>
    </div>
  )

  if (isError) return (
    <Card className="border-red-100 bg-red-50 dark:bg-red-900/10">
      <p className="text-red-600 dark:text-red-400 font-medium">Error al cargar las métricas de ventas.</p>
    </Card>
  )

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-display font-bold text-slate-900 dark:text-white">Ingresos y Ventas</h1>
        <p className="text-slate-500 dark:text-slate-400 mt-1">
          Monitor de finanzas y ventas en tiempo real.
        </p>
      </div>

      {/* Tarjetas de Métricas */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="bg-gradient-to-br from-emerald-500 to-emerald-700 text-white border-0">
          <div className="flex items-start justify-between">
            <div>
              <p className="text-emerald-100 font-medium text-sm">Ingresos Líquidos (Cobrado)</p>
              <h3 className="text-3xl font-bold mt-2 font-display">{formatCurrency(metricas.ingresosLiquidos)}</h3>
            </div>
            <div className="p-3 bg-white/20 rounded-xl backdrop-blur-sm">
              <DollarSign size={24} className="text-white" />
            </div>
          </div>
        </Card>

        <Card className="bg-gradient-to-br from-indigo-500 to-indigo-700 text-white border-0">
          <div className="flex items-start justify-between">
            <div>
              <p className="text-indigo-100 font-medium text-sm">A Liquidar (En Tránsito/Prep)</p>
              <h3 className="text-3xl font-bold mt-2 font-display">{formatCurrency(metricas.aLiquidar)}</h3>
            </div>
            <div className="p-3 bg-white/20 rounded-xl backdrop-blur-sm">
              <Clock size={24} className="text-white" />
            </div>
          </div>
        </Card>

        <Card className="bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800">
          <div className="flex items-start justify-between">
            <div>
              <p className="text-slate-500 dark:text-slate-400 font-medium text-sm">Ticket Promedio</p>
              <h3 className="text-3xl font-bold mt-2 text-slate-900 dark:text-white font-display">{formatCurrency(metricas.ticketPromedio)}</h3>
              <p className="text-xs text-slate-400 mt-1">En base a {metricas.cantidadVentas} ventas cobradas.</p>
            </div>
            <div className="p-3 bg-primary/10 rounded-xl">
              <TrendingUp size={24} className="text-primary" />
            </div>
          </div>
        </Card>
      </div>

      <div className="flex items-center gap-4">
        <div className="relative min-w-[200px]">
          <label className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none">
            <Filter size={18} />
          </label>
          <select
            value={filtroEstado}
            onChange={(e) => setFiltroEstado(e.target.value)}
            className="w-full pl-11 pr-10 py-2.5 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl text-sm appearance-none focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all shadow-sm"
          >
            <option value="">Ingresos (Entregados y en Tránsito)</option>
            <option value="ENTREGADO">Entregados (Cobrados)</option>
            <option value="A_LIQUIDAR">A Liquidar (En Tránsito/Prep)</option>
          </select>
        </div>
      </div>

      <Card noPadding className="overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead>
              <tr>
                <th className="premium-table-header">Pedido</th>
                <th className="premium-table-header">Fecha</th>
                <th className="premium-table-header">Estado</th>
                <th className="premium-table-header text-right">Subtotal</th>
                <th className="premium-table-header text-right">Costo Envío</th>
                <th className="premium-table-header text-right">Total Ingreso</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
              {listaFiltrada.map((p) => (
                <tr key={p.id} className="premium-table-row">
                  <td className="px-6 py-4 font-mono text-xs font-bold text-slate-500">#{p.id}</td>
                  <td className="px-6 py-4">{new Date(p.created_at).toLocaleString('es-AR', { dateStyle: 'short', timeStyle: 'short' })}</td>
                  <td className="px-6 py-4">
                    <span className={`px-2.5 py-1 rounded-full text-[10px] uppercase font-bold tracking-widest ${(estadoBadge[p.estado_codigo] ?? { className: 'bg-slate-100 text-slate-700' }).className}`}>
                      {estadoBadge[p.estado_codigo]?.label ?? p.estado_codigo}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-right text-slate-600 dark:text-slate-400">{formatCurrency(Number(p.subtotal) || 0)}</td>
                  <td className="px-6 py-4 text-right text-slate-600 dark:text-slate-400">{formatCurrency(Number(p.costo_envio) || 0)}</td>
                  <td className="px-6 py-4 text-right font-display font-bold text-emerald-600 dark:text-emerald-400">{formatCurrency(Number(p.total) || 0)}</td>
                </tr>
              ))}
              {listaFiltrada.length === 0 && (
                <tr>
                  <td colSpan={6} className="px-6 py-20 text-center">
                    <div className="flex flex-col items-center gap-3">
                      <LayoutDashboard size={48} className="text-slate-200 dark:text-slate-700" />
                      <p className="text-slate-500 dark:text-slate-400 font-medium">No hay registros para mostrar.</p>
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
