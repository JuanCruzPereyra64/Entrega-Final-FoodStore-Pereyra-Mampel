from datetime import date
from fastapi import APIRouter, Depends, Query
from backend.database import get_uow
from backend.services import estadisticas_service
from backend.uow.unit_of_work import UnitOfWork
from backend.models.usuario import Usuario
from backend.api.deps import check_role
from backend.schemas.estadisticas import (
    VentasPeriodoItem, ProductoTopItem, PedidosEstadoItem,
    ResumenResponse, IngresosResponse,
)

router = APIRouter(prefix="/api/v1/estadisticas", tags=["Estadisticas"])

@router.get("/ventas", response_model=list[VentasPeriodoItem])
def ventas_periodo(
    desde: date = Query(...),
    hasta: date = Query(...),
    agrupacion: str = Query("day", pattern="^(day|week|month)$"),
    current_user: Usuario = Depends(check_role(["ADMIN"])),
    uow: UnitOfWork = Depends(get_uow),
):
    with uow:
        return estadisticas_service.get_ventas_periodo(uow, desde, hasta, agrupacion)

@router.get("/productos-top", response_model=list[ProductoTopItem])
def productos_top(
    limit: int = Query(10, ge=1, le=100),
    current_user: Usuario = Depends(check_role(["ADMIN"])),
    uow: UnitOfWork = Depends(get_uow),
):
    with uow:
        return estadisticas_service.get_productos_top(uow, limit)

@router.get("/pedidos-por-estado", response_model=list[PedidosEstadoItem])
def pedidos_por_estado(
    current_user: Usuario = Depends(check_role(["ADMIN"])),
    uow: UnitOfWork = Depends(get_uow),
):
    with uow:
        return estadisticas_service.get_pedidos_por_estado(uow)

@router.get("/resumen", response_model=ResumenResponse)
def resumen_kpis(
    current_user: Usuario = Depends(check_role(["ADMIN"])),
    uow: UnitOfWork = Depends(get_uow),
):
    with uow:
        return estadisticas_service.get_resumen_kpis(uow)

@router.get("/ingresos", response_model=list[IngresosResponse])
def ingresos_forma_pago(
    desde: date | None = Query(None),
    hasta: date | None = Query(None),
    current_user: Usuario = Depends(check_role(["ADMIN"])),
    uow: UnitOfWork = Depends(get_uow),
):
    with uow:
        return estadisticas_service.get_ingresos_por_forma_pago(uow, desde, hasta)
