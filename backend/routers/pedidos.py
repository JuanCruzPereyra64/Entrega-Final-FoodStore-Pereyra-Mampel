from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from backend.database import get_uow
from backend.schemas.pedido import PedidoCreate, PedidoReadConDetalles
from backend.services import pedido_service
from backend.uow.unit_of_work import UnitOfWork
from backend.models.usuario import Usuario
from backend.api.deps import get_current_user

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


@router.post("/", response_model=PedidoReadConDetalles, status_code=status.HTTP_201_CREATED)
def crear_pedido(
    data: PedidoCreate, 
    current_user: Usuario = Depends(get_current_user), 
    uow: UnitOfWork = Depends(get_uow)
):
    with uow:
        return pedido_service.crear_pedido(uow, current_user.id, data)


class TransicionEstado(BaseModel):
    nuevo_estado_codigo: str
    motivo: str = None


@router.put("/{pedido_id}/estado", response_model=PedidoReadConDetalles)
def transicionar_estado(
    pedido_id: int, 
    data: TransicionEstado, 
    current_user: Usuario = Depends(get_current_user), 
    uow: UnitOfWork = Depends(get_uow)
):
    with uow:
        return pedido_service.transicionar_estado(uow, pedido_id, data.nuevo_estado_codigo, current_user.id, data.motivo)
