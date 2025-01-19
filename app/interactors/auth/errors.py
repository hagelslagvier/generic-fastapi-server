class ExpiredSignatureError(Exception):
    pass


class InvalidTokenError(Exception):
    pass


class UnknownTokenError(Exception):
    pass


class SecretVerificationError(Exception):
    pass


class UserNotFoundError(Exception):
    pass
