from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import EmailStr


class UsuarioBase(SQLModel):
    nombre: str = Field(min_length=2, max_length=80)
    apellido: str = Field(min_length=2, max_length=80)
    email: EmailStr
    celular: Optional[str] = None


class UsuarioCreate(UsuarioBase):
    password: str = Field(min_length=8)


class UsuarioUpdate(SQLModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    celular: Optional[str] = None


class RolRead(SQLModel):
    nombre: str


class UsuarioRead(UsuarioBase):
    id: int
    created_at: datetime
    updated_at: datetime


class UsuarioReadWithRoles(UsuarioRead):
    roles: list[RolRead] = []


class UsuarioLogin(SQLModel):
    email: EmailStr
    password: str = Field(min_length=8)
