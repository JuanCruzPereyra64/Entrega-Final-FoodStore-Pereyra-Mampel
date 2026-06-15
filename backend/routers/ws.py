import jwt
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from backend.core.config import settings
from backend.core.ws_manager import ws_manager
from backend.database import get_uow
from backend.uow.unit_of_work import UnitOfWork

router = APIRouter()


@router.websocket("/ws/pedidos")
async def pedidos_ws(websocket: WebSocket, token: str = Query(...)):
    user_id = None
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id = int(payload.get("sub"))
        if not user_id:
            await websocket.close(4001)
            return
    except Exception:
        await websocket.close(4001)
        return

    uow = get_uow()
    with uow:
        user = uow.usuarios.get_by_id(user_id)
        if not user:
            await websocket.close(4001)
            return
        roles = [r.nombre for r in user.roles]
        if "ADMIN" not in roles and "PEDIDOS" not in roles:
            await websocket.close(4001)
            return

    await ws_manager.connect(websocket, "admin")
    try:
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_json({"event": "pong"})
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, "admin")


@router.websocket("/ws/mis-pedidos")
async def mis_pedidos_ws(websocket: WebSocket, token: str = Query(...)):
    user_id = None
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id = int(payload.get("sub"))
    except Exception:
        await websocket.close(4001)
        return

    if not user_id:
        await websocket.close(4001)
        return

    await ws_manager.connect(websocket, f"user_{user_id}")
    try:
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_json({"event": "pong"})
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, f"user_{user_id}")
