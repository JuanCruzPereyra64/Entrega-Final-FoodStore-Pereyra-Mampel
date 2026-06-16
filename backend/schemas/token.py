from sqlmodel import SQLModel

class Token(SQLModel):
    access_token: str
    token_type: str

class TokenPayload(SQLModel):
    sub: str | None = None
    type: str | None = None

class TokenResponse(SQLModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
