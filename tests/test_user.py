from jose import jwt
import pytest
from app.schemas.schemas import UserResponse, Token
from app.config import settings


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


def test_login_user(client, test_user):
    res = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )  # in this case we use /<name> since the route does not have a prefix, and data instead of json

    login_res = Token(**res.json())
    payload = jwt.decode(
        login_res.access_token, settings.secret_key, algorithms=settings.algorithm
    )
    id = payload.get("user_id")
    print(test_user)
    assert res.status_code == 200
    assert test_user["id"] == id
    assert login_res.token_type == "bearer"


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@gmail.com", "test123", 403),
        ("topogigio@gmail.com", "wrong password", 403),
        ("wrongemail@gmail.com", "wrong password", 403),
        (None, "wrong password", 422),  # Unprocessible Entity, None is = Empty
        ("topogigio@gmail.com", None, 422),  # Unprocessible Entity, None is = Empty
    ],
)
def test_incorrect_login(client, test_user, email, password, status_code):

    res = client.post(
        "/login",
        data={"username": email, "password": password, "status_code": status_code},
    )
    print(res.json())
    assert res.status_code == status_code
    # assert res.json()["detail"] == "Invalid Credentials"
