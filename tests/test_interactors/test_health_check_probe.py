import datetime
from unittest.mock import Mock, patch

from app.interactors.health_check.interactors import HealthCheckProbe


def test_if_can_get_uptime() -> None:
    datetime_patch = patch("app.interactors.health_check.interactors.datetime")
    psutil_patch = patch("app.interactors.health_check.interactors.psutil")
    with datetime_patch as datetime_mock, psutil_patch as psutil_mock:
        now = datetime.datetime.now()
        expected_uptime = datetime.timedelta(hours=1)
        datetime_mock.now.return_value = now
        datetime_mock.fromtimestamp.return_value = now - expected_uptime

        probe = HealthCheckProbe()
        actual_uptime = probe.get_uptime()

        psutil_mock.boot_time.assert_called_once()
        assert actual_uptime == expected_uptime


def test_if_can_get_cpu_usage() -> None:
    with patch("app.interactors.health_check.interactors.psutil") as psutil_mock:
        psutil_mock.cpu_percent.return_value = "42"

        probe = HealthCheckProbe()
        cpu_usage = probe.get_cpu_usage()

        psutil_mock.cpu_percent.assert_called_once_with(interval=0.05)
        assert cpu_usage == 42


def test_if_can_get_ram_usage() -> None:
    with patch("app.interactors.health_check.interactors.psutil") as psutil_mock:
        psutil_mock.virtual_memory.return_value = Mock(percent=42)

        probe = HealthCheckProbe()
        ram_usage = probe.get_ram_usage()

        psutil_mock.virtual_memory.assert_called_once()
        assert ram_usage == 42
