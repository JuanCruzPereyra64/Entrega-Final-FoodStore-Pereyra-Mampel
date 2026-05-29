import { useState, useMemo } from 'react'
import { Plus, Edit2, Trash2, Leaf, Settings2 } from 'lucide-react'
import { Modal } from '../components/common/Modal'
import { Button } from '../components/common/Button'
import { Card } from '../components/common/Card'
import { useIngredientes, useCreateIngrediente, useUpdateIngrediente, useDeleteIngrediente } from '../hooks/useIngredientes'
import { useUnidadesMedida, useCreateUnidadMedida, useDeleteUnidadMedida } from '../hooks/useUnidadesMedida'
import type { Ingrediente, IngredienteCreate } from '../types'

function UnidadesMedidaManagerModal({ open, onClose }: { open: boolean, onClose: () => void }) {
  const { data: unidades, isLoading } = useUnidadesMedida()
  const createMutation = useCreateUnidadMedida()
  const deleteMutation = useDeleteUnidadMedida()
  const [nombre, setNombre] = useState('')
  const [deleteError, setDeleteError] = useState<string | null>(null)

  function handleCreate(e: React.FormEvent) {
    e.preventDefault()
    if (!nombre.trim()) return
    createMutation.mutate({ nombre }, { onSuccess: () => setNombre('') })
  }

  function handleDelete(id: number) {
    if (!window.confirm('¿Seguro que querés eliminarla?')) return
    setDeleteError(null)
    deleteMutation.mutate(id, {
      onError: (err: any) => {
        const msg = err?.response?.data?.detail ?? 'No se puede eliminar esta unidad.'
        setDeleteError(msg)
      }
    })
  }

  return (
    <Modal open={open} onClose={onClose} title="Gestionar Unidades de Medida" maxWidth="max-w-md">
      <div className="space-y-6">
        <form onSubmit={handleCreate} className="flex gap-2">
          <input
            required
            placeholder="Nueva unidad (ej. Mililitros)"
            value={nombre}
            onChange={(e) => setNombre(e.target.value)}
            className="flex-1 bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-700 rounded-xl px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all"
          />
          <Button type="submit" variant="primary" isLoading={createMutation.isPending}>Agregar</Button>
        </form>

        {deleteError && (
          <p className="text-sm text-red-500 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl px-4 py-2">
            {deleteError}
          </p>
        )}

        <div className="space-y-2 max-h-60 overflow-y-auto pr-2 custom-scrollbar">
          {isLoading && <p className="text-center text-sm text-slate-500 py-4">Cargando...</p>}
          {unidades?.map((u) => (
            <div key={u.id} className="flex items-center justify-between p-3 rounded-xl border border-slate-100 dark:border-slate-800 bg-white dark:bg-slate-900/50 group">
              <span className="text-sm font-medium text-slate-700 dark:text-slate-300">{u.nombre}</span>
              <button
                type="button"
                onClick={() => handleDelete(u.id)}
                className="text-slate-300 hover:text-red-500 transition-colors p-1 opacity-0 group-hover:opacity-100"
                disabled={deleteMutation.isPending}
              >
                <Trash2 size={14} />
              </button>
            </div>
          ))}
          {unidades?.length === 0 && <p className="text-center text-sm text-slate-500 py-4">No hay unidades cargadas.</p>}
        </div>
      </div>
    </Modal>
  )
}

