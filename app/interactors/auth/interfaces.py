from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Any, Generic, TypeVar


class TokenManagerInterface(ABC):
    @abstractmethod
    def create_token(self, payload: dict[str, Any], ttl: timedelta) -> str:
        pass

    @abstractmethod
    def decode_token(self, token: str) -> dict[str, Any]:
        pass


class SecretManagerInterface(ABC):
    @abstractmethod
    def make_hash(self, secret: str) -> str:
        pass

    @abstractmethod
    def verify_secret(self, secret: str, hash: str) -> None:
        pass


UT = TypeVar("UT")


class AuthInterface(ABC, Generic[UT]):
    @abstractmethod
    def get_user(self, login: str) -> UT:
        pass

    @abstractmethod
    def authenticate(self, secret: str, hash: str) -> None:
        pass

    @abstractmethod
    def create_token(self, payload: dict, ttl: timedelta) -> str:
        pass

    @abstractmethod
    def decode_token(self, token: str) -> dict:
        pass
