from fastapi import APIRouter, Depends, status
from backend.database import get_uow
from backend.schemas.usuario import UsuarioCreate, UsuarioRead, UsuarioLogin
from backend.schemas.token import Token
from backend.core.security import create_access_token
from backend.services import usuario_service
from backend.uow.unit_of_work import UnitOfWork

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post("/registro", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def registro(data: UsuarioCreate, uow: UnitOfWork = Depends(get_uow)):
    with uow:
        return usuario_service.registrar_usuario(uow, data)


@router.post("/login", response_model=Token)
def login(data: UsuarioLogin, uow: UnitOfWork = Depends(get_uow)):
    with uow:
        usuario = usuario_service.autenticar_usuario(uow, data.email, data.password)
        access_token = create_access_token(subject=usuario.id)
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
