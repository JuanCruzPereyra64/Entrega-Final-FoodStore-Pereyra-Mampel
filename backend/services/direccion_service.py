from fastapi import HTTPException
from datetime import datetime, timezone
from backend.models.direccion_entrega import DireccionEntrega
from backend.schemas.direccion import DireccionCreate, DireccionUpdate
from backend.uow.unit_of_work import UnitOfWork

def get_by_user(uow: UnitOfWork, usuario_id: int) -> list[DireccionEntrega]:
    return uow.direcciones.get_by_user(usuario_id)

def get_by_id(uow: UnitOfWork, direccion_id: int, usuario_id: int) -> DireccionEntrega:
    direccion = uow.direcciones.get_by_id(direccion_id)
    if not direccion or direccion.usuario_id != usuario_id or direccion.deleted_at:
        raise HTTPException(status_code=404, detail="Direccion no encontrada")
    return direccion

def create(uow: UnitOfWork, usuario_id: int, data: DireccionCreate) -> DireccionEntrega:
    if data.es_principal:
        vieja_principal = uow.direcciones.get_principal(usuario_id)
        if vieja_principal:
            vieja_principal.es_principal = False
            uow.direcciones.add(vieja_principal)
            
    direccion = DireccionEntrega(**data.model_dump(), usuario_id=usuario_id)
    uow.direcciones.add(direccion)
    uow.session.flush()
    uow.session.refresh(direccion)
    return direccion

def update(uow: UnitOfWork, direccion_id: int, usuario_id: int, data: DireccionUpdate) -> DireccionEntrega:
    direccion = get_by_id(uow, direccion_id, usuario_id)
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(direccion, k, v)
    uow.direcciones.add(direccion)
    uow.session.flush()
    uow.session.refresh(direccion)
    return direccion

def set_principal(uow: UnitOfWork, direccion_id: int, usuario_id: int) -> DireccionEntrega:
    direccion = get_by_id(uow, direccion_id, usuario_id)
    if not direccion.es_principal:
        vieja = uow.direcciones.get_principal(usuario_id)
        if vieja:
            vieja.es_principal = False
            uow.direcciones.add(vieja)
        direccion.es_principal = True
        uow.direcciones.add(direccion)
        uow.session.flush()
        uow.session.refresh(direccion)
    return direccion

def delete(uow: UnitOfWork, direccion_id: int, usuario_id: int):
    direccion = get_by_id(uow, direccion_id, usuario_id)
    direccion.deleted_at = datetime.now(timezone.utc)
    uow.direcciones.add(direccion)
    uow.session.flush()
