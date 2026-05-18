from typing import Optional
from sqlmodel import Session, select
from backend.models.estado_pedido import EstadoPedido

class EstadoPedidoRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_codigo(self, codigo: str) -> Optional[EstadoPedido]:
        return self.session.get(EstadoPedido, codigo)
