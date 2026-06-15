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
