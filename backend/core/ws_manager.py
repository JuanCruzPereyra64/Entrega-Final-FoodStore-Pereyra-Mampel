import asyncio
import json
from collections import defaultdict
from datetime import datetime, timezone
from fastapi import WebSocket


class WSManager:
    def __init__(self):
        self._connections: dict[str, set[WebSocket]] = defaultdict(set)

    def set_loop(self, loop: asyncio.AbstractEventLoop):
        self._loop = loop

    async def connect(self, ws: WebSocket, channel: str):
        await ws.accept()
        self._connections[channel].add(ws)

    def disconnect(self, ws: WebSocket, channel: str):
        self._connections[channel].discard(ws)

    def _build_evento(
        self,
        event_type: str,
        pedido_id: int,
        estado_anterior: str = None,
        estado_nuevo: str = None,
        usuario_id: int = None,
        motivo: str = None,
    ) -> dict:
        return {
            "event": event_type,
            "pedido_id": pedido_id,
            "estado_anterior": estado_anterior,
            "estado_nuevo": estado_nuevo,
            "usuario_id": usuario_id,
            "motivo": motivo,
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }

    def broadcast_pedido(self, pedido_id: int, evento: dict):
        channels = [str(pedido_id), "admin"]
        for ch in channels:
            for ws in list(self._connections.get(ch, set())):
                try:
                    asyncio.run_coroutine_threadsafe(
                        ws.send_json(evento), self._loop
                    )
                except Exception:
                    self._connections[ch].discard(ws)

    def broadcast_to_user(self, user_id: int, evento: dict):
        ch = f"user_{user_id}"
        for ws in list(self._connections.get(ch, set())):
            try:
                asyncio.run_coroutine_threadsafe(
                    ws.send_json(evento), self._loop
                )
            except Exception:
                self._connections[ch].discard(ws)


ws_manager = WSManager()
