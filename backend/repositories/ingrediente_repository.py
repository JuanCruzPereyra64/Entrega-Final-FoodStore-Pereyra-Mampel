from typing import Optional
from sqlmodel import Session, select
from backend.models.ingrediente import Ingrediente

class IngredienteRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self, offset: int = 0, limit: int = 100) -> list[Ingrediente]:
        statement = select(Ingrediente).offset(offset).limit(limit)
        return list(self.session.exec(statement).all())

    def get_by_id(self, ingrediente_id: int) -> Optional[Ingrediente]:
        return self.session.get(Ingrediente, ingrediente_id)

    def add(self, ingrediente: Ingrediente) -> None:
        self.session.add(ingrediente)

    def delete(self, ingrediente: Ingrediente) -> None:
        self.session.delete(ingrediente)
