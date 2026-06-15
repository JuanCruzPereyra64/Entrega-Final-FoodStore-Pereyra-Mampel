from decimal import Decimal
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import field_validator
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


class AvanzarEstadoRequest(SQLModel):
    nuevo_estado: str
    motivo: Optional[str] = None

    @field_validator("motivo")
    @classmethod
    def motivo_requerido_si_cancelado(cls, v, info):
        if info.data.get("nuevo_estado") == "CANCELADO" and not v:
            raise ValueError("El motivo es obligatorio cuando se cancela un pedido (RN-05)")
        return v
