from typing import Any, Optional

from fastapi import APIRouter
from injector import Injector


class Router(APIRouter):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.injector: Optional[Injector] = None
