from datetime import timedelta

import pytest
from fastapi import FastAPI
from injector import Injector
from sqlalchemy import Engine
from starlette.testclient import TestClient

from app.database.orm.factories import session_factory
from app.interactors.health_check.interfaces import HealthCheckProbeInterface
from app.interactors.users.interactors import UserCRUD
from tests.assembly import test_root_injector
from tests.types import SideEffect


@pytest.fixture
def content(engine: Engine) -> None:
    with session_factory(bind=engine) as session:
        user_crud = UserCRUD(session=session)
        user_crud.create_many(
            payload=[
                {
                    "login": f"user-{index}",
                    "password": f"password-{index}",
                    "email": f"user-{index}@abc.com",
                }
                for index in range(5)
            ]
        )


@pytest.fixture
def test_injector() -> Injector:
    return test_root_injector


@pytest.fixture
def healthy_probe(test_injector: Injector) -> SideEffect:
    class HealthyProbe(HealthCheckProbeInterface):
        def get_uptime(self) -> timedelta:
            return timedelta(hours=1)

        def get_cpu_usage(self) -> int:
            return 8

        def get_ram_usage(self) -> int:
            return 32

    test_injector.binder.bind(HealthCheckProbeInterface, to=HealthyProbe())  # type: ignore[type-abstract]


@pytest.fixture
def faulty_probe(test_injector: Injector) -> SideEffect:
    class FaultyProbe(HealthCheckProbeInterface):
        def get_uptime(self) -> timedelta:
            raise OSError("Foo")

        def get_cpu_usage(self) -> int:
            return 8

        def get_ram_usage(self) -> int:
            return 32

    test_injector.binder.bind(HealthCheckProbeInterface, to=FaultyProbe())


@pytest.fixture
def test_client(test_injector: Injector, content: SideEffect) -> TestClient:
    app = test_injector.get(FastAPI)
    client = TestClient(app)
    return client
