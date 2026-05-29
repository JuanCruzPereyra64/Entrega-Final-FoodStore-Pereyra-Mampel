import { useState, useEffect } from 'react'
import { authApi, direccionesApi } from '../services/api'
import type { UsuarioRead, Direccion } from '../types'
import { Button } from '../components/common/Button'
import { Card, CardHeader } from '../components/common/Card'
import { Modal } from '../components/common/Modal'
import { MapPin, Plus, Pencil, Trash2, Star, Check } from 'lucide-react'

const INPUT = 'w-full bg-slate-50 dark:bg-slate-800 border-none rounded-2xl px-4 py-3 focus:ring-2 focus:ring-primary/20 text-sm'
const LABEL = 'block text-sm font-semibold mb-1.5 text-slate-700 dark:text-slate-300'

export function PerfilPage() {
  const [usuario, setUsuario] = useState<UsuarioRead | null>(null)
  const [direcciones, setDirecciones] = useState<Direccion[]>([])
  const [loading, setLoading] = useState(true)

  const [nombre, setNombre] = useState('')
  const [apellido, setApellido] = useState('')
  const [celular, setCelular] = useState('')
  const [saving, setSaving] = useState(false)
  const [saveSuccess, setSaveSuccess] = useState(false)
  const [saveError, setSaveError] = useState('')

  const [modalOpen, setModalOpen] = useState(false)
  const [editingDir, setEditingDir] = useState<Direccion | null>(null)
  const [addrForm, setAddrForm] = useState({ etiqueta: '', linea1: '', linea2: '', ciudad: '', es_principal: false })
  const [addrSaving, setAddrSaving] = useState(false)
  const [addrError, setAddrError] = useState('')

  useEffect(() => { loadData() }, [])

  async function loadData() {
    setLoading(true)
    try {
      const [user, dirs] = await Promise.all([authApi.me(), direccionesApi.getAll()])
      setUsuario(user)
      setNombre(user.nombre)
      setApellido(user.apellido)
      setCelular(user.celular || '')
      setDirecciones(dirs)
    } finally {
      setLoading(false)
    }
  }

  async function handleSavePerfil(e: React.FormEvent) {
    e.preventDefault()
    setSaving(true)
    setSaveError('')
    setSaveSuccess(false)
    try {
      const updated = await authApi.updateMe({ nombre, apellido, celular: celular || undefined })
      setUsuario(updated)
      setSaveSuccess(true)
      setTimeout(() => setSaveSuccess(false), 3000)
    } catch (err: any) {
      setSaveError(err.message || 'Error al guardar')
    } finally {
      setSaving(false)
    }
  }

  function openAddDir() {
    setEditingDir(null)
    setAddrForm({ etiqueta: '', linea1: '', linea2: '', ciudad: '', es_principal: false })
    setAddrError('')
    setModalOpen(true)
  }

  function openEditDir(dir: Direccion) {
    setEditingDir(dir)
    setAddrForm({
      etiqueta: dir.etiqueta || '',
      linea1: dir.linea1,
      linea2: dir.linea2 || '',
      ciudad: dir.ciudad,
      es_principal: dir.es_principal,
    })
    setAddrError('')
    setModalOpen(true)
  }

  async function handleSaveDir(e: React.FormEvent) {
    e.preventDefault()
    setAddrSaving(true)
    setAddrError('')
    try {
      if (editingDir) {
        const updated = await direccionesApi.update(editingDir.id, {
          etiqueta: addrForm.etiqueta || undefined,
          linea1: addrForm.linea1,
          linea2: addrForm.linea2 || undefined,
          ciudad: addrForm.ciudad,
        })
        setDirecciones(prev => prev.map(d => d.id === updated.id ? updated : d))
      } else {
        const created = await direccionesApi.create({
          etiqueta: addrForm.etiqueta || undefined,
          linea1: addrForm.linea1,
          linea2: addrForm.linea2 || undefined,
          ciudad: addrForm.ciudad,
          es_principal: addrForm.es_principal,
        })
        setDirecciones(prev =>
          addrForm.es_principal
            ? [...prev.map(d => ({ ...d, es_principal: false })), created]
            : [...prev, created]
        )
      }
      setModalOpen(false)
    } catch (err: any) {
      setAddrError(err.message || 'Error al guardar')
    } finally {
      setAddrSaving(false)
    }
  }

  async function handleDeleteDir(id: number) {
    if (!window.confirm('¿Eliminar esta dirección?')) return
    try {
      await direccionesApi.delete(id)
      setDirecciones(prev => prev.filter(d => d.id !== id))
    } catch {
      // silent
    }
  }

  async function handleSetPrincipal(id: number) {
    try {
      await direccionesApi.setPrincipal(id)
      setDirecciones(prev => prev.map(d => ({ ...d, es_principal: d.id === id })))
    } catch {
      // silent
    }
  }

  if (loading) return (
    <div className="flex items-center justify-center py-20">
      <div className="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin" />
    </div>
  )

  return (
    <div className="max-w-2xl mx-auto space-y-8">
      <h1 className="text-3xl font-bold font-display">Mi Perfil</h1>

      <Card>
        <CardHeader title="Datos personales" subtitle="Actualizá tu información" />
        <form onSubmit={handleSavePerfil} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className={LABEL}>Nombre</label>
              <input className={INPUT} value={nombre} onChange={e => setNombre(e.target.value)} required />
            </div>
            <div>
              <label className={LABEL}>Apellido</label>
              <input className={INPUT} value={apellido} onChange={e => setApellido(e.target.value)} required />
            </div>
          </div>
          <div>
            <label className={LABEL}>Celular</label>
            <input className={INPUT} value={celular} onChange={e => setCelular(e.target.value)} placeholder="Opcional" />
          </div>
          <div>
            <label className={LABEL}>Email</label>
            <input className={`${INPUT} opacity-60 cursor-not-allowed`} value={usuario?.email || ''} disabled />
          </div>
          {saveError && <p className="text-sm text-red-500">{saveError}</p>}
          {saveSuccess && (
            <p className="text-sm text-green-600 flex items-center gap-1">
              <Check size={14} /> Cambios guardados
            </p>
          )}
          <div className="flex justify-end pt-2">
            <Button type="submit" isLoading={saving}>Guardar cambios</Button>
          </div>
        </form>
      </Card>

      <Card>
        <CardHeader
          title="Mis direcciones"
          subtitle="Direcciones de entrega guardadas"
          action={<Button size="sm" icon={Plus} onClick={openAddDir}>Agregar</Button>}
        />
        {direcciones.length === 0 ? (
          <div className="text-center py-8 text-slate-400">
            <MapPin size={40} className="mx-auto mb-3 opacity-40" />
            <p className="text-sm">No tenés direcciones guardadas</p>
          </div>
        ) : (
          <div className="space-y-3">
            {direcciones.map(dir => (
              <div key={dir.id} className="flex items-start justify-between p-4 rounded-2xl bg-slate-50 dark:bg-slate-800/50">
                <div className="flex items-start gap-3">
                  <MapPin size={18} className="text-primary mt-0.5 shrink-0" />
                  <div>
                    <div className="flex items-center gap-2 mb-0.5">
                      {dir.etiqueta && (
                        <span className="text-xs font-bold text-primary bg-primary/10 px-2 py-0.5 rounded-full">
                          {dir.etiqueta}
                        </span>
                      )}
                      {dir.es_principal && (
                        <span className="text-xs font-bold text-amber-600 bg-amber-50 px-2 py-0.5 rounded-full flex items-center gap-1">
                          <Star size={10} fill="currentColor" /> Principal
                        </span>
                      )}
                    </div>
                    <p className="text-sm font-medium text-slate-900 dark:text-white">{dir.linea1}</p>
                    {dir.linea2 && <p className="text-xs text-slate-500">{dir.linea2}</p>}
                    <p className="text-xs text-slate-500">{dir.ciudad}</p>
                  </div>
                </div>
                <div className="flex items-center gap-1 ml-2 shrink-0">
                  {!dir.es_principal && (
                    <button
                      onClick={() => handleSetPrincipal(dir.id)}
                      className="p-1.5 text-slate-400 hover:text-amber-500 transition-colors"
                      title="Marcar como principal"
                    >
                      <Star size={16} />
                    </button>
                  )}
                  <button
                    onClick={() => openEditDir(dir)}
                    className="p-1.5 text-slate-400 hover:text-primary transition-colors"
                    title="Editar"
                  >
                    <Pencil size={16} />
                  </button>
                  <button
                    onClick={() => handleDeleteDir(dir.id)}
                    className="p-1.5 text-slate-400 hover:text-red-500 transition-colors"
                    title="Eliminar"
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </Card>

      <Modal open={modalOpen} title={editingDir ? 'Editar dirección' : 'Nueva dirección'} onClose={() => setModalOpen(false)}>
        <form onSubmit={handleSaveDir} className="space-y-4">
          <div>
            <label className={LABEL}>
              Etiqueta <span className="font-normal text-slate-400">(ej: Casa, Trabajo)</span>
            </label>
            <input
              className={INPUT}
              value={addrForm.etiqueta}
              onChange={e => setAddrForm(p => ({ ...p, etiqueta: e.target.value }))}
              placeholder="Opcional"
            />
          </div>
          <div>
            <label className={LABEL}>Dirección *</label>
            <input
              className={INPUT}
              value={addrForm.linea1}
              onChange={e => setAddrForm(p => ({ ...p, linea1: e.target.value }))}
              placeholder="Calle y número"
              required
            />
          </div>
          <div>
            <label className={LABEL}>Piso / Depto</label>
            <input
              className={INPUT}
              value={addrForm.linea2}
              onChange={e => setAddrForm(p => ({ ...p, linea2: e.target.value }))}
              placeholder="Opcional"
            />
          </div>
          <div>
            <label className={LABEL}>Ciudad *</label>
            <input
              className={INPUT}
              value={addrForm.ciudad}
              onChange={e => setAddrForm(p => ({ ...p, ciudad: e.target.value }))}
              required
            />
          </div>
          {!editingDir && (
            <label className="flex items-center gap-3 cursor-pointer">
              <input
                type="checkbox"
                checked={addrForm.es_principal}
                onChange={e => setAddrForm(p => ({ ...p, es_principal: e.target.checked }))}
                className="w-4 h-4 rounded accent-primary"
              />
              <span className="text-sm text-slate-700 dark:text-slate-300">Marcar como dirección principal</span>
            </label>
          )}
          {addrError && <p className="text-sm text-red-500">{addrError}</p>}
          <div className="flex gap-3 justify-end pt-2">
            <Button type="button" variant="secondary" onClick={() => setModalOpen(false)}>Cancelar</Button>
            <Button type="submit" isLoading={addrSaving}>
              {editingDir ? 'Guardar cambios' : 'Agregar dirección'}
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  )
}
