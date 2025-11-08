from typing import Any
from datetime import datetime
from decimal import Decimal
from sqlalchemy import JSON, String, DateTime, Numeric, Text, func, UniqueConstraint
from sqlalchemy.ext.mutable import MutableList, MutableDict
from sqlalchemy.orm import Mapped, mapped_column
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
    topic: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    level: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    tags: Mapped[list[dict[str, Any]]] = mapped_column(
        MutableList.as_mutable(JSON),
        nullable=False,
        default=list,
    )
    summary: Mapped[dict[str, Any] | None] = mapped_column(
        MutableDict.as_mutable(JSON),
        nullable=True,
    )
    content: Mapped[list[dict[str, Any]] | None] = mapped_column(
        MutableList.as_mutable(JSON), 
        nullable=True, 
    )
    image_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    image_alt: Mapped[str | None] = mapped_column(String(255), nullable=True)
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
            "price": float(self.price),
            "discount": float(self.discount),
            "level": self.level,
            "tags": self.tags,
            "description": self.description,
            "summary": self.summary,
            "image_url": self.image_url,
            "image_alt": self.image_alt,
            "topic": self.topic,
            "content": self.content,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f"<Course {self.name}>"
