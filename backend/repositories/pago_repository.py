from typing import Optional
from sqlmodel import Session, select
from backend.models.pago import Pago
from backend.repositories.base_repository import BaseRepository


class PagoRepository(BaseRepository[Pago]):
    def __init__(self, session: Session):
        super().__init__(Pago, session)

    def get_by_pedido_id(self, pedido_id: int) -> Optional[Pago]:
        statement = select(Pago).where(Pago.pedido_id == pedido_id)
        return self.session.exec(statement).first()

    def get_by_idempotency_key(self, key: str) -> Optional[Pago]:
        statement = select(Pago).where(Pago.idempotency_key == key)
        return self.session.exec(statement).first()

    def get_by_external_reference(self, ref: str) -> Optional[Pago]:
        statement = select(Pago).where(Pago.external_reference == ref)
        return self.session.exec(statement).first()

    def get_by_mp_payment_id(self, mp_id: int) -> Optional[Pago]:
        statement = select(Pago).where(Pago.mp_payment_id == mp_id)
        return self.session.exec(statement).first()
