import logging
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..crud import create_user, get_users, modify_user, soft_delete_user
from ..database import get_db
from ..schemas import UserCreate, UserDelete, UserRead, UserUpdate

logger = logging.getLogger("app.routers.users")
router = APIRouter(tags=["users"])


@router.get("/", response_model=list[UserRead])
def list_users(db: Session = Depends(get_db)):
    try:
        return get_users(db)
    except Exception as exc:
        logger.error("Failed to fetch users via API", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
        )


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def add_user(user_in: UserCreate, db: Session = Depends(get_db)):
    try:
        return create_user(db=db, name=user_in.name, color_hex=user_in.color_hex)
    except Exception as exc:
        logger.error("Failed to create user via API", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
        )


@router.patch("/{user_id}", response_model=UserRead)
def update_user(user_id: int, user_in: UserUpdate, db: Session = Depends(get_db)):
    try:
        return modify_user(db=db, user_id=user_id, user_in=user_in)
    except Exception as exc:
        logger.error("Failed to modify user via API", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
        )


@router.delete("/{user_id}", response_model=UserDelete)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user_in = UserDelete(id=user_id, deleted_at=datetime.now())
        return soft_delete_user(db=db, user_id=user_id, user_in=user_in)
    except Exception as exc:
        logger.error("Failed to delete user via API", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
        )
