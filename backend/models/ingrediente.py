from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship, SQLModel, Column, String, BigInteger, Boolean, DateTime, Text, Numeric

from backend.models.producto import ProductoIngrediente

if TYPE_CHECKING:
    from backend.models.producto import Producto

from backend.models.unidad_medida import UnidadMedida


class Ingrediente(SQLModel, table=True):
    __tablename__ = "ingredientes"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(sa_column=Column(String(100), unique=True, nullable=False))
    unidad_medida_id: int = Field(foreign_key="unidades_medida.id", nullable=False)
    
    unidad_medida: Optional["UnidadMedida"] = Relationship(back_populates="ingredientes", sa_relationship_kwargs={"lazy": "joined"})
    es_alergeno: bool = Field(default=False, sa_column=Column(Boolean, nullable=False, default=False))
    
    stock_actual: float = Field(default=0.0, sa_column=Column(Numeric(10, 2), nullable=False, default=0.0))
    stock_minimo: float = Field(default=0.0, sa_column=Column(Numeric(10, 2), nullable=False, default=0.0))

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), nullable=False))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), nullable=False))

    # Relación N:M
    productos: list["Producto"] = Relationship(
        back_populates="ingredientes", link_model=ProductoIngrediente
    )
