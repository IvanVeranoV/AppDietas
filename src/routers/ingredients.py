import logging
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..crud import (
    create_ingredient,
    get_categories,
    get_ingredients,
    modify_ingredient,
    soft_delete_ingredient,
)
from ..database import get_db
from ..schemas import IngredientCreate, IngredientDelete, IngredientRead, IngredientUpdate

logger = logging.getLogger("app.routers.ingredients")
router = APIRouter(tags=["ingredients"])


@router.get("/", response_model=list[IngredientRead])
def list_ingredients(db: Session = Depends(get_db)):
    """
    Endpoint to list all ingredients.
    """
    try:
        return get_ingredients(db)
    except Exception as e:
        logger.error("Failed to fetch ingredients via API", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/", response_model=IngredientRead, status_code=status.HTTP_201_CREATED)
def add_ingredient(
    ingredient_in: IngredientCreate,
    db: Session = Depends(get_db),
):
    try:
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

        new_ingredient = create_ingredient(
            db=db,
            name=ingredient_in.name,
            is_fresh=ingredient_in.is_fresh,
            category_id=category_id,
        )
        return new_ingredient

    except Exception as e:
        logger.error("Failed to add new ingredient via API", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.patch("/{ingredient_id}", response_model=IngredientRead)
def update_ingredient(
    ingredient_id: int, ingredient_in: IngredientUpdate, db: Session = Depends(get_db)
):
    try:
        return modify_ingredient(
            db=db, ingredient_id=ingredient_id, ingredient_in=ingredient_in
        )
    except Exception as e:
        logger.error("Failed to update ingredient via API", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete("/{ingredient_id}", response_model=IngredientDelete)
def delete_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    try:
        ingredient_in = IngredientDelete(id=ingredient_id, deleted_at=datetime.now())
        return soft_delete_ingredient(
            db=db, ingredient_id=ingredient_id, ingredient_in=ingredient_in
        )
    except Exception as e:
        logger.error("Failed to delete ingredient via API", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
