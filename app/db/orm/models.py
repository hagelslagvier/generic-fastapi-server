from typing import Any, List, Type, TypeVar

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship

T = TypeVar("T", bound="Base")


class Base(DeclarativeBase):
    __abstract__ = True
    id = mapped_column(Integer, primary_key=True)
    created_on = mapped_column(DateTime, default=func.now())
    updated_on = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    __mapper_args__ = {"eager_defaults": True}

    @classmethod
    def _get_primary_key(cls) -> List[str]:
        primary_key = [c.name for c in cls.__mapper__.primary_key]
        return primary_key

    @classmethod
    def _get_attributes(cls) -> List[str]:
        primary_key = set(cls._get_primary_key())
        attributes = {c.name for c in cls.__mapper__.columns} | {
            r.key for r in cls.__mapper__.relationships
        }
        safe_attributes = list(attributes - primary_key)
        return safe_attributes

    @classmethod
    def new(cls: Type[T], **kwargs: Any) -> T:
        safe_kwargs = {k: v for k, v in kwargs.items() if k in cls._get_attributes()}
        return cls(**safe_kwargs)

    def update(self, **kwargs: Any) -> None:
        safe_kwargs = {k: v for k, v in kwargs.items() if k in self._get_attributes()}
        for k, v in safe_kwargs.items():
            setattr(self, k, v)


class User(Base):
    __tablename__ = "users"

    login = mapped_column(String(64), unique=True, nullable=False)
    password = mapped_column(String(64), nullable=False)
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
