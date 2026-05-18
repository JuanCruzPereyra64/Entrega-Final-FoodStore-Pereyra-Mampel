from decimal import Decimal
from typing import Optional
from sqlmodel import SQLModel


class DireccionEntregaBase(SQLModel):
    etiqueta: Optional[str] = None
    linea1: str
    linea2: Optional[str] = None
    ciudad: str
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
    es_principal: bool = False


class DireccionEntregaCreate(DireccionEntregaBase):
    pass


class DireccionEntregaUpdate(SQLModel):
    etiqueta: Optional[str] = None
    linea1: Optional[str] = None
    linea2: Optional[str] = None
    ciudad: Optional[str] = None
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
    es_principal: Optional[bool] = None


class DireccionEntregaRead(DireccionEntregaBase):
    id: int
    usuario_id: int
