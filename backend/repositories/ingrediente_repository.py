from typing import Optional
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from backend.models.ingrediente import Ingrediente
from backend.repositories.base_repository import BaseRepository

class IngredienteRepository(BaseRepository[Ingrediente]):
    def __init__(self, session: Session):
        super().__init__(Ingrediente, session)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Ingrediente]:
        stmt = select(self.model).options(selectinload(self.model.unidad_medida)).offset(skip).limit(limit)
        return self.session.exec(stmt).all()

    def get_by_id(self, id: int) -> Optional[Ingrediente]:
        stmt = select(self.model).options(selectinload(self.model.unidad_medida)).where(self.model.id == id)
        return self.session.exec(stmt).first()
