import logging
import time
from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor

from app.schemas.schemas import (
    Base,
)
from app.utils import get_keys
from app.database.database import engine
from app.routers import post, user, auth

# docu at: 127.0.0.1:8000/docs or at 127.0.0.1:8000/redoc

logging.config.fileConfig("logging.config", disable_existing_loggers=False)
logger = logging.getLogger(__name__)

USERNAME, PASSWORD, HOST_NAME, DB_NAME = get_keys()

# creates table based on sqlalchemy classes if not exist
Base.metadata.create_all(bind=engine)

while True:
    try:
        # cursor to return column names when querying data
        conn = psycopg2.connect(
            user=USERNAME,
            password=PASSWORD,
            host=HOST_NAME,
            database=DB_NAME,
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        logger.info("Database connection was successfull.")
        break

    except Exception as e:
        logger.info(f"Connection failed: {e}")
        time.sleep(2)

app = FastAPI()


@app.get("/")  # path operation
def root():
    return {"message": "yoooooo World"}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
