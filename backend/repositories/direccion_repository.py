from sqlmodel import select
from backend.repositories.base_repository import BaseRepository
from backend.models.direccion_entrega import DireccionEntrega

class DireccionRepository(BaseRepository[DireccionEntrega]):
    def __init__(self, session):
        super().__init__(DireccionEntrega, session)
        
    def get_by_user(self, usuario_id: int) -> list[DireccionEntrega]:
        return self.session.exec(
            select(DireccionEntrega)
            .where(DireccionEntrega.usuario_id == usuario_id)
            .where(DireccionEntrega.deleted_at == None)
        ).all()
        
    def get_principal(self, usuario_id: int) -> DireccionEntrega | None:
        return self.session.exec(
            select(DireccionEntrega)
            .where(DireccionEntrega.usuario_id == usuario_id)
            .where(DireccionEntrega.es_principal == True)
            .where(DireccionEntrega.deleted_at == None)
        ).first()
