import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import post, user, auth, vote

# docu at: 127.0.0.1:8000/docs or at 127.0.0.1:8000/redoc

# logging.config.fileConfig("logging.config", disable_existing_loggers=False)
# logger = logging.getLogger(__name__)

# from app.schemas.schemas import Base
# from app.database.database import engine
# creates table based on sqlalchemy classes if not exist (not needed anymore with Alembic) # noqa: E501
# Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")  # path operation
def root():
    return {"message": "Hey Ubuntu!!"}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
