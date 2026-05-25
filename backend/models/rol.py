from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship, SQLModel, Column, BigInteger, String, Text

from backend.models.usuario_rol import UsuarioRol

if TYPE_CHECKING:
    from backend.models.usuario import Usuario


class Rol(SQLModel, table=True):
    __tablename__ = "roles"

    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )
    nombre: str = Field(
        sa_column=Column(String(50), unique=True, nullable=False)
    )
    descripcion: Optional[str] = Field(
        default=None,
        sa_column=Column(Text)
    )

    usuarios: list["Usuario"] = Relationship(
        back_populates="roles", link_model=UsuarioRol,
        sa_relationship_kwargs={
            "primaryjoin": "Rol.id==UsuarioRol.rol_id",
            "secondaryjoin": "Usuario.id==UsuarioRol.usuario_id"
        }
    )