export function IngredientesPage() {
  const { data: ingredientes, isLoading, isError } = useIngredientes()

  const ingredientesOrdenados = useMemo(() => {
    if (!ingredientes) return []
    return [...ingredientes].sort((a, b) => (a.stock_actual || 0) - (b.stock_actual || 0))
  }, [ingredientes])

  const createMutation = useCreateIngrediente()
  const updateMutation = useUpdateIngrediente()
  const deleteMutation = useDeleteIngrediente()

  const { data: unidades } = useUnidadesMedida()

  const [modalOpen, setModalOpen] = useState(false)
  const [managerOpen, setManagerOpen] = useState(false)
  const [editing, setEditing] = useState<Ingrediente | null>(null)
  const [form, setForm] = useState<IngredienteCreate>({ nombre: '', unidad_medida_id: 0, es_alergeno: false, stock_actual: 0, stock_minimo: 0 })

  function openCreate() {
    setEditing(null)
    setForm({ nombre: '', unidad_medida_id: unidades?.[0]?.id || 0, es_alergeno: false, stock_actual: 0, stock_minimo: 0 })
    setModalOpen(true)
  }

  function openEdit(ing: Ingrediente) {
    setEditing(ing)
    setForm({ nombre: ing.nombre, unidad_medida_id: ing.unidad_medida_id || 0, es_alergeno: ing.es_alergeno, stock_actual: ing.stock_actual || 0, stock_minimo: ing.stock_minimo || 0 })
    setModalOpen(true)
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (editing) {
      updateMutation.mutate({ id: editing.id, data: form }, { onSuccess: () => setModalOpen(false) })
    } else {
      createMutation.mutate(form, { onSuccess: () => setModalOpen(false) })
    }
  }

  if (isLoading) return (
    <div className="flex flex-col items-center justify-center min-h-[400px] gap-4">
      <div className="w-12 h-12 border-4 border-primary/20 border-t-primary rounded-full animate-spin" />
      <p className="text-slate-500 font-medium italic">Recolectando ingredientes...</p>
    </div>
  )

  if (isError) return (
    <Card className="border-red-100 bg-red-50 dark:bg-red-900/10">
      <p className="text-red-600 dark:text-red-400 font-medium">Hubo un error al cargar la despensa.</p>
    </Card>
  )

  return (
    <div className="space-y-8">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-display font-bold text-slate-900 dark:text-white">Ingredientes</h1>
          <p className="text-slate-500 dark:text-slate-400 mt-1">
            Gestioná la materia prima para tus creaciones culinarias.
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Button onClick={() => setManagerOpen(true)} icon={Settings2} size="lg" variant="secondary">
            Unidades
          </Button>
          <Button onClick={openCreate} icon={Plus} size="lg" variant="accent">
            Nuevo ingrediente
          </Button>
        </div>
      </div>

      <Card noPadding className="overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead>
              <tr>
                <th className="premium-table-header w-16">ID</th>
                <th className="premium-table-header">Nombre</th>
                <th className="premium-table-header">Alérgeno</th>
                <th className="premium-table-header text-right">Stock</th>
                <th className="premium-table-header">Unidad de Medida</th>
                <th className="premium-table-header text-right">Acciones</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
              {ingredientesOrdenados.map((ing) => (
                <tr key={ing.id} className="premium-table-row">
                  <td className="px-6 py-4 font-mono text-xs text-slate-400">#{ing.id}</td>
                  <td className="px-6 py-4">
                    <span className="font-semibold text-slate-900 dark:text-slate-200">{ing.nombre}</span>
                  </td>
                  <td className="px-6 py-4">
                    {ing.es_alergeno ? (
                      <span className="bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400 text-[10px] uppercase font-bold tracking-widest px-2.5 py-1 rounded-full border border-red-200 dark:border-red-800">
                        Sí
                      </span>
                    ) : (
                      <span className="bg-slate-100 text-slate-500 dark:bg-slate-800 dark:text-slate-400 text-[10px] uppercase font-bold tracking-widest px-2.5 py-1 rounded-full border border-slate-200 dark:border-slate-700">
                        No
                      </span>
                    )}
                  </td>
                  <td className="px-6 py-4 text-right">
                    <div className="flex flex-col items-end">
                      <span className={`font-semibold ${ing.stock_actual <= ing.stock_minimo ? 'text-red-500' : 'text-slate-900 dark:text-slate-200'}`}>
                        {ing.stock_actual}
                      </span>
                      <span className="text-[10px] text-slate-500">Mín: {ing.stock_minimo}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <span className="bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 text-[10px] uppercase font-bold tracking-widest px-2.5 py-1 rounded-full border border-slate-200 dark:border-slate-700">
                      {ing.unidad_medida?.nombre || '-'}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <div className="flex justify-end gap-2">
                      <Button variant="secondary" size="sm" icon={Edit2} onClick={() => openEdit(ing)} />
                      <Button variant="danger" size="sm" icon={Trash2} onClick={() => deleteMutation.mutate(ing.id)} />
                    </div>
                  </td>
                </tr>
              ))}
              {ingredientes?.length === 0 && (
                <tr>
                  <td colSpan={5} className="px-6 py-20 text-center">
                    <div className="flex flex-col items-center gap-3">
                      <Leaf size={48} className="text-slate-200 dark:text-slate-700" />
                      <p className="text-slate-500 dark:text-slate-400 font-medium">La despensa está vacía.</p>
                      <Button variant="ghost" size="sm" onClick={openCreate}>Abastecer ahora</Button>
                    </div>
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </Card>

      <Modal
        open={modalOpen}
        title={editing ? 'Editar Ingrediente' : 'Nuevo Ingrediente'}
        onClose={() => setModalOpen(false)}
      >
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <label className="text-sm font-semibold text-slate-700 dark:text-slate-300 ml-1">Nombre</label>
            <input
              required
              placeholder="Ej: Harina 000, Sal, Tomate..."
              value={form.nombre}
              onChange={(e) => setForm({ ...form, nombre: e.target.value })}
              className="w-full bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-700 rounded-2xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-accent/20 focus:border-accent transition-all"
            />
          </div>
          <div className="space-y-2">
            <div className="flex items-center justify-between ml-1">
              <label className="text-sm font-semibold text-slate-700 dark:text-slate-300">Unidad de Medida</label>
              <button type="button" onClick={() => setManagerOpen(true)} className="text-xs font-semibold text-accent hover:text-accent/80 flex items-center gap-1 transition-colors">
                <Settings2 size={12} /> Gestionar
              </button>
            </div>
            <select
              required
              value={form.unidad_medida_id || ''}
              onChange={(e) => setForm({ ...form, unidad_medida_id: Number(e.target.value) })}
              className="w-full bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-700 rounded-2xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-accent/20 focus:border-accent transition-all appearance-none cursor-pointer"
            >
              <option value="" disabled>Seleccioná una unidad...</option>
              {unidades?.map((u) => (
                <option key={u.id} value={u.id}>{u.nombre}</option>
              ))}
            </select>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <label className="text-sm font-semibold text-slate-700 dark:text-slate-300 ml-1">Stock Actual</label>
              <input
                type="number"
                step="0.01"
                required
                value={form.stock_actual}
                onChange={(e) => setForm({ ...form, stock_actual: Number(e.target.value) })}
                className="w-full bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-700 rounded-2xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-accent/20 focus:border-accent transition-all"
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-semibold text-slate-700 dark:text-slate-300 ml-1">Stock Mínimo</label>
              <input
                type="number"
                step="0.01"
                required
                value={form.stock_minimo}
                onChange={(e) => setForm({ ...form, stock_minimo: Number(e.target.value) })}
                className="w-full bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-700 rounded-2xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-accent/20 focus:border-accent transition-all"
              />
            </div>
          </div>

          <label className="flex items-center gap-3 p-4 rounded-2xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-900/50 cursor-pointer hover:border-accent/50 transition-colors">
            <div className="relative flex items-center">
              <input
                type="checkbox"
                checked={form.es_alergeno}
                onChange={(e) => setForm({ ...form, es_alergeno: e.target.checked })}
                className="peer sr-only"
              />
              <div className="w-6 h-6 rounded-md border-2 border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 peer-checked:bg-red-500 peer-checked:border-red-500 transition-all flex items-center justify-center">
                <svg className="w-4 h-4 text-white opacity-0 peer-checked:opacity-100 transition-opacity" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="3">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                </svg>
              </div>
            </div>
            <div>
              <p className="text-sm font-semibold text-slate-700 dark:text-slate-300">Es un alérgeno</p>
              <p className="text-xs text-slate-500">Marcar si contiene gluten, lácteos, nueces, etc.</p>
            </div>
          </label>
          
          <div className="pt-2 pb-4">
            <Button
              type="submit"
              variant="accent"
              className="w-full py-4 text-base"
              isLoading={createMutation.isPending || updateMutation.isPending}
            >
              {editing ? 'Actualizar Ingrediente' : 'Cargar Ingrediente'}
            </Button>
          </div>
        </form>
      </Modal>
      <UnidadesMedidaManagerModal open={managerOpen} onClose={() => setManagerOpen(false)} />
    </div>
  )
}
