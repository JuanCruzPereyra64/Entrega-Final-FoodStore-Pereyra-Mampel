from typing import Annotated
from fastapi import APIRouter, Depends, Query
from backend.database import get_uow
from backend.schemas.ingrediente import IngredienteCreate, IngredienteRead, IngredienteUpdate
from backend.services import ingrediente_service
from backend.uow.unit_of_work import UnitOfWork
from backend.models.usuario import Usuario
from backend.api.deps import check_role

router = APIRouter(prefix="/ingredientes", tags=["Ingredientes"])

@router.get("/", response_model=list[IngredienteRead])
def get_ingredientes(
    uow: UnitOfWork = Depends(get_uow),
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
):
    with uow:
        ingredientes = ingrediente_service.get_all(uow, offset, limit)
        return [IngredienteRead.model_validate(i) for i in ingredientes]

@router.get("/{ingrediente_id}", response_model=IngredienteRead)
def get_ingrediente(ingrediente_id: int, uow: UnitOfWork = Depends(get_uow)):
    with uow:
        ingrediente = ingrediente_service.get_by_id(uow, ingrediente_id)
        return IngredienteRead.model_validate(ingrediente)

@router.post("/", response_model=IngredienteRead, status_code=201)
def create_ingrediente(
    data: IngredienteCreate, 
    current_user: Usuario = Depends(check_role(["ADMIN", "STOCK"])),
    uow: UnitOfWork = Depends(get_uow)
):
    with uow:
        ingrediente = ingrediente_service.create(uow, data, current_user.id)
        return IngredienteRead.model_validate(ingrediente)

@router.put("/{ingrediente_id}", response_model=IngredienteRead)
def update_ingrediente(
    ingrediente_id: int, 
    data: IngredienteUpdate, 
    current_user: Usuario = Depends(check_role(["ADMIN", "STOCK"])),
    uow: UnitOfWork = Depends(get_uow)
):
    with uow:
        ingrediente = ingrediente_service.update(uow, ingrediente_id, data, current_user.id)
        return IngredienteRead.model_validate(ingrediente)

@router.delete("/{ingrediente_id}", status_code=204)
def delete_ingrediente(
    ingrediente_id: int, 
    current_user: Usuario = Depends(check_role(["ADMIN", "STOCK"])),
    uow: UnitOfWork = Depends(get_uow)
):
    with uow:
        ingrediente_service.delete(uow, ingrediente_id)
