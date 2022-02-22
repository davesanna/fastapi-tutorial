from typing import List

from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.schemas import (
    PostTable,
    PostCreate,
    PostUpdate,
    PostResponse,
)

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=List[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(PostTable).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_posts(post: PostCreate, db: Session = Depends(get_db)):

    # cursor.execute(
    #     """ INSERT INTO post (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #     (post.title, post.content, post.published),
    # )

    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = PostTable(**post.dict())
    print(new_post)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # as RETURNING * in SQL

    return new_post


@router.get("/{id}", response_model=PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):

    # cursor.execute(""" SELECT * FROM post WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()

    post = db.query(PostTable).filter(PostTable.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found",
        )

    return post


@router.delete("/{id}", status_code=status.HTTP_404_NOT_FOUND)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" DELETE FROM post WHERE id = %s RETURNING *""", str(id))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    deleted_post = db.query(PostTable).filter(PostTable.id == id)

    if deleted_post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found.",
        )

    deleted_post.delete(synchronize_session=False)  # must be the "query".delete()
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=PostResponse)
def update_post(id: int, post: PostUpdate, db: Session = Depends(get_db)):

    # cursor.execute(
    #     """UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #     (post.title, post.content, post.published, str(id)),
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(PostTable).filter(PostTable.id == id)

    post_to_update = post_query.first()

    if post_to_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found.",
        )

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
