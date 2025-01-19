from typing import cast

from fastapi import Request
from injector import Injector


def make_injector(request: Request) -> Injector:
    return cast(Injector, request.app.state.injector)
