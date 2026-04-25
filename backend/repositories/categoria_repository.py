from typing import Optional
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from backend.models.categoria import Categoria

class CategoriaRepository:
    def __init__(self, session: Session):
        self.session = session

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

    def add(self, categoria: Categoria) -> None:
        self.session.add(categoria)

    def delete(self, categoria: Categoria) -> None:
        self.session.delete(categoria)
