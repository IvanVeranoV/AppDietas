import logging
from datetime import datetime

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..crud import create_category as create_category_record
from ..crud import get_categories, modify_category, generic_soft_delete
from ..database import get_db
from ..schemas import CategoryCreate, CategoryDelete, CategoryRead, CategoryUpdate

logger = logging.getLogger("app.routers.categories")
router = APIRouter(tags=["categories"])

# Los DatabaseError y ResourceNotFoundError serán capturados por los manejadores globales en main.py


@router.get("", response_model=list[CategoryRead])
@router.get("/", response_model=list[CategoryRead])
def list_categories(db: Session = Depends(get_db)):
    return get_categories(db)


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def add_category(category_in: CategoryCreate, db: Session = Depends(get_db)):
    return create_category_record(db=db, name=category_in.name)


@router.patch("/{category_id}", response_model=CategoryRead)
def update_category(
    category_id: int, category_in: CategoryUpdate, db: Session = Depends(get_db)
):
    return modify_category(db=db, category_id=category_id, category_in=category_in)


@router.delete("/{category_id}", response_model=CategoryDelete)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category_in = CategoryDelete(id=category_id, deleted_at=datetime.now())
    return generic_soft_delete(db=db, category_id=category_id, category_in=category_in)
