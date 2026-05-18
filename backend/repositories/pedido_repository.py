from typing import Optional
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from backend.models.pedido import Pedido

class PedidoRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, pedido_id: int) -> Optional[Pedido]:
        statement = (
            select(Pedido)
            .where(Pedido.id == pedido_id)
            .options(selectinload(Pedido.detalles), selectinload(Pedido.historial))
        )
        return self.session.exec(statement).first()

    def add(self, pedido: Pedido) -> None:
        self.session.add(pedido)
