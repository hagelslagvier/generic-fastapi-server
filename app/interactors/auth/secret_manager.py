import hashlib
from os import urandom

from app.interactors.auth.errors import SecretVerificationError
from app.interactors.auth.interfaces import SecretManagerInterface


class SecretManager(SecretManagerInterface):
    def __init__(self, key_length: int, iterations: int) -> None:
        self.key_length = key_length
        self.iterations = iterations

    def make_hash(self, secret: str) -> str:
        salt = urandom(16)
        body = hashlib.pbkdf2_hmac(
            hash_name="sha256",
            password=str(secret).encode(),
            salt=salt,
            iterations=self.iterations,
            dklen=self.key_length,
        )
        hash = f"{salt.hex()}:{body.hex()}"
        return hash

    def verify_secret(self, secret: str, hash: str) -> None:
        prefix, body = str(hash).split(":")
        salt = bytes.fromhex(prefix)
        actual_hash = bytes.fromhex(body)
        expected_hash = hashlib.pbkdf2_hmac(
            hash_name="sha256",
            password=str(secret).encode(),
            salt=salt,
            iterations=self.iterations,
            dklen=self.key_length,
        )
        if expected_hash != actual_hash:
            raise SecretVerificationError(
                "Provided hash doesn't pass verification procedure"
            )
