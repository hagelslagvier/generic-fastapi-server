from typing import List

from sqlalchemy import ForeignKey, String, asc, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.orm.models import Base


class Group(Base):
    __tablename__ = "groups"

    title: Mapped[str] = mapped_column(String(8), unique=True)
    students: Mapped[
        List["Student"]
    ] = relationship(  # Mapped[List[<model>]] -> one-to-many
        back_populates="group", order_by=asc(text("students.id"))
    )

    def __repr__(self) -> str:
        return f"Group(id={self.id})"


class Student(Base):
    __tablename__ = "students"

    name: Mapped[str] = mapped_column(String(64), unique=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    group: Mapped["Group"] = relationship(
        back_populates="students",
    )
    locker_id: Mapped[int] = mapped_column(ForeignKey("lockers.id"))
    locker: Mapped["Locker"] = relationship(back_populates="student")

    def __repr__(self) -> str:
        return f"Student(id={self.id})"


class Locker(Base):
    __tablename__ = "lockers"

    code: Mapped[str] = mapped_column(String(16))
    student: Mapped[Student] = relationship(
        back_populates="locker"
    )  # Mapped[<model>] -> one-to-one

    def __repr__(self) -> str:
        return f"Locker(id={self.id})"
