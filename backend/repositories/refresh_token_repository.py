from typing import Optional
from sqlmodel import Session, select
from backend.models.refresh_token import RefreshToken
from backend.repositories.base_repository import BaseRepository


class RefreshTokenRepository(BaseRepository[RefreshToken]):
    def __init__(self, session: Session):
        super().__init__(RefreshToken, session)

    def get_by_hash(self, token_hash: str) -> Optional[RefreshToken]:
        statement = select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        return self.session.exec(statement).first()

    def get_active_by_user(self, usuario_id: int) -> list[RefreshToken]:
        statement = select(RefreshToken).where(
            RefreshToken.usuario_id == usuario_id,
            RefreshToken.revoked_at.is_(None),
        )
        return self.session.exec(statement).all()
