from decimal import Decimal
from sqlmodel import SQLModel


class VentasPeriodoItem(SQLModel):
    periodo: str
    total_ventas: Decimal
    cantidad_pedidos: int


class ProductoTopItem(SQLModel):
    producto_id: int
    nombre: str
    cantidad_vendida: int
    ingresos: Decimal


class PedidosEstadoItem(SQLModel):
    estado_codigo: str
    cantidad: int


class ResumenResponse(SQLModel):
    ventas_hoy: Decimal
    ticket_promedio: Decimal
    pedidos_activos: int
    total_mes_actual: Decimal


class IngresosResponse(SQLModel):
    forma_pago_codigo: str
    total: Decimal
    cantidad: int
