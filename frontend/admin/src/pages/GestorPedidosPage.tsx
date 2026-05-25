import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { pedidosApi } from '../services/api'
import { Card } from '../components/common/Card'
import { Button } from '../components/common/Button'
import { LayoutDashboard } from 'lucide-react'

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
            {pedidos?.map((p) => (
              <tr key={p.id} className="premium-table-row">
                <td className="px-6 py-4 font-mono text-xs">#{p.id}</td>
                <td className="px-6 py-4">{new Date(p.created_at).toLocaleString()}</td>
                <td className="px-6 py-4 font-semibold">${p.total}</td>
                <td className="px-6 py-4">
                  <span className="px-3 py-1 rounded-full text-xs font-semibold bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300">
                    {p.estado_codigo}
                  </span>
                </td>
                <td className="px-6 py-4">
                  <div className="flex gap-2">
                    {p.estado_codigo === 'PENDIENTE' && (
                      <Button size="sm" onClick={() => updateMutation.mutate({ id: p.id, estado: 'CONFIRMADO' })}>Confirmar</Button>
                    )}
                    {p.estado_codigo === 'CONFIRMADO' && (
                      <Button size="sm" onClick={() => updateMutation.mutate({ id: p.id, estado: 'EN_PREP' })}>Preparar</Button>
                    )}
                    {p.estado_codigo === 'EN_PREP' && (
                      <Button size="sm" onClick={() => updateMutation.mutate({ id: p.id, estado: 'EN_CAMINO' })}>Despachar</Button>
                    )}
                    {p.estado_codigo === 'EN_CAMINO' && (
                      <Button size="sm" onClick={() => updateMutation.mutate({ id: p.id, estado: 'ENTREGADO' })}>Entregado</Button>
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
