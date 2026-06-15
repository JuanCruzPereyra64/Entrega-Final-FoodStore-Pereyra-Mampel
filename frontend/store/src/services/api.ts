import axios from 'axios'
import { useAuthStore } from '../store/useAuthStore'

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
})

apiClient.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

apiClient.interceptors.response.use(
  (response) => {
    if (response.data && typeof response.data === 'object' && Array.isArray(response.data.items)) {
      response.data = response.data.items
    }
    return response
  },
  (error) => {
    const isLoginRoute = error.config?.url?.includes('/api/v1/auth/login')
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
  getAll: () => request<import('../types').Categoria[]>('/api/v1/categorias/'),
  getById: (id: number) => request<import('../types').Categoria>(`/api/v1/categorias/${id}`),
  create: (data: import('../types').CategoriaCreate) =>
    request<import('../types').Categoria>('/api/v1/categorias/', { method: 'POST', body: JSON.stringify(data) }),
  update: (id: number, data: Partial<import('../types').CategoriaCreate>) =>
    request<import('../types').Categoria>(`/api/v1/categorias/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  delete: (id: number) => request<void>(`/api/v1/categorias/${id}`, { method: 'DELETE' }),
}

export const ingredientesApi = {
  getAll: () => request<import('../types').Ingrediente[]>('/api/v1/ingredientes/'),
  getById: (id: number) => request<import('../types').Ingrediente>(`/api/v1/ingredientes/${id}`),
  create: (data: import('../types').IngredienteCreate) =>
    request<import('../types').Ingrediente>('/api/v1/ingredientes/', { method: 'POST', body: JSON.stringify(data) }),
  update: (id: number, data: Partial<import('../types').IngredienteCreate>) =>
    request<import('../types').Ingrediente>(`/api/v1/ingredientes/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  delete: (id: number) => request<void>(`/api/v1/ingredientes/${id}`, { method: 'DELETE' }),
}

export const productosApi = {
  getAll: (categoriaId?: number) => {
    const params = categoriaId ? `?categoria_id=${categoriaId}` : ''
    return request<import('../types').Producto[]>(`/api/v1/productos/${params}`)
  },
  getById: (id: number) => request<import('../types').Producto>(`/api/v1/productos/${id}`),
  create: (data: import('../types').ProductoCreate) =>
    request<import('../types').Producto>('/api/v1/productos/', { method: 'POST', body: JSON.stringify(data) }),
  update: (id: number, data: Partial<import('../types').ProductoCreate>) =>
    request<import('../types').Producto>(`/api/v1/productos/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  delete: (id: number) => request<void>(`/api/v1/productos/${id}`, { method: 'DELETE' }),
  addIngrediente: (productoId: number, ingredienteId: number) =>
    request<import('../types').Producto>(`/api/v1/productos/${productoId}/ingredientes/${ingredienteId}`, { method: 'POST' }),
  removeIngrediente: (productoId: number, ingredienteId: number) =>
    request<import('../types').Producto>(`/api/v1/productos/${productoId}/ingredientes/${ingredienteId}`, { method: 'DELETE' }),
}

export const authApi = {
  login: (data: import('../types').UsuarioLogin) =>
    request<{message: string, rol: string[], access_token: string}>('/api/v1/auth/login', { method: 'POST', body: JSON.stringify(data) }),
  logout: () => request<{message: string}>('/api/v1/auth/logout', { method: 'POST' }),
  me: () => request<import('../types').UsuarioRead>('/api/v1/auth/me'),
  register: (data: import('../types').UsuarioCreate) =>
    request<import('../types').UsuarioRead>('/api/v1/auth/registro', { method: 'POST', body: JSON.stringify(data) }),
  updateMe: (data: import('../types').UsuarioUpdate) =>
    request<import('../types').UsuarioRead>('/api/v1/auth/me', { method: 'PUT', body: JSON.stringify(data) }),
}

export const direccionesApi = {
  getAll: () => request<import('../types').Direccion[]>('/api/v1/direcciones/'),
  create: (data: import('../types').DireccionCreate) =>
    request<import('../types').Direccion>('/api/v1/direcciones/', { method: 'POST', body: JSON.stringify(data) }),
  update: (id: number, data: import('../types').DireccionUpdate) =>
    request<import('../types').Direccion>(`/api/v1/direcciones/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  delete: (id: number) => request<void>(`/api/v1/direcciones/${id}`, { method: 'DELETE' }),
  setPrincipal: (id: number) =>
    request<import('../types').Direccion>(`/api/v1/direcciones/${id}/principal`, { method: 'PATCH' }),
}

export const pedidosApi = {
  getAll: () => request<import('../types').Pedido[]>('/api/v1/pedidos/'),
  create: (data: any) => request<import('../types').Pedido>('/api/v1/pedidos/', { method: 'POST', body: JSON.stringify(data) }),
  cancelar: (id: number) => request<import('../types').Pedido>(`/api/v1/pedidos/${id}`, { method: 'DELETE' }),
}

export const pagosApi = {
  getPublicKey: () => request<{ public_key: string }>('/api/v1/pagos/public-key'),
  crear: (data: import('../types').PagoCreate) =>
    request<import('../types').PagoResponse>('/api/v1/pagos/crear', { method: 'POST', body: JSON.stringify(data) }),
  getByPedido: (pedidoId: number) =>
    request<import('../types').PagoResponse>(`/api/v1/pagos/${pedidoId}`),
}
