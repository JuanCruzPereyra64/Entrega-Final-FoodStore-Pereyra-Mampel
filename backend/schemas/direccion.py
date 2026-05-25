from typing import Optional
from pydantic import BaseModel
from decimal import Decimal

class DireccionBase(BaseModel):
    etiqueta: Optional[str] = None
    linea1: str
    linea2: Optional[str] = None
    ciudad: str
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
    es_principal: bool = False

class DireccionCreate(DireccionBase):
    pass

class DireccionUpdate(BaseModel):
    etiqueta: Optional[str] = None
    linea1: Optional[str] = None
    linea2: Optional[str] = None
    ciudad: Optional[str] = None
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None

class DireccionRead(DireccionBase):
    id: int
    usuario_id: int
