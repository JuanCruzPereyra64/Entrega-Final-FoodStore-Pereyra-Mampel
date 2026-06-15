import jwt
from fastapi import Depends, HTTPException, status, Request
from pydantic import ValidationError
from backend.core.config import settings
from backend.models.usuario import Usuario
from backend.schemas.token import TokenPayload
from backend.database import get_uow
from backend.uow.unit_of_work import UnitOfWork

def get_token_from_request(request: Request) -> str:
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header.split(" ", 1)[1]
    token = request.cookies.get("access_token")
    if token:
        return token
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Falta loguearse",
    )

def get_current_user(
    token: str = Depends(get_token_from_request),
    uow: UnitOfWork = Depends(get_uow)
) -> Usuario:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        token_data = TokenPayload(**payload)
    except (jwt.InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token invalido",
        )

    with uow:
        user = uow.usuarios.get_by_id(int(token_data.sub))
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        if user.deleted_at is not None:
            raise HTTPException(status_code=400, detail="Usuario borrado")

        _ = user.roles

        return user

def check_role(required_roles: list[str]):
    def role_checker(current_user: Usuario = Depends(get_current_user)):
        user_roles = [r.nombre for r in current_user.roles]
        if not any(role in user_roles for role in required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tenes permisos para acceder aca"
            )
        return current_user
    return role_checker
