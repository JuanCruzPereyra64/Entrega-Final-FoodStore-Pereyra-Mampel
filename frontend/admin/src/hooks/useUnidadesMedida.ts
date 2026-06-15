import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import type { UnidadMedida } from '../types'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export function useUnidadesMedida() {
  return useQuery({
    queryKey: ['unidades-medida'],
    queryFn: async (): Promise<UnidadMedida[]> => {
      const res = await fetch(`${API_URL}/api/v1/unidades-medida`)
      if (!res.ok) throw new Error('Error al cargar unidades de medida')
      const data = await res.json()
      return Array.isArray(data?.items) ? data.items : data
    }
  })
}

export function useCreateUnidadMedida() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: async (data: { nombre: string }) => {
      const res = await fetch(`${API_URL}/api/v1/unidades-medida/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
      if (!res.ok) {
        const err = await res.json()
        throw new Error(err.detail || 'Error al crear unidad de medida')
      }
      return res.json()
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['unidades-medida'] })
    }
  })
}

export function useDeleteUnidadMedida() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: async (id: number) => {
      const res = await fetch(`${API_URL}/api/v1/unidades-medida/${id}`, {
        method: 'DELETE'
      })
      if (!res.ok) {
        const err = await res.json()
        throw new Error(err.detail || 'Error al eliminar unidad de medida')
      }
      return res.json()
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['unidades-medida'] })
    }
  })
}
