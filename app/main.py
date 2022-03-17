import logging
from fastapi import FastAPI

from app.schemas.schemas import (
    Base,
)
from app.database.database import engine
from app.routers import post, user, auth, vote

# docu at: 127.0.0.1:8000/docs or at 127.0.0.1:8000/redoc

logging.config.fileConfig("logging.config", disable_existing_loggers=False)
logger = logging.getLogger(__name__)

# creates table based on sqlalchemy classes if not exist
Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")  # path operation
def root():
    return {"message": "yoooooo World"}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
