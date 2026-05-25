from fastapi import APIRouter, Depends, status
from backend.database import get_uow
from backend.schemas.direccion import DireccionCreate, DireccionRead, DireccionUpdate
from backend.services import direccion_service
from backend.uow.unit_of_work import UnitOfWork
from backend.models.usuario import Usuario
from backend.api.deps import get_current_user

router = APIRouter(prefix="/direcciones", tags=["Direcciones"])

@router.get("/", response_model=list[DireccionRead])
def get_direcciones(
    current_user: Usuario = Depends(get_current_user),
    uow: UnitOfWork = Depends(get_uow)
):
    with uow:
        return direccion_service.get_by_user(uow, current_user.id)

@router.post("/", response_model=DireccionRead, status_code=201)
def create_direccion(
    data: DireccionCreate,
    current_user: Usuario = Depends(get_current_user),
    uow: UnitOfWork = Depends(get_uow)
):
    with uow:
        return direccion_service.create(uow, current_user.id, data)

@router.put("/{direccion_id}", response_model=DireccionRead)
def update_direccion(
    direccion_id: int,
    data: DireccionUpdate,
    current_user: Usuario = Depends(get_current_user),
    uow: UnitOfWork = Depends(get_uow)
):
    with uow:
        return direccion_service.update(uow, direccion_id, current_user.id, data)

@router.patch("/{direccion_id}/principal", response_model=DireccionRead)
def set_principal(
    direccion_id: int,
    current_user: Usuario = Depends(get_current_user),
    uow: UnitOfWork = Depends(get_uow)
):
    with uow:
        return direccion_service.set_principal(uow, direccion_id, current_user.id)

@router.delete("/{direccion_id}", status_code=204)
def delete_direccion(
    direccion_id: int,
    current_user: Usuario = Depends(get_current_user),
    uow: UnitOfWork = Depends(get_uow)
):
    with uow:
        direccion_service.delete(uow, direccion_id, current_user.id)
