import logging
from sqlalchemy.orm import Session
from .models import Ingredient, Category

logger = logging.getLogger("app.crud")


class CategoryPersistenceError(Exception):
    """Raised when category persistence fails."""
    pass


def get_categories(db: Session):
    """
    Retrieves all product categories from the database.
    """
    try:
        return db.query(Category).all()
    except Exception:
        logger.error("Database error while fetching categories", exc_info=True)
        raise CategoryPersistenceError("Failed to fetch categories from the database.") from None


def create_category(db: Session, name: str) -> Category:
    """
    Creates and persists a new Category in the database.
    """
    try:
        new_category = Category(name=name)
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category
    except Exception:
        logger.error("Database error while creating category", exc_info=True)
        raise CategoryPersistenceError("Failed to create category in the database.") from None


def create_ingredient(db: Session, name: str, is_fresh: bool, category_id: int | None) -> Ingredient:
    """
    Creates and persists a new Ingredient in the database.
    """
    try:
        new_ingredient = Ingredient(
            name=name,
            is_fresh=is_fresh,
            category_id=category_id
        )
        db.add(new_ingredient)
        db.commit()
        db.refresh(new_ingredient)
        return new_ingredient
    except Exception:
        logger.error("Database error while creating ingredient", exc_info=True)
        raise
