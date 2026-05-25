from typing import Optional
from sqlmodel import Session, select
from backend.models.usuario import Usuario
from backend.repositories.base_repository import BaseRepository

class UsuarioRepository(BaseRepository[Usuario]):
    def __init__(self, session: Session):
        super().__init__(Usuario, session)
        
    def get_by_email(self, email: str) -> Optional[Usuario]:
        statement = select(Usuario).where(Usuario.email == email)
        return self.session.exec(statement).first()
