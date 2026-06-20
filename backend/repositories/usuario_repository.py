from typing import Optional
from sqlmodel import Session, select
from backend.models.usuario import Usuario
from backend.models.refresh_token import RefreshToken
from backend.models.usuario_rol import UsuarioRol
from backend.models.rol import Rol
from backend.repositories.base_repository import BaseRepository


class UsuarioRepository(BaseRepository[Usuario]):
    def __init__(self, session: Session):
        super().__init__(Usuario, session)
        
    def get_by_email(self, email: str) -> Optional[Usuario]:
        statement = select(Usuario).where(Usuario.email == email)
        return self.session.exec(statement).first()
    
    def get_all_with_filters(self, rol: str = None, offset: int = 0, limit: int = 100) -> list[Usuario]:
        query = select(Usuario).where(Usuario.deleted_at == None)
        if rol:
            query = query.join(UsuarioRol).join(Rol).where(Rol.nombre == rol)
        return self.session.exec(query.offset(offset).limit(limit)).all()
    
    def get_refresh_token_by_hash(self, token_hash: str) -> Optional[RefreshToken]:
        statement = select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        return self.session.exec(statement).first()
    
    def get_active_refresh_tokens(self, usuario_id: int) -> list[RefreshToken]:
        statement = select(RefreshToken).where(
            RefreshToken.usuario_id == usuario_id,
            RefreshToken.revoked_at.is_(None),
        )
        return self.session.exec(statement).all()
    
    def add_refresh_token(self, rt: RefreshToken):
        self.session.add(rt)
    
    def add_refresh_token_direct(self, rt: RefreshToken):
        self.session.add(rt)
    
    def get_usuario_roles(self, usuario_id: int) -> list[UsuarioRol]:
        statement = select(UsuarioRol).where(UsuarioRol.usuario_id == usuario_id)
        return self.session.exec(statement).all()
    
    def add_usuario_rol(self, usuario_id: int, rol_id: int) -> UsuarioRol:
        link = UsuarioRol(usuario_id=usuario_id, rol_id=rol_id)
        self.session.add(link)
        return link
    
    def delete_usuario_rol(self, link: UsuarioRol):
        self.session.delete(link)

    def refresh(self, entity):
        self.session.refresh(entity)

    def flush(self):
        self.session.flush()
