from fastapi import HTTPException
from backend.models.unidad_medida import UnidadMedida
from backend.schemas.unidad_medida import UnidadMedidaCreate, UnidadMedidaUpdate
from backend.uow.unit_of_work import UnitOfWork


def get_all(uow: UnitOfWork) -> list[UnidadMedida]:
    return uow.unidades_medida.get_all()


def get_by_id(uow: UnitOfWork, id: int) -> UnidadMedida:
    unidad = uow.unidades_medida.get_by_id(id)
    if not unidad:
        raise HTTPException(status_code=404, detail="Unidad de medida no encontrada")
    return unidad


def create(uow: UnitOfWork, data: UnidadMedidaCreate) -> UnidadMedida:
    existing = uow.unidades_medida.get_all()
    for u in existing:
        if u.nombre == data.nombre:
            raise HTTPException(status_code=400, detail="Ya existe una unidad de medida con ese nombre")
    nueva = UnidadMedida(**data.model_dump())
    uow.unidades_medida.add(nueva)
    uow.flush()
    uow.unidades_medida.refresh(nueva)
    return nueva


def update(uow: UnitOfWork, id: int, data: UnidadMedidaUpdate) -> UnidadMedida:
    unidad = get_by_id(uow, id)
    if data.nombre is not None:
        unidad.nombre = data.nombre
    uow.unidades_medida.add(unidad)
    uow.flush()
    uow.unidades_medida.refresh(unidad)
    return unidad


def delete(uow: UnitOfWork, id: int) -> None:
    unidad = get_by_id(uow, id)
    if unidad.ingredientes:
        raise HTTPException(status_code=400, detail="No se puede eliminar la unidad de medida porque está siendo usada por uno o más ingredientes")
    uow.unidades_medida.delete(unidad)
    uow.flush()
