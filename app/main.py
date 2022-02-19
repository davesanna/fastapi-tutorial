import logging

import time
from fastapi import FastAPI, Response, status, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor

from app.models.post import Post
from app.utils import get_keys

# docu at: 127.0.0.1:8000/docs or at 127.0.0.1:8000/redoc

logging.config.fileConfig("logging.config", disable_existing_loggers=True)
logger = logging.getLogger(__name__)

USERNAME, PASSWORD = get_keys()

while True:
    try:
        # cursor to return column names when querying data
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user=USERNAME,
            password=PASSWORD,
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        logger.info("Database connection was successfull.")
        break

    except Exception as e:
        logger.info(f"Connection failed: {e}")
        time.sleep(2)

app = FastAPI()

my_posts = [
    {"title": "title post 1", "content": "content post 1", "id": 1},
    {"title": "title post 2", "content": "content post 2", "id": 2},
]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            print(p)
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.get("/")  # path operation
def root():
    return {"message": "yoooooo World"}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM post""")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):

    cursor.execute(
        """ INSERT INTO post (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
        (post.title, post.content, post.published),
    )

    new_post = cursor.fetchone()
    conn.commit()

    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int):

    cursor.execute(""" SELECT * FROM post WHERE id = %s""", (str(id)))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found",
        )

    return post


@app.delete("/posts/{id}", status_code=status.HTTP_404_NOT_FOUND)
def delete_post(id: int):
    cursor.execute(""" DELETE FROM post WHERE id = %s RETURNING *""", str(id))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found.",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    cursor.execute(
        """UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
        (post.title, post.content, post.published, str(id)),
    )
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found.",
        )

    return {"data": updated_post}
