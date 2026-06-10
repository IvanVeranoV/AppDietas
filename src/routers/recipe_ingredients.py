import logging
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..crud import (
    create_recipe_ingredient,
    get_recipe_ingredients,
    modify_recipe_ingredient,
    soft_delete_recipe_ingredient,
)
from ..database import get_db
from ..schemas import (
    RecipeIngredientCreate,
    RecipeIngredientDelete,
    RecipeIngredientRead,
    RecipeIngredientUpdate,
)

logger = logging.getLogger("app.routers.recipe_ingredients")
router = APIRouter(tags=["recipe-ingredients"])


@router.get("/", response_model=list[RecipeIngredientRead])
def list_recipe_ingredients(db: Session = Depends(get_db)):
    try:
        return get_recipe_ingredients(db)
    except Exception as exc:
        logger.error("Failed to fetch recipe ingredients via API", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
        )


@router.post(
    "/", response_model=RecipeIngredientRead, status_code=status.HTTP_201_CREATED
)
def add_recipe_ingredient(
    recipe_ingredient_in: RecipeIngredientCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_recipe_ingredient(
            db=db,
            recipe_id=recipe_ingredient_in.recipe_id,
            ingredient_id=recipe_ingredient_in.ingredient_id,
            quantity=recipe_ingredient_in.quantity,
        )
    except Exception as exc:
        logger.error("Failed to create recipe ingredient via API", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
        )


@router.patch("/{recipe_ingredient_id}", response_model=RecipeIngredientRead)
def update_recipe_ingredient(
    recipe_ingredient_id: int,
    recipe_ingredient_in: RecipeIngredientUpdate,
    db: Session = Depends(get_db),
):
    try:
        return modify_recipe_ingredient(
            db=db,
            recipe_ingredient_id=recipe_ingredient_id,
            recipe_ingredient_in=recipe_ingredient_in,
        )
    except Exception as exc:
        logger.error("Failed to modify recipe ingredient via API", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
        )


@router.delete("/{recipe_ingredient_id}", response_model=RecipeIngredientDelete)
def delete_recipe_ingredient(recipe_ingredient_id: int, db: Session = Depends(get_db)):
    try:
        recipe_ingredient_in = RecipeIngredientDelete(
            id=recipe_ingredient_id, deleted_at=datetime.now()
        )
        return soft_delete_recipe_ingredient(
            db=db,
            recipe_ingredient_id=recipe_ingredient_id,
            recipe_ingredient_in=recipe_ingredient_in,
        )
    except Exception as exc:
        logger.error("Failed to delete recipe ingredient via API", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
        )
