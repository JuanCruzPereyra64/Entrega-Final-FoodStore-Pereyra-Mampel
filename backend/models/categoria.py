from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship, SQLModel

from backend.models.producto import ProductoCategoria

if TYPE_CHECKING:
    from backend.models.producto import Producto


class Categoria(SQLModel, table=True):
    __tablename__ = "categorias"

    id: Optional[int] = Field(default=None, primary_key=True)
    parent_id: Optional[int] = Field(default=None, foreign_key="categorias.id")
    nombre: str = Field(min_length=1, max_length=100, unique=True)
    descripcion: Optional[str] = None
    imagen_url: Optional[str] = None

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: Optional[datetime] = None

    # Auto-referencia
    subcategorias: list["Categoria"] = Relationship(
        sa_relationship_kwargs={"remote_side": "Categoria.id"}
    )
    
    # 3. Relación N:M (Sin comillas en link_model)
    productos: list["Producto"] = Relationship(
        back_populates="categorias", link_model=ProductoCategoria
    )
