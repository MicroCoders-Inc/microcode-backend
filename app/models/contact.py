from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import db

class Contact(db.Model):
    __tablename__ = "contact"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), nullable=False)
    messages: Mapped[str] = mapped_column(String(1000), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "messages": self.messages,
        }

    def __repr__(self):
        return f"<Contact {self.id}>"
