from app.db.orm.crud.generic import GenericCRUD
from app.db.orm.models import User


class UserCRUD(GenericCRUD[User]):
    pass
