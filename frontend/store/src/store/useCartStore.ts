import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface CartItem {
  id: number
  producto_id: number
  nombre: string
  precio: number
  cantidad: number
  imagen_url?: string
}

interface CartState {
  items: CartItem[]
  addItem: (item: CartItem) => void
  removeItem: (id: number) => void
  clearCart: () => void
  updateQuantity: (producto_id: number, cantidad: number) => void
  getTotal: () => number
}

export const useCartStore = create<CartState>()(
  persist(
    (set, get) => ({
      items: [],
      addItem: (item) =>
        set((state) => {
          const existing = state.items.find((i) => i.producto_id === item.producto_id)
          if (existing) {
            return {
              items: state.items.map((i) =>
                i.producto_id === item.producto_id ? { ...i, cantidad: i.cantidad + item.cantidad } : i
              ),
            }
          }
          return { items: [...state.items, item] }
        }),
      removeItem: (id) =>
        set((state) => ({ items: state.items.filter((i) => i.producto_id !== id) })),
      clearCart: () => set({ items: [] }),
      updateQuantity: (producto_id, cantidad) =>
        set((state) => ({
          items: state.items.map((i) =>
            i.producto_id === producto_id ? { ...i, cantidad } : i
          ),
        })),
      getTotal: () => {
        return get().items.reduce((total, item) => total + item.precio * item.cantidad, 0)
      },
    }),
    {
      name: 'cart-storage',
    }
  )
)
