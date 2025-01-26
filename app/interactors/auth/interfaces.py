from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Any, Generic, TypeVar


class TokenManagerInterface(ABC):
    """Defines the interface for managing tokens."""

    @abstractmethod
    def create_token(self, payload: dict[str, Any], ttl: timedelta) -> str:
        """Create a token with the given payload and time-to-live (TTL).

        Args:
            payload (dict[str, Any]): The data to be encoded in the token.
            ttl (timedelta): The time-to-live for the token, after which it expires.

        Returns:
            str: The generated token as a string.
        """

    @abstractmethod
    def decode_token(self, token: str) -> dict[str, Any]:
        """Decode the provided token and extract the payload.

        Args:
            token (str): The token to decode.

        Returns:
            dict[str, Any]: The decoded payload from the token.

        Raises:
            ValueError: If the token is invalid or expired.
        """


class SecretManagerInterface(ABC):
    """Define the interface for managing secrets securely."""

    @abstractmethod
    def make_hash(self, secret: str) -> str:
        """Generate a hash for a given secret.

        Args:
            secret (str): The secret to hash.

        Returns:
            str: A hashed representation of the secret.
        """

    @abstractmethod
    def verify_secret(self, secret: str, hash: str) -> None:
        """Verify that a secret matches a given hash.

        Args:
            secret (str): The secret to verify.
            hash (str): The hash to compare the secret against.

        Returns:
            bool: True if the secret matches the hash, False otherwise.
        """


UT = TypeVar("UT")


class AuthInterface(ABC, Generic[UT]):
    """Defines the interface for implementing authentication-related operations.

    Attributes:
        UT: A generic type that represents the user model or user-related object.
    """

    @abstractmethod
    def get_user(self, login: str) -> UT:
        """Fetch user details by login identifier.

        Args:
            login (str): The unique login identifier of the user (e.g., username or email).

        Returns:
            UT: The user object corresponding to the given login. This could be any type defined by the implementing
            class.
        """

    @abstractmethod
    def authenticate(self, secret: str, hash: str) -> None:
        """Authenticate a user by validating a secret against a hash.

        Args:
            secret (str): The raw secret (e.g., password) provided by the user.
            hash (str): The hashed version of the secret for comparison.

        Raises:
            AuthenticationError: If the provided secret does not match the hash.
        """

    @abstractmethod
    def create_token(self, payload: dict[str, Any], ttl: timedelta) -> str:
        """Create a token with the specified payload and time-to-live.

        Args:
            payload (dict[str, Any]): The data to encode within the token.
            ttl (timedelta): The duration for which the token will remain valid.

        Returns:
            str: A securely generated token as a string.
        """

    @abstractmethod
    def decode_token(self, token: str) -> dict[str, Any]:
        """Decode a token to retrieve its payload.

        Args:
            token (str): The token to decode.

        Returns:
            dict[str, Any]: The payload extracted from the token.

        Raises:
            TokenDecodeError: If the token is invalid or expired.
        """
