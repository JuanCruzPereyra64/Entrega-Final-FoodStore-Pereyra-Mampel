from typing import Optional
from sqlmodel import SQLModel, Field
from backend.schemas.categoria import CategoriaRead
from backend.schemas.ingrediente import IngredienteRead


class ProductoCreate(SQLModel):
    nombre: str
    precio_base: float
    descripcion: Optional[str] = None
    categoria_ids: list[int] = Field(min_length=1)
    ingrediente_ids: list[int] = Field(default=[])
    stock_cantidad: int = 0
    disponible: bool = True
    imagenes_url: list[str] = Field(default=[])


class ProductoUpdate(SQLModel):
    nombre: Optional[str] = None
    precio_base: Optional[float] = None
    descripcion: Optional[str] = None
    categoria_ids: Optional[list[int]] = None
    ingrediente_ids: Optional[list[int]] = None
    stock_cantidad: Optional[int] = None
    disponible: Optional[bool] = None
    imagenes_url: Optional[list[str]] = None


class ProductoRead(SQLModel):
    id: int
    nombre: str
    precio_base: float
    descripcion: Optional[str] = None
    stock_cantidad: int
    disponible: bool
    imagenes_url: list[str] = []
    categorias: list[CategoriaRead] = []
    ingredientes: list[IngredienteRead] = []
