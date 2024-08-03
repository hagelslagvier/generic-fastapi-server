from typing import Any, Optional

from fastapi import APIRouter, FastAPI
from injector import Injector


class App(FastAPI):
    def __init__(self, injector: Injector, **kwargs: Any) -> None:
        self.injector = injector
        super().__init__(**kwargs)

    def include_router(self, router: APIRouter, **kwargs: Any) -> Any:
        setattr(router, "injector", self.injector)
        return super().include_router(router, **kwargs)


class Router(APIRouter):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.injector: Optional[Injector] = None
