import uuid
from decimal import Decimal
from datetime import datetime, timezone
from fastapi import HTTPException
from backend.models.pago import Pago
from backend.models.pedido import Pedido
from backend.uow.unit_of_work import UnitOfWork
from backend.schemas.pago import PagoCreate
from backend.core.config import mp_sdk, settings


def crear_pago(uow: UnitOfWork, usuario_id: int, data: PagoCreate) -> Pago:
    pedido = uow.pedidos.get_by_id(data.pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    if pedido.usuario_id != usuario_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para pagar este pedido")

    if pedido.estado_codigo != "PENDIENTE":
        raise HTTPException(status_code=400, detail=f"El pedido no está pendiente de pago. Estado actual: {pedido.estado_codigo}")

    existing = uow.pagos.get_by_pedido_id(data.pedido_id)
    if existing:
        if existing.mp_status == "approved":
            raise HTTPException(status_code=400, detail="El pedido ya está pagado")
        return existing

    if mp_sdk is None:
        raise HTTPException(status_code=500, detail="MercadoPago no configurado")

    idempotency_key = str(uuid.uuid4())

    payment_data = {
        "token": data.card_token_id,
        "transaction_amount": float(data.transaction_amount),
        "description": data.description or f"Food Store - Pedido #{data.pedido_id}",
        "installments": data.installments,
        "payer": {"email": data.email},
        "external_reference": str(data.pedido_id),
        "idempotency_key": idempotency_key,
    }
    if data.payment_method_id:
        payment_data["payment_method_id"] = data.payment_method_id
    if settings.mp_notification_url:
        payment_data["notification_url"] = settings.mp_notification_url

    result = mp_sdk.payment().create(payment_data)

    if result["status"] not in (200, 201):
        raise HTTPException(status_code=502, detail="Error al procesar el pago con MercadoPago")

    mp_response = result["response"]

    pago = Pago(
        pedido_id=data.pedido_id,
        transaction_amount=data.transaction_amount,
        external_reference=str(data.pedido_id),
        idempotency_key=idempotency_key,
        mp_payment_id=mp_response.get("id"),
        mp_status=mp_response.get("status", "pending"),
        mp_status_detail=mp_response.get("status_detail"),
        payment_method_id=mp_response.get("payment_method_id"),
        payer_email=data.email,
        installments=data.installments,
    )

    uow.pagos.add(pago)
    uow.session.flush()
    uow.session.refresh(pago)

    if mp_response.get("status") == "approved":
        pedido.estado_codigo = "CONFIRMADO"
        from backend.models.historial_estado_pedido import HistorialEstadoPedido
        historial = HistorialEstadoPedido(
            pedido_id=pedido.id,
            estado_desde="PENDIENTE",
            estado_hacia="CONFIRMADO",
            usuario_id=None,
            motivo="Pago aprobado inmediatamente"
        )
        uow.session.add(historial)
        uow.session.flush()

    return pago


def procesar_webhook(uow: UnitOfWork, mp_payment_id: int) -> Pago:
    if mp_sdk is None:
        raise HTTPException(status_code=500, detail="MercadoPago no configurado")

    result = mp_sdk.payment().get(mp_payment_id)
    if result["status"] != 200:
        raise HTTPException(status_code=502, detail="Error al consultar el pago en MercadoPago")

    mp_response = result["response"]
    external_ref = mp_response.get("external_reference", "")

    pago = uow.pagos.get_by_external_reference(external_ref)
    if not pago:
        pago = uow.pagos.get_by_mp_payment_id(mp_payment_id)
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")

    pago.mp_payment_id = mp_response["id"]
    pago.mp_status = mp_response["status"]
    pago.mp_status_detail = mp_response.get("status_detail")
    pago.payment_method_id = mp_response.get("payment_method_id")
    pago.updated_at = datetime.now(timezone.utc)

    uow.pagos.add(pago)

    if mp_response["status"] == "approved":
        pedido = uow.pedidos.get_by_id(pago.pedido_id)
        if pedido and pedido.estado_codigo == "PENDIENTE":
            pedido.estado_codigo = "CONFIRMADO"
            from backend.models.historial_estado_pedido import HistorialEstadoPedido
            historial = HistorialEstadoPedido(
                pedido_id=pedido.id,
                estado_desde="PENDIENTE",
                estado_hacia="CONFIRMADO",
                usuario_id=None,
                motivo="Pago confirmado vía webhook MP"
            )
            uow.session.add(historial)

    uow.session.flush()

    return pago


def get_pago_by_pedido(uow: UnitOfWork, pedido_id: int, usuario_id: int) -> Pago:
    pago = uow.pagos.get_by_pedido_id(pedido_id)
    if not pago:
        raise HTTPException(status_code=404, detail="No hay pago registrado para este pedido")

    pedido = uow.pedidos.get_by_id(pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    if pedido.usuario_id != usuario_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para ver este pago")

    return pago
