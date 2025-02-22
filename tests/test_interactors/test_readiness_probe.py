from app.interactors.readiness.interactors import ReadinessProbe
from tests.aliases import SideEffect


def test_if_can_check_readiness(lock_file_path: str) -> None:
    probe = ReadinessProbe()
    assert not probe.is_ready()


def test_if_can_set_readiness(lock_file: SideEffect) -> None:
    probe_1 = ReadinessProbe()
    assert probe_1.is_ready()

    probe_1.set_ready(False)
    assert not probe_1.is_ready()

    probe_2 = ReadinessProbe()
    assert not probe_2.is_ready()

    probe_2.set_ready(True)
    assert probe_2.is_ready()
    assert probe_1.is_ready()
