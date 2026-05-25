from fastapi import HTTPException
from backend.models.categoria import Categoria
from backend.schemas.categoria import CategoriaCreate, CategoriaUpdate
from backend.uow.unit_of_work import UnitOfWork


def get_all(uow: UnitOfWork, offset: int = 0, limit: int = 100) -> list[Categoria]:
    return uow.categorias.get_all(offset, limit)


def get_by_id(uow: UnitOfWork, categoria_id: int) -> Categoria:
    categoria = uow.categorias.get_by_id(categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria


def create(uow: UnitOfWork, data: CategoriaCreate) -> Categoria:
    categoria = Categoria.model_validate(data)
    uow.categorias.add(categoria)
    uow.session.flush()
    uow.session.refresh(categoria)
    return categoria


def update(uow: UnitOfWork, categoria_id: int, data: CategoriaUpdate) -> Categoria:
    categoria = get_by_id(uow, categoria_id)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(categoria, key, value)
    uow.categorias.add(categoria)
    uow.session.flush()
    uow.session.refresh(categoria)
    return categoria


def delete(uow: UnitOfWork, categoria_id: int) -> None:
    categoria = get_by_id(uow, categoria_id)
    if any(p.deleted_at is None for p in categoria.productos):
        raise HTTPException(status_code=409, detail="No se puede eliminar la categoria porque tiene productos activos")
    uow.categorias.delete(categoria)
    uow.session.flush()
