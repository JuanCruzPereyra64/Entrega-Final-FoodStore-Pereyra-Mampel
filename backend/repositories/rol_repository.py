from typing import Optional
from sqlmodel import Session, select
from backend.models.rol import Rol
from backend.repositories.base_repository import BaseRepository


class RolRepository(BaseRepository[Rol]):
    def __init__(self, session: Session):
        super().__init__(Rol, session)

    def get_by_nombre(self, nombre: str) -> Optional[Rol]:
        statement = select(Rol).where(Rol.nombre == nombre)
        return self.session.exec(statement).first()
