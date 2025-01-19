from typing import TypeVar

from inzicht import DeclarativeBase
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import mapped_column, relationship

T = TypeVar("T", bound="Base")


class Base(DeclarativeBase):
    __abstract__ = True
    id = mapped_column(Integer, primary_key=True)
    created_on = mapped_column(DateTime, default=func.now())
    updated_on = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class User(Base):
    __tablename__ = "users"

    login = mapped_column(String(64), unique=True, nullable=False)
    password = mapped_column(String(128), nullable=False)
    email = mapped_column(String(64), nullable=False)
    is_email_confirmed = mapped_column(Boolean, default=False)
    refresh_token = mapped_column(String, nullable=True)
    access_token = mapped_column(String, nullable=True)
    is_admin = mapped_column(Boolean, default=False)
    confirmation = relationship("Confirmation", back_populates="user", uselist=False)

    def __repr__(self) -> str:
        return f"User(id={self.id}, login={self.login}, email={self.email}, is_admin={self.is_admin})"


class Confirmation(Base):
    __tablename__ = "confirmations"

    confirmation_code = mapped_column(String, nullable=False)
    user_id = mapped_column(ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="confirmation")

    def __repr__(self) -> str:
        return f"Confirmation(id={self.id}, user={self.user})"
