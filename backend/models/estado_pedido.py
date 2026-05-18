from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel, Column, String, Integer, Boolean

if TYPE_CHECKING:
    from backend.models.pedido import Pedido
    from backend.models.historial_estado_pedido import HistorialEstadoPedido


class EstadoPedido(SQLModel, table=True):
    __tablename__ = "estados_pedido"

    codigo: str = Field(
        sa_column=Column(String(20), primary_key=True)
    )
    descripcion: str = Field(
        sa_column=Column(String(80), nullable=False)
    )
    orden: int = Field(
        sa_column=Column(Integer, nullable=False)
    )
    es_terminal: bool = Field(
        sa_column=Column(Boolean, nullable=False, default=False)
    )

    pedidos: list["Pedido"] = Relationship(back_populates="estado")
    historiales_desde: list["HistorialEstadoPedido"] = Relationship(
        back_populates="estado_desde_ref", sa_relationship_kwargs={"foreign_keys": "[HistorialEstadoPedido.estado_desde]"}
    )
    historiales_hacia: list["HistorialEstadoPedido"] = Relationship(
        back_populates="estado_hacia_ref", sa_relationship_kwargs={"foreign_keys": "[HistorialEstadoPedido.estado_hacia]"}
    )
