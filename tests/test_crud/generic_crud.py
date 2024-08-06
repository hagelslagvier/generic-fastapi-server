from app.db.orm.crud.common import GenericCRUD
from tests.test_crud.generic_models import Group, Student


class GroupCRUD(GenericCRUD[Group]):
    pass


class StudentCRUD(GenericCRUD[Student]):
    pass
