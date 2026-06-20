from datetime import date, datetime, time, timezone
from decimal import Decimal
from collections import defaultdict
from sqlmodel import Session, select, func
from backend.models.pedido import Pedido
from backend.models.detalle_pedido import DetallePedido
from backend.models.pago import Pago
from backend.schemas.estadisticas import (
    VentasPeriodoItem,
    ProductoTopItem,
    PedidosEstadoItem,
    ResumenResponse,
    IngresosResponse,
)


class EstadisticasRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_ventas_periodo(self, desde: date, hasta: date, agrupacion: str = "day") -> list[VentasPeriodoItem]:
        desde_dt = datetime.combine(desde, time.min).replace(tzinfo=timezone.utc)
        hasta_dt = datetime.combine(hasta, time.max).replace(tzinfo=timezone.utc)

        stmt = select(Pedido).where(
            Pedido.deleted_at.is_(None),
            Pedido.estado_codigo != "CANCELADO",
            Pedido.created_at >= desde_dt,
            Pedido.created_at <= hasta_dt,
        )
        pedidos = self.session.exec(stmt).all()

        fmt_map = {"day": "%Y-%m-%d", "week": "%Y-W%W", "month": "%Y-%m"}
        fmt = fmt_map.get(agrupacion, "%Y-%m-%d")

        grupos: dict[str, dict] = defaultdict(lambda: {"total_ventas": Decimal("0.00"), "cantidad_pedidos": 0})
        for p in pedidos:
            key = p.created_at.strftime(fmt)
            grupos[key]["total_ventas"] += p.total
            grupos[key]["cantidad_pedidos"] += 1

        return [VentasPeriodoItem(periodo=k, **v) for k, v in sorted(grupos.items())]

    def get_productos_top(self, limit: int = 10) -> list[ProductoTopItem]:
        stmt = (
            select(
                DetallePedido.producto_id,
                DetallePedido.nombre_producto_snap.label("nombre"),
                func.sum(DetallePedido.cantidad).label("cantidad_vendida"),
                func.sum(DetallePedido.subtotal_snap).label("ingresos"),
            )
            .join(Pedido, DetallePedido.pedido_id == Pedido.id)
            .where(
                Pedido.deleted_at.is_(None),
                Pedido.estado_codigo != "CANCELADO",
            )
            .group_by(DetallePedido.producto_id, DetallePedido.nombre_producto_snap)
            .order_by(func.sum(DetallePedido.subtotal_snap).desc())
            .limit(limit)
        )
        rows = self.session.exec(stmt).all()
        return [
            ProductoTopItem(
                producto_id=r.producto_id,
                nombre=r.nombre,
                cantidad_vendida=int(r.cantidad_vendida) if r.cantidad_vendida else 0,
                ingresos=Decimal(str(r.ingresos)) if r.ingresos else Decimal("0.00"),
            )
            for r in rows
        ]

    def get_pedidos_por_estado(self) -> list[PedidosEstadoItem]:
        stmt = (
            select(
                Pedido.estado_codigo,
                func.count(Pedido.id).label("cantidad"),
            )
            .where(Pedido.deleted_at.is_(None))
            .group_by(Pedido.estado_codigo)
        )
        rows = self.session.exec(stmt).all()
        return [
            PedidosEstadoItem(estado_codigo=r.estado_codigo, cantidad=int(r.cantidad))
            for r in rows
        ]

    def get_resumen_kpis(self) -> ResumenResponse:
        today_start = datetime.combine(date.today(), time.min).replace(tzinfo=timezone.utc)
        month_start = datetime.combine(date.today().replace(day=1), time.min).replace(tzinfo=timezone.utc)

        base = (Pedido.deleted_at.is_(None), Pedido.estado_codigo != "CANCELADO")

        ventas_hoy = self.session.exec(
            select(func.sum(Pedido.total)).where(*base, Pedido.created_at >= today_start)
        ).first() or Decimal("0.00")

        ticket_promedio = self.session.exec(
            select(func.avg(Pedido.total)).where(*base)
        ).first() or Decimal("0.00")

        pedidos_activos = self.session.exec(
            select(func.count(Pedido.id)).where(
                Pedido.deleted_at.is_(None),
                Pedido.estado_codigo.not_in(["ENTREGADO", "CANCELADO"]),
            )
        ).first() or 0

        total_mes_actual = self.session.exec(
            select(func.sum(Pedido.total)).where(*base, Pedido.created_at >= month_start)
        ).first() or Decimal("0.00")

        return ResumenResponse(
            ventas_hoy=Decimal(str(ventas_hoy)),
            ticket_promedio=Decimal(str(ticket_promedio)),
            pedidos_activos=int(pedidos_activos),
            total_mes_actual=Decimal(str(total_mes_actual)),
        )

    def get_ingresos_por_forma_pago(self, desde: date | None = None, hasta: date | None = None) -> list[IngresosResponse]:
        stmt = (
            select(
                Pedido.forma_pago_codigo,
                func.sum(Pedido.total).label("total"),
                func.count(Pedido.id).label("cantidad"),
            )
            .join(Pago, Pago.pedido_id == Pedido.id)
            .where(
                Pedido.deleted_at.is_(None),
                Pago.mp_status == "approved",
            )
        )

        if desde:
            desde_dt = datetime.combine(desde, time.min).replace(tzinfo=timezone.utc)
            stmt = stmt.where(Pedido.created_at >= desde_dt)
        if hasta:
            hasta_dt = datetime.combine(hasta, time.max).replace(tzinfo=timezone.utc)
            stmt = stmt.where(Pedido.created_at <= hasta_dt)

        stmt = stmt.group_by(Pedido.forma_pago_codigo)

        rows = self.session.exec(stmt).all()
        return [
            IngresosResponse(
                forma_pago_codigo=r.forma_pago_codigo,
                total=Decimal(str(r.total)) if r.total else Decimal("0.00"),
                cantidad=int(r.cantidad),
            )
            for r in rows
        ]
