from sqlmodel import Session, select
from backend.repositories.base_repository import BaseRepository
from backend.models.movimiento_stock import MovimientoStock

class MovimientoStockRepository(BaseRepository[MovimientoStock]):
    def __init__(self, session: Session):
        super().__init__(MovimientoStock, session)
        
    def get_historial(self, ingrediente_id: int = None, offset: int = 0, limit: int = 100):
        query = select(MovimientoStock).order_by(MovimientoStock.created_at.desc()).offset(offset).limit(limit)
        if ingrediente_id:
            query = query.where(MovimientoStock.ingrediente_id == ingrediente_id)
        return self.session.exec(query).all()
