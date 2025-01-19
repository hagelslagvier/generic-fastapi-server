from copy import copy
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from jwt.exceptions import ExpiredSignatureError as ExpiredJWTSignatureError
from jwt.exceptions import InvalidTokenError as InvalidJWTTokenError

from app.interactors.auth.errors import (
    ExpiredSignatureError,
    InvalidTokenError,
    UnknownTokenError,
)
from app.interactors.auth.interfaces import TokenManagerInterface


class TokenManager(TokenManagerInterface):
    def __init__(self, secret_key: str, algorithm: str) -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_token(self, payload: dict[str, Any], ttl: timedelta) -> str:
        expiration = datetime.now(timezone.utc) + ttl
        token_payload = copy(payload)
        token_payload.update({"exp": expiration})
        token = jwt.encode(
            payload=token_payload, key=self.secret_key, algorithm=self.algorithm
        )

        return token

    def decode_token(self, token: str) -> dict[str, Any]:
        try:
            payload: dict[str, Any] = jwt.decode(
                jwt=token, key=self.secret_key, algorithms=[self.algorithm]
            )
        except ExpiredJWTSignatureError as error:
            raise ExpiredSignatureError(
                f"Token has expired signature, token: '{token}'"
            ) from error
        except InvalidJWTTokenError as error:
            raise InvalidTokenError(
                f"Token has invalid content, token: '{token}'"
            ) from error
        except Exception as error:
            raise UnknownTokenError(
                f"Unknown error decoding token, token: '{token}'"
            ) from error

        return payload
