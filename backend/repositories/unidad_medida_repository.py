from typing import Optional
from sqlmodel import Session, select
from backend.models.unidad_medida import UnidadMedida
from backend.repositories.base_repository import BaseRepository

class UnidadMedidaRepository(BaseRepository[UnidadMedida]):
    def __init__(self, session: Session):
        super().__init__(UnidadMedida, session)
