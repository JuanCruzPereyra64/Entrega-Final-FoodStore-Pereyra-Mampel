from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship, SQLModel, Column
from sqlalchemy import ARRAY, String

if TYPE_CHECKING:
    from backend.models.categoria import Categoria
    from backend.models.ingrediente import Ingrediente


class ProductoCategoria(SQLModel, table=True):
    __tablename__ = "producto_categoria"

    producto_id: int = Field(default=None, foreign_key="productos.id", primary_key=True)
    categoria_id: int = Field(default=None, foreign_key="categorias.id", primary_key=True)
    es_principal: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ProductoIngrediente(SQLModel, table=True):
    __tablename__ = "producto_ingrediente"

    producto_id: int = Field(default=None, foreign_key="productos.id", primary_key=True)
    ingrediente_id: int = Field(default=None, foreign_key="ingredientes.id", primary_key=True)
    es_removible: bool = Field(default=False)


class Producto(SQLModel, table=True):
    __tablename__ = "productos"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(min_length=1, max_length=150)
    descripcion: Optional[str] = None
    precio_base: float = Field(ge=0.0)
    imagenes_url: list[str] = Field(default_factory=list, sa_column=Column(ARRAY(String)))
    stock_cantidad: int = Field(default=0, ge=0)
    disponible: bool = Field(default=True)
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: Optional[datetime] = None

    # Relaciones N:M
    categorias: list["Categoria"] = Relationship(
        back_populates="productos", link_model=ProductoCategoria
    )
    ingredientes: list["Ingrediente"] = Relationship(
        back_populates="productos", link_model=ProductoIngrediente
    )
