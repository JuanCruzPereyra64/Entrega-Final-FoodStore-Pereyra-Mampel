from fastapi import APIRouter, Depends, status, Response
from backend.database import get_uow
from backend.schemas.usuario import UsuarioCreate, UsuarioRead, UsuarioLogin
from backend.core.security import create_access_token
from backend.services import usuario_service
from backend.uow.unit_of_work import UnitOfWork
from backend.models.usuario import Usuario
from backend.api.deps import get_current_user

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.post("/registro", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def registro(data: UsuarioCreate, uow: UnitOfWork = Depends(get_uow)):
    with uow:
        return usuario_service.registrar_usuario(uow, data)

@router.post("/login")
def login(data: UsuarioLogin, response: Response, uow: UnitOfWork = Depends(get_uow)):
    with uow:
        usuario = usuario_service.autenticar_usuario(uow, data.email, data.password)
        access_token = create_access_token(subject=usuario.id)
        
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            max_age=1800,
            samesite="lax"
        )
        return {"message": "Login exitoso", "rol": [r.nombre for r in usuario.roles]}

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Deslogueado"}

@router.get("/me", response_model=UsuarioRead)
def get_me(current_user: Usuario = Depends(get_current_user)):
    return current_user
