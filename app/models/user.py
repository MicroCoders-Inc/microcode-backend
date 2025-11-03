from datetime import datetime
from sqlalchemy import String, DateTime, func, UniqueConstraint, JSON
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.mutable import MutableList
from app.database import db


class User(db.Model):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("username", name="username"),
        UniqueConstraint("email", name="user_email"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(80), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    profile_picture: Mapped[str | None] = mapped_column(String(255), nullable=True)
    owned_courses: Mapped[list[int]] = mapped_column(
        MutableList.as_mutable(JSON),
        default=list,
    )
    favourite_courses: Mapped[list[int]] = mapped_column(
        MutableList.as_mutable(JSON),
        default=list,
    )
    saved_blogs: Mapped[list[int]] = mapped_column(
        MutableList.as_mutable(JSON),
        default=list,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "profile_picture": self.profile_picture,
            "created_at": self.created_at.isoformat(),
            "owned_courses": self.owned_courses or [],
            "favourite_courses": self.favourite_courses or [],
            "saved_blogs": self.saved_blogs or [],
        }

    def __repr__(self):
        return f"<User {self.username}>"
