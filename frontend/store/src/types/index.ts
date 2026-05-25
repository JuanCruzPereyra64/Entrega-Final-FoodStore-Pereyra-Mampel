export interface Categoria {
  id: number
  nombre: string
  descripcion?: string
}

export interface Ingrediente {
  id: number
  nombre: string
  unidad_medida: string
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

export interface CategoriaCreate {
  nombre: string
  descripcion?: string
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
