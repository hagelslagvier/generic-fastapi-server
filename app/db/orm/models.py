from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True
    id = mapped_column(Integer, primary_key=True)
    created_on = mapped_column(DateTime(timezone=True), default=func.now())
    updated_on = mapped_column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )


class User(Base):
    __tablename__ = "users"

    login = mapped_column(String, unique=True, nullable=False)
    password = mapped_column(String, nullable=False)
    refresh_token = mapped_column(String, nullable=True)
    access_token = mapped_column(String, nullable=True)
    is_admin = mapped_column(Boolean, default=False)

    def __repr__(self) -> str:
        return f"User(id={self.id}, login={self.login}, is_admin={self.is_admin})"
