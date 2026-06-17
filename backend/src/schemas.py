from datetime import date as date_type
from datetime import datetime

from pydantic import BaseModel, Field

# --- Ingredient Schemas ---


class IngredientBase(BaseModel):
    name: str = Field(..., max_length=100)
    is_fresh: bool = Field(default=False)
    category_id: int | None = Field(default=None)


class IngredientCreate(IngredientBase):
    category_name: str | None = Field(default=None)


class IngredientRead(IngredientBase):
    id: int
    category_id: int | None

    class Config:
        from_attributes = True


class IngredientUpdate(IngredientBase):
    category_id: int | None


class IngredientDelete(BaseModel):
    id: int
    deleted_at: datetime

    class Config:
        from_attributes = True


# --- Category Schemas ---


class CategoryBase(BaseModel):
    name: str = Field(..., max_length=100)


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int

    class Config:
        from_attributes = True


class CategoryUpdate(CategoryBase):
    pass


class CategoryDelete(BaseModel):
    id: int
    deleted_at: datetime

    class Config:
        from_attributes = True


# --- Recipe Schemas ---


class RecipeBase(BaseModel):
    name: str = Field(..., max_length=255)
    instructions: str | None = Field(default=None)


class RecipeCreate(RecipeBase):
    pass


class RecipeRead(RecipeBase):
    id: int

    class Config:
        from_attributes = True


class RecipeUpdate(RecipeBase):
    pass


class RecipeDelete(BaseModel):
    id: int
    deleted_at: datetime

    class Config:
        from_attributes = True


# --- RecipeIngredient Schemas ---


class RecipeIngredientBase(BaseModel):
    recipe_id: int
    ingredient_id: int
    quantity: int = Field(..., ge=1)


class RecipeIngredientCreate(RecipeIngredientBase):
    pass


class RecipeIngredientRead(RecipeIngredientBase):
    id: int

    class Config:
        from_attributes = True


class RecipeIngredientUpdate(BaseModel):
    recipe_id: int | None = None
    ingredient_id: int | None = None
    quantity: int | None = Field(default=None, ge=1)


class RecipeIngredientDelete(BaseModel):
    id: int
    deleted_at: datetime

    class Config:
        from_attributes = True


# --- User Schemas ---


class UserBase(BaseModel):
    name: str = Field(..., max_length=100)
    color_hex: str = Field(..., max_length=7)


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserUpdate(UserBase):
    pass


class UserDelete(BaseModel):
    id: int
    deleted_at: datetime

    class Config:
        from_attributes = True


# --- CalendarMenu Schemas ---


class CalendarMenuBase(BaseModel):
    date: date_type
    user_id: int
    recipe_id: int
    meal_type: str | None = Field(default=None, max_length=50)


class CalendarMenuCreate(CalendarMenuBase):
    pass


class CalendarMenuRead(CalendarMenuBase):
    id: int

    class Config:
        from_attributes = True


class CalendarMenuUpdate(BaseModel):
    date: date_type | None = None
    user_id: int | None = None
    recipe_id: int | None = None
    meal_type: str | None = Field(default=None, max_length=50)


class CalendarMenuDelete(BaseModel):
    id: int
    deleted_at: datetime

    class Config:
        from_attributes = True
