from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import select
from datetime import datetime, timezone
from backend.database import get_uow
from backend.uow.unit_of_work import UnitOfWork
from backend.models.usuario import Usuario
from backend.models.usuario_rol import UsuarioRol
from backend.models.rol import Rol
from backend.api.deps import check_role
from backend.schemas.usuario import UsuarioRead

router = APIRouter(prefix="/api/v1/admin", tags=["Admin"], dependencies=[Depends(check_role(["ADMIN"]))])

@router.get("/usuarios", response_model=list[UsuarioRead])
def get_usuarios(
    uow: UnitOfWork = Depends(get_uow),
    rol: str = None,
    offset: int = 0,
    limit: int = 100
):
    with uow:
        query = select(Usuario).where(Usuario.deleted_at == None)
        if rol:
            query = query.join(UsuarioRol).join(Rol).where(Rol.nombre == rol)
        return uow.session.exec(query.offset(offset).limit(limit)).all()

@router.delete("/usuarios/{usuario_id}", status_code=204)
def delete_usuario(usuario_id: int, uow: UnitOfWork = Depends(get_uow)):
    with uow:
        usuario = uow.usuarios.get_by_id(usuario_id)
        if not usuario:
            raise HTTPException(404)
        usuario.deleted_at = datetime.now(timezone.utc)
        uow.usuarios.add(usuario)
        uow.session.flush()

@router.patch("/usuarios/{usuario_id}/roles", response_model=UsuarioRead)
def assign_roles(usuario_id: int, roles: list[str], uow: UnitOfWork = Depends(get_uow)):
    with uow:
        usuario = uow.usuarios.get_by_id(usuario_id)
        if not usuario:
            raise HTTPException(404)
            
        links = uow.session.exec(select(UsuarioRol).where(UsuarioRol.usuario_id == usuario_id)).all()
        for link in links:
            uow.session.delete(link)
            
        for r_name in roles:
            rol_obj = uow.session.exec(select(Rol).where(Rol.nombre == r_name)).first()
            if rol_obj:
                uow.session.add(UsuarioRol(usuario_id=usuario.id, rol_id=rol_obj.id))
        
        uow.session.flush()
        uow.session.refresh(usuario)
        return usuario
