import logging
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..crud import create_category as create_category_record
from ..crud import get_categories, modify_category, soft_delete_category
from ..database import get_db
from ..schemas import CategoryCreate, CategoryDelete, CategoryRead, CategoryUpdate

logger = logging.getLogger("app.routers.categories")
router = APIRouter(tags=["categories"])


@router.get("/", response_model=list[CategoryRead])
def list_categories(db: Session = Depends(get_db)):
    try:
        return get_categories(db)
    except Exception as exc:
        logger.error("Failed to fetch categories via API", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
        )


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def add_category(category_in: CategoryCreate, db: Session = Depends(get_db)):
    try:
        return create_category_record(db=db, name=category_in.name)
    except Exception as exc:
        logger.error("Failed to create category via API", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
        )


@router.patch("/{category_id}", response_model=CategoryRead)
def update_category(
    category_id: int, category_in: CategoryUpdate, db: Session = Depends(get_db)
):
    try:
        return modify_category(db=db, category_id=category_id, category_in=category_in)
    except Exception as exc:
        logger.error("Failed to modify category via API", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
        )


@router.delete("/{category_id}", response_model=CategoryDelete)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    try:
        category_in = CategoryDelete(
            id=category_id, deleted_at=datetime.now()
        )  # Pass deleted_at to mark as deleted
        return soft_delete_category(
            db=db, category_id=category_id, category_in=category_in
        )
    except Exception as exc:
        logger.error("Failed to delete category via API", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
        )
