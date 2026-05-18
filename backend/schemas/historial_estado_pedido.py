from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel


class HistorialEstadoPedidoBase(SQLModel):
    estado_desde: Optional[str] = None
    estado_hacia: str
    usuario_id: Optional[int] = None
    motivo: Optional[str] = None


class HistorialEstadoPedidoCreate(HistorialEstadoPedidoBase):
    pedido_id: int


class HistorialEstadoPedidoRead(HistorialEstadoPedidoBase):
    id: int
    pedido_id: int
    created_at: datetime
