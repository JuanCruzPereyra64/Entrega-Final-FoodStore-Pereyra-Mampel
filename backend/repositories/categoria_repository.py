from typing import Optional
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from backend.models.categoria import Categoria
from backend.repositories.base_repository import BaseRepository

class CategoriaRepository(BaseRepository[Categoria]):
    def __init__(self, session: Session):
        super().__init__(Categoria, session)

    def get_all(self, offset: int = 0, limit: int = 100) -> list[Categoria]:
        statement = (
            select(Categoria)
            .options(selectinload(Categoria.subcategorias))
            .offset(offset)
            .limit(limit)
        )
        return list(self.session.exec(statement).all())

    def get_by_id(self, categoria_id: int) -> Optional[Categoria]:
        statement = (
            select(Categoria)
            .where(Categoria.id == categoria_id)
            .options(selectinload(Categoria.subcategorias))
        )
        return self.session.exec(statement).first()
