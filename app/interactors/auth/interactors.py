from datetime import timedelta

from inzicht import session_factory
from sqlalchemy import Engine

from app.database.orm.models import User
from app.interactors.auth.errors import UserNotFoundError
from app.interactors.auth.interfaces import (
    AuthInterface,
    SecretManagerInterface,
    TokenManagerInterface,
)
from app.interactors.users.interactors import UserCRUD


class Auth(AuthInterface[User]):
    def __init__(
        self,
        engine: Engine,
        secret_manager: SecretManagerInterface,
        token_manager: TokenManagerInterface,
        token_ttl: int,
    ):
        self.engine = engine
        self.secret_manager = secret_manager
        self.token_manager = token_manager
        self.token_ttl = token_ttl

    def get_user(self, login: str) -> User:
        with session_factory(bind=self.engine) as session:
            users = UserCRUD(session=session).read_many(where=User.login == login)
            found: list[User] = list(users)
        if len(found) == 1:
            [user] = found
            return user
        else:
            raise UserNotFoundError(f"User with login name '{login}' not found")

    def authenticate(self, secret: str, hash: str) -> None:
        self.secret_manager.verify_secret(secret=secret, hash=hash)

    def create_token(self, payload: dict, ttl: timedelta) -> str:
        token = self.token_manager.create_token(payload=payload, ttl=ttl)
        return token

    def decode_token(self, token: str) -> dict:
        payload = self.token_manager.decode_token(token=token)
        return payload
