from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel, Column, String, Boolean

if TYPE_CHECKING:
    from backend.models.pedido import Pedido


class FormaPago(SQLModel, table=True):
    __tablename__ = "formas_pago"

    codigo: str = Field(
        sa_column=Column(String(30), primary_key=True)
    )
    descripcion: str = Field(
        sa_column=Column(String(80), nullable=False)
    )
    activo: bool = Field(
        default=True, 
        sa_column=Column(Boolean, nullable=False, default=True)
    )

    pedidos: list["Pedido"] = Relationship(back_populates="forma_pago")
