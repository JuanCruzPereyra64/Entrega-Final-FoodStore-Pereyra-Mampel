from decimal import Decimal
from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel, Column, BigInteger, String, Numeric, DateTime, ForeignKey, Integer

if TYPE_CHECKING:
    from backend.models.pedido import Pedido


class Pago(SQLModel, table=True):
    __tablename__ = "pagos"

    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )
    pedido_id: int = Field(
        sa_column=Column(BigInteger, ForeignKey("pedidos.id", ondelete="RESTRICT"), nullable=False)
    )
    mp_payment_id: Optional[int] = Field(
        default=None,
        sa_column=Column(BigInteger)
    )
    mp_status: str = Field(
        default="pending",
        sa_column=Column(String(30), nullable=False)
    )
    mp_status_detail: Optional[str] = Field(
        default=None,
        sa_column=Column(String(100))
    )
    transaction_amount: Decimal = Field(
        sa_column=Column(Numeric(10, 2), nullable=False)
    )
    payment_method_id: Optional[str] = Field(
        default=None,
        sa_column=Column(String(50))
    )
    payer_email: Optional[str] = Field(
        default=None,
        sa_column=Column(String(150))
    )
    installments: Optional[int] = Field(
        default=None,
        sa_column=Column(Integer)
    )
    external_reference: str = Field(
        sa_column=Column(String(100), nullable=False, unique=True)
    )
    idempotency_key: str = Field(
        sa_column=Column(String(100), nullable=False, unique=True)
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )

    pedido: "Pedido" = Relationship(back_populates="pago")
