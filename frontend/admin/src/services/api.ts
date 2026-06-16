import axios from 'axios'
import { useAuthStore } from '../store/useAuthStore'

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  withCredentials: true,
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
    const isMeRoute = error.config?.url?.includes('/api/v1/auth/me')
    const status = error.response?.status
    const detail = error.response?.data?.detail
    const isTokenInvalid = status === 403 && detail === 'Token invalido'
    if (!isLoginRoute && !isMeRoute && (status === 401 || isTokenInvalid)) {
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
    request<{access_token: string, refresh_token: string, token_type: string, expires_in: number}>('/api/v1/auth/login', { method: 'POST', body: JSON.stringify(data) }),
  logout: () => request<{message: string}>('/api/v1/auth/logout', { method: 'POST' }),
  me: () => request<{id: number, email: string, roles: {nombre: string}[]}>('/api/v1/auth/me'),
}

export const pedidosApi = {
  getAll: () => request<import('../types').Pedido[]>('/api/v1/pedidos/'),
  updateEstado: (id: number, estado_codigo: string) =>
    request<import('../types').Pedido>(`/api/v1/pedidos/${id}/estado`, { method: 'PATCH', body: JSON.stringify({ nuevo_estado: estado_codigo }) }),
}

export const unidadesMedidaApi = {
  getAll: () => request<import('../types').UnidadMedida[]>('/api/v1/unidades-medida/'),
  create: (data: import('../types').UnidadMedidaCreate) =>
    request<import('../types').UnidadMedida>('/api/v1/unidades-medida/', { method: 'POST', body: JSON.stringify(data) }),
  remove: (id: number) => request<void>(`/api/v1/unidades-medida/${id}`, { method: 'DELETE' }),
}

export const uploadApi = {
  uploadImage: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    const res = await apiClient.post<{url: string}>('/api/v1/uploads/imagen', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    return res.data;
  }
}

export const stockApi = {
  getMovimientos: (ingredienteId?: number) => {
    const params = ingredienteId ? `?ingrediente_id=${ingredienteId}` : ''
    return request<import('../types').MovimientoStock[]>(`/api/v1/stock/movimientos${params}`)
  }
}

export const estadisticasApi = {
  resumen: () => request<import('../types').ResumenResponse>('/api/v1/estadisticas/resumen'),
  ventas: (desde: string, hasta: string, agrupacion = 'day') =>
    request<import('../types').VentasPeriodoItem[]>(`/api/v1/estadisticas/ventas?desde=${desde}&hasta=${hasta}&agrupacion=${agrupacion}`),
  productosTop: (limit = 5) => request<import('../types').ProductoTopItem[]>(`/api/v1/estadisticas/productos-top?limit=${limit}`),
  pedidosPorEstado: () => request<import('../types').PedidosEstadoItem[]>('/api/v1/estadisticas/pedidos-por-estado'),
  ingresos: (desde?: string, hasta?: string) => {
    let path = '/api/v1/estadisticas/ingresos'
    const params: string[] = []
    if (desde) params.push(`desde=${desde}`)
    if (hasta) params.push(`hasta=${hasta}`)
    if (params.length) path += '?' + params.join('&')
    return request<import('../types').IngresosResponse[]>(path)
  }
}
