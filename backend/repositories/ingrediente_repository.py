from typing import Optional
from sqlmodel import Session, select
from backend.models.ingrediente import Ingrediente
from backend.repositories.base_repository import BaseRepository

class IngredienteRepository(BaseRepository[Ingrediente]):
    def __init__(self, session: Session):
        super().__init__(Ingrediente, session)
