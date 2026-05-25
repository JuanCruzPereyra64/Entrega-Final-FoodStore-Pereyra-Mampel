import axios from 'axios'
import { useAuthStore } from '../store/useAuthStore'

export const apiClient = axios.create({
  baseURL: 'http://localhost:8000',
  withCredentials: true,
})

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const isLoginRoute = error.config?.url?.includes('/usuarios/login')
    if (error.response?.status === 401 && !isLoginRoute) {
      useAuthStore.getState().logout()
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  try {
    const res = await apiClient.request<T>({
      url: path,
      method: options?.method || 'GET',
      data: options?.body ? JSON.parse(options.body as string) : undefined,
      headers: options?.headers as Record<string, string>,
    })
    return res.data
  } catch (error: any) {
    let msg = 'Error en la petición'
    if (error.response?.data?.detail) {
      if (typeof error.response.data.detail === 'string') {
        msg = error.response.data.detail
      } else if (Array.isArray(error.response.data.detail)) {
        msg = error.response.data.detail.map((e: any) => e.msg).join(', ')
      }
    }
    throw new Error(msg)
  }
}

export const categoriasApi = {
  getAll: () => request<import('../types').Categoria[]>('/categorias/'),
  getById: (id: number) => request<import('../types').Categoria>(`/categorias/${id}`),
  create: (data: import('../types').CategoriaCreate) =>
    request<import('../types').Categoria>('/categorias/', { method: 'POST', body: JSON.stringify(data) }),
  update: (id: number, data: Partial<import('../types').CategoriaCreate>) =>
    request<import('../types').Categoria>(`/categorias/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  delete: (id: number) => request<void>(`/categorias/${id}`, { method: 'DELETE' }),
}

export const ingredientesApi = {
  getAll: () => request<import('../types').Ingrediente[]>('/ingredientes/'),
  getById: (id: number) => request<import('../types').Ingrediente>(`/ingredientes/${id}`),
  create: (data: import('../types').IngredienteCreate) =>
    request<import('../types').Ingrediente>('/ingredientes/', { method: 'POST', body: JSON.stringify(data) }),
  update: (id: number, data: Partial<import('../types').IngredienteCreate>) =>
    request<import('../types').Ingrediente>(`/ingredientes/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  delete: (id: number) => request<void>(`/ingredientes/${id}`, { method: 'DELETE' }),
}

export const productosApi = {
  getAll: (categoriaId?: number) => {
    const params = categoriaId ? `?categoria_id=${categoriaId}` : ''
    return request<import('../types').Producto[]>(`/productos/${params}`)
  },
  getById: (id: number) => request<import('../types').Producto>(`/productos/${id}`),
  create: (data: import('../types').ProductoCreate) =>
    request<import('../types').Producto>('/productos/', { method: 'POST', body: JSON.stringify(data) }),
  update: (id: number, data: Partial<import('../types').ProductoCreate>) =>
    request<import('../types').Producto>(`/productos/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  delete: (id: number) => request<void>(`/productos/${id}`, { method: 'DELETE' }),
  addIngrediente: (productoId: number, ingredienteId: number) =>
    request<import('../types').Producto>(`/productos/${productoId}/ingredientes/${ingredienteId}`, { method: 'POST' }),
  removeIngrediente: (productoId: number, ingredienteId: number) =>
    request<import('../types').Producto>(`/productos/${productoId}/ingredientes/${ingredienteId}`, { method: 'DELETE' }),
}

export const authApi = {
  login: (data: import('../types').UsuarioLogin) =>
    request<{message: string, rol: string[]}>('/usuarios/login', { method: 'POST', body: JSON.stringify(data) }),
  logout: () => request<{message: string}>('/usuarios/logout', { method: 'POST' }),
  me: () => request<import('../types').UsuarioRead>('/usuarios/me')
}

export const pedidosApi = {
  getAll: () => request<import('../types').Pedido[]>('/pedidos/'),
  create: (data: any) => request<import('../types').Pedido>('/pedidos/', { method: 'POST', body: JSON.stringify(data) }),
}
