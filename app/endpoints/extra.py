from fastapi import APIRouter
from typing import Any, Optional
from injector import Injector


class Router(APIRouter):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.injector: Optional[Injector] = None
