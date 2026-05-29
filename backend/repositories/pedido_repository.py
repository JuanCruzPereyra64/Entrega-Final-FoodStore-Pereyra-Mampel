from typing import Optional
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from backend.models.pedido import Pedido
from backend.repositories.base_repository import BaseRepository

class PedidoRepository(BaseRepository[Pedido]):
    def __init__(self, session: Session):
        super().__init__(Pedido, session)

    def get_by_id(self, pedido_id: int) -> Optional[Pedido]:
        statement = (
            select(Pedido)
            .where(Pedido.id == pedido_id)
            .options(selectinload(Pedido.detalles), selectinload(Pedido.historial))
        )
        return self.session.exec(statement).first()

    def get_by_usuario_id(self, usuario_id: int) -> list[Pedido]:
        statement = (
            select(Pedido)
            .where(Pedido.usuario_id == usuario_id)
            .options(selectinload(Pedido.detalles), selectinload(Pedido.historial))
            .order_by(Pedido.created_at.desc())
        )
        return self.session.exec(statement).all()
