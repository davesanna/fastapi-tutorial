import time
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

# docu at: 127.0.0.1:8000/docs or at 127.0.0.1:8000/redoc


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


while True:
    try:
        conn = psycopg2.connect(host="localhost", database= 'fastapi', user="postgres", password='crgkart96', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfull.")
        break

    except Exception as e:
        print(f"Connection failed: {e}")
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
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):

    post_dict = post.dict()
    post_dict["id"] = randrange(start=0, stop=1000000)
    my_posts.append(post_dict)

    return {"data": post_dict}


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found",
        )

    return post


@app.delete("/posts/{id}", status_code=status.HTTP_404_NOT_FOUND)
def delete_post(id: int):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found.",
        )
    my_posts.pop(index)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found.",
        )
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict

    return {"data": post_dict}
