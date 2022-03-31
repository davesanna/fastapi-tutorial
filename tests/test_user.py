from app.schemas.schemas import UserResponse
from tests.database import (
    client,
    session,
)  # we need to import both fixtures since one is dependent from the other


def test_root(client):
    res = client.get("/")
    print(res.json().get("message"))
    print(res.status_code)
    assert res.json().get("message") == "lolol World"
    assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "topogigio@gmail.com", "password": "test123"}
    )
    print(res.json())

    new_user = UserResponse(**res.json())

    assert new_user.email == "topogigio@gmail.com"
    assert (
        res.status_code == 201
    )  # watch out to the url passed into client.post, it has to be /<name>/ and not /<name> otherwise, it redirects and returns a 307 first


def test_login_user(client):
    res = client.post(
        "/login", data={"username": "topogigio@gmail.com", "password": "test123"}
    )  # in this case we use /<name> since the route does not have a prefix, and data instead of json

    print(res.json())
    assert res.status_code == 200
