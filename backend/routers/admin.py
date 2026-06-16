from fastapi import APIRouter, Depends
from backend.database import get_uow
from backend.uow.unit_of_work import UnitOfWork
from backend.api.deps import check_role
from backend.schemas.usuario import UsuarioRead
from backend.services import admin_service

router = APIRouter(prefix="/api/v1/admin", tags=["Admin"], dependencies=[Depends(check_role(["ADMIN"]))])


@router.get("/usuarios", response_model=list[UsuarioRead])
def get_usuarios(
    uow: UnitOfWork = Depends(get_uow),
    rol: str = None,
    offset: int = 0,
    limit: int = 100,
):
    with uow:
        return admin_service.get_usuarios(uow, rol, offset, limit)


@router.delete("/usuarios/{usuario_id}", status_code=204)
def delete_usuario(usuario_id: int, uow: UnitOfWork = Depends(get_uow)):
    with uow:
        admin_service.delete_usuario(uow, usuario_id)


@router.patch("/usuarios/{usuario_id}/roles", response_model=UsuarioRead)
def assign_roles(usuario_id: int, roles: list[str], uow: UnitOfWork = Depends(get_uow)):
    with uow:
        return admin_service.assign_roles(uow, usuario_id, roles)
