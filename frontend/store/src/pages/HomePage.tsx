import { useQuery } from '@tanstack/react-query'
import { productosApi, categoriasApi } from '../services/api'
import { useCartStore } from '../store/useCartStore'
import { Card } from '../components/common/Card'
import { Button } from '../components/common/Button'
import { ShoppingCart } from 'lucide-react'

export function HomePage() {
  const { data: productos, isLoading: isLoadingProd } = useQuery({ queryKey: ['productos'], queryFn: () => productosApi.getAll() })
  const { data: categorias } = useQuery({ queryKey: ['categorias'], queryFn: categoriasApi.getAll })
  const addItem = useCartStore(s => s.addItem)

  if (isLoadingProd) return <div className="p-10 flex justify-center"><div className="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin"></div></div>

  return (
    <div className="space-y-8">
      <div className="text-center py-10 bg-slate-50 dark:bg-slate-900 rounded-3xl">
        <h1 className="text-4xl font-display font-bold">Catálogo de Productos</h1>
        <p className="text-slate-500 mt-2">Encuentra todo lo que buscas</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {productos?.filter(p => p.disponible).map(p => (
          <Card key={p.id} className="flex flex-col">
            {p.imagenes_url && p.imagenes_url[0] && (
              <img src={p.imagenes_url[0]} alt={p.nombre} className="h-48 w-full object-cover rounded-xl mb-4" />
            )}
            <h3 className="text-lg font-bold">{p.nombre}</h3>
            <p className="text-sm text-slate-500 flex-1 my-2 line-clamp-2">{p.descripcion}</p>
            <div className="flex items-center justify-between mt-4">
              <span className="text-xl font-bold text-primary">${p.precio_base}</span>
              <Button size="sm" icon={ShoppingCart} onClick={() => addItem({ id: Date.now(), producto_id: p.id!, cantidad: 1, precio: p.precio_base, nombre: p.nombre, imagen_url: p.imagenes_url?.[0] })}>
                Agregar
              </Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  )
}
