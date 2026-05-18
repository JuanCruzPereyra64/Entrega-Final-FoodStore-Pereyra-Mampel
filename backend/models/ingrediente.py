from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship, SQLModel, Column, String, BigInteger, Boolean, DateTime, Text

from backend.models.producto import ProductoIngrediente

if TYPE_CHECKING:
    from backend.models.producto import Producto


class Ingrediente(SQLModel, table=True):
    __tablename__ = "ingredientes"

    id: Optional[int] = Field(default=None, sa_column=Column(BigInteger, primary_key=True, autoincrement=True))
    nombre: str = Field(sa_column=Column(String(100), unique=True, nullable=False))
    descripcion: Optional[str] = Field(default=None, sa_column=Column(Text))
    es_alergeno: bool = Field(default=False, sa_column=Column(Boolean, nullable=False, default=False))

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), nullable=False))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), nullable=False))

    # Relación N:M
    productos: list["Producto"] = Relationship(
        back_populates="ingredientes", link_model=ProductoIngrediente
    )
