from app.endpoints.users.schema import UserSchemaInput


def test_if_can_get_many(test_client) -> None:
    response = test_client.get("/users")
    assert response.status_code == 200


def test_if_can_get_one(test_client) -> None:
    response = test_client.get("/users/1")
    assert response.status_code == 200


def test_if_can_post(test_client) -> None:
    user_schema = UserSchemaInput(login="foo", password="bar")
    response = test_client.post("/users", json=user_schema.dict())
    assert response.status_code == 200


def test_if_can_put(test_client) -> None:
    user_schema = UserSchemaInput(login="foo", password="bar")
    response = test_client.put("/users/1", json=user_schema.dict())
    assert response.status_code == 200


def test_if_can_delete(test_client) -> None:
    response = test_client.delete("/users/1")
    assert response.status_code == 200
