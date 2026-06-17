import logging

from sqlalchemy.orm import Session

from .exceptions import DatabaseError, ResourceNotFoundError
from .models import CalendarMenu, Category, Ingredient, Recipe, RecipeIngredient, User
from .schemas import (
    CalendarMenuDelete,
    CalendarMenuUpdate,
    CategoryDelete,
    CategoryUpdate,
    IngredientDelete,
    IngredientUpdate,
    RecipeDelete,
    RecipeIngredientDelete,
    RecipeIngredientUpdate,
    RecipeUpdate,
    UserDelete,
    UserUpdate,
)

logger = logging.getLogger("app.crud")


# --- Reusable Helpers (Abstracción limpia sin duplicados) ---


def _get_entity_by_id(db: Session, model_class, entity_id: int):
    """
    Retrieves an entity by ID from the database.
    Raises ResourceNotFoundError if not found.
    """
    entity = db.query(model_class).filter(model_class.id == entity_id).first()
    if not entity:
        raise ResourceNotFoundError(
            f"{model_class.__name__} with id {entity_id} does not exist."
        )
    return entity


def _update_entity_fields(entity, update_schema):
    """
    Updates entity fields from a Pydantic schema dynamically.
    Only updates fields explicitly set by the client.
    Ignores internal audit identifiers to avoid accidental overwrites.
    """
    protected_fields = {
        "id",
        "created_at",
        "updated_at",
        "created_by_id",
        "updated_by_id",
        "deleted_by_id",
    }
    update_data = update_schema.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field in protected_fields:
            continue
        setattr(entity, field, value)
    return entity


# --- Core CRUD Functions ---

# --- Category CRUD ---


def get_categories(db: Session):
    try:
        return db.query(Category).filter(Category.deleted_at.is_(None)).all()
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


def modify_category(
    db: Session, category_id: int, category_in: CategoryUpdate
) -> Category:
    try:
        category = _get_entity_by_id(db, Category, category_id)
        updated_category = _update_entity_fields(category, category_in)
        db.commit()
        db.refresh(updated_category)
        return updated_category
    except ResourceNotFoundError:
        # Re-lanzamos sin alterar, para que el router sepa que es un 404
        raise
    except Exception as e:
        db.rollback()  # Evita bloquear las conexiones
        logger.error(
            f"Database error while modifying category {category_id}", exc_info=True
        )
        raise DatabaseError("Failed to modify category in the database.") from e


def soft_delete_category(
    db: Session, category_id: int, category_in: CategoryDelete
) -> Category:
    try:
        category = _get_entity_by_id(db, Category, category_id)
        deleted_category = _update_entity_fields(category, category_in)
        db.commit()
        db.refresh(deleted_category)
        return deleted_category
    except ResourceNotFoundError:
        raise
    except Exception as e:
        db.rollback()
        logger.error(
            f"Database error while soft deleting category {category_id}", exc_info=True
        )
        raise DatabaseError("Failed to delete category in the database.") from e


# --- Ingredient CRUD ---


def get_ingredients(db: Session):
    try:
        return db.query(Ingredient).filter(Ingredient.deleted_at.is_(None)).all()
    except Exception as e:
        logger.error("Database error while fetching ingredients", exc_info=True)
        raise DatabaseError("Failed to fetch ingredients from the database.") from e


def create_ingredient(
    db: Session, name: str, is_fresh: bool, category_id: int | None
) -> Ingredient:
    try:
        new_ingredient = Ingredient(
            name=name, is_fresh=is_fresh, category_id=category_id
        )
        db.add(new_ingredient)
        db.commit()
        db.refresh(new_ingredient)
        return new_ingredient
    except Exception as e:
        db.rollback()
        logger.error("Database error while creating ingredient", exc_info=True)
        raise DatabaseError("Failed to create ingredient in the database.") from e


def modify_ingredient(
    db: Session, ingredient_id: int, ingredient_in: IngredientUpdate
) -> Ingredient:
    try:
        ingredient = _get_entity_by_id(db, Ingredient, ingredient_id)
        updated_ingredient = _update_entity_fields(ingredient, ingredient_in)
        db.commit()
        db.refresh(updated_ingredient)
        return updated_ingredient
    except ResourceNotFoundError:
        raise
    except Exception as e:
        db.rollback()
        logger.error(
            f"Database error while modifying ingredient {ingredient_id}", exc_info=True
        )
        raise DatabaseError("Failed to modify ingredient in the database.") from e


