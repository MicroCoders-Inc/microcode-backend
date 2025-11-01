from datetime import datetime
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from app.database import db

class Contact(db.Model):
    __tablename__ = "contact"

    id = db.Column(db.Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    messages: Mapped[str] = mapped_column(String(100), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "messages": self.messages,
        }

    def __repr__(self):
        return f"<Contact {self.id}>"
