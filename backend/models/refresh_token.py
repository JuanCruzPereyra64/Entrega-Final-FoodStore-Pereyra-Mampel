from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel, Column, BigInteger, String, DateTime, ForeignKey


class RefreshToken(SQLModel, table=True):
    __tablename__ = "refresh_tokens"

    id: Optional[int] = Field(default=None, primary_key=True)
    token_hash: str = Field(sa_column=Column(String(64), nullable=False, unique=True))
    usuario_id: int = Field(
        sa_column=Column(BigInteger, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    )
    expires_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    revoked_at: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime(timezone=True))
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )
