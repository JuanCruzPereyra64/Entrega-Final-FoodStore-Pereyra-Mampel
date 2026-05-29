from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, SQLModel, Column, String, Numeric, DateTime, Relationship

if TYPE_CHECKING:
    from backend.models.ingrediente import Ingrediente
    from backend.models.usuario import Usuario

class MovimientoStock(SQLModel, table=True):
    __tablename__ = "movimientos_stock"

    id: Optional[int] = Field(default=None, primary_key=True)
    ingrediente_id: int = Field(foreign_key="ingredientes.id", nullable=False)
    cantidad: float = Field(sa_column=Column(Numeric(10, 2), nullable=False))
    tipo: str = Field(sa_column=Column(String(20), nullable=False)) # 'INGRESO' o 'EGRESO'
    motivo: str = Field(sa_column=Column(String(255), nullable=False))
    usuario_id: Optional[int] = Field(default=None, foreign_key="usuarios.id")
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), nullable=False))

    ingrediente: Optional["Ingrediente"] = Relationship(sa_relationship_kwargs={"lazy": "joined"})
    usuario: Optional["Usuario"] = Relationship(sa_relationship_kwargs={"lazy": "joined"})
