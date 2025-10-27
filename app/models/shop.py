from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, DateTime, Numeric, func, UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from app.database import db

class Shop(db.Model):
    __tablename__ = "shop"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(primary_key=True)
    article: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[Decimal] = mapped_column(
        Numeric(precision=4, scale=2), nullable=False
    )
    date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    total_price: Mapped[Decimal] = mapped_column(
        Numeric(precision=4, scale=2), nullable=False
    )
    method_payment: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(100), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "article": self.article,
            "price": self.price,
            "date": self.date,
            "total_price": self.total_price,
            "method_payment": self.method_payment,
            "status": self.status,
        }


    def __repr__(self):
        return f"<User {self.id}>"