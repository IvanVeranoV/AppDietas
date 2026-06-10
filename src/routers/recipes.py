import logging
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..crud import create_recipe, get_recipes, modify_recipe, soft_delete_recipe
from ..database import get_db
from ..schemas import RecipeCreate, RecipeDelete, RecipeRead, RecipeUpdate

logger = logging.getLogger("app.routers.recipes")
router = APIRouter(tags=["recipes"])


@router.get("/", response_model=list[RecipeRead])
def list_recipes(db: Session = Depends(get_db)):
    try:
        return get_recipes(db)
    except Exception as exc:
        logger.error("Failed to fetch recipes via API", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
        )


@router.post("/", response_model=RecipeRead, status_code=status.HTTP_201_CREATED)
def add_recipe(recipe_in: RecipeCreate, db: Session = Depends(get_db)):
    try:
        return create_recipe(
            db=db,
            name=recipe_in.name,
            instructions=recipe_in.instructions,
        )
    except Exception as exc:
        logger.error("Failed to create recipe via API", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
        )


@router.patch("/{recipe_id}", response_model=RecipeRead)
def update_recipe(
    recipe_id: int, recipe_in: RecipeUpdate, db: Session = Depends(get_db)
):
    try:
        return modify_recipe(db=db, recipe_id=recipe_id, recipe_in=recipe_in)
    except Exception as exc:
        logger.error("Failed to modify recipe via API", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
        )


@router.delete("/{recipe_id}", response_model=RecipeDelete)
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    try:
        recipe_in = RecipeDelete(id=recipe_id, deleted_at=datetime.now())
        return soft_delete_recipe(db=db, recipe_id=recipe_id, recipe_in=recipe_in)
    except Exception as exc:
        logger.error("Failed to delete recipe via API", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
        )
