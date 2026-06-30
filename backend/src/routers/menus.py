import logging
from datetime import datetime

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..crud import (
    create_calendar_menu,
    get_calendar_menus,
    modify_calendar_menu,
    generic_soft_delete,
)
from ..database import get_db
from ..schemas import (
    CalendarMenuCreate,
    CalendarMenuDelete,
    CalendarMenuRead,
    CalendarMenuUpdate,
)

logger = logging.getLogger("app.routers.menus")
router = APIRouter(tags=["menus"])


@router.get("/", response_model=list[CalendarMenuRead])
def list_menus(db: Session = Depends(get_db)):
    return get_calendar_menus(db)


@router.post("/", response_model=CalendarMenuRead, status_code=status.HTTP_201_CREATED)
def add_menu(menu_in: CalendarMenuCreate, db: Session = Depends(get_db)):
    return create_calendar_menu(
        db=db,
        date=menu_in.date,
        user_id=menu_in.user_id,
        recipe_id=menu_in.recipe_id,
        meal_type=menu_in.meal_type,
    )


@router.patch("/{menu_id}", response_model=CalendarMenuRead)
def update_menu(
    menu_id: int, menu_in: CalendarMenuUpdate, db: Session = Depends(get_db)
):
    return modify_calendar_menu(
        db=db, calendar_menu_id=menu_id, calendar_menu_in=menu_in
    )


@router.delete("/{menu_id}", response_model=CalendarMenuDelete)
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    menu_in = CalendarMenuDelete(id=menu_id, deleted_at=datetime.now())
    return generic_soft_delete(
        db=db, calendar_menu_id=menu_id, calendar_menu_in=menu_in
    )
