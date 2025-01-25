import pytest
from fastapi import FastAPI
from injector import Injector
from inzicht import session_factory
from sqlalchemy import Engine
from starlette.testclient import TestClient

from app.interactors.liveness.interfaces import LivenessProbeInterface
from app.interactors.readiness.interfaces import ReadinessProbeInterface
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
    class HealthyProbe(LivenessProbeInterface):
        def is_alive(self) -> bool:
            return True

    test_injector.binder.bind(LivenessProbeInterface, to=HealthyProbe())


@pytest.fixture
def faulty_probe(test_injector: Injector) -> SideEffect:
    class UnhealthyProbe(LivenessProbeInterface):
        def is_alive(self) -> bool:
            return False

    test_injector.binder.bind(LivenessProbeInterface, to=UnhealthyProbe())


@pytest.fixture
def ready_probe(test_injector: Injector) -> SideEffect:
    class ReadyProbe(ReadinessProbeInterface):
        def is_ready(self) -> bool:
            return True

        def set_ready(self, ready: bool) -> None:
            raise NotImplementedError()

    test_injector.binder.bind(ReadinessProbeInterface, to=ReadyProbe())


@pytest.fixture
def unready_probe(test_injector: Injector) -> SideEffect:
    class UnreadyProbe(ReadinessProbeInterface):
        def is_ready(self) -> bool:
            return False

        def set_ready(self, ready: bool) -> None:
            raise NotImplementedError()

    test_injector.binder.bind(ReadinessProbeInterface, to=UnreadyProbe())


@pytest.fixture
def test_client(test_injector: Injector, content: SideEffect) -> TestClient:
    app = test_injector.get(FastAPI)
    client = TestClient(app)
    return client
