from pydantic import BaseModel
from fastapi import APIRouter, Depends, Request, status
from backend.database import get_uow
from backend.schemas.pago import PagoCreate, PagoResponse, PreferenciaCreate, PreferenciaResponse
from backend.services import pago_service
from backend.uow.unit_of_work import UnitOfWork
from backend.models.usuario import Usuario
from backend.api.deps import check_role
from backend.core.ws_manager import ws_manager
from backend.core.config import settings

router = APIRouter(prefix="/api/v1/pagos", tags=["Pagos"])


class PublicKeyResponse(BaseModel):
    public_key: str


@router.get("/public-key", response_model=PublicKeyResponse)
def get_public_key():
    return PublicKeyResponse(public_key=settings.mp_public_key)


@router.post("/preferencia", response_model=PreferenciaResponse, status_code=status.HTTP_201_CREATED)
def crear_preferencia(
    data: PreferenciaCreate,
    current_user: Usuario = Depends(check_role(["CLIENT"])),
    uow: UnitOfWork = Depends(get_uow)
):
    with uow:
        return pago_service.crear_preferencia(
            uow,
            current_user.id,
            data.pedido_id,
            data.email,
            {
                "success": data.back_url_success,
                "failure": data.back_url_failure,
                "pending": data.back_url_pending,
            }
        )


@router.post("/crear", response_model=PagoResponse, status_code=status.HTTP_201_CREATED)
def crear_pago(
    data: PagoCreate,
    current_user: Usuario = Depends(check_role(["CLIENT"])),
    uow: UnitOfWork = Depends(get_uow)
):
    with uow:
        return pago_service.crear_pago(uow, current_user.id, data)


@router.post("/webhook")
async def webhook_pago(
    request: Request,
    uow: UnitOfWork = Depends(get_uow)
):
    mp_payment_id = None
    try:
        body = await request.json()
        if isinstance(body.get("data"), dict) and body["data"].get("id"):
            mp_payment_id = int(body["data"]["id"])
        elif body.get("id"):
            mp_payment_id = int(body["id"])
    except Exception:
        form = await request.form()
        if form.get("id"):
            mp_payment_id = int(form["id"])
        elif form.get("topic") == "payment" and form.get("id"):
            mp_payment_id = int(form["id"])

    pago = None
    usuario_id = None
    if mp_payment_id:
        with uow:
            pago = pago_service.procesar_webhook(uow, mp_payment_id)
            if pago:
                pedido = uow.pedidos.get_by_id(pago.pedido_id)
                usuario_id = pedido.usuario_id if pedido else None

    if pago and pago.mp_status == "approved":
        evento = ws_manager._build_evento(
            event_type="pago_confirmado",
            pedido_id=pago.pedido_id,
            estado_anterior="PENDIENTE",
            estado_nuevo="CONFIRMADO",
            usuario_id=None,
            motivo="Pago confirmado vía MercadoPago",
        )
        ws_manager.broadcast_pedido(pago.pedido_id, evento)
        if usuario_id:
            ws_manager.broadcast_to_user(usuario_id, evento)

    return {"status": "ok"}


@router.get("/{pedido_id}", response_model=PagoResponse)
def get_pago(
    pedido_id: int,
    current_user: Usuario = Depends(check_role(["CLIENT", "ADMIN"])),
    uow: UnitOfWork = Depends(get_uow)
):
    with uow:
        return pago_service.get_pago_by_pedido(uow, pedido_id, current_user.id)
