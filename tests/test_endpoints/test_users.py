from starlette.testclient import TestClient

from app.endpoints.users.schema import UserSchemaInput, UserSchemaOutput


def test_if_can_get_many(test_client: TestClient) -> None:
    response = test_client.get("/users")
    assert response.status_code == 200
    assert {UserSchemaOutput(**item).id for item in response.json()} == {1, 2, 3, 4, 5}


def test_if_can_get_one(test_client: TestClient) -> None:
    response = test_client.get("/users/1")
    assert response.status_code == 200

    actual = UserSchemaOutput(**response.json()).dict()
    assert actual.pop("created_on")
    assert actual.pop("updated_on")
    assert actual == {
        "id": 1,
        "login": "user-0",
        "password": "password-0",
        "email": "user-0@abc.com",
        "is_email_confirmed": False,
        "refresh_token": None,
        "access_token": None,
        "is_admin": False,
    }


def test_if_can_post(test_client: TestClient) -> None:
    input_schema = UserSchemaInput(login="foo", password="bar", email="foo@bar.baz")
    response = test_client.post("/users", json=input_schema.dict())
    assert response.status_code == 200

    actual = UserSchemaOutput(**response.json()).dict()
    assert actual.pop("id")
    assert actual.pop("created_on")
    assert actual.pop("updated_on")
    assert actual == input_schema.dict()


def test_if_can_put(test_client: TestClient) -> None:
    input_schema = UserSchemaInput(
        login="foo-new", password="bar-new", email="foo-new@bar.baz"
    )
    response = test_client.put("/users/1", json=input_schema.dict())
    assert response.status_code == 200

    actual = UserSchemaOutput(**response.json()).dict()
    assert actual.pop("created_on")
    assert actual.pop("updated_on")
    assert actual == {"id": 1, **input_schema.dict()}


def test_if_can_delete(test_client: TestClient) -> None:
    response = test_client.delete("/users/1")
    assert response.status_code == 200
    assert UserSchemaOutput(**response.json()).id == 1
