import logging

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.exceptions import DependencyError

from ..models import RecipeIngredient, Ingredient

from ..crud import (
    create_ingredient,
    get_categories,
    get_ingredients,
    modify_ingredient,
    generic_soft_delete,
)
from ..database import get_db
from ..schemas import IngredientCreate, IngredientRead, IngredientUpdate

logger = logging.getLogger("app.routers.ingredients")
router = APIRouter(tags=["ingredients"])


@router.get("", response_model=list[IngredientRead])
@router.get("/", response_model=list[IngredientRead])
def list_ingredients(db: Session = Depends(get_db)):
    return get_ingredients(db)


@router.post("", response_model=IngredientRead, status_code=status.HTTP_201_CREATED)
@router.post("/", response_model=IngredientRead, status_code=status.HTTP_201_CREATED)
def add_ingredient(
    ingredient_in: IngredientCreate,
    db: Session = Depends(get_db),
):
    categories = get_categories(db)
    category_map = {cat.name.lower().strip(): cat.id for cat in categories}

    category_id = None
    if ingredient_in.category_name:
        normalized_name = ingredient_in.category_name.lower().strip()
        category_id = category_map.get(normalized_name)

        if not category_id:
            logger.info(
                f"Category '{ingredient_in.category_name}' not found. "
                "Assigning None (Uncategorized) to the ingredient."
            )

    return create_ingredient(
        db=db,
        name=ingredient_in.name,
        is_fresh=ingredient_in.is_fresh,
        category_id=category_id,
    )


# En tu routers/ingredients.py
@router.put("/{ingredient_id}", response_model=IngredientRead)
def update_ingredient(
    ingredient_in: IngredientUpdate, 
    db: Session = Depends(get_db)
):
    return modify_ingredient(
        db=db, ingredient_in=ingredient_in
    )


@router.delete("/{ingredient_id}")
def delete_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    used_in_recipes = db.query(RecipeIngredient).filter(RecipeIngredient.ingredient_id == ingredient_id).all()
    
    if used_in_recipes:
        recipe_names = [item.recipe.name for item in used_in_recipes]
        raise DependencyError("Error al borrar el ingrediente", details=recipe_names)
    
    return generic_soft_delete(db=db, model_class=Ingredient, entity_id=ingredient_id)
