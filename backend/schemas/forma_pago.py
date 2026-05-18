from typing import Optional
from sqlmodel import SQLModel

class FormaPagoBase(SQLModel):
    codigo: str
    descripcion: str
    activo: bool = True

class FormaPagoCreate(FormaPagoBase):
    pass

class FormaPagoUpdate(SQLModel):
    descripcion: Optional[str] = None
    activo: Optional[bool] = None

class FormaPagoRead(FormaPagoBase):
    pass
