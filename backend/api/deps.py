import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from backend.core.security import ALGORITHM, SECRET_KEY
from backend.models.usuario import Usuario
from backend.schemas.token import TokenPayload
from backend.database import get_uow
from backend.uow.unit_of_work import UnitOfWork

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/usuarios/login"
)

def get_current_user(
    token: str = Depends(reusable_oauth2), 
    uow: UnitOfWork = Depends(get_uow)
) -> Usuario:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except (jwt.InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No se pudieron validar las credenciales de seguridad.",
        )
        
    with uow:
        user = uow.usuarios.get_by_id(int(token_data.sub))
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado en el sistema.")
        if user.deleted_at is not None:
            raise HTTPException(status_code=400, detail="El usuario ha sido eliminado (soft delete).")
            
        return user
