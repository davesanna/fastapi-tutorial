from tokenize import String
from pydantic import BaseModel
from sqlalchemy import TIMESTAMP, Column, Integer, Boolean, text

from app.database.database import Base


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


class PostTable(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default="True")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
