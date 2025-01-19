from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from injector import Injector

from app.database.orm.models import User
from app.dependencies.injector import make_injector
from app.interactors.auth.interfaces import AuthInterface
from app.interactors.auth.token_manager import InvalidTokenError

oauth2_password_bearer = OAuth2PasswordBearer(tokenUrl="tokens")


def get_user_from_token(
    injector: Injector = Depends(make_injector),
    token: str = Depends(oauth2_password_bearer),
) -> User | None:
    auth = injector.get(AuthInterface)

    try:
        payload = auth.decode_token(token=token)
    except InvalidTokenError:
        # logging here
        raise

    user_name = payload.get("sub")
    if user_name is None:
        raise Exception

    try:
        user: User = auth.get_user(login=user_name)
    except Exception:
        raise Exception

    return user
