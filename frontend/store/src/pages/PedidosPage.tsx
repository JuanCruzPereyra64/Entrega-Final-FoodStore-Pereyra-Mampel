import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { pedidosApi } from '../services/api'
import { Card } from '../components/common/Card'
import { Button } from '../components/common/Button'
import { Package } from 'lucide-react'

export function PedidosPage() {
  const qc = useQueryClient()
  const [cancelError, setCancelError] = useState('')

  const { data: pedidos, isLoading } = useQuery({
    queryKey: ['mis-pedidos'],
    queryFn: pedidosApi.getAll
  })

  const cancelMutation = useMutation({
    mutationFn: (id: number) => pedidosApi.cancelar(id),
    onSuccess: () => {
      setCancelError('')
      qc.invalidateQueries({ queryKey: ['mis-pedidos'] })
    },
    onError: (err: any) => {
      setCancelError(err.message || 'No se pudo cancelar el pedido')
    }
  })

  if (isLoading) return <div className="flex justify-center p-10"><div className="w-10 h-10 border-4 border-primary border-t-transparent rounded-full animate-spin" /></div>

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <h1 className="text-3xl font-bold font-display">Mis Pedidos</h1>

      {cancelError && (
        <div className="bg-red-50 text-red-600 p-4 rounded-xl text-sm">{cancelError}</div>
      )}

      {pedidos?.length === 0 ? (
        <div className="flex flex-col items-center justify-center p-20 text-center">
          <Package size={64} className="text-slate-300 mb-6" />
          <h2 className="text-2xl font-bold font-display">No tienes pedidos</h2>
        </div>
      ) : (
        <div className="space-y-4">
          {pedidos?.map(p => (
            <Card key={p.id} className="flex justify-between items-center">
              <div>
                <p className="font-bold text-lg">Pedido #{p.id}</p>
                <p className="text-slate-500 text-sm">{new Date(p.created_at).toLocaleString()}</p>
              </div>
              <div className="text-right flex flex-col items-end gap-2">
                <span className="inline-block px-3 py-1 rounded-full text-xs font-semibold bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300">
                  {p.estado_codigo}
                </span>
                <p className="font-bold mb-2">${p.total}</p>

                {(p.estado_codigo === 'PENDIENTE' || p.estado_codigo === 'CONFIRMADO') && (
                  <Button 
                    size="sm" 
                    variant="outline" 
                    className="text-red-600 border-red-200 hover:bg-red-50"
                    isLoading={cancelMutation.isPending}
                    onClick={() => cancelMutation.mutate(p.id)}
                  >
                    Cancelar Pedido
                  </Button>
                )}
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}
