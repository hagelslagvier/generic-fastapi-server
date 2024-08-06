from datetime import datetime
from typing import List

from sqlalchemy import DateTime, ForeignKey, Integer, String, asc, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    updated_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )


class Group(Base):
    __tablename__ = "groups"

    code: Mapped[str] = mapped_column(String(8), unique=True, nullable=False)
    students: Mapped[List["Student"]] = relationship(back_populates="group")

    def __repr__(self) -> str:
        return f"Group(id={self.id}, code={self.code})"


class Student(Base):
    __tablename__ = "students"

    name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"), nullable=False)
    group: Mapped["Group"] = relationship(
        back_populates="students", order_by=asc("Student.id")
    )

    def __repr__(self) -> str:
        return f"Student(id={self.id}, name={self.name}, group={self.group})"
