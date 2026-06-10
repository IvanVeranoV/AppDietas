import logging
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..crud import (
    create_calendar_menu,
    get_calendar_menus,
    modify_calendar_menu,
    soft_delete_calendar_menu,
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
    try:
        return get_calendar_menus(db)
    except Exception as exc:
        logger.error("Failed to fetch menus via API", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
        )


@router.post("/", response_model=CalendarMenuRead, status_code=status.HTTP_201_CREATED)
def add_menu(menu_in: CalendarMenuCreate, db: Session = Depends(get_db)):
    try:
        return create_calendar_menu(
            db=db,
            date=menu_in.date,
            user_id=menu_in.user_id,
            recipe_id=menu_in.recipe_id,
            meal_type=menu_in.meal_type,
        )
    except Exception as exc:
        logger.error("Failed to create menu via API", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
        )


@router.patch("/{menu_id}", response_model=CalendarMenuRead)
def update_menu(
    menu_id: int, menu_in: CalendarMenuUpdate, db: Session = Depends(get_db)
):
    try:
        return modify_calendar_menu(
            db=db, calendar_menu_id=menu_id, calendar_menu_in=menu_in
        )
    except Exception as exc:
        logger.error("Failed to modify menu via API", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
        )


@router.delete("/{menu_id}", response_model=CalendarMenuDelete)
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    try:
        menu_in = CalendarMenuDelete(id=menu_id, deleted_at=datetime.now())
        return soft_delete_calendar_menu(
            db=db, calendar_menu_id=menu_id, calendar_menu_in=menu_in
        )
    except Exception as exc:
        logger.error("Failed to delete menu via API", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
        )
