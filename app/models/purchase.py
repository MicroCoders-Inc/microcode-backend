from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, DateTime, Numeric, ForeignKey, func, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.database import db
import secrets


class Purchase(db.Model):
    __tablename__ = "purchases"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    course_id: Mapped[int] = mapped_column(ForeignKey("course.id"), nullable=False)
    price_paid: Mapped[Decimal] = mapped_column(
        Numeric(precision=6, scale=2), nullable=False
    )
    discount_applied: Mapped[Decimal] = mapped_column(
        Numeric(precision=6, scale=2), nullable=False, default=0
    )
    final_price: Mapped[Decimal] = mapped_column(
        Numeric(precision=6, scale=2), nullable=False
    )
    invoice_number: Mapped[str] = mapped_column(
        String(20), nullable=False, unique=True, index=True
    )
    purchase_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    @staticmethod
    def generate_invoice_number():
        """Generate a unique invoice number in format INV-XXXXXXXXXX"""
        return f"INV-{secrets.token_hex(5).upper()}"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "course_id": self.course_id,
            "price_paid": float(self.price_paid),
            "discount_applied": float(self.discount_applied),
            "final_price": float(self.final_price),
            "invoice_number": self.invoice_number,
            "purchase_date": self.purchase_date.isoformat() if self.purchase_date else None,
        }

    def __repr__(self):
        return f"<Purchase {self.invoice_number}>"
