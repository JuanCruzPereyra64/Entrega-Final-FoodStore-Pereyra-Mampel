import { useEffect, useRef, useCallback, useState } from 'react'
import { toast } from 'sonner'
import { useQueryClient } from '@tanstack/react-query'
import { useAuthStore } from '../store/useAuthStore'

const WS_URL = 'ws://localhost:8000/ws/pedidos'
const RECONNECT_DELAY = 3000
const PING_INTERVAL = 25000

export function useAdminOrdersFeed() {
  const qc = useQueryClient()
  const token = useAuthStore(s => s.token)
  const wsRef = useRef<WebSocket | null>(null)
  const reconnectRef = useRef<ReturnType<typeof setTimeout> | null>(null)
  const pingRef = useRef<ReturnType<typeof setInterval> | null>(null)
  const [isConnected, setIsConnected] = useState(false)

  const connect = useCallback(() => {
    if (!token) return

    const ws = new WebSocket(`${WS_URL}?token=${token}`)
    wsRef.current = ws

    ws.onopen = () => {
      setIsConnected(true)
      pingRef.current = setInterval(() => {
        if (ws.readyState === WebSocket.OPEN) ws.send('ping')
      }, PING_INTERVAL)
    }

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        if (data.event === 'pong') return

        qc.invalidateQueries({ queryKey: ['pedidos'] })
      } catch {
        // ignore parse errors
      }
    }

    ws.onclose = () => {
      setIsConnected(false)
      if (pingRef.current) clearInterval(pingRef.current)
      reconnectRef.current = setTimeout(connect, RECONNECT_DELAY)
    }

    ws.onerror = () => {
      ws.close()
    }
  }, [token, qc])

  useEffect(() => {
    connect()
    return () => {
      if (reconnectRef.current) clearTimeout(reconnectRef.current)
      if (pingRef.current) clearInterval(pingRef.current)
      if (wsRef.current) wsRef.current.close()
    }
  }, [connect])

  return isConnected
}
