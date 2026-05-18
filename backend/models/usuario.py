from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship, SQLModel, Column, BigInteger, String, CHAR, DateTime

from backend.models.usuario_rol import UsuarioRol

if TYPE_CHECKING:
    from backend.models.rol import Rol
    from backend.models.direccion_entrega import DireccionEntrega


class Usuario(SQLModel, table=True):
    __tablename__ = "usuarios"

    id: Optional[int] = Field(
        default=None, 
        sa_column=Column(BigInteger, primary_key=True, autoincrement=True)
    )
    nombre: str = Field(
        sa_column=Column(String(80), nullable=False)
    )
    apellido: str = Field(
        sa_column=Column(String(80), nullable=False)
    )
    email: str = Field(
        sa_column=Column(String(254), unique=True, nullable=False)
    )
    celular: Optional[str] = Field(
        default=None, 
        sa_column=Column(String(20))
    )
    password_hash: str = Field(
        sa_column=Column(CHAR(60), nullable=False)
    )
    
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    deleted_at: Optional[datetime] = Field(
        default=None, 
        sa_column=Column(DateTime(timezone=True))
    )

    roles: list["Rol"] = Relationship(
        back_populates="usuarios", link_model=UsuarioRol
    )
    direcciones: list["DireccionEntrega"] = Relationship(
        back_populates="usuario", sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
