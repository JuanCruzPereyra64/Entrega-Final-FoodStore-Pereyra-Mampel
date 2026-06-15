from fastapi import APIRouter, Body, Depends, HTTPException, Request, status, Response
from backend.database import get_uow
from backend.schemas.token import TokenResponse
from backend.schemas.usuario import UsuarioCreate, UsuarioRead, UsuarioReadWithRoles, UsuarioLogin, UsuarioUpdate
from backend.core.security import create_access_token, create_refresh_token
from backend.core.limiter import limiter
from backend.services import usuario_service
from backend.uow.unit_of_work import UnitOfWork
from backend.models.usuario import Usuario
from backend.api.deps import get_current_user
from backend.core.config import settings

router = APIRouter(prefix="/api/v1/auth", tags=["Usuarios"])


@router.post("/registro", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/15minutes")
def registro(request: Request, data: UsuarioCreate, uow: UnitOfWork = Depends(get_uow)):
    with uow:
        return usuario_service.registrar_usuario(uow, data)


@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/15minutes")
def login(request: Request, data: UsuarioLogin, response: Response, uow: UnitOfWork = Depends(get_uow)):
    with uow:
        usuario = usuario_service.autenticar_usuario(uow, data.email, data.password)
        access_token = create_access_token(subject=usuario.id)
        refresh_token = create_refresh_token(subject=usuario.id)
        usuario_service.guardar_refresh_token(uow, usuario.id, refresh_token)

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            max_age=settings.access_token_expire_minutes * 60,
            samesite="lax",
        )
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.access_token_expire_minutes * 60,
        )


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(
    refresh_token_str: str = Body(..., alias="refresh_token"),
    uow: UnitOfWork = Depends(get_uow),
):
    with uow:
        usuario = usuario_service.validar_refresh_token(uow, refresh_token_str)

        new_access = create_access_token(subject=usuario.id)
        new_refresh = create_refresh_token(subject=usuario.id)
        usuario_service.guardar_refresh_token(uow, usuario.id, new_refresh)

        return TokenResponse(
            access_token=new_access,
            refresh_token=new_refresh,
            token_type="bearer",
            expires_in=settings.access_token_expire_minutes * 60,
        )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    refresh_token_str: str = Body(..., alias="refresh_token"),
    uow: UnitOfWork = Depends(get_uow),
    current_user: Usuario = Depends(get_current_user),
):
    with uow:
        usuario_service.revocar_refresh_token(uow, refresh_token_str)


@router.get("/me", response_model=UsuarioReadWithRoles)
def get_me(current_user: Usuario = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=UsuarioRead)
def update_me(
    data: UsuarioUpdate,
    current_user: Usuario = Depends(get_current_user),
    uow: UnitOfWork = Depends(get_uow),
):
    with uow:
        usuario = uow.usuarios.get_by_id(current_user.id)
        return usuario_service.actualizar_usuario(uow, usuario, data)
