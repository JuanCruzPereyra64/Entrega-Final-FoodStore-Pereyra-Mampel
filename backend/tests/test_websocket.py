from fastapi.testclient import TestClient
from backend.main import app


def test_ws_mis_pedidos_autenticado(client, client_headers):
    token = client_headers["Authorization"].replace("Bearer ", "")
    with client.websocket_connect(f"/ws/mis-pedidos?token={token}") as ws:
        ws.send_text("ping")
        data = ws.receive_json()
        assert data == {"event": "pong"}


def test_ws_admin_pedidos_autenticado(client, admin_headers):
    token = admin_headers["Authorization"].replace("Bearer ", "")
    with client.websocket_connect(f"/ws/pedidos?token={token}") as ws:
        ws.send_text("ping")
        data = ws.receive_json()
        assert data == {"event": "pong"}
