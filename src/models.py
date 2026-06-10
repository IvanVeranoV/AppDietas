from datetime import date as date_type, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class AuditMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now()
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, default=None, onupdate=datetime.now()
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_by_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    updated_by_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    deleted_by_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )


class Category(AuditMixin, Base):
    __tablename__ = "product_categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    # Relationships (No cascade delete-orphan, DB sets category_id to NULL on delete)
    ingredients: Mapped[list["Ingredient"]] = relationship(
        back_populates="category", foreign_keys="[Ingredient.category_id]"
    )


class Ingredient(AuditMixin, Base):
    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_fresh: Mapped[bool] = mapped_column(Boolean, default=False)
    category_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("product_categories.id", ondelete="SET NULL"), nullable=True
    )

    # Relationships
    category: Mapped["Category | None"] = relationship(
        back_populates="ingredients", foreign_keys="[Ingredient.category_id]"
    )
    recipe_ingredients: Mapped[list["RecipeIngredient"]] = relationship(
        back_populates="ingredient",
        cascade="all, delete-orphan",
        foreign_keys="[RecipeIngredient.ingredient_id]",
    )


class Recipe(AuditMixin, Base):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    instructions: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    recipe_ingredients: Mapped[list["RecipeIngredient"]] = relationship(
        back_populates="recipe",
        cascade="all, delete-orphan",
        foreign_keys="[RecipeIngredient.recipe_id]",
    )
    calendar_menus: Mapped[list["CalendarMenu"]] = relationship(
        back_populates="recipe",
        cascade="all, delete-orphan",
        foreign_keys="[CalendarMenu.recipe_id]",
    )


class RecipeIngredient(AuditMixin, Base):
    __tablename__ = "recipe_ingredients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    recipe_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False
    )
    ingredient_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("ingredients.id", ondelete="CASCADE"), nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relationships
    recipe: Mapped["Recipe"] = relationship(
        back_populates="recipe_ingredients", foreign_keys="[RecipeIngredient.recipe_id]"
    )
    ingredient: Mapped["Ingredient"] = relationship(
        back_populates="recipe_ingredients",
        foreign_keys="[RecipeIngredient.ingredient_id]",
    )


class User(AuditMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    color_hex: Mapped[str] = mapped_column(String(7), nullable=False)

    # Relationships
    calendar_menus: Mapped[list["CalendarMenu"]] = relationship(
        "CalendarMenu",
        back_populates="user",
        cascade="all, delete-orphan",
        foreign_keys="[CalendarMenu.user_id]",
    )


class CalendarMenu(AuditMixin, Base):
    __tablename__ = "calendar_menus"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    date: Mapped[date_type] = mapped_column(Date, nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    recipe_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False
    )
    meal_type: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # Relationships
    user: Mapped["User"] = relationship(
        "User", back_populates="calendar_menus", foreign_keys="[CalendarMenu.user_id]"
    )
    recipe: Mapped["Recipe"] = relationship(
        "Recipe",
        back_populates="calendar_menus",
        foreign_keys="[CalendarMenu.recipe_id]",
    )
