from inzicht.crud.generic import GenericCRUD  # type: ignore

from app.database.orm.models import User


class UserCRUD(GenericCRUD[User]):
    pass
