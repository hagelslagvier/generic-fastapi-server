from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.db.orm.crud.common import GenericCRUD


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    updated_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )


class User(Base):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=True)

    def __repr__(self) -> str:
        return f"User(id={self.id}, " f"name={self.name}, " f"age={self.age})"


class UserCRUD(GenericCRUD[User]):
    pass
