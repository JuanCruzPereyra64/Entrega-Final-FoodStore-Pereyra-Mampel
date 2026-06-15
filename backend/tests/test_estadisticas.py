from fastapi import status


def test_resumen_kpis_admin(client, admin_headers):
    res = client.get("/api/v1/estadisticas/resumen", headers=admin_headers)
    assert res.status_code == status.HTTP_200_OK
    data = res.json()
    assert "ventas_hoy" in data
    assert "ticket_promedio" in data
    assert "pedidos_activos" in data
    assert "total_mes_actual" in data


def test_ventas_periodo_admin(client, admin_headers):
    res = client.get("/api/v1/estadisticas/ventas?desde=2024-01-01&hasta=2026-12-31&agrupacion=month", headers=admin_headers)
    assert res.status_code == status.HTTP_200_OK
    assert isinstance(res.json(), list)


def test_productos_top_admin(client, admin_headers):
    res = client.get("/api/v1/estadisticas/productos-top?limit=5", headers=admin_headers)
    assert res.status_code == status.HTTP_200_OK
    assert isinstance(res.json(), list)


def test_pedidos_por_estado_admin(client, admin_headers):
    res = client.get("/api/v1/estadisticas/pedidos-por-estado", headers=admin_headers)
    assert res.status_code == status.HTTP_200_OK
    assert isinstance(res.json(), list)


def test_ingresos_admin(client, admin_headers):
    res = client.get("/api/v1/estadisticas/ingresos", headers=admin_headers)
    assert res.status_code == status.HTTP_200_OK
    assert isinstance(res.json(), list)


def test_estadisticas_requiere_admin(client, client_headers):
    for path in ["/api/v1/estadisticas/resumen", "/api/v1/estadisticas/pedidos-por-estado"]:
        res = client.get(path, headers=client_headers)
        assert res.status_code == status.HTTP_403_FORBIDDEN
