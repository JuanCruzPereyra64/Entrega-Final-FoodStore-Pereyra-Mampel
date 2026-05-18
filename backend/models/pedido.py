from decimal import Decimal
from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel, Column, BigInteger, String, Text, Numeric, DateTime, ForeignKey

if TYPE_CHECKING:
    from backend.models.usuario import Usuario
    from backend.models.direccion_entrega import DireccionEntrega
    from backend.models.forma_pago import FormaPago
    from backend.models.estado_pedido import EstadoPedido
    from backend.models.detalle_pedido import DetallePedido
    from backend.models.historial_estado_pedido import HistorialEstadoPedido


class Pedido(SQLModel, table=True):
    __tablename__ = "pedidos"

    id: Optional[int] = Field(
        default=None, 
        sa_column=Column(BigInteger, primary_key=True, autoincrement=True)
    )
    usuario_id: int = Field(
        sa_column=Column(BigInteger, ForeignKey("usuarios.id", ondelete="RESTRICT"), nullable=False)
    )
    direccion_id: Optional[int] = Field(
        default=None,
        sa_column=Column(BigInteger, ForeignKey("direcciones_entrega.id", ondelete="SET NULL"))
    )
    estado_codigo: str = Field(
        sa_column=Column(String(20), ForeignKey("estados_pedido.codigo", ondelete="RESTRICT"), nullable=False)
    )
    forma_pago_codigo: str = Field(
        sa_column=Column(String(30), ForeignKey("formas_pago.codigo", ondelete="RESTRICT"), nullable=False)
    )
    
    subtotal: Decimal = Field(sa_column=Column(Numeric(10, 2), nullable=False))
    descuento: Decimal = Field(sa_column=Column(Numeric(10, 2), nullable=False, default=Decimal('0.00')))
    costo_envio: Decimal = Field(sa_column=Column(Numeric(10, 2), nullable=False))
    total: Decimal = Field(sa_column=Column(Numeric(10, 2), nullable=False))
    
    notas: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    deleted_at: Optional[datetime] = Field(
        default=None, 
        sa_column=Column(DateTime(timezone=True))
    )

    usuario: "Usuario" = Relationship()
    direccion: Optional["DireccionEntrega"] = Relationship()
    estado: "EstadoPedido" = Relationship(back_populates="pedidos")
    forma_pago: "FormaPago" = Relationship(back_populates="pedidos")
    
    detalles: list["DetallePedido"] = Relationship(
        back_populates="pedido", sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    historial: list["HistorialEstadoPedido"] = Relationship(
        back_populates="pedido", sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
