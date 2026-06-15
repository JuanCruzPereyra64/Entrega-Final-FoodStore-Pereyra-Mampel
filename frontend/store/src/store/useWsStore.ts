import { create } from 'zustand'

interface WsState {
  isConnected: boolean
  lastEvent: object | null
  reconnectAttempts: number
  setConnected: (connected: boolean) => void
  setLastEvent: (event: object) => void
  incrementReconnect: () => void
  resetReconnect: () => void
}

export const useWsStore = create<WsState>((set) => ({
  isConnected: false,
  lastEvent: null,
  reconnectAttempts: 0,
  setConnected: (connected) => set({ isConnected: connected }),
  setLastEvent: (event) => set({ lastEvent: event }),
  incrementReconnect: () => set((s) => ({ reconnectAttempts: s.reconnectAttempts + 1 })),
  resetReconnect: () => set({ reconnectAttempts: 0 }),
}))
