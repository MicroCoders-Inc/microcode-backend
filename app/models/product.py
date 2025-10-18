from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, DateTime, Numeric, func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from app.database import db


class Product(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    price: Mapped[Decimal] = mapped_column(
        Numeric(precision=4, scale=2), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "created_at": self.created_at.isoformat(),
        }

    def __repr__(self):
        return f"<User {self.name}>"
