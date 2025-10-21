from datetime import datetime
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from app.database import db


class Blog(db.Model):
    __tablename__ = "blog"

    id: Mapped[int] = mapped_column(primary_key=True)
    publication_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    author_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    url: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(100), nullable=False)


def to_dict(self):
    return {
        "id": self.id,
        "publication_date": self.publication_date,
        "author_name": self.author_name,
        "email": self.email,
        "url": self.url,
        "description": self.description,
    }


def __repr__(self):
    return f"<User {self.id}>"
