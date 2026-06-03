from pydantic import BaseModel, Field

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
