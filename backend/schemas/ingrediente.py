from typing import Optional
from sqlmodel import SQLModel

from backend.schemas.unidad_medida import UnidadMedidaRead

class IngredienteCreate(SQLModel):
    nombre: str
    unidad_medida_id: int
    es_alergeno: bool = False
    stock_cantidad: int = 0


class IngredienteUpdate(SQLModel):
    nombre: Optional[str] = None
    unidad_medida_id: Optional[int] = None
    es_alergeno: Optional[bool] = None
    stock_cantidad: Optional[int] = None


class IngredienteRead(SQLModel):
    id: int
    nombre: str
    unidad_medida_id: int
    es_alergeno: bool
    stock_cantidad: int
    unidad_medida: Optional[UnidadMedidaRead] = None
