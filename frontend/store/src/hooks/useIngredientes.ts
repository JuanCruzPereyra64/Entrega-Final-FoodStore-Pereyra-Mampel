import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { ingredientesApi } from '../services/api'
import type { IngredienteCreate } from '../types'

export function useIngredientes() {
  return useQuery({
    queryKey: ['ingredientes'],
    queryFn: ingredientesApi.getAll,
  })
}

export function useCreateIngrediente() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data: IngredienteCreate) => ingredientesApi.create(data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['ingredientes'] }),
  })
}

export function useUpdateIngrediente() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<IngredienteCreate> }) =>
      ingredientesApi.update(id, data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['ingredientes'] }),
  })
}

export function useDeleteIngrediente() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (id: number) => ingredientesApi.delete(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['ingredientes'] }),
  })
}
