from unittest.mock import Mock, patch

import pytest

from app.interactors.liveness.interactors import LivenessProbe


@pytest.mark.parametrize(
    "cpu_usage, ram_usage, alive",
    [
        (1, 1, True),
        (50, 50, True),
        (1, 100, False),
        (100, 1, False),
        (100, 100, False),
        (-1, 1, False),
        (1, -1, False),
        (101, 1, False),
        (1, 101, False),
        (101, 101, False),
    ],
)
def test_if_can_check_liveness(cpu_usage: int, ram_usage: int, alive: bool) -> None:
    with patch("app.interactors.liveness.interactors.psutil") as psutil_mock:
        psutil_mock.cpu_percent.return_value = cpu_usage
        psutil_mock.virtual_memory.return_value = Mock(percent=ram_usage)

        probe = LivenessProbe(CPU_LIMIT=95, RAM_LIMIT=95)
        assert probe.is_alive() is alive
