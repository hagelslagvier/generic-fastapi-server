from datetime import datetime
from unittest.mock import Mock, patch

from starlette.testclient import TestClient


@patch("app.endpoints.health.health.psutil")
@patch("app.endpoints.health.health.datetime")
def test_if_can_get_health_report_when_healthy(
    datetime_mock: Mock, psutil_mock: Mock, test_client: TestClient
) -> None:
    psutil_mock.cpu_percent.return_value = 8
    psutil_mock.virtual_memory.return_value = Mock(percent=32)
    datetime_mock.now.return_value = datetime(2024, 1, 1, 1, 0, 0, 0)
    datetime_mock.fromtimestamp.return_value = datetime(2024, 1, 1, 0, 0, 0, 0)

    response = test_client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "uptime": "1:00:00",
        "cpu": "8",
        "ram": "32",
    }


@patch("app.endpoints.health.health.psutil")
def test_if_can_get_health_report_when_unhealthy(
    psutil_mock: Mock, test_client: TestClient
) -> None:
    psutil_mock.cpu_percent.side_effect = OSError("Foo")

    response = test_client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "unhealthy",
        "error_type": "OSError",
        "error": "Foo",
    }
