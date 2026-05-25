import { useState } from 'react'
import { Plus, Edit2, Trash2, Leaf } from 'lucide-react'
import { Modal } from '../components/common/Modal'
import { Button } from '../components/common/Button'
import { Card } from '../components/common/Card'
import { useIngredientes, useCreateIngrediente, useUpdateIngrediente, useDeleteIngrediente } from '../hooks/useIngredientes'
import type { Ingrediente, IngredienteCreate } from '../types'

export function IngredientesPage() {
  const { data: ingredientes, isLoading, isError } = useIngredientes()
  const createMutation = useCreateIngrediente()
  const updateMutation = useUpdateIngrediente()
  const deleteMutation = useDeleteIngrediente()

  const [modalOpen, setModalOpen] = useState(false)
  const [editing, setEditing] = useState<Ingrediente | null>(null)
  const [form, setForm] = useState<IngredienteCreate>({ nombre: '', unidad_medida: '' })

  function openCreate() {
    setEditing(null)
    setForm({ nombre: '', unidad_medida: '' })
    setModalOpen(true)
  }

  function openEdit(ing: Ingrediente) {
    setEditing(ing)
    setForm({ nombre: ing.nombre, unidad_medida: ing.unidad_medida })
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
        <Button onClick={openCreate} icon={Plus} size="lg" variant="accent">
          Nuevo ingrediente
        </Button>
      </div>

      <Card noPadding className="overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead>
              <tr>
                <th className="premium-table-header w-16">ID</th>
                <th className="premium-table-header">Nombre</th>
                <th className="premium-table-header">Unidad de Medida</th>
                <th className="premium-table-header text-right">Acciones</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
              {ingredientes?.map((ing) => (
                <tr key={ing.id} className="premium-table-row">
                  <td className="px-6 py-4 font-mono text-xs text-slate-400">#{ing.id}</td>
                  <td className="px-6 py-4">
                    <span className="font-semibold text-slate-900 dark:text-slate-200">{ing.nombre}</span>
                  </td>
                  <td className="px-6 py-4">
                    <span className="bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 text-[10px] uppercase font-bold tracking-widest px-2.5 py-1 rounded-full border border-slate-200 dark:border-slate-700">
                      {ing.unidad_medida}
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
                  <td colSpan={4} className="px-6 py-20 text-center">
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
            <label className="text-sm font-semibold text-slate-700 dark:text-slate-300 ml-1">Unidad de Medida</label>
            <input
              required
              placeholder="ej: kg, litros, gramos, unidades..."
              value={form.unidad_medida}
              onChange={(e) => setForm({ ...form, unidad_medida: e.target.value })}
              className="w-full bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-700 rounded-2xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-accent/20 focus:border-accent transition-all"
            />
          </div>
          
          <div className="pt-2">
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
    </div>
  )
}
