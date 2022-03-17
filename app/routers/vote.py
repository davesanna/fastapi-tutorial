from os import sync
from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session

from app.utils import hash
from app.schemas.schemas import (
    PostTable,
    Vote,
    VoteTable,
)
from app.database.database import get_db
from oauth2 import get_current_user

router = APIRouter(prefix="/vote", tags=["vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote_post(
    vote: Vote,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    post = db.query(PostTable).filter(PostTable.id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post {vote.post_id} does not exist",
        )

    vote_query = db.query(VoteTable).filter(
        VoteTable.post_id == vote.post_id, VoteTable.user_id == current_user.id
    )

    found_vote = vote_query.first()

    if vote.direction == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user {current_user.id} has already voted on post {vote.post_id}",
            )

        else:
            new_vote = VoteTable(post_id=vote.post_id, user_id=current_user.id)

        db.add(new_vote)
        db.commit()

        return {"message": "successfully added vote"}

    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist"
            )
        else:
            vote_query.delete(synchronize_session=False)
            db.commit()

            return {"message": "Successfully delete vote"}