def soft_delete_ingredient(
    db: Session, ingredient_id: int, ingredient_in: IngredientDelete
) -> Ingredient:
    try:
        ingredient = _get_entity_by_id(db, Ingredient, ingredient_id)
        deleted_ingredient = _update_entity_fields(ingredient, ingredient_in)
        db.commit()
        db.refresh(deleted_ingredient)
        return deleted_ingredient
    except ResourceNotFoundError:
        raise
    except Exception as e:
        db.rollback()
        logger.error(
            f"Database error while soft deleting ingredient {ingredient_id}",
            exc_info=True,
        )
        raise DatabaseError("Failed to delete ingredient in the database.") from e


# --- Recipe CRUD ---


def get_recipes(db: Session):
    try:
        return db.query(Recipe).filter(Recipe.deleted_at.is_(None)).all()
    except Exception as e:
        logger.error("Database error while fetching recipes", exc_info=True)
        raise DatabaseError("Failed to fetch recipes from the database.") from e


def create_recipe(
    db: Session, name: str, instructions: str | None = None
) -> Recipe:
    try:
        new_recipe = Recipe(name=name, instructions=instructions)
        db.add(new_recipe)
        db.commit()
        db.refresh(new_recipe)
        return new_recipe
    except Exception as e:
        db.rollback()
        logger.error("Database error while creating recipe", exc_info=True)
        raise DatabaseError("Failed to create recipe in the database.") from e


def modify_recipe(db: Session, recipe_id: int, recipe_in: RecipeUpdate) -> Recipe:
    try:
        recipe = _get_entity_by_id(db, Recipe, recipe_id)
        updated_recipe = _update_entity_fields(recipe, recipe_in)
        db.commit()
        db.refresh(updated_recipe)
        return updated_recipe
    except ResourceNotFoundError:
        raise
    except Exception as e:
        db.rollback()
        logger.error(
            f"Database error while modifying recipe {recipe_id}", exc_info=True
        )
        raise DatabaseError("Failed to modify recipe in the database.") from e


def soft_delete_recipe(db: Session, recipe_id: int, recipe_in: RecipeDelete) -> Recipe:
    try:
        recipe = _get_entity_by_id(db, Recipe, recipe_id)
        deleted_recipe = _update_entity_fields(recipe, recipe_in)
        db.commit()
        db.refresh(deleted_recipe)
        return deleted_recipe
    except ResourceNotFoundError:
        raise
    except Exception as e:
        db.rollback()
        logger.error(
            f"Database error while soft deleting recipe {recipe_id}", exc_info=True
        )
        raise DatabaseError("Failed to delete recipe from the database.") from e


# --- RecipeIngredient CRUD ---


def get_recipe_ingredients(db: Session):
    try:
        return (
            db.query(RecipeIngredient)
            .filter(RecipeIngredient.deleted_at.is_(None))
            .all()
        )
    except Exception as e:
        logger.error("Database error while fetching recipe ingredients", exc_info=True)
        raise DatabaseError(
            "Failed to fetch recipe ingredients from the database."
        ) from e


def create_recipe_ingredient(
    db: Session, recipe_id: int, ingredient_id: int, quantity: int
) -> RecipeIngredient:
    try:
        new_recipe_ingredient = RecipeIngredient(
            recipe_id=recipe_id,
            ingredient_id=ingredient_id,
            quantity=quantity,
        )
        db.add(new_recipe_ingredient)
        db.commit()
        db.refresh(new_recipe_ingredient)
        return new_recipe_ingredient
    except Exception as e:
        db.rollback()
        logger.error("Database error while creating recipe ingredient", exc_info=True)
        raise DatabaseError(
            "Failed to create recipe ingredient in the database."
        ) from e


def modify_recipe_ingredient(
    db: Session, recipe_ingredient_id: int, recipe_ingredient_in: RecipeIngredientUpdate
) -> RecipeIngredient:
    try:
        recipe_ingredient = _get_entity_by_id(
            db, RecipeIngredient, recipe_ingredient_id
        )
        updated_recipe_ingredient = _update_entity_fields(
            recipe_ingredient, recipe_ingredient_in
        )
        db.commit()
        db.refresh(updated_recipe_ingredient)
        return updated_recipe_ingredient
    except ResourceNotFoundError:
        raise
    except Exception as e:
        db.rollback()
        logger.error(
            f"Database error while modifying recipe ingredient {recipe_ingredient_id}",
            exc_info=True,
        )
        raise DatabaseError(
            "Failed to modify recipe ingredient in the database."
        ) from e


