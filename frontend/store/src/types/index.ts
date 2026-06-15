export interface Categoria {
  id: number
  nombre: string
  descripcion?: string
  parent_id?: number | null
}

export interface Ingrediente {
  id: number
  nombre: string
  unidad_medida: string
  es_alergeno?: boolean
}

export interface Producto {
  id: number
  nombre: string
  precio_base: number
  descripcion?: string
  stock_cantidad: number
  disponible: boolean
  imagenes_url: string[]
  categorias: Categoria[]
  ingredientes: Ingrediente[]
}

export interface DetallePedido {
  id: number
  producto_id: number
  nombre_producto_snap: string
  precio_unitario_snap: number
  cantidad: number
  subtotal_snap: number
  producto?: Producto
}

export interface HistorialEstado {
  id: number
  estado_codigo: string
  created_at: string
  motivo?: string
}

export interface Pedido {
  id: number
  usuario_id: number
  estado_codigo: string
  subtotal: number
  descuento: number
  costo_envio: number
  total: number
  forma_pago_codigo: string
  direccion_id?: number | null
  notas?: string | null
  created_at: string
  updated_at: string
  detalles: DetallePedido[]
  historial: HistorialEstado[]
}

export interface UsuarioLogin {
  email: string
  password: string
}

export interface UsuarioRead {
  id: number
  nombre: string
  apellido: string
  email: string
  celular?: string | null
  created_at: string
  updated_at: string
}

export interface UsuarioCreate {
  nombre: string
  apellido: string
  email: string
  password: string
  celular?: string
}

export interface UsuarioUpdate {
  nombre?: string
  apellido?: string
  celular?: string
}

export interface Direccion {
  id: number
  usuario_id: number
  etiqueta?: string | null
  linea1: string
  linea2?: string | null
  ciudad: string
  es_principal: boolean
}

export interface DireccionCreate {
  etiqueta?: string
  linea1: string
  linea2?: string
  ciudad: string
  es_principal?: boolean
}

export interface DireccionUpdate {
  etiqueta?: string
  linea1?: string
  linea2?: string
  ciudad?: string
}

export interface CategoriaCreate {
  nombre: string
  descripcion?: string
  parent_id?: number | null
}

export interface IngredienteCreate {
  nombre: string
  unidad_medida: string
}

export interface ProductoCreate {
  nombre: string
  precio_base: number
  descripcion?: string
  categoria_ids: number[]
  ingrediente_ids: number[]
  stock_cantidad?: number
  disponible?: boolean
  imagenes_url?: string[]
}

export interface PagoCreate {
  pedido_id: number
  transaction_amount: number
  card_token_id: string
  email: string
  payment_method_id?: string
  installments?: number
  description?: string
}

export interface PagoResponse {
  id: number
  pedido_id: number
  mp_payment_id: number | null
  mp_status: string
  mp_status_detail: string | null
  transaction_amount: number
  payment_method_id: string | null
  payer_email: string | null
  installments: number | null
  external_reference: string
  created_at: string
}
