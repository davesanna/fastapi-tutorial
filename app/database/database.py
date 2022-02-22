import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.utils import get_keys

logger = logging.getLogger(__name__)

USERNAME, PASSWORD, HOST_NAME, DB_NAME = get_keys()

SQLALCHEMY_DATABASE_URL = "postgresql://%s:%s@%s/%s" % (
    USERNAME,
    PASSWORD,
    HOST_NAME,
    DB_NAME,
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
