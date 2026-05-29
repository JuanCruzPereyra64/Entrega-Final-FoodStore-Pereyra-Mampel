from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel

class MovimientoStockRead(SQLModel):
    id: int
    ingrediente_id: int
    cantidad: float
    tipo: str
    motivo: str
    usuario_id: Optional[int] = None
    created_at: datetime
    
    # Podríamos incluir los nombres del ingrediente y el usuario
    ingrediente_nombre: Optional[str] = None
    usuario_nombre: Optional[str] = None
