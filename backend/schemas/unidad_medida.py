from typing import Optional
from sqlmodel import SQLModel


class UnidadMedidaCreate(SQLModel):
    nombre: str


class UnidadMedidaUpdate(SQLModel):
    nombre: Optional[str] = None


class UnidadMedidaRead(SQLModel):
    id: int
    nombre: str
