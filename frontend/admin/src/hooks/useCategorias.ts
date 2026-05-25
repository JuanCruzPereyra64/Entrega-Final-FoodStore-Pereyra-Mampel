import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { categoriasApi } from '../services/api'
import type { CategoriaCreate } from '../types'

export function useCategorias() {
  return useQuery({
    queryKey: ['categorias'],
    queryFn: categoriasApi.getAll,
  })
}

export function useCreateCategoria() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data: CategoriaCreate) => categoriasApi.create(data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['categorias'] }),
  })
}

export function useUpdateCategoria() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<CategoriaCreate> }) =>
      categoriasApi.update(id, data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['categorias'] }),
  })
}

export function useDeleteCategoria() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (id: number) => categoriasApi.delete(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['categorias'] }),
  })
}
