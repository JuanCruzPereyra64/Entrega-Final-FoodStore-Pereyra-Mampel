from datetime import datetime, timezone
from fastapi import HTTPException
from sqlmodel import select, Session
from backend.models.usuario import Usuario
from backend.models.usuario_rol import UsuarioRol
from backend.models.rol import Rol
from backend.uow.unit_of_work import UnitOfWork


def get_usuarios(uow: UnitOfWork, rol: str = None, offset: int = 0, limit: int = 100) -> list[Usuario]:
    query = select(Usuario).where(Usuario.deleted_at == None)
    if rol:
        query = query.join(UsuarioRol).join(Rol).where(Rol.nombre == rol)
    return uow.session.exec(query.offset(offset).limit(limit)).all()


def delete_usuario(uow: UnitOfWork, usuario_id: int) -> None:
    usuario = uow.usuarios.get_by_id(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario.deleted_at = datetime.now(timezone.utc)
    uow.usuarios.add(usuario)
    uow.session.flush()


def assign_roles(uow: UnitOfWork, usuario_id: int, roles: list[str]) -> Usuario:
    usuario = uow.usuarios.get_by_id(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

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
