from typing import Annotated
from fastapi import APIRouter, Depends, Query, status
from backend.database import get_uow
from backend.schemas.pedido import PedidoCreate, PedidoReadConDetalles, AvanzarEstadoRequest
from backend.schemas.historial_estado_pedido import HistorialEstadoPedidoRead
from backend.schemas.pagination import PaginatedResponse
from backend.services import pedido_service
from backend.uow.unit_of_work import UnitOfWork
from backend.models.usuario import Usuario
from backend.api.deps import check_role
from backend.core.ws_manager import ws_manager

router = APIRouter(prefix="/api/v1/pedidos", tags=["Pedidos"])

@router.get("/", response_model=PaginatedResponse[PedidoReadConDetalles])
def get_pedidos(
    current_user: Usuario = Depends(check_role(["CLIENT", "ADMIN", "PEDIDOS"])), 
    uow: UnitOfWork = Depends(get_uow),
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 20,
):
    with uow:
        if any(r.nombre == "CLIENT" for r in current_user.roles):
            pedidos = pedido_service.get_by_usuario(uow, current_user.id)
        else:
            pedidos = pedido_service.get_all(uow)
            
        for p in pedidos:
            _ = p.detalles
            if p.detalles:
                for d in p.detalles:
                    _ = d.producto
            _ = p.historial
        return PaginatedResponse.create(items=pedidos, total=len(pedidos), page=page, size=size)

@router.post("/", response_model=PedidoReadConDetalles, status_code=status.HTTP_201_CREATED)
def crear_pedido(
    data: PedidoCreate, 
    current_user: Usuario = Depends(check_role(["CLIENT"])), 
    uow: UnitOfWork = Depends(get_uow)
):
    with uow:
        pedido = pedido_service.crear_pedido(uow, current_user.id, data)
        _ = pedido.detalles
        if pedido.detalles:
            for d in pedido.detalles:
                _ = d.producto
        _ = pedido.historial
    return pedido


@router.get("/{pedido_id}", response_model=PedidoReadConDetalles)
def get_pedido(
    pedido_id: int,
    current_user: Usuario = Depends(check_role(["CLIENT", "ADMIN", "PEDIDOS"])),
    uow: UnitOfWork = Depends(get_uow)
):
    with uow:
        pedido = pedido_service.get_by_id(uow, pedido_id)
        _ = pedido.detalles
        if pedido.detalles:
            for d in pedido.detalles:
                _ = d.producto
        _ = pedido.historial
        return pedido


@router.get("/{pedido_id}/historial", response_model=list[HistorialEstadoPedidoRead])
def get_pedido_historial(
    pedido_id: int,
    current_user: Usuario = Depends(check_role(["CLIENT", "ADMIN", "PEDIDOS"])),
    uow: UnitOfWork = Depends(get_uow)
):
    with uow:
        pedido = pedido_service.get_by_id(uow, pedido_id)
        _ = pedido.historial
        return pedido.historial


@router.patch("/{pedido_id}/estado", response_model=PedidoReadConDetalles)
def transicionar_estado(
    pedido_id: int, 
    data: AvanzarEstadoRequest, 
    current_user: Usuario = Depends(check_role(["ADMIN", "PEDIDOS"])), 
    uow: UnitOfWork = Depends(get_uow)
):
    with uow:
        pedido = uow.pedidos.get_by_id(pedido_id)
        estado_anterior = pedido.estado_codigo if pedido else None

        pedido = pedido_service.transicionar_estado(uow, pedido_id, data.nuevo_estado, current_user.id, data.motivo)
        _ = pedido.detalles
        if pedido.detalles:
            for d in pedido.detalles:
                _ = d.producto
        _ = pedido.historial

    if estado_anterior:
        event_type = "pedido_cancelado" if data.nuevo_estado == "CANCELADO" else "estado_cambiado"
        evento = ws_manager._build_evento(
            event_type=event_type,
            pedido_id=pedido_id,
            estado_anterior=estado_anterior,
            estado_nuevo=data.nuevo_estado,
            usuario_id=current_user.id,
            motivo=data.motivo,
        )
        ws_manager.broadcast_pedido(pedido_id, evento)
        ws_manager.broadcast_to_user(pedido.usuario_id, evento)

    return pedido


@router.delete("/{pedido_id}", response_model=PedidoReadConDetalles)
def cancelar_pedido_cliente(
    pedido_id: int,
    current_user: Usuario = Depends(check_role(["CLIENT"])),
    uow: UnitOfWork = Depends(get_uow)
):
    with uow:
        pedido = uow.pedidos.get_by_id(pedido_id)
        estado_anterior = pedido.estado_codigo if pedido else None

        pedido = pedido_service.cancelar_pedido_cliente(uow, pedido_id, current_user.id)
        _ = pedido.detalles
        if pedido.detalles:
            for d in pedido.detalles:
                _ = d.producto
        _ = pedido.historial

    if estado_anterior:
        evento = ws_manager._build_evento(
            event_type="pedido_cancelado",
            pedido_id=pedido_id,
            estado_anterior=estado_anterior,
            estado_nuevo="CANCELADO",
            usuario_id=current_user.id,
            motivo="Cancelado por el cliente",
        )
        ws_manager.broadcast_pedido(pedido_id, evento)
        ws_manager.broadcast_to_user(pedido.usuario_id, evento)

    return pedido
