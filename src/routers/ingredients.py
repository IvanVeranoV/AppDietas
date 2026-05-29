import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.models import Ingredient
from ..database import get_db
from ..schemas import IngredientCreate, IngredientRead
from ..crud import get_categories, create_ingredient

logger = logging.getLogger("app.routers.ingredients")
router = APIRouter(tags=["ingredients"])

@router.post("/", response_model=IngredientRead, status_code=status.HTTP_201_CREATED)
def add_ingredient(ingredient_in: IngredientCreate, db: Session = Depends(get_db)):
    """
    Endpoint to create a new ingredient, resolving the category_id from the provided category_name.
    """
    try:
        # Fetch categories to build the O(1) in-memory lookup map
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
            category_id=category_id
        )
        return new_ingredient

    except Exception as e:
        logger.error("Failed to add new ingredient via API", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the ingredient."
        )

@router.get("/", response_model=list[IngredientRead])
def list_ingredients(db: Session = Depends(get_db)):
    """
    Endpoint to list all ingredients.
    """
    try:
        return db.query(Ingredient).all()
    except Exception as e:
        logger.error("Failed to fetch ingredients via API", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching the ingredients."
        )