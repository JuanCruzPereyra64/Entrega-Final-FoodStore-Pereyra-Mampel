import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { pedidosApi } from '../services/api'
import { useCartStore } from '../store/useCartStore'
import { Card } from '../components/common/Card'
import { Button } from '../components/common/Button'
import { Package, RefreshCcw, ShoppingBag, ChevronRight } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

export function PedidosPage() {
  const qc = useQueryClient()
  const navigate = useNavigate()
  const addItem = useCartStore(s => s.addItem)
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

  const handleRepetirPedido = (pedido: any) => {
    if (!pedido.detalles) return
    pedido.detalles.forEach((det: any) => {
      // Si el producto sigue existiendo, lo agregamos al carrito
      if (det.producto) {
        addItem({
          id: Date.now() + det.producto_id,
          producto_id: det.producto_id,
          cantidad: det.cantidad,
          precio: Number(det.producto.precio_base) || Number(det.precio_unitario_snap) || 0,
          nombre: det.producto.nombre || det.nombre_producto_snap,
          imagen_url: det.producto?.imagenes_url?.[0]
        })
      }
    })
    navigate('/carrito')
  }

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
            <Card key={p.id} className="flex flex-col md:flex-row justify-between gap-6">
              <div className="flex-1 space-y-4">
                <div>
                  <p className="font-bold text-lg">Pedido #{p.id}</p>
                  <p className="text-slate-500 text-sm">{new Date(p.created_at).toLocaleString()}</p>
                </div>
                
                {/* Lista de productos del pedido */}
                <div className="space-y-3 bg-slate-50 dark:bg-slate-900/50 p-4 rounded-2xl">
                  <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest">Detalle del pedido</h4>
                  {p.detalles?.map(det => (
                    <div key={det.id} className="flex items-center gap-3">
                      <div className="w-12 h-12 rounded-xl bg-white dark:bg-slate-800 overflow-hidden shrink-0 border border-slate-200 dark:border-slate-700">
                        {det.producto?.imagenes_url?.[0] ? (
                          <img src={det.producto.imagenes_url[0]} alt={det.nombre_producto_snap} className="w-full h-full object-cover" />
                        ) : (
                          <div className="w-full h-full flex items-center justify-center text-slate-400">
                            <ShoppingBag size={16} />
                          </div>
                        )}
                      </div>
                      <div className="flex-1">
                        <p className="font-semibold text-sm text-slate-900 dark:text-white leading-tight">{det.nombre_producto_snap}</p>
                        <p className="text-xs text-slate-500">{det.cantidad} x ${det.precio_unitario_snap}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="text-right flex flex-col items-end gap-3 md:w-48 shrink-0">
                <span className="inline-block px-3 py-1 rounded-full text-xs font-semibold bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300">
                  {p.estado_codigo}
                </span>
                <p className="font-display font-bold text-2xl text-primary mb-2">${p.total}</p>

                <div className="flex flex-col gap-2 w-full mt-auto">
                  <Button 
                    size="sm" 
                    className="w-full justify-center bg-slate-900 text-white hover:bg-slate-800 dark:bg-white dark:text-slate-900 dark:hover:bg-slate-200"
                    icon={RefreshCcw}
                    onClick={() => handleRepetirPedido(p)}
                  >
                    Repetir Pedido
                  </Button>

                  {(p.estado_codigo === 'PENDIENTE' || p.estado_codigo === 'CONFIRMADO') && (
                    <Button 
                      size="sm" 
                      variant="outline" 
                      className="w-full justify-center text-red-600 border-red-200 hover:bg-red-50"
                      isLoading={cancelMutation.isPending}
                      onClick={() => cancelMutation.mutate(p.id)}
                    >
                      Cancelar Pedido
                    </Button>
                  )}
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}
