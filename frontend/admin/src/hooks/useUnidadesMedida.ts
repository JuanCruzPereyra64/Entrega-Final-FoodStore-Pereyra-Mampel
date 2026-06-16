import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import type { UnidadMedida, UnidadMedidaCreate } from '../types'
import { unidadesMedidaApi } from '../services/api'

export function useUnidadesMedida() {
  return useQuery({
    queryKey: ['unidades-medida'],
    queryFn: (): Promise<UnidadMedida[]> => unidadesMedidaApi.getAll(),
  })
}

export function useCreateUnidadMedida() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: async (data: UnidadMedidaCreate) => {
      const res = await unidadesMedidaApi.create(data)
      return res
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
      await unidadesMedidaApi.remove(id)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['unidades-medida'] })
    }
  })
}
