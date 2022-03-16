import logging

# import time
# import psycopg2
# from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ..config import settings
logger = logging.getLogger(__name__)


SQLALCHEMY_DATABASE_URL = "postgresql://%s:%s@%s/%s" % (
    settings.database_username,
    settings.database_password,
    settings.database_hostname,
    settings.database_name,
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


# while True:
#     try:
#         # cursor to return column names when querying data
#         conn = psycopg2.connect(
#             user=USERNAME,
#             password=PASSWORD,
#             host=HOST_NAME,
#             database=DB_NAME,
#             cursor_factory=RealDictCursor,
#         )
#         cursor = conn.cursor()
#         logger.info("Database connection was successfull.")
#         break

#     except Exception as e:
#         logger.info(f"Connection failed: {e}")
#         time.sleep(2)
