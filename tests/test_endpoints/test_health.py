from starlette.testclient import TestClient


def test_if_can_get_health_report(test_client: TestClient) -> None:
    response = test_client.get("/health")
    assert response.status_code == 200

    report = response.json()
    assert isinstance(report, dict)
    assert "stats" in report
