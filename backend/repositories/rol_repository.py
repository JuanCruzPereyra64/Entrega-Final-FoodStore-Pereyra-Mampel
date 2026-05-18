from typing import Optional
from sqlmodel import Session, select
from backend.models.rol import Rol

class RolRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self, offset: int = 0, limit: int = 100) -> list[Rol]:
        statement = select(Rol).offset(offset).limit(limit)
        return list(self.session.exec(statement).all())

    def get_by_id(self, rol_id: int) -> Optional[Rol]:
        return self.session.get(Rol, rol_id)

    def add(self, rol: Rol) -> None:
        self.session.add(rol)

    def delete(self, rol: Rol) -> None:
        self.session.delete(rol)
