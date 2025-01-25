from starlette.testclient import TestClient

from tests.types import SideEffect


def test_if_can_get_liveness_report_when_healthy(
    test_client: TestClient, healthy_probe: SideEffect
) -> None:
    response = test_client.get("/liveness")

    assert response.status_code == 200
    assert response.json() == {"is_alive": True}


def test_if_can_get_liveness_report_when_unhealthy(
    test_client: TestClient, faulty_probe: SideEffect
) -> None:
    response = test_client.get("/liveness")

    assert response.status_code == 200
    assert response.json() == {
        "is_alive": False,
    }
