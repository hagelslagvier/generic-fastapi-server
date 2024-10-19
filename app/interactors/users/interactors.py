from app.database.orm.crud.generic import GenericCRUD
from app.database.orm.models import User


class UserCRUD(GenericCRUD[User]):
    pass
