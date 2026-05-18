from typing import Optional
from sqlmodel import SQLModel

class EstadoPedidoBase(SQLModel):
    codigo: str
    descripcion: str
    orden: int
    es_terminal: bool = False

class EstadoPedidoCreate(EstadoPedidoBase):
    pass

class EstadoPedidoUpdate(SQLModel):
    descripcion: Optional[str] = None
    orden: Optional[int] = None
    es_terminal: Optional[bool] = None

class EstadoPedidoRead(EstadoPedidoBase):
    pass
