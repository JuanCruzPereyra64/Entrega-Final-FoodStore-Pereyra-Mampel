from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship, SQLModel, Column, String

if TYPE_CHECKING:
    from backend.models.ingrediente import Ingrediente

class UnidadMedida(SQLModel, table=True):
    __tablename__ = "unidades_medida"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(sa_column=Column(String(50), unique=True, nullable=False))
    simbolo: str = Field(sa_column=Column(String(10), unique=True, nullable=False))
    tipo: str = Field(sa_column=Column(String(20), nullable=False))

    ingredientes: list["Ingrediente"] = Relationship(back_populates="unidad_medida")
