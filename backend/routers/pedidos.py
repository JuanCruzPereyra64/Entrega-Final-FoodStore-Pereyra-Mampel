from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from backend.database import get_uow
from backend.schemas.pedido import PedidoCreate, PedidoReadConDetalles
from backend.services import pedido_service
from backend.uow.unit_of_work import UnitOfWork
from backend.models.usuario import Usuario
from backend.api.deps import check_role

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

@router.get("/", response_model=list[PedidoReadConDetalles])
def get_pedidos(
    current_user: Usuario = Depends(check_role(["ADMIN", "STOCK", "PEDIDOS"])), 
    uow: UnitOfWork = Depends(get_uow)
):
    with uow:
        pedidos = pedido_service.get_all(uow)
        for p in pedidos:
            _ = p.detalles
            _ = p.historial
        return pedidos

@router.post("/", response_model=PedidoReadConDetalles, status_code=status.HTTP_201_CREATED)
def crear_pedido(
    data: PedidoCreate, 
    current_user: Usuario = Depends(check_role(["CLIENT", "ADMIN"])), 
    uow: UnitOfWork = Depends(get_uow)
):
    with uow:
        pedido = pedido_service.crear_pedido(uow, current_user.id, data)
        _ = pedido.detalles
        _ = pedido.historial
        return pedido

class TransicionEstado(BaseModel):
    nuevo_estado_codigo: str
    motivo: str = None

@router.put("/{pedido_id}/estado", response_model=PedidoReadConDetalles)
def transicionar_estado(
    pedido_id: int, 
    data: TransicionEstado, 
    current_user: Usuario = Depends(check_role(["ADMIN", "STOCK", "PEDIDOS"])), 
    uow: UnitOfWork = Depends(get_uow)
):
    with uow:
        pedido = pedido_service.transicionar_estado(uow, pedido_id, data.nuevo_estado_codigo, current_user.id, data.motivo)
        _ = pedido.detalles
        _ = pedido.historial
        return pedido
