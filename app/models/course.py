from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, DateTime, Numeric, func, UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from app.database import db

class Course(db.Model):
    __tablename__ = "course"
    __table_args__ = (UniqueConstraint("name", name="course_name"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[Decimal] = mapped_column(
        Numeric(precision=4, scale=2), nullable=False
    )
    discount: Mapped[Decimal] = mapped_column(
        Numeric(precision=4, scale=2), nullable=False
    )
    language: Mapped[str] = mapped_column(String(100), nullable=False)
    topic: Mapped[str] = mapped_column(String(100), nullable=False)
    level: Mapped[str] = mapped_column(String(100), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "discount": self.discount,
            "language": self.language,
            "topic": self.topic,
            "level": self.level,
            "updated_at": self.updated_at,
            "created_at": self.created_at,
        }

    def __repr__(self):
        return f"<User {self.name}>"
