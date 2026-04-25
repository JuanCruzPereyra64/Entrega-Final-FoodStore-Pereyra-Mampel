from typing import Optional
from fastapi import HTTPException
from sqlmodel import select
from backend.models.producto import Producto, ProductoIngrediente, ProductoCategoria
from backend.schemas.producto import ProductoCreate, ProductoUpdate
from backend.services import categoria_service, ingrediente_service
from backend.uow.unit_of_work import UnitOfWork


def get_all(uow: UnitOfWork, categoria_id: Optional[int] = None, offset: int = 0, limit: int = 100) -> list[Producto]:
    return uow.productos.get_all(categoria_id, offset, limit)


def get_by_id(uow: UnitOfWork, producto_id: int) -> Producto:
    producto = uow.productos.get_by_id(producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


def create(uow: UnitOfWork, data: ProductoCreate) -> Producto:
    # Validar categorías
    for cat_id in data.categoria_ids:
        categoria_service.get_by_id(uow, cat_id)
    
    # Validar ingredientes
    for ing_id in data.ingrediente_ids:
        ingrediente_service.get_by_id(uow, ing_id)
        
    producto = Producto.model_validate(data, update={"categorias": [], "ingredientes": []})
    uow.productos.add(producto)
    uow.commit()
    uow.session.refresh(producto)
    
    # Unir categorías
    for cat_id in data.categoria_ids:
        link_cat = ProductoCategoria(producto_id=producto.id, categoria_id=cat_id)
        uow.session.add(link_cat)

    # Unir ingredientes
    for ing_id in data.ingrediente_ids:
        link_ing = ProductoIngrediente(producto_id=producto.id, ingrediente_id=ing_id)
        uow.session.add(link_ing)
    
    uow.commit()
    return get_by_id(uow, producto.id)


def update(uow: UnitOfWork, producto_id: int, data: ProductoUpdate) -> Producto:
    producto = get_by_id(uow, producto_id)
    
    if data.categoria_ids is not None:
        links_cat = uow.session.exec(select(ProductoCategoria).where(ProductoCategoria.producto_id == producto_id)).all()
        for link in links_cat:
            uow.session.delete(link)
        
        for cat_id in data.categoria_ids:
            categoria_service.get_by_id(uow, cat_id)
            link_cat = ProductoCategoria(producto_id=producto.id, categoria_id=cat_id)
            uow.session.add(link_cat)
    
    if data.ingrediente_ids is not None:
        links_ing = uow.session.exec(select(ProductoIngrediente).where(ProductoIngrediente.producto_id == producto_id)).all()
        for link in links_ing:
            uow.session.delete(link)
        
        for ing_id in data.ingrediente_ids:
            ingrediente_service.get_by_id(uow, ing_id)
            link = ProductoIngrediente(producto_id=producto_id, ingrediente_id=ing_id)
            uow.session.add(link)

    for key, value in data.model_dump(exclude_unset=True, exclude={"ingrediente_ids", "categoria_ids"}).items():
        setattr(producto, key, value)
    
    uow.productos.add(producto)
    uow.commit()
    return get_by_id(uow, producto_id)


def delete(uow: UnitOfWork, producto_id: int) -> None:
    producto = get_by_id(uow, producto_id)
    uow.productos.delete(producto)
    uow.commit()


def add_ingrediente(uow: UnitOfWork, producto_id: int, ingrediente_id: int) -> Producto:
    producto = get_by_id(uow, producto_id)
    ingrediente_service.get_by_id(uow, ingrediente_id)
    
    existing = uow.session.get(ProductoIngrediente, (producto_id, ingrediente_id))
    if not existing:
        link = ProductoIngrediente(producto_id=producto_id, ingrediente_id=ingrediente_id)
        uow.session.add(link)
        uow.commit()
    
    return get_by_id(uow, producto_id)


def remove_ingrediente(uow: UnitOfWork, producto_id: int, ingrediente_id: int) -> Producto:
    link = uow.session.get(ProductoIngrediente, (producto_id, ingrediente_id))
    if not link:
        raise HTTPException(status_code=404, detail="Ingrediente no presente en el producto")
    uow.session.delete(link)
    uow.commit()
    return get_by_id(uow, producto_id)
