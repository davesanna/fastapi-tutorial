from fastapi.testclient import TestClient

from app.main import app
from app.schemas import UserResponse

client = TestClient(app)


def test_root():
    res = client.get("/")
    print(res.json().get("message"))
    print(res.status_code)
    assert res.json().get("message") == "lolol World"
    assert res.status_code == 200


def test_create_user():
    res = client.post(
        "/users/", json={"email": "topogigio@gmail.com", "password": "test123"}
    )
    print(res.json())

    new_user = UserResponse(**res.json())

    assert new_user.email == "topogigio@gmail.com"
    assert res.status_code == 201
