import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.models import Category
from ..database import get_db
from ..schemas import CategoryCreate, CategoryRead
from ..crud import CategoryPersistenceError, create_category as create_category_record, get_categories

logger = logging.getLogger("app.routers.categories")
router = APIRouter(tags=["categories"])

@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def add_category(category_in: CategoryCreate, db: Session = Depends(get_db)):
    """
    Endpoint to create a new product category.
    """
    try:
        return create_category_record(db=db, name=category_in.name)
    except CategoryPersistenceError as exc:
        logger.error("Failed to create category via API", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc)
        )

@router.get("/", response_model=list[CategoryRead])
def list_categories(db: Session = Depends(get_db)):
    """
    Endpoint to list all product categories.
    """
    try:
        return get_categories(db)
    except CategoryPersistenceError as exc:
        logger.error("Failed to fetch categories via API", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc)
        )
