from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel
from pydantic import EmailStr


class UsuarioBase(SQLModel):
    nombre: str
    apellido: str
    email: EmailStr
    celular: Optional[str] = None


class UsuarioCreate(UsuarioBase):
    password: str


class UsuarioUpdate(SQLModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    celular: Optional[str] = None


class UsuarioRead(UsuarioBase):
    id: int
    created_at: datetime
    updated_at: datetime


class UsuarioLogin(SQLModel):
    email: EmailStr
    password: str