def soft_delete_recipe_ingredient(
    db: Session, recipe_ingredient_id: int, recipe_ingredient_in: RecipeIngredientDelete
) -> RecipeIngredient:
    try:
        recipe_ingredient = _get_entity_by_id(
            db, RecipeIngredient, recipe_ingredient_id
        )
        deleted_recipe_ingredient = _update_entity_fields(
            recipe_ingredient, recipe_ingredient_in
        )
        db.commit()
        db.refresh(deleted_recipe_ingredient)
        return deleted_recipe_ingredient
    except ResourceNotFoundError:
        raise
    except Exception as e:
        db.rollback()
        logger.error(
            f"Database error while soft deleting recipe ingredient {recipe_ingredient_id}",
            exc_info=True,
        )
        raise DatabaseError(
            "Failed to delete recipe ingredient from the database."
        ) from e


# --- User CRUD ---


def get_users(db: Session):
    try:
        return db.query(User).filter(User.deleted_at.is_(None)).all()
    except Exception as e:
        logger.error("Database error while fetching users", exc_info=True)
        raise DatabaseError("Failed to fetch users from the database.") from e


def create_user(db: Session, name: str, color_hex: str) -> User:
    try:
        new_user = User(name=name, color_hex=color_hex)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        db.rollback()
        logger.error("Database error while creating user", exc_info=True)
        raise DatabaseError("Failed to create user in the database.") from e


def modify_user(db: Session, user_id: int, user_in: UserUpdate) -> User:
    try:
        user = _get_entity_by_id(db, User, user_id)
        updated_user = _update_entity_fields(user, user_in)
        db.commit()
        db.refresh(updated_user)
        return updated_user
    except ResourceNotFoundError:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Database error while modifying user {user_id}", exc_info=True)
        raise DatabaseError("Failed to modify user in the database.") from e


def soft_delete_user(db: Session, user_id: int, user_in: UserDelete) -> User:
    try:
        user = _get_entity_by_id(db, User, user_id)
        deleted_user = _update_entity_fields(user, user_in)
        db.commit()
        db.refresh(deleted_user)
        return deleted_user
    except ResourceNotFoundError:
        raise
    except Exception as e:
        db.rollback()
        logger.error(
            f"Database error while soft deleting user {user_id}", exc_info=True
        )
        raise DatabaseError("Failed to delete user from the database.") from e


# --- CalendarMenu CRUD ---


def get_calendar_menus(db: Session):
    try:
        return db.query(CalendarMenu).filter(CalendarMenu.deleted_at.is_(None)).all()
    except Exception as e:
        logger.error("Database error while fetching calendar menus", exc_info=True)
        raise DatabaseError("Failed to fetch calendar menus from the database.") from e


def create_calendar_menu(
    db: Session, date, user_id: int, recipe_id: int, meal_type: str | None = None
) -> CalendarMenu:
    try:
        new_calendar_menu = CalendarMenu(
            date=date,
            user_id=user_id,
            recipe_id=recipe_id,
            meal_type=meal_type,
        )
        db.add(new_calendar_menu)
        db.commit()
        db.refresh(new_calendar_menu)
        return new_calendar_menu
    except Exception as e:
        db.rollback()
        logger.error("Database error while creating calendar menu", exc_info=True)
        raise DatabaseError("Failed to create calendar menu in the database.") from e


def modify_calendar_menu(
    db: Session, calendar_menu_id: int, calendar_menu_in: CalendarMenuUpdate
) -> CalendarMenu:
    try:
        calendar_menu = _get_entity_by_id(db, CalendarMenu, calendar_menu_id)
        updated_calendar_menu = _update_entity_fields(calendar_menu, calendar_menu_in)
        db.commit()
        db.refresh(updated_calendar_menu)
        return updated_calendar_menu
    except ResourceNotFoundError:
        raise
    except Exception as e:
        db.rollback()
        logger.error(
            f"Database error while modifying calendar menu {calendar_menu_id}",
            exc_info=True,
        )
        raise DatabaseError("Failed to modify calendar menu in the database.") from e


def soft_delete_calendar_menu(
    db: Session, calendar_menu_id: int, calendar_menu_in: CalendarMenuDelete
) -> CalendarMenu:
    try:
        calendar_menu = _get_entity_by_id(db, CalendarMenu, calendar_menu_id)
        deleted_calendar_menu = _update_entity_fields(calendar_menu, calendar_menu_in)
        db.commit()
        db.refresh(deleted_calendar_menu)
        return deleted_calendar_menu
    except ResourceNotFoundError:
        raise
    except Exception as e:
        db.rollback()
        logger.error(
            f"Database error while soft deleting calendar menu {calendar_menu_id}",
            exc_info=True,
        )
        raise DatabaseError("Failed to delete calendar menu from the database.") from e
