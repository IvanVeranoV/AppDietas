import logging
from sqlalchemy.orm import Session
from .models import Ingredient, Category
from .schemas import IngredientUpdate, CategoryUpdate
from .exceptions import ResourceNotFoundError, DatabaseError

logger = logging.getLogger("app.crud")


# --- Reusable Helpers (Abstracción limpia sin duplicados) ---

def _get_entity_by_id(db: Session, model_class, entity_id: int):
    """
    Retrieves an entity by ID from the database.
    Raises ResourceNotFoundError if not found.
    """
    entity = db.query(model_class).filter(model_class.id == entity_id).first()
    if not entity:
        raise ResourceNotFoundError(f"{model_class.__name__} with id {entity_id} does not exist.")
    return entity


def _update_entity_fields(db: Session, entity, update_schema):
    """
    Updates entity fields from a Pydantic schema dynamically.
    Only updates fields explicitly set by the client.
    """
    update_data = update_schema.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(entity, field, value)
    return entity


# --- Core CRUD Functions ---

def get_categories(db: Session):
    try:
        return db.query(Category).all()
    except Exception as e:
        logger.error("Database error while fetching categories", exc_info=True)
        raise DatabaseError("Failed to fetch categories from the database.") from e


def create_category(db: Session, name: str) -> Category:
    try:
        new_category = Category(name=name)
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category
    except Exception as e:
        db.rollback()  # ¡Obligatorio para liberar la transacción!
        logger.error("Database error while creating category", exc_info=True)
        raise DatabaseError("Failed to create category in the database.") from e


def modify_category(db: Session, category_id: int, category_in: CategoryUpdate) -> Category:
    try:
        category = _get_entity_by_id(db, Category, category_id)
        updated_category = _update_entity_fields(db, category, category_in)
        db.commit()
        db.refresh(updated_category)
        return updated_category
    except ResourceNotFoundError:
        # Re-lanzamos sin alterar, para que el router sepa que es un 404
        raise
    except Exception as e:
        db.rollback()  # Evita bloquear las conexiones
        logger.error(f"Database error while modifying category {category_id}", exc_info=True)
        raise DatabaseError("Failed to modify category in the database.") from e


def create_ingredient(db: Session, name: str, is_fresh: bool, category_id: int | None) -> Ingredient:
    try:
        new_ingredient = Ingredient(name=name, is_fresh=is_fresh, category_id=category_id)
        db.add(new_ingredient)
        db.commit()
        db.refresh(new_ingredient)
        return new_ingredient
    except Exception as e:
        db.rollback()
        logger.error("Database error while creating ingredient", exc_info=True)
        raise DatabaseError("Failed to create ingredient in the database.") from e


def modify_ingredient(db: Session, ingredient_id: int, ingredient_in: IngredientUpdate) -> Ingredient:
    try:
        ingredient = _get_entity_by_id(db, Ingredient, ingredient_id)
        updated_ingredient = _update_entity_fields(db, ingredient, ingredient_in)
        db.commit()
        db.refresh(updated_ingredient)
        return updated_ingredient
    except ResourceNotFoundError:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Database error while modifying ingredient {ingredient_id}", exc_info=True)
        raise DatabaseError("Failed to modify ingredient in the database.") from e