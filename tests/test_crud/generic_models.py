from typing import List

from sqlalchemy import ForeignKey, String, asc
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.orm.models import Base


class Group(Base):
    __tablename__ = "groups"

    code: Mapped[str] = mapped_column(String(8), unique=True, nullable=False)
    students: Mapped[List["Student"]] = relationship(
        back_populates="group"
    )  # TODO: sort students

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
