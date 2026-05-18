from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel, Column, BigInteger, DateTime, ForeignKey

class UsuarioRol(SQLModel, table=True):
    __tablename__ = "usuarios_roles"

    usuario_id: int = Field(
        sa_column=Column(BigInteger, ForeignKey("usuarios.id", ondelete="CASCADE"), primary_key=True)
    )
    rol_id: int = Field(
        sa_column=Column(BigInteger, ForeignKey("roles.id", ondelete="RESTRICT"), primary_key=True)
    )
    asignado_por_id: Optional[int] = Field(
        default=None,
        sa_column=Column(BigInteger, ForeignKey("usuarios.id", ondelete="SET NULL"))
    )
    expires_at: Optional[datetime] = Field(
        default=None, 
        sa_column=Column(DateTime(timezone=True))
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
