from datetime import datetime, timezone
from fastapi import HTTPException
from backend.uow.unit_of_work import UnitOfWork


def get_usuarios(uow: UnitOfWork, rol: str = None, offset: int = 0, limit: int = 100) -> list:
    return uow.usuarios.get_all_with_filters(rol, offset, limit)


def delete_usuario(uow: UnitOfWork, usuario_id: int) -> None:
    usuario = uow.usuarios.get_by_id(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario.deleted_at = datetime.now(timezone.utc)
    uow.usuarios.add(usuario)
    uow.flush()


def assign_roles(uow: UnitOfWork, usuario_id: int, roles: list[str]) -> None:
    usuario = uow.usuarios.get_by_id(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    links = uow.usuarios.get_usuario_roles(usuario_id)
    for link in links:
        uow.usuarios.delete_usuario_rol(link)

    for r_name in roles:
        rol_obj = uow.roles.get_by_nombre(r_name)
        if rol_obj:
            uow.usuarios.add_usuario_rol(usuario.id, rol_obj.id)

    uow.flush()
    uow.usuarios.refresh(usuario)
    return usuario
