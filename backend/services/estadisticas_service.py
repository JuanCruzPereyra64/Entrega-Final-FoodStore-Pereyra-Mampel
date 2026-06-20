from datetime import date
from backend.uow.unit_of_work import UnitOfWork
from backend.schemas.estadisticas import (
    VentasPeriodoItem, ProductoTopItem, PedidosEstadoItem,
    ResumenResponse, IngresosResponse,
)


def get_ventas_periodo(uow: UnitOfWork, desde: date, hasta: date, agrupacion: str = "day") -> list[VentasPeriodoItem]:
    return uow.estadisticas.get_ventas_periodo(desde, hasta, agrupacion)


def get_productos_top(uow: UnitOfWork, limit: int = 10) -> list[ProductoTopItem]:
    return uow.estadisticas.get_productos_top(limit)


def get_pedidos_por_estado(uow: UnitOfWork) -> list[PedidosEstadoItem]:
    return uow.estadisticas.get_pedidos_por_estado()


def get_resumen_kpis(uow: UnitOfWork) -> ResumenResponse:
    return uow.estadisticas.get_resumen_kpis()


def get_ingresos_por_forma_pago(uow: UnitOfWork, desde: date | None = None, hasta: date | None = None) -> list[IngresosResponse]:
    return uow.estadisticas.get_ingresos_por_forma_pago(desde, hasta)
