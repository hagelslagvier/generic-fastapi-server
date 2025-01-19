import datetime

import pytest
from freezegun import freeze_time

from app.interactors.auth.token_manager import (
    ExpiredSignatureError,
    InvalidTokenError,
    TokenManager,
)


def test_if_can_create_valid_token(token_manager: TokenManager) -> None:
    token = token_manager.create_token(
        payload={"foo": "bar"}, ttl=datetime.timedelta(minutes=15)
    )

    assert isinstance(token, str)
    assert len(token)


def test_if_can_decode_valid_token(token_manager: TokenManager) -> None:
    token = token_manager.create_token(
        payload={"foo": "bar"}, ttl=datetime.timedelta(minutes=15)
    )

    payload = token_manager.decode_token(token=token)

    assert payload.get("exp")
    assert payload.get("foo") == "bar"


@pytest.mark.parametrize(
    "invalid_token",
    [
        "foo",
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalid.content.jJTQ-riFmE4Wp3o74J03RVLXXbD-QGvykNZ38libyg",
    ],
)
def test_if_raises_error_when_decoding_invalid_token(
    token_manager: TokenManager, invalid_token: str
) -> None:
    with pytest.raises(InvalidTokenError) as error_info:
        token_manager.decode_token(token=invalid_token)

    assert (
        str(error_info.value) == f"Token has invalid content, token: '{invalid_token}'"
    )


def test_if_raises_error_when_decoding_expired_token(
    token_manager: TokenManager,
) -> None:
    now = datetime.datetime.now()
    ttl = datetime.timedelta(minutes=15)
    expire = now + datetime.timedelta(minutes=16)
    token = token_manager.create_token(payload={"foo": "bar"}, ttl=ttl)

    with pytest.raises(ExpiredSignatureError) as error_info:
        with freeze_time(expire):
            token_manager.decode_token(token=token)

    assert str(error_info.value) == f"Token has expired signature, token: '{token}'"
