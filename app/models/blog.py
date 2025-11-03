from typing import Any
from datetime import datetime
from sqlalchemy import JSON, String, DateTime, func
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from app.database import db


class Blog(db.Model):
    __tablename__ = "blog"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    publication_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    author_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    url: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(100), nullable=False)
    tags: Mapped[list[dict[str, Any]]] = mapped_column(
        MutableList.as_mutable(JSON),
        nullable=False,
        default=list,
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "publication_date": self.publication_date,
            "author_name": self.author_name,
            "email": self.email,
            "url": self.url,
            "description": self.description,
            "tags": self.tags,
        }

    def __repr__(self):
        return f"<User {self.id}>"
