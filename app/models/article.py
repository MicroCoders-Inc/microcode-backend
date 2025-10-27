from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, DateTime, Numeric, func, UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from app.database import db


class Article(db.Model):
    __tablename__ = "article"

    id: Mapped[int] = mapped_column(primary_key=True)
    shop_id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[int] = mapped_column(primary_key=True)
    price: Mapped[Decimal] = mapped_column(
        Numeric(precision=4, scale=2), nullable=False
    )
    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(precision=4, scale=2), nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "shop_id": self.shop_id,
            "course_id": self.course_id,
            "quantity": self.quantity,
            "price": self.price,
            "subtotal": self.subtotal,
        }

    def __repr__(self):
        return f"<User {self.id}>"
