from backend.uow.unit_of_work import UnitOfWork
from backend.models.movimiento_stock import MovimientoStock

def registrar_movimiento(
    uow: UnitOfWork,
    ingrediente_id: int,
    cantidad: float,
    motivo: str,
    usuario_id: int = None
) -> MovimientoStock:
    if cantidad == 0:
        return None
        
    tipo = 'INGRESO' if cantidad > 0 else 'EGRESO'
    
    movimiento = MovimientoStock(
        ingrediente_id=ingrediente_id,
        cantidad=abs(cantidad),
        tipo=tipo,
        motivo=motivo,
        usuario_id=usuario_id
    )
    
    uow.movimientos_stock.add(movimiento)
    return movimiento

def get_historial(uow: UnitOfWork, offset: int = 0, limit: int = 100, ingrediente_id: int = None):
    return uow.movimientos_stock.get_historial(ingrediente_id, offset, limit)
