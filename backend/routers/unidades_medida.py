from typing import List
from fastapi import APIRouter, Depends
from backend.database import get_uow
from backend.uow.unit_of_work import UnitOfWork
from backend.schemas.unidad_medida import UnidadMedidaRead, UnidadMedidaCreate, UnidadMedidaUpdate
from backend.models.usuario import Usuario
from backend.api.deps import check_role
from backend.services import unidad_medida_service

router = APIRouter(prefix="/api/v1/unidades-medida", tags=["unidades-medida"])

@router.get("/", response_model=List[UnidadMedidaRead])
def get_unidades_medida(current_user: Usuario = Depends(check_role(["ADMIN"])), uow: UnitOfWork = Depends(get_uow)):
    with uow:
        return unidad_medida_service.get_all(uow)

@router.get("/{id}", response_model=UnidadMedidaRead)
def get_unidad_medida(id: int, current_user: Usuario = Depends(check_role(["ADMIN"])), uow: UnitOfWork = Depends(get_uow)):
    with uow:
        return unidad_medida_service.get_by_id(uow, id)

@router.post("/", response_model=UnidadMedidaRead)
def create_unidad_medida(data: UnidadMedidaCreate, current_user: Usuario = Depends(check_role(["ADMIN"])), uow: UnitOfWork = Depends(get_uow)):
    with uow:
        return unidad_medida_service.create(uow, data)

@router.put("/{id}", response_model=UnidadMedidaRead)
def update_unidad_medida(id: int, data: UnidadMedidaUpdate, current_user: Usuario = Depends(check_role(["ADMIN"])), uow: UnitOfWork = Depends(get_uow)):
    with uow:
        return unidad_medida_service.update(uow, id, data)

@router.delete("/{id}")
def delete_unidad_medida(id: int, current_user: Usuario = Depends(check_role(["ADMIN"])), uow: UnitOfWork = Depends(get_uow)):
    with uow:
        unidad_medida_service.delete(uow, id)
        return {"ok": True}
