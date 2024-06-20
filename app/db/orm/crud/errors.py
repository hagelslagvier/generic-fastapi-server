class BaseORMError(Exception):
    pass


class DoesNotExistError(BaseORMError):
    pass
