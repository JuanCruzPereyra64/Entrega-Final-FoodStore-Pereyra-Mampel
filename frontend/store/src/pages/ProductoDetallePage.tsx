import { useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { ArrowLeft, Plus, Trash2, ChefHat, Tag, Info } from 'lucide-react'
import { motion } from 'framer-motion'
import { useProducto, useAddIngrediente, useRemoveIngrediente } from '../hooks/useProductos'
import { useIngredientes } from '../hooks/useIngredientes'
import { Card, CardHeader } from '../components/common/Card'
import { Button } from '../components/common/Button'

export function ProductoDetallePage() {
  const { id } = useParams<{ id: string }>()
  const productoId = Number(id)

  const { data: producto, isLoading, isError } = useProducto(productoId)
  const { data: todosIngredientes } = useIngredientes()
  const addMutation = useAddIngrediente()
  const removeMutation = useRemoveIngrediente()

  const [ingredienteSeleccionado, setIngredienteSeleccionado] = useState<number>(0)

  if (isLoading) return (
    <div className="flex flex-col items-center justify-center min-h-[400px] gap-4">
      <div className="w-12 h-12 border-4 border-primary/20 border-t-primary rounded-full animate-spin" />
      <p className="text-slate-500 font-medium italic">Emplatando detalles...</p>
    </div>
  )

  if (isError || !producto) return (
    <Card className="border-red-100 bg-red-50 dark:bg-red-900/10 max-w-2xl mx-auto mt-10">
      <p className="text-red-600 dark:text-red-400 font-medium text-center">Ups! No pudimos encontrar este producto.</p>
      <div className="flex justify-center mt-4">
        <Link to="/productos">
          <Button variant="secondary" size="sm" icon={ArrowLeft}>Volver a la carta</Button>
        </Link>
      </div>
    </Card>
  )

  const ingredientesActualesIds = new Set(producto.ingredientes?.map((i) => i.id) ?? [])
  const ingredientesDisponibles = todosIngredientes?.filter((i) => !ingredientesActualesIds.has(i.id)) ?? []

  function handleAgregar() {
    if (!ingredienteSeleccionado) return
    addMutation.mutate({ productoId, ingredienteId: ingredienteSeleccionado }, {
      onSuccess: () => setIngredienteSeleccionado(0),
    })
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Back Button */}
      <Link to="/productos" className="inline-flex items-center text-slate-500 hover:text-primary transition-colors gap-2 group">
        <ArrowLeft size={18} className="group-hover:-translate-x-1 transition-transform" />
        <span className="text-sm font-medium">Volver a Productos</span>
      </Link>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Product Info */}
        <div className="lg:col-span-2 space-y-6">
          <Card className="relative overflow-hidden">
            <div className="absolute top-0 right-0 p-8 text-primary/10 pointer-events-none">
              <ChefHat size={120} strokeWidth={1} />
            </div>
            
            <div className="relative z-10">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h1 className="text-4xl font-display font-bold text-slate-900 dark:text-white leading-tight">
                    {producto.nombre}
                  </h1>
                  <div className="flex items-center gap-2 mt-2">
                    <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-primary/10 text-primary border border-primary/20">
                      <Tag size={12} />
                      {producto.categorias?.[0]?.nombre || 'General'}
                    </span>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-3xl font-display font-bold text-accent dark:text-accent">
                    ${producto.precio_base.toFixed(2)}
                  </p>
                  <p className="text-xs text-slate-400 font-medium uppercase tracking-widest mt-1">Precio Sugerido</p>
                </div>
              </div>

              <div className="mt-8 pt-8 border-t border-slate-100 dark:border-slate-800">
                <div className="flex items-center gap-2 text-slate-900 dark:text-white font-semibold mb-3">
                  <Info size={18} className="text-primary" />
                  <h3>Descripción del Producto</h3>
                </div>
                <p className="text-slate-600 dark:text-slate-400 leading-relaxed">
                  {producto.descripcion || 'Este producto aún no cuenta con una descripción detallada en nuestra carta.'}
                </p>
              </div>
            </div>
          </Card>
        </div>

        {/* Right Column: Ingredients Management */}
        <div className="space-y-6">
          <Card className="h-full flex flex-col">
            <CardHeader 
              title="Ingredientes" 
              subtitle={`${producto.ingredientes?.length || 0} ingredientes asignados`}
            />

            <div className="flex-1 space-y-4">
              {producto.ingredientes?.length ? (
                <ul className="space-y-3">
                  {producto.ingredientes.map((ing) => (
                    <motion.li 
                      layout
                      initial={{ opacity: 0, x: 20 }}
                      animate={{ opacity: 1, x: 0 }}
                      key={ing.id} 
                      className="flex items-center justify-between p-3 rounded-2xl bg-slate-50 dark:bg-slate-900/50 border border-slate-100 dark:border-slate-800 group"
                    >
                      <div>
                        <p className="text-sm font-semibold text-slate-900 dark:text-slate-200">{ing.nombre}</p>
                        <p className="text-[10px] text-slate-400 uppercase font-bold tracking-tighter">{ing.unidad_medida}</p>
                      </div>
                      <button
                        onClick={() => removeMutation.mutate({ productoId, ingredienteId: ing.id })}
                        className="p-2 text-slate-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-xl transition-all opacity-0 group-hover:opacity-100"
                        title="Quitar ingrediente"
                      >
                        <Trash2 size={16} />
                      </button>
                    </motion.li>
                  ))}
                </ul>
              ) : (
                <div className="py-10 text-center space-y-3">
                  <div className="inline-flex items-center justify-center w-12 h-12 rounded-2xl bg-slate-100 dark:bg-slate-800 text-slate-400">
                    <Plus size={24} />
                  </div>
                  <p className="text-sm text-slate-500 italic">No hay ingredientes asignados aún.</p>
                </div>
              )}
            </div>

            {/* Add Ingredient Section */}
            {ingredientesDisponibles.length > 0 && (
              <div className="mt-8 pt-6 border-t border-slate-100 dark:border-slate-800 space-y-4">
                <p className="text-xs font-bold text-slate-400 uppercase tracking-widest px-1 text-center">Añadir a la receta</p>
                <div className="space-y-3">
                  <select
                    value={ingredienteSeleccionado}
                    onChange={(e) => setIngredienteSeleccionado(Number(e.target.value))}
                    className="w-full bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-700 rounded-2xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all appearance-none"
                  >
                    <option value={0} disabled>Seleccionar...</option>
                    {ingredientesDisponibles.map((i) => (
                      <option key={i.id} value={i.id}>{i.nombre} ({i.unidad_medida})</option>
                    ))}
                  </select>
                  <Button
                    onClick={handleAgregar}
                    disabled={!ingredienteSeleccionado || addMutation.isPending}
                    className="w-full"
                    variant="primary"
                    isLoading={addMutation.isPending}
                    icon={Plus}
                  >
                    Agregar Ingrediente
                  </Button>
                </div>
              </div>
            )}
          </Card>
        </div>
      </div>
    </div>
  )
}
