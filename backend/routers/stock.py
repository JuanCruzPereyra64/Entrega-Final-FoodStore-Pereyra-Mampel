from typing import Annotated
from fastapi import APIRouter, Depends, Query
from backend.database import get_uow
from backend.schemas.movimiento_stock import MovimientoStockRead
from backend.services import movimiento_stock_service
from backend.uow.unit_of_work import UnitOfWork
from backend.models.usuario import Usuario
from backend.api.deps import check_role

router = APIRouter(prefix="/api/v1/stock", tags=["Stock"])

@router.get("/movimientos", response_model=list[MovimientoStockRead])
def get_movimientos(
    ingrediente_id: Annotated[int, Query()] = None,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
    current_user: Usuario = Depends(check_role(["ADMIN", "STOCK"])),
    uow: UnitOfWork = Depends(get_uow)
):
    with uow:
        movimientos = movimiento_stock_service.get_historial(uow, offset, limit, ingrediente_id)
        
        resultado = []
        for mov in movimientos:
            mov_read = MovimientoStockRead.model_validate(mov)
            if mov.ingrediente:
                mov_read.ingrediente_nombre = mov.ingrediente.nombre
            if mov.usuario:
                mov_read.usuario_nombre = f"{mov.usuario.nombre} {mov.usuario.apellido}".strip()
            resultado.append(mov_read)
            
        return resultado
