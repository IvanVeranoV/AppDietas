import logging
from datetime import date

from src.database import get_db
from src.models import (
    CalendarMenu,
    Category,
    Ingredient,
    Recipe,
    RecipeIngredient,
    User,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("test")


def run_integration_test():
    # Obtener el generador de sesión
    db_gen = get_db()
    db = next(db_gen)
    logger.info("Starting integration test for MVP...")

    try:
        # 1. Test Usuario
        user = User(name="Test User", color_hex="#FF0000")
        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info(f"Created User: {user.id}")

        # 2. Test Categoría
        category = Category(name="Vegetables", created_by_id=user.id)
        db.add(category)
        db.commit()
        db.refresh(category)
        logger.info(f"Created Category: {category.id}")

        # 3. Test Ingrediente (con FK a categoría)
        ingredient = Ingredient(
            name="Carrot", is_fresh=True, category_id=category.id, created_by_id=user.id
        )
        db.add(ingredient)
        db.commit()
        db.refresh(ingredient)
        logger.info(f"Created Ingredient: {ingredient.id}")

        # 4. Test Receta
        recipe = Recipe(
            name="Carrot Soup", instructions="Cook carrots.", created_by_id=user.id
        )
        db.add(recipe)
        db.commit()
        db.refresh(recipe)
        logger.info(f"Created Recipe: {recipe.id}")

        # 5. Test Relación Receta-Ingrediente
        recipe_ing = RecipeIngredient(
            recipe_id=recipe.id,
            ingredient_id=ingredient.id,
            quantity=5,
            created_by_id=user.id,
        )
        db.add(recipe_ing)
        db.commit()
        logger.info("Created RecipeIngredient relationship")

        # 6. Test Menú
        menu = CalendarMenu(
            date=date.today(),
            user_id=user.id,
            recipe_id=recipe.id,
            created_by_id=user.id,
        )
        db.add(menu)
        db.commit()
        logger.info("Created CalendarMenu")

        logger.info("Integration test passed successfully!")

    except Exception:
        db.rollback()
        logger.error("Integration test failed", exc_info=True)
    finally:
        # El generador cierra la sesión automáticamente en su bloque finally
        next(db_gen, None)


if __name__ == "__main__":
    run_integration_test()
