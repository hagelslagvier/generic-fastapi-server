from typing import List

from sqlalchemy import Column, ForeignKey, Integer, String, Table, asc, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.orm.models import Base

m2m_student_course = Table(
    "m2m_student_course",
    Base.metadata,
    Column(
        "student_id",
        Integer,
        ForeignKey("students.id"),
        primary_key=True,
        nullable=True,
    ),
    Column(
        "course_id", Integer, ForeignKey("courses.id"), primary_key=True, nullable=True
    ),
)


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

    courses: Mapped[List["Course"]] = relationship(
        secondary=m2m_student_course,  # many-to-many
        back_populates="students",
        order_by=asc("Course.id"),
    )

    def __repr__(self) -> str:
        return f"Student(id={self.id})"


class Course(Base):
    __tablename__ = "courses"

    title: Mapped[str] = mapped_column(String(64), unique=True)

    students: Mapped[List["Student"]] = relationship(
        secondary=m2m_student_course,  # many-to-many
        back_populates="courses",
        order_by=asc("Student.id"),
    )

    def __repr__(self) -> str:
        return f"Course(id={self.id})"


class Locker(Base):
    __tablename__ = "lockers"

    code: Mapped[str] = mapped_column(String(16))
    student: Mapped[Student] = relationship(
        back_populates="locker"
    )  # Mapped[<model>] -> one-to-one

    def __repr__(self) -> str:
        return f"Locker(id={self.id})"
