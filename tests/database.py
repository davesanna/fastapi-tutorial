import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# from alembic import command

from app.config import settings
from app.database.database import Base, get_db
from app.main import app

# during testing we can hard code the variables
SQLALCHEMY_DATABASE_URL = "postgresql://%s:%s@%s/%s" % (
    settings.database_username,
    settings.database_password,
    settings.database_hostname,
    settings.database_name + "_test",
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
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


@pytest.fixture(scope="module")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
