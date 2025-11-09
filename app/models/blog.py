from typing import Any
from datetime import datetime
from sqlalchemy import JSON, String, DateTime, Text, func 
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
    description: Mapped[str] = mapped_column(String(500), nullable=False)  
    tags: Mapped[list[dict[str, Any]]] = mapped_column(
        MutableList.as_mutable(JSON),
        nullable=False,
        default=list,
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)  
    image_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    image_alt: Mapped[str | None] = mapped_column(String(255), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "publication_date": self.publication_date.isoformat() if self.publication_date else None,
            "author_name": self.author_name,
            "email": self.email,
            "url": self.url,
            "description": self.description,
            "tags": self.tags,
            "content": self.content,
            "image_url": self.image_url,
            "image_alt": self.image_alt,
        }

    def __repr__(self):
        return f"<Blog {self.id}>"  