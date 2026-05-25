from decimal import Decimal
from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel, Column, BigInteger, String, Text, Numeric, Boolean, DateTime, ForeignKey

if TYPE_CHECKING:
    from backend.models.usuario import Usuario


class DireccionEntrega(SQLModel, table=True):
    __tablename__ = "direcciones_entrega"

    id: Optional[int] = Field(
        default=None, 
        primary_key=True
    )
    usuario_id: int = Field(
        sa_column=Column(BigInteger, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    )
    etiqueta: Optional[str] = Field(
        default=None, 
        sa_column=Column(String(80))
    )
    linea1: str = Field(
        sa_column=Column(Text, nullable=False)
    )
    linea2: Optional[str] = Field(
        default=None, 
        sa_column=Column(Text)
    )
    ciudad: str = Field(
        sa_column=Column(String(100), nullable=False)
    )
    latitud: Optional[Decimal] = Field(
        default=None, 
        sa_column=Column(Numeric(9, 6))
    )
    longitud: Optional[Decimal] = Field(
        default=None, 
        sa_column=Column(Numeric(9, 6))
    )
    es_principal: bool = Field(
        default=False, 
        sa_column=Column(Boolean, nullable=False, default=False)
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

    usuario: "Usuario" = Relationship(back_populates="direcciones")
