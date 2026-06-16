from decimal import Decimal
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from sqlmodel import SQLModel


class PagoCreate(SQLModel):
    pedido_id: int
    transaction_amount: Decimal
    card_token_id: str
    email: str
    payment_method_id: Optional[str] = None
    installments: int = 1
    description: Optional[str] = None


class PreferenciaCreate(BaseModel):
    pedido_id: int
    email: str
    back_url_success: str = "http://localhost:5173/mis-pedidos"
    back_url_failure: str = "http://localhost:5173/carrito"
    back_url_pending: str = "http://localhost:5173/mis-pedidos"


class PreferenciaResponse(BaseModel):
    preference_id: str
    init_point: str
    sandbox_init_point: str


class MPNotification(BaseModel):
    id: Optional[int] = None
    type: Optional[str] = None
    data: Optional[dict] = None
    action: Optional[str] = None
    topic: Optional[str] = None


class PagoResponse(SQLModel):
    id: int
    pedido_id: int
    mp_payment_id: Optional[int] = None
    mp_status: str
    mp_status_detail: Optional[str] = None
    transaction_amount: Decimal
    payment_method_id: Optional[str] = None
    payer_email: Optional[str] = None
    installments: Optional[int] = None
    external_reference: str
    created_at: datetime
