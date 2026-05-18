from decimal import Decimal
from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING, Any
from sqlmodel import Field, Relationship, SQLModel, Column, BigInteger, String, Numeric, DateTime, ForeignKey, JSON
from sqlalchemy import SmallInteger

if TYPE_CHECKING:
    from backend.models.pedido import Pedido
    from backend.models.producto import Producto


class DetallePedido(SQLModel, table=True):
    __tablename__ = "detalles_pedido"

    pedido_id: int = Field(
        sa_column=Column(BigInteger, ForeignKey("pedidos.id", ondelete="CASCADE"), primary_key=True)
    )
    producto_id: int = Field(
        sa_column=Column(BigInteger, ForeignKey("productos.id", ondelete="RESTRICT"), primary_key=True)
    )
    cantidad: int = Field(
        sa_column=Column(SmallInteger, nullable=False)
    )
    nombre_producto_snap: str = Field(
        sa_column=Column(String(150), nullable=False)
    )
    precio_unitario_snap: Decimal = Field(
        sa_column=Column(Numeric(10, 2), nullable=False)
    )
    subtotal_snap: Decimal = Field(
        sa_column=Column(Numeric(10, 2), nullable=False)
    )
    personalizacion: Optional[dict[str, Any]] = Field(
        default=None,
        sa_column=Column(JSON)
    )
    
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )

    pedido: "Pedido" = Relationship(back_populates="detalles")
    producto: "Producto" = Relationship()
