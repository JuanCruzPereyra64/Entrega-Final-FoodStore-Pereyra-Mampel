from typing import Optional
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from backend.models.pedido import Pedido
from backend.models.historial_estado_pedido import HistorialEstadoPedido
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

    def add_historial(self, historial: HistorialEstadoPedido):
        self.session.add(historial)

    def get_ingrediente_links_for_producto(self, producto_id: int):
        from backend.models.producto import ProductoIngrediente
        statement = select(ProductoIngrediente).where(ProductoIngrediente.producto_id == producto_id)
        return list(self.session.exec(statement).all())

    def refresh(self, entity):
        self.session.refresh(entity)
