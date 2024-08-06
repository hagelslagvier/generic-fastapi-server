from app.db.orm.crud.generic import GenericCRUD
from app.db.orm.models import Confirmation, User


class UserCRUD(GenericCRUD[User]):
    pass


class ConfirmationCRUD(GenericCRUD[Confirmation]):
    pass
