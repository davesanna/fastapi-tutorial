import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# from alembic import command

from app.config import settings
from app.database.database import Base, get_db
from app.main import app
from app.schemas.schemas import UserResponse, PostTable
from oauth2 import create_access_token

# during testing we can hard code the variables
SQLALCHEMY_DATABASE_URL = "postgresql://%s:%s@%s/%s" % (
    settings.database_username,
    settings.database_password,
    settings.database_hostname,
    settings.database_name + "_test",
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)  # sqlalchemy commands
    Base.metadata.create_all(bind=engine)  # sqlalchemy commands
    # command.upgrade("head") alembic commands
    # command.downgrade("base") alembic commands

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "topogigio@gmail.com", "password": "test123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]

    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token(data={"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@pytest.fixture
def test_posts(test_user, session):
    posts_data = [
        {
            "title": "First Title",
            "content": "first content",
            "owner_id": test_user["id"],
        },
        {
            "title": "Second Title",
            "content": "second content",
            "owner_id": test_user["id"],
        },
        {
            "title": "First Title",
            "content": "third content",
            "owner_id": test_user["id"],
        },
    ]

    def create_post_model(post):
        return PostTable(**post)

    posts = list(map(create_post_model, posts_data))

    session.add_all(posts)

    session.commit()

    queried_posts = session.query(PostTable).all()

    return queried_posts
