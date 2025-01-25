from starlette.testclient import TestClient

from tests.types import SideEffect


def test_if_can_get_readiness_report_when_ready(
    test_client: TestClient, ready_probe: SideEffect
) -> None:
    response = test_client.get("/readiness")

    assert response.status_code == 200
    assert response.json() == {"is_ready": True}


def test_if_can_get_readiness_report_when_unready(
    test_client: TestClient, unready_probe: SideEffect
) -> None:
    response = test_client.get("/readiness")

    assert response.status_code == 200
    assert response.json() == {
        "is_ready": False,
    }
