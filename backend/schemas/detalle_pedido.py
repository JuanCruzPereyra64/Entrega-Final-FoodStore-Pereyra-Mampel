from decimal import Decimal
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel
from backend.schemas.producto import ProductoReadBasico


class DetallePedidoBase(SQLModel):
    producto_id: int
    cantidad: int
    personalizacion: Optional[list[int]] = None


class DetallePedidoCreate(DetallePedidoBase):
    pass


class DetallePedidoRead(DetallePedidoBase):
    pedido_id: int
    nombre_producto_snap: str
    precio_unitario_snap: Decimal
    subtotal_snap: Decimal
    created_at: datetime
    producto: Optional[ProductoReadBasico] = None
