from fastapi import status


def test_listar_pedidos_vacio(client, client_headers):
    res = client.get("/api/v1/pedidos/", headers=client_headers)
    assert res.status_code == status.HTTP_200_OK
    assert res.json()["items"] == []


def test_crear_pedido(client, client_headers):
    prod_res = client.get("/api/v1/productos/")
    productos = prod_res.json()["items"]
    prod_id = productos[0]["id"]

    res = client.post("/api/v1/pedidos/", headers=client_headers, json={
        "forma_pago_codigo": "EFECTIVO",
        "detalles": [{"producto_id": prod_id, "cantidad": 1}],
    })
    assert res.status_code == status.HTTP_201_CREATED
    data = res.json()
    assert data["estado_codigo"] == "PENDIENTE"
    assert len(data["detalles"]) == 1
    assert data["detalles"][0]["producto_id"] == prod_id
    assert "id" in data
    assert "total" in data


def test_crear_pedido_stock_insuficiente(client, client_headers):
    prod_res = client.get("/api/v1/productos/")
    productos = prod_res.json()["items"]
    prod_id = productos[0]["id"]

    res = client.post("/api/v1/pedidos/", headers=client_headers, json={
        "forma_pago_codigo": "EFECTIVO",
        "detalles": [{"producto_id": prod_id, "cantidad": 99999}],
    })
    assert res.status_code == status.HTTP_400_BAD_REQUEST


def test_cliente_lista_sus_pedidos(client, client_headers):
    prod_res = client.get("/api/v1/productos/")
    prod_id = prod_res.json()["items"][0]["id"]
    client.post("/api/v1/pedidos/", headers=client_headers, json={
        "forma_pago_codigo": "EFECTIVO",
        "detalles": [{"producto_id": prod_id, "cantidad": 1}],
    })

    res = client.get("/api/v1/pedidos/", headers=client_headers)
    assert res.status_code == status.HTTP_200_OK
    data = res.json()
    assert len(data["items"]) >= 1
    assert data["items"][0]["usuario_id"] is not None


def test_cancelar_pedido_cliente(client, client_headers):
    prod_res = client.get("/api/v1/productos/")
    prod_id = prod_res.json()["items"][0]["id"]
    create_res = client.post("/api/v1/pedidos/", headers=client_headers, json={
        "forma_pago_codigo": "EFECTIVO",
        "detalles": [{"producto_id": prod_id, "cantidad": 1}],
    })
    pedido_id = create_res.json()["id"]

    res = client.delete(f"/api/v1/pedidos/{pedido_id}", headers=client_headers)
    assert res.status_code == status.HTTP_200_OK
    assert res.json()["estado_codigo"] == "CANCELADO"


def test_transicionar_estado(client, client_headers, admin_headers):
    prod_res = client.get("/api/v1/productos/")
    prod_id = prod_res.json()["items"][0]["id"]
    create_res = client.post("/api/v1/pedidos/", headers=client_headers, json={
        "forma_pago_codigo": "EFECTIVO",
        "detalles": [{"producto_id": prod_id, "cantidad": 1}],
    })
    pedido_id = create_res.json()["id"]

    res = client.patch(f"/api/v1/pedidos/{pedido_id}/estado", headers=admin_headers, json={
        "nuevo_estado": "CONFIRMADO",
    })
    assert res.status_code == status.HTTP_200_OK
    assert res.json()["estado_codigo"] == "CONFIRMADO"

    res = client.patch(f"/api/v1/pedidos/{pedido_id}/estado", headers=admin_headers, json={
        "nuevo_estado": "EN_PREP",
    })
    assert res.status_code == status.HTTP_200_OK
    assert res.json()["estado_codigo"] == "EN_PREP"

    res = client.patch(f"/api/v1/pedidos/{pedido_id}/estado", headers=admin_headers, json={
        "nuevo_estado": "ENTREGADO",
    })
    assert res.status_code == status.HTTP_200_OK
    assert res.json()["estado_codigo"] == "ENTREGADO"


def test_transicion_estado_terminal_rechaza(client, client_headers, admin_headers):
    prod_res = client.get("/api/v1/productos/")
    prod_id = prod_res.json()["items"][0]["id"]
    create_res = client.post("/api/v1/pedidos/", headers=client_headers, json={
        "forma_pago_codigo": "EFECTIVO",
        "detalles": [{"producto_id": prod_id, "cantidad": 1}],
    })
    pedido_id = create_res.json()["id"]

    client.patch(f"/api/v1/pedidos/{pedido_id}/estado", headers=admin_headers, json={
        "nuevo_estado": "CANCELADO",
    })

    res = client.patch(f"/api/v1/pedidos/{pedido_id}/estado", headers=admin_headers, json={
        "nuevo_estado": "CONFIRMADO",
    })
    assert res.status_code == status.HTTP_400_BAD_REQUEST


def test_cliente_no_puede_transicionar(client, client_headers):
    prod_res = client.get("/api/v1/productos/")
    prod_id = prod_res.json()["items"][0]["id"]
    create_res = client.post("/api/v1/pedidos/", headers=client_headers, json={
        "forma_pago_codigo": "EFECTIVO",
        "detalles": [{"producto_id": prod_id, "cantidad": 1}],
    })
    pedido_id = create_res.json()["id"]

    res = client.patch(f"/api/v1/pedidos/{pedido_id}/estado", headers=client_headers, json={
        "nuevo_estado": "CONFIRMADO",
    })
    assert res.status_code == status.HTTP_403_FORBIDDEN
