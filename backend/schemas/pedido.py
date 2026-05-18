from decimal import Decimal
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel
from backend.schemas.detalle_pedido import DetallePedidoCreate, DetallePedidoRead
from backend.schemas.historial_estado_pedido import HistorialEstadoPedidoRead


class PedidoBase(SQLModel):
    direccion_id: Optional[int] = None
    forma_pago_codigo: str
    notas: Optional[str] = None


class PedidoCreate(PedidoBase):
    detalles: list[DetallePedidoCreate]


class PedidoUpdate(SQLModel):
    estado_codigo: Optional[str] = None
    direccion_id: Optional[int] = None
    forma_pago_codigo: Optional[str] = None
    notas: Optional[str] = None
    motivo_cambio_estado: Optional[str] = None


class PedidoRead(PedidoBase):
    id: int
    usuario_id: int
    estado_codigo: str
    subtotal: Decimal
    descuento: Decimal
    costo_envio: Decimal
    total: Decimal
    created_at: datetime
    updated_at: datetime


class PedidoReadConDetalles(PedidoRead):
    detalles: list[DetallePedidoRead]
    historial: list[HistorialEstadoPedidoRead]
