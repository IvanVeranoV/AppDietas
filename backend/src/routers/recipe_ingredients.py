import logging
from datetime import datetime

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..crud import (
    create_recipe_ingredient,
    get_recipe_ingredients,
    modify_recipe_ingredient,
    generic_soft_delete,
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
    return get_recipe_ingredients(db)


@router.post(
    "/", response_model=RecipeIngredientRead, status_code=status.HTTP_201_CREATED
)
def add_recipe_ingredient(
    recipe_ingredient_in: RecipeIngredientCreate,
    db: Session = Depends(get_db),
):
    return create_recipe_ingredient(
        db=db,
        recipe_id=recipe_ingredient_in.recipe_id,
        ingredient_id=recipe_ingredient_in.ingredient_id,
        quantity=recipe_ingredient_in.quantity,
    )


@router.patch("/{recipe_ingredient_id}", response_model=RecipeIngredientRead)
def update_recipe_ingredient(
    recipe_ingredient_id: int,
    recipe_ingredient_in: RecipeIngredientUpdate,
    db: Session = Depends(get_db),
):
    return modify_recipe_ingredient(
        db=db,
        recipe_ingredient_id=recipe_ingredient_id,
        recipe_ingredient_in=recipe_ingredient_in,
    )


@router.delete("/{recipe_ingredient_id}", response_model=RecipeIngredientDelete)
def delete_recipe_ingredient(recipe_ingredient_id: int, db: Session = Depends(get_db)):
    recipe_ingredient_in = RecipeIngredientDelete(
        id=recipe_ingredient_id, deleted_at=datetime.now()
    )
    return generic_soft_delete(
        db=db,
        recipe_ingredient_id=recipe_ingredient_id,
        recipe_ingredient_in=recipe_ingredient_in,
    )
