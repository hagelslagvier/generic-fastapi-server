from fastapi import Request
from injector import Injector


def make_injector(request: Request) -> Injector:
    return request.app.state.injector  # type: ignore[no-any-return]
