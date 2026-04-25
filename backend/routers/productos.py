from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Query
from backend.database import get_uow
from backend.schemas.producto import ProductoCreate, ProductoRead, ProductoUpdate
from backend.services import producto_service
from backend.uow.unit_of_work import UnitOfWork

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.get("/", response_model=list[ProductoRead])
def get_productos(
    uow: UnitOfWork = Depends(get_uow),
    categoria_id: Annotated[Optional[int], Query(description="Filtrar por categoría")] = None,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
):
    return producto_service.get_all(uow, categoria_id, offset, limit)


@router.get("/{producto_id}", response_model=ProductoRead)
def get_producto(producto_id: int, uow: UnitOfWork = Depends(get_uow)):
    return producto_service.get_by_id(uow, producto_id)


@router.post("/", response_model=ProductoRead, status_code=201)
def create_producto(data: ProductoCreate, uow: UnitOfWork = Depends(get_uow)):
    return producto_service.create(uow, data)


@router.put("/{producto_id}", response_model=ProductoRead)
def update_producto(producto_id: int, data: ProductoUpdate, uow: UnitOfWork = Depends(get_uow)):
    return producto_service.update(uow, producto_id, data)


@router.delete("/{producto_id}", status_code=204)
def delete_producto(producto_id: int, uow: UnitOfWork = Depends(get_uow)):
    producto_service.delete(uow, producto_id)


@router.post("/{producto_id}/ingredientes/{ingrediente_id}", response_model=ProductoRead)
def add_ingrediente(producto_id: int, ingrediente_id: int, uow: UnitOfWork = Depends(get_uow)):
    return producto_service.add_ingrediente(uow, producto_id, ingrediente_id)


@router.delete("/{producto_id}/ingredientes/{ingrediente_id}", response_model=ProductoRead)
def remove_ingrediente(producto_id: int, ingrediente_id: int, uow: UnitOfWork = Depends(get_uow)):
    return producto_service.remove_ingrediente(uow, producto_id, ingrediente_id)
