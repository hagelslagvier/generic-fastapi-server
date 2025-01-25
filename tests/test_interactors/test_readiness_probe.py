from sqlalchemy import Engine

from app.interactors.readiness.interactors import ReadinessProbe
from tests.aliases import SideEffect


def test_if_can_check_readiness(engine: Engine, content: SideEffect) -> None:
    probe = ReadinessProbe(bind=engine, hostname="foo")
    assert probe.hostname == "foo"
    assert probe.is_ready() is False


def test_if_can_set_readiness(engine: Engine, content: SideEffect) -> None:
    probe = ReadinessProbe(bind=engine, hostname="foo")

    probe.set_ready(True)
    assert probe.is_ready() is True

    probe.set_ready(False)
    assert probe.is_ready() is False

    probe.set_ready(True)
    assert probe.is_ready() is True
