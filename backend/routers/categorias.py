from typing import Annotated
from fastapi import APIRouter, Depends, Query
from backend.database import get_uow
from backend.schemas.categoria import CategoriaCreate, CategoriaRead, CategoriaUpdate
from backend.services import categoria_service
from backend.uow.unit_of_work import UnitOfWork

router = APIRouter(prefix="/categorias", tags=["Categorías"])


@router.get("/", response_model=list[CategoriaRead])
def get_categorias(
    uow: UnitOfWork = Depends(get_uow),
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
):
    return categoria_service.get_all(uow, offset, limit)


@router.get("/{categoria_id}", response_model=CategoriaRead)
def get_categoria(categoria_id: int, uow: UnitOfWork = Depends(get_uow)):
    return categoria_service.get_by_id(uow, categoria_id)


@router.post("/", response_model=CategoriaRead, status_code=201)
def create_categoria(data: CategoriaCreate, uow: UnitOfWork = Depends(get_uow)):
    return categoria_service.create(uow, data)


@router.put("/{categoria_id}", response_model=CategoriaRead)
def update_categoria(categoria_id: int, data: CategoriaUpdate, uow: UnitOfWork = Depends(get_uow)):
    return categoria_service.update(uow, categoria_id, data)


@router.delete("/{categoria_id}", status_code=204)
def delete_categoria(categoria_id: int, uow: UnitOfWork = Depends(get_uow)):
    categoria_service.delete(uow, categoria_id)
