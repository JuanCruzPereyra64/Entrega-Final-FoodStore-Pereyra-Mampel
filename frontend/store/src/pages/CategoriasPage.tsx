import { useState } from 'react'
import { Plus, Edit2, Trash2, LayoutDashboard } from 'lucide-react'
import { Modal } from '../components/common/Modal'
import { Button } from '../components/common/Button'
import { Card } from '../components/common/Card'
import { useCategorias, useCreateCategoria, useUpdateCategoria, useDeleteCategoria } from '../hooks/useCategorias'
import type { Categoria, CategoriaCreate } from '../types'

export function CategoriasPage() {
  const { data: categorias, isLoading, isError } = useCategorias()
  const createMutation = useCreateCategoria()
  const updateMutation = useUpdateCategoria()
  const deleteMutation = useDeleteCategoria()

  const [modalOpen, setModalOpen] = useState(false)
  const [editing, setEditing] = useState<Categoria | null>(null)
  const [form, setForm] = useState<CategoriaCreate>({ nombre: '', descripcion: '' })

  function openCreate() {
    setEditing(null)
    setForm({ nombre: '', descripcion: '' })
    setModalOpen(true)
  }

  function openEdit(cat: Categoria) {
    setEditing(cat)
    setForm({ nombre: cat.nombre, descripcion: cat.descripcion ?? '' })
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
      <p className="text-slate-500 font-medium italic">Sintonizando categorías...</p>
    </div>
  )

  if (isError) return (
    <Card className="border-red-100 bg-red-50 dark:bg-red-900/10">
      <p className="text-red-600 dark:text-red-400 font-medium">Ups! Hubo un problema al cargar las categorías.</p>
    </Card>
  )

  return (
    <div className="space-y-8">
      {/* Header Section */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-display font-bold text-slate-900 dark:text-white">Categorías</h1>
          <p className="text-slate-500 dark:text-slate-400 mt-1">
            Gestioná las clasificaciones de tus productos gastronómicos.
          </p>
        </div>
        <Button onClick={openCreate} icon={Plus} size="lg">
          Nueva categoría
        </Button>
      </div>

      {/* Main Content Table */}
      <Card noPadding className="overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead>
              <tr>
                <th className="premium-table-header w-16">ID</th>
                <th className="premium-table-header">Nombre</th>
                <th className="premium-table-header">Descripción</th>
                <th className="premium-table-header text-right">Acciones</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
              {categorias?.map((cat) => (
                <tr key={cat.id} className="premium-table-row">
                  <td className="px-6 py-4 font-mono text-xs text-slate-400">
                    #{cat.id}
                  </td>
                  <td className="px-6 py-4">
                    <span className="font-semibold text-slate-900 dark:text-slate-200">{cat.nombre}</span>
                  </td>
                  <td className="px-6 py-4">
                    <span className="text-slate-500 dark:text-slate-400 italic">
                      {cat.descripcion || 'Sin descripción'}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex justify-end gap-2">
                      <Button 
                        variant="secondary" 
                        size="sm" 
                        icon={Edit2} 
                        onClick={() => openEdit(cat)}
                        title="Editar"
                      />
                      <Button 
                        variant="danger" 
                        size="sm" 
                        icon={Trash2} 
                        onClick={() => deleteMutation.mutate(cat.id)}
                        title="Eliminar"
                      />
                    </div>
                  </td>
                </tr>
              ))}
              {categorias?.length === 0 && (
                <tr>
                  <td colSpan={4} className="px-6 py-20 text-center">
                    <div className="flex flex-col items-center gap-3">
                      <LayoutDashboard size={48} className="text-slate-200 dark:text-slate-700" />
                      <p className="text-slate-500 dark:text-slate-400 font-medium">No hay categorías registradas aún.</p>
                      <Button variant="ghost" size="sm" onClick={openCreate}>Crear la primera</Button>
                    </div>
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </Card>

      {/* Form Modal */}
      <Modal
        open={modalOpen}
        title={editing ? 'Editar Categoría' : 'Nueva Categoría'}
        onClose={() => setModalOpen(false)}
      >
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <label className="text-sm font-semibold text-slate-700 dark:text-slate-300 ml-1">Nombre de la categoría</label>
            <input
              required
              placeholder="Ej: Entradas, Plato Principal..."
              value={form.nombre}
              onChange={(e) => setForm({ ...form, nombre: e.target.value })}
              className="w-full bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-700 rounded-2xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all"
            />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-semibold text-slate-700 dark:text-slate-300 ml-1">Descripción (opcional)</label>
            <textarea
              placeholder="Breve detalle sobre qué incluye esta categoría..."
              value={form.descripcion ?? ''}
              onChange={(e) => setForm({ ...form, descripcion: e.target.value })}
              className="w-full bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-700 rounded-2xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all min-h-[100px]"
            />
          </div>
          
          <div className="pt-2">
            <Button
              type="submit"
              className="w-full py-4 text-base"
              isLoading={createMutation.isPending || updateMutation.isPending}
            >
              {editing ? 'Guardar Cambios' : 'Crear Categoría'}
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  )
}
