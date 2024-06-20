from starlette.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_if_can_post() -> None:
    response = client.post("/items", json={"name": "foo", "age": 42})
    assert response.status_code == 200


def test_if_can_get_one() -> None:
    response = client.get("/items/1")
    assert response.status_code == 200


def test_if_can_get_many() -> None:
    response = client.get("/items")
    assert response.status_code == 200


def test_if_can_put() -> None:
    response = client.put("/items/1", json={"name": "foo", "age": 42})
    assert response.status_code == 200


def test_if_can_delete() -> None:
    response = client.delete("/items/1")
    assert response.status_code == 200
