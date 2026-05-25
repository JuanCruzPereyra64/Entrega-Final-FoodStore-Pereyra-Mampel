from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel, Column, BigInteger, String, Text, DateTime, ForeignKey

if TYPE_CHECKING:
    from backend.models.pedido import Pedido
    from backend.models.usuario import Usuario
    from backend.models.estado_pedido import EstadoPedido


class HistorialEstadoPedido(SQLModel, table=True):
    __tablename__ = "historial_estados_pedido"

    id: Optional[int] = Field(
        default=None, 
        primary_key=True
    )
    pedido_id: int = Field(
        sa_column=Column(BigInteger, ForeignKey("pedidos.id", ondelete="CASCADE"), nullable=False)
    )
    estado_desde: Optional[str] = Field(
        default=None,
        sa_column=Column(String(20), ForeignKey("estados_pedido.codigo", ondelete="SET NULL"))
    )
    estado_hacia: str = Field(
        sa_column=Column(String(20), ForeignKey("estados_pedido.codigo", ondelete="RESTRICT"), nullable=False)
    )
    usuario_id: Optional[int] = Field(
        default=None,
        sa_column=Column(BigInteger, ForeignKey("usuarios.id", ondelete="SET NULL"))
    )
    motivo: Optional[str] = Field(
        default=None,
        sa_column=Column(Text)
    )
    
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )

    pedido: "Pedido" = Relationship(back_populates="historial")
    usuario: Optional["Usuario"] = Relationship()
    estado_desde_ref: Optional["EstadoPedido"] = Relationship(
        back_populates="historiales_desde",
        sa_relationship_kwargs={"foreign_keys": "[HistorialEstadoPedido.estado_desde]"}
    )
    estado_hacia_ref: "EstadoPedido" = Relationship(
        back_populates="historiales_hacia",
        sa_relationship_kwargs={"foreign_keys": "[HistorialEstadoPedido.estado_hacia]"}
    )
