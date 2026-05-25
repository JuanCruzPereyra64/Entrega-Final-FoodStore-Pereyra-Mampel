import { useState } from 'react'
import { useCartStore } from '../store/useCartStore'
import { pedidosApi } from '../services/api'
import { Button } from '../components/common/Button'
import { Card } from '../components/common/Card'
import { Trash2, ShoppingBag } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

export function CartPage() {
  const { items, clearCart, removeItem, updateQuantity, getTotal } = useCartStore()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  async function handleCheckout() {
    if (items.length === 0) return
    setLoading(true)
    setError('')
    try {
      await pedidosApi.create({
        detalles: items.map(item => ({
          producto_id: item.producto_id,
          cantidad: item.cantidad
        })),
        forma_pago_codigo: "EFECTIVO",
        direccion_id: undefined
      })
      clearCart()
      navigate('/mis-pedidos')
    } catch (err: any) {
      const msg = err.response?.data?.detail || err.message || 'Error desconocido';
      setError(typeof msg === 'string' ? msg : JSON.stringify(msg))
    } finally {
      setLoading(false)
    }
  }

  if (items.length === 0) return (
    <div className="flex flex-col items-center justify-center p-20 text-center">
      <ShoppingBag size={64} className="text-slate-300 mb-6" />
      <h2 className="text-2xl font-bold font-display">Tu carrito está vacío</h2>
      <Button className="mt-6" onClick={() => navigate('/')}>Volver al Catálogo</Button>
    </div>
  )

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <h1 className="text-3xl font-bold font-display">Tu Carrito</h1>
      {error && <div className="bg-red-50 text-red-600 p-4 rounded-xl text-sm">{error}</div>}
      
      <Card className="divide-y divide-slate-100">
        {items.map(item => (
          <div key={item.producto_id} className="py-4 flex justify-between items-center">
            <div>
              <h3 className="font-bold">{item.nombre}</h3>
              <p className="text-slate-500">${item.precio} c/u</p>
            </div>
            <div className="flex items-center gap-4">
              <input 
                type="number" 
                min="1" 
                value={item.cantidad}
                onChange={e => updateQuantity(item.producto_id, Number(e.target.value))}
                className="w-16 border border-slate-200 rounded-xl px-2 py-1 text-center"
              />
              <span className="font-bold w-20 text-right">${item.precio * item.cantidad}</span>
              <button onClick={() => removeItem(item.producto_id)} className="text-red-500 hover:text-red-700 p-2"><Trash2 size={20}/></button>
            </div>
          </div>
        ))}
        <div className="py-6 flex justify-between items-center">
          <span className="text-xl font-bold">Total:</span>
          <span className="text-2xl font-bold text-primary">${getTotal()}</span>
        </div>
      </Card>
      
      <div className="flex justify-end">
        <Button size="lg" onClick={handleCheckout} isLoading={loading}>Realizar Pedido</Button>
      </div>
    </div>
  )
}
