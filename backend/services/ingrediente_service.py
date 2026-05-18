from fastapi import HTTPException
from backend.models.ingrediente import Ingrediente
from backend.schemas.ingrediente import IngredienteCreate, IngredienteUpdate
from backend.uow.unit_of_work import UnitOfWork


def get_all(uow: UnitOfWork, offset: int = 0, limit: int = 100) -> list[Ingrediente]:
    return uow.ingredientes.get_all(offset, limit)


def get_by_id(uow: UnitOfWork, ingrediente_id: int) -> Ingrediente:
    ingrediente = uow.ingredientes.get_by_id(ingrediente_id)
    if not ingrediente:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
    return ingrediente


def create(uow: UnitOfWork, data: IngredienteCreate) -> Ingrediente:
    ingrediente = Ingrediente.model_validate(data)
    uow.ingredientes.add(ingrediente)
    uow.session.flush()
    uow.session.refresh(ingrediente)
    return ingrediente


def update(uow: UnitOfWork, ingrediente_id: int, data: IngredienteUpdate) -> Ingrediente:
    ingrediente = get_by_id(uow, ingrediente_id)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(ingrediente, key, value)
    uow.ingredientes.add(ingrediente)
    uow.session.flush()
    uow.session.refresh(ingrediente)
    return ingrediente


def delete(uow: UnitOfWork, ingrediente_id: int) -> None:
    ingrediente = get_by_id(uow, ingrediente_id)
    uow.ingredientes.delete(ingrediente)
    uow.session.flush()
