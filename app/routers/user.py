from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session

from app.utils import hash
from app.schemas.schemas import (
    UserResponse,
    UserTable,
    UserCreate,
)
from app.database.database import get_db

router = APIRouter()

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    # generate hashing for psw
    hashed_psw = hash(user.password)
    user.password = hashed_psw

    # create user
    new_user = UserTable(**user.dict())

    # add user
    db.add(new_user)

    # commit changes
    db.commit()

    # return for confirmation
    db.refresh(new_user)  # as RETURNING * in SQL

    return new_user


@router.get("/users/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(UserTable).filter(UserTable.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found",
        )

    return user
