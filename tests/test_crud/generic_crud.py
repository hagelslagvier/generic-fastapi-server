from sqlalchemy import String
from sqlalchemy.orm import mapped_column

from app.db.orm.crud.common import GenericCRUD
from app.db.orm.models import Base
from tests.test_crud.generic_models import Group, Student


class GroupCRUD(GenericCRUD[Group]):
    pass


class StudentCRUD(GenericCRUD[Student]):
    pass


class Dummy(Base):
    __tablename__ = "dummies"
    foo = mapped_column(String(8), unique=True, nullable=True)
    bar = mapped_column(String(8), unique=True, nullable=True)
    baz = mapped_column(String(8), unique=True, nullable=True)


class DummyCRUD(GenericCRUD[Dummy]):
    pass
