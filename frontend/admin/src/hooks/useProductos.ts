import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { productosApi } from '../services/api'
import type { ProductoCreate } from '../types'

export function useProductos(categoriaId?: number) {
  return useQuery({
    queryKey: ['productos', categoriaId],
    queryFn: () => productosApi.getAll(categoriaId),
  })
}

export function useProducto(id: number) {
  return useQuery({
    queryKey: ['productos', id],
    queryFn: () => productosApi.getById(id),
  })
}

export function useCreateProducto() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data: ProductoCreate) => productosApi.create(data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['productos'] }),
  })
}

export function useUpdateProducto() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<ProductoCreate> }) =>
      productosApi.update(id, data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['productos'] }),
  })
}

export function useDeleteProducto() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (id: number) => productosApi.delete(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['productos'] }),
  })
}

export function useAddIngrediente() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ productoId, ingredienteId }: { productoId: number; ingredienteId: number }) =>
      productosApi.addIngrediente(productoId, ingredienteId),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['productos'] }),
  })
}

export function useRemoveIngrediente() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ productoId, ingredienteId }: { productoId: number; ingredienteId: number }) =>
      productosApi.removeIngrediente(productoId, ingredienteId),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['productos'] }),
  })
}
