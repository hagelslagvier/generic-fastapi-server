from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

from sqlalchemy import DateTime, func, String, Boolean, Integer

from datetime import datetime


class Base(DeclarativeBase):
    __abstract__ = True
    # id: Mapped[UUID] = mapped_column(
    #     UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    # )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    updated_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )


class User(Base):
    __tablename__ = "users"

    login: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    refresh_token: Mapped[str] = mapped_column(String, nullable=True)
    access_token: Mapped[str] = mapped_column(String, nullable=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self) -> str:
        return f"User(id={self.id}, login={self.login}, is_admin={self.is_admin})"
