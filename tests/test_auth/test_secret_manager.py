from contextlib import nullcontext as AssertNotRaises

import pytest

from app.interactors.auth.secret_manager import SecretManager, SecretVerificationError


def test_if_can_make_hash(secret_manager: SecretManager) -> None:
    hashed_secret = secret_manager.make_hash(secret="hello")

    assert isinstance(hashed_secret, str)
    assert len(hashed_secret) != 0


def test_if_uses_salt_to_make_hash(secret_manager: SecretManager) -> None:
    hashed_secrets = {secret_manager.make_hash(secret="hello") for _ in range(5)}

    assert len(hashed_secrets) == 5


def test_if_can_approve_valid_secret(secret_manager: SecretManager) -> None:
    with AssertNotRaises():
        hashed_secrets = {secret_manager.make_hash(secret="hello") for _ in range(5)}
        for hashed_secret in hashed_secrets:
            secret_manager.verify_secret(secret="hello", hash=hashed_secret)


@pytest.mark.parametrize(
    "invalid_secret, expected_error",
    [
        ("", ValueError),
        ("invalid-secret", ValueError),
        (
            "bc52c3ef23c2692e58b108663ba5ec9f:4cdab5a3968c43f602ee272961ca35d11de0e47e65b57dd10792835b95a50b71",
            SecretVerificationError,
        ),
        (
            "7c754f1863a513f58ad5bb3dcf0c26fe:ab5a06289c0f15f72dca9e741e6e625d8d24105ca4c4c8079276aa3e74abf412",
            SecretVerificationError,
        ),
        (
            "a6d1965f559210426ab1faca035e9876:b40cf8294c659707b910a732417cf78e893128ba1c389bbfae07f7868373e732",
            SecretVerificationError,
        ),
        (
            "731826be33b5459aa258316facbba481:7d49ef9efa5901327a6740bc1442faa1e9fbbf5eaa207acd0f88e5530f8d6bee",
            SecretVerificationError,
        ),
        (
            "8632b4dd033e0018e0e56c3a832f431b:b365deecb9601b0f5960f0a261907ac81c5ffa733c9d8db05e510b9a060f4180",
            SecretVerificationError,
        ),
    ],
)
def test_if_can_disapprove_invalid_secret(
    secret_manager: SecretManager, invalid_secret: str, expected_error: Exception
) -> None:
    with pytest.raises(expected_error):  # type: ignore[call-overload]
        secret_manager.verify_secret(secret="hello", hash=invalid_secret)
