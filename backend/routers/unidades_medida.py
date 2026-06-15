from typing import List
from fastapi import APIRouter, Depends, HTTPException
from backend.database import get_uow
from backend.uow.unit_of_work import UnitOfWork
from backend.schemas.unidad_medida import UnidadMedidaRead, UnidadMedidaCreate, UnidadMedidaUpdate
from backend.models.unidad_medida import UnidadMedida
from backend.models.usuario import Usuario
from backend.api.deps import check_role

router = APIRouter(prefix="/api/v1/unidades-medida", tags=["unidades-medida"])

@router.get("/", response_model=List[UnidadMedidaRead])
def get_unidades_medida(current_user: Usuario = Depends(check_role(["ADMIN"])), uow: UnitOfWork = Depends(get_uow)):
    with uow:
        return uow.unidades_medida.get_all()

@router.get("/{id}", response_model=UnidadMedidaRead)
def get_unidad_medida(id: int, current_user: Usuario = Depends(check_role(["ADMIN"])), uow: UnitOfWork = Depends(get_uow)):
    with uow:
        unidad = uow.unidades_medida.get_by_id(id)
        if not unidad:
            raise HTTPException(status_code=404, detail="Unidad de medida no encontrada")
        return unidad

@router.post("/", response_model=UnidadMedidaRead)
def create_unidad_medida(data: UnidadMedidaCreate, current_user: Usuario = Depends(check_role(["ADMIN"])), uow: UnitOfWork = Depends(get_uow)):
    with uow:
        # Check duplicate
        existing = uow.session.query(UnidadMedida).filter(UnidadMedida.nombre == data.nombre).first()
        if existing:
            raise HTTPException(status_code=400, detail="Ya existe una unidad de medida con ese nombre")
        nueva = UnidadMedida(**data.model_dump())
        uow.unidades_medida.add(nueva)
        uow.session.commit()
        uow.session.refresh(nueva)
        return nueva

@router.put("/{id}", response_model=UnidadMedidaRead)
def update_unidad_medida(id: int, data: UnidadMedidaUpdate, current_user: Usuario = Depends(check_role(["ADMIN"])), uow: UnitOfWork = Depends(get_uow)):
    with uow:
        unidad = uow.unidades_medida.get_by_id(id)
        if not unidad:
            raise HTTPException(status_code=404, detail="Unidad de medida no encontrada")
        if data.nombre is not None:
            unidad.nombre = data.nombre
        uow.session.commit()
        uow.session.refresh(unidad)
        return unidad

@router.delete("/{id}")
def delete_unidad_medida(id: int, current_user: Usuario = Depends(check_role(["ADMIN"])), uow: UnitOfWork = Depends(get_uow)):
    with uow:
        unidad = uow.unidades_medida.get_by_id(id)
        if not unidad:
            raise HTTPException(status_code=404, detail="Unidad de medida no encontrada")
        # Ensure it's not being used
        if unidad.ingredientes:
            raise HTTPException(status_code=400, detail="No se puede eliminar la unidad de medida porque está siendo usada por uno o más ingredientes")
        uow.unidades_medida.delete(unidad)
        uow.session.commit()
        return {"ok": True}
