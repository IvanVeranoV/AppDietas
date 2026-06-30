import logging
from datetime import datetime

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..crud import create_recipe, get_recipes, modify_recipe, generic_soft_delete
from ..database import get_db
from ..schemas import RecipeCreate, RecipeDelete, RecipeRead, RecipeUpdate

logger = logging.getLogger("app.routers.recipes")
router = APIRouter(tags=["recipes"])


@router.get("", response_model=list[RecipeRead])
@router.get("/", response_model=list[RecipeRead])
def list_recipes(db: Session = Depends(get_db)):
    return get_recipes(db)

@router.post("", response_model=RecipeRead, status_code=status.HTTP_201_CREATED)
@router.post("/", response_model=RecipeRead, status_code=status.HTTP_201_CREATED)
def add_recipe(recipe_in: RecipeCreate, db: Session = Depends(get_db)):
    return create_recipe(
        db=db,
        recipe_in=recipe_in,
    )


@router.patch("/{recipe_id}", response_model=RecipeRead)
def update_recipe(
    recipe_id: int, recipe_in: RecipeUpdate, db: Session = Depends(get_db)
):
    return modify_recipe(db=db, recipe_id=recipe_id, recipe_in=recipe_in)


@router.delete("/{recipe_id}", response_model=RecipeDelete)
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe_in = RecipeDelete(id=recipe_id, deleted_at=datetime.now())
    return generic_soft_delete(db=db, recipe_id=recipe_id, recipe_in=recipe_in)
