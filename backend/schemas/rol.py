from typing import Optional
from sqlmodel import SQLModel


class RolBase(SQLModel):
    nombre: str
    descripcion: Optional[str] = None


class RolCreate(RolBase):
    pass


class RolUpdate(SQLModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None


class RolRead(RolBase):
    id: int
