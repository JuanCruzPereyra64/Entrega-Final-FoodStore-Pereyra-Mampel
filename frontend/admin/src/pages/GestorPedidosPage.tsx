import { useMemo } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { pedidosApi } from '../services/api'
import { Card } from '../components/common/Card'
import { Button } from '../components/common/Button'
import { LayoutDashboard } from 'lucide-react'
import { formatCurrency } from '../utils/format'

export function GestorPedidosPage() {
  const qc = useQueryClient()
  const { data: pedidos, isLoading } = useQuery({
    queryKey: ['pedidos'],
    queryFn: pedidosApi.getAll
  })

  const updateMutation = useMutation({
    mutationFn: ({ id, estado }: { id: number, estado: string }) => pedidosApi.updateEstado(id, estado),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['pedidos'] })
  })

  const estadoBadge: Record<string, { label: string; className: string }> = {
    PENDIENTE:  { label: 'Pendiente',       className: 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400' },
    CONFIRMADO: { label: 'Confirmado',      className: 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400' },
    EN_PREP:    { label: 'En Preparación',  className: 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400' },
    EN_CAMINO:  { label: 'En Camino',       className: 'bg-indigo-100 text-indigo-700 dark:bg-indigo-900/30 dark:text-indigo-400' },
    ENTREGADO:  { label: 'Entregado',       className: 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400' },
    CANCELADO:  { label: 'Cancelado',       className: 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400' },
  }

  const pedidosOrdenados = useMemo(() => {
    if (!pedidos) return []
    
    const prioridades: Record<string, number> = {
      PENDIENTE: 1,
      CONFIRMADO: 2,
      EN_PREP: 3,
      EN_CAMINO: 4,
      ENTREGADO: 5,
      CANCELADO: 6
    }

    return [...pedidos].sort((a, b) => {
      const pA = prioridades[a.estado_codigo] ?? 99
      const pB = prioridades[b.estado_codigo] ?? 99
      if (pA !== pB) return pA - pB
      return new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
    })
  }, [pedidos])

  if (isLoading) return <div className="flex justify-center p-10"><div className="w-10 h-10 border-4 border-primary border-t-transparent rounded-full animate-spin" /></div>

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold font-display">Gestor de Pedidos</h1>
      </div>

      <Card noPadding className="overflow-hidden">
        <table className="w-full text-sm text-left">
          <thead>
            <tr>
              <th className="premium-table-header">ID</th>
              <th className="premium-table-header">Fecha</th>
              <th className="premium-table-header">Total</th>
              <th className="premium-table-header">Estado Actual</th>
              <th className="premium-table-header">Acciones</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
            {pedidosOrdenados.map((p) => (
              <tr key={p.id} className="premium-table-row">
                <td className="px-6 py-4 font-mono text-xs">#{p.id}</td>
                <td className="px-6 py-4">{new Date(p.created_at).toLocaleString()}</td>
                <td className="px-6 py-4 font-semibold">{formatCurrency(Number(p.total) || 0)}</td>
                <td className="px-6 py-4">
                  <span className={`px-3 py-1 rounded-full text-xs font-semibold ${(estadoBadge[p.estado_codigo] ?? { className: 'bg-slate-100 text-slate-700' }).className}`}>
                    {estadoBadge[p.estado_codigo]?.label ?? p.estado_codigo}
                  </span>
                </td>
                <td className="px-6 py-4">
                  <div className="flex gap-2">
                    {p.estado_codigo === 'PENDIENTE' && (
                      <>
                        <Button size="sm" className="!bg-green-500 !shadow-green-500/20 hover:!bg-green-600" onClick={() => updateMutation.mutate({ id: p.id, estado: 'CONFIRMADO' })}>Confirmar</Button>
                        <Button size="sm" className="!bg-red-500 !shadow-red-500/20 hover:!bg-red-600" onClick={() => updateMutation.mutate({ id: p.id, estado: 'CANCELADO' })}>Rechazar</Button>
                      </>
                    )}
                    {p.estado_codigo === 'CONFIRMADO' && (
                      <Button size="sm" variant="accent" onClick={() => updateMutation.mutate({ id: p.id, estado: 'EN_PREP' })}>Preparar</Button>
                    )}
                    {p.estado_codigo === 'EN_PREP' && (
                      <Button size="sm" variant="primary" onClick={() => updateMutation.mutate({ id: p.id, estado: 'EN_CAMINO' })}>Despachar</Button>
                    )}
                    {p.estado_codigo === 'EN_CAMINO' && (
                      <Button size="sm" className="!bg-emerald-600 !shadow-emerald-600/20 hover:!bg-emerald-700" onClick={() => updateMutation.mutate({ id: p.id, estado: 'ENTREGADO' })}>Entregado</Button>
                    )}
                  </div>
                </td>
              </tr>
            ))}
            {pedidos?.length === 0 && (
              <tr>
                <td colSpan={5} className="px-6 py-20 text-center">
                  <LayoutDashboard className="mx-auto text-slate-300 mb-4" size={48} />
                  <p className="text-slate-500 font-medium">No hay pedidos registrados.</p>
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </Card>
    </div>
  )
}
