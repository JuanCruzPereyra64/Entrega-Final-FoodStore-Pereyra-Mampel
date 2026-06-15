from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlmodel import select
from backend.database import get_uow
from backend.schemas.producto import ProductoCreate, ProductoRead, ProductoUpdate, ProductoIngredienteRead, AddIngredienteRequest
from backend.schemas.pagination import PaginatedResponse
from backend.services import producto_service
from backend.uow.unit_of_work import UnitOfWork
from backend.models.usuario import Usuario
from backend.models.producto import ProductoIngrediente
from backend.api.deps import check_role

router = APIRouter(prefix="/api/v1/productos", tags=["Productos"])

@router.get("/", response_model=PaginatedResponse[ProductoRead])
def get_productos(
    uow: UnitOfWork = Depends(get_uow),
    categoria_id: Annotated[Optional[int], Query(description="Filtrar por categoría")] = None,
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 20,
):
    with uow:
        items = producto_service.get_all(uow, categoria_id, page, size)
        total = producto_service.count_all(uow, categoria_id)
        return PaginatedResponse.create(items=items, total=total, page=page, size=size)

@router.get("/{producto_id}", response_model=ProductoRead)
def get_producto(producto_id: int, uow: UnitOfWork = Depends(get_uow)):
    with uow:
        return producto_service.get_by_id(uow, producto_id)

@router.post("/", response_model=ProductoRead, status_code=201)
def create_producto(
    data: ProductoCreate, 
    current_user: Usuario = Depends(check_role(["ADMIN"])),
    uow: UnitOfWork = Depends(get_uow)
):
    with uow:
        return producto_service.create(uow, data)

@router.put("/{producto_id}", response_model=ProductoRead)
def update_producto(
    producto_id: int, 
    data: ProductoUpdate, 
    current_user: Usuario = Depends(check_role(["ADMIN"])),
    uow: UnitOfWork = Depends(get_uow)
):
    with uow:
        return producto_service.update(uow, producto_id, data)

@router.delete("/{producto_id}", status_code=204)
def delete_producto(
    producto_id: int, 
    current_user: Usuario = Depends(check_role(["ADMIN"])),
    uow: UnitOfWork = Depends(get_uow)
):
    with uow:
        producto_service.delete(uow, producto_id)

@router.post("/{producto_id}/ingredientes", response_model=ProductoIngredienteRead, status_code=201)
def add_ingrediente(
    producto_id: int, 
    data: AddIngredienteRequest,
    current_user: Usuario = Depends(check_role(["ADMIN"])),
    uow: UnitOfWork = Depends(get_uow)
):
    with uow:
        return producto_service.add_ingrediente(uow, producto_id, data.ingrediente_id, data.cantidad, data.unidad_medida_id)

@router.delete("/{producto_id}/ingredientes/{ingrediente_id}", response_model=ProductoRead)
def remove_ingrediente(
    producto_id: int, 
    ingrediente_id: int, 
    current_user: Usuario = Depends(check_role(["ADMIN"])),
    uow: UnitOfWork = Depends(get_uow)
):
    with uow:
        return producto_service.remove_ingrediente(uow, producto_id, ingrediente_id)

class ProductoDisponibilidad(BaseModel):
    disponible: bool

@router.patch("/{producto_id}/disponibilidad", response_model=ProductoRead)
def update_disponibilidad(
    producto_id: int,
    data: ProductoDisponibilidad,
    current_user: Usuario = Depends(check_role(["ADMIN", "STOCK"])),
    uow: UnitOfWork = Depends(get_uow)
):
    with uow:
        return producto_service.update_disponibilidad(uow, producto_id, data.disponible)


class StockUpdate(BaseModel):
    stock_cantidad: int


@router.patch("/{producto_id}/stock", response_model=ProductoRead)
def update_stock(
    producto_id: int,
    data: StockUpdate,
    current_user: Usuario = Depends(check_role(["ADMIN", "STOCK"])),
    uow: UnitOfWork = Depends(get_uow)
):
    with uow:
        producto = producto_service.get_by_id(uow, producto_id)
        producto.stock_cantidad = data.stock_cantidad
        uow.productos.add(producto)
        uow.session.flush()
        uow.session.refresh(producto)
        return producto


class ImagenesUpdate(BaseModel):
    imagenes_url: list[str]

@router.patch("/{producto_id}/imagenes", response_model=ProductoRead)
def update_imagenes(
    producto_id: int,
    data: ImagenesUpdate,
    current_user: Usuario = Depends(check_role(["ADMIN"])),
    uow: UnitOfWork = Depends(get_uow)
):
    with uow:
        producto = producto_service.get_by_id(uow, producto_id)
        producto.imagenes_url = data.imagenes_url
        uow.productos.add(producto)
        uow.session.flush()
        uow.session.refresh(producto)
        return producto


@router.get("/{producto_id}/ingredientes", response_model=list[ProductoIngredienteRead])
def get_producto_ingredientes(
    producto_id: int,
    uow: UnitOfWork = Depends(get_uow)
):
    with uow:
        links = uow.session.exec(select(ProductoIngrediente).where(ProductoIngrediente.producto_id == producto_id)).all()
        return links
