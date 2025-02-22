from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from injector import Injector

from app.database.orm.models import User
from app.dependencies.injector import make_injector
from app.interactors.auth.interfaces import AuthInterface
from app.interactors.auth.token_manager import InvalidTokenError

oauth2_password_bearer = OAuth2PasswordBearer(tokenUrl="tokens")


async def get_token(request: Request) -> str | None:
    try:
        token = await oauth2_password_bearer(request)
    except HTTPException:
        return None
    else:
        return token


def get_user_from_token(
    injector: Injector = Depends(make_injector),
    token: str | None = Depends(get_token),
) -> User | None:
    auth = injector.get(AuthInterface)

    if token is None:
        return None

    try:
        payload = auth.decode_token(token=token)
    except InvalidTokenError:
        return None

    user_name = payload.get("sub")
    if user_name is None:
        return None

    try:
        user: User = auth.get_user(login=user_name)
    except Exception:
        return None

    return user
