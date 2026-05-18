from typing import Optional
from sqlmodel import Session, select
from backend.models.usuario import Usuario

class UsuarioRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self, offset: int = 0, limit: int = 100) -> list[Usuario]:
        statement = select(Usuario).offset(offset).limit(limit)
        return list(self.session.exec(statement).all())

    def get_by_id(self, usuario_id: int) -> Optional[Usuario]:
        return self.session.get(Usuario, usuario_id)
        
    def get_by_email(self, email: str) -> Optional[Usuario]:
        statement = select(Usuario).where(Usuario.email == email)
        return self.session.exec(statement).first()

    def add(self, usuario: Usuario) -> None:
        self.session.add(usuario)

    def delete(self, usuario: Usuario) -> None:
        self.session.delete(usuario)
