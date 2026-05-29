from pydantic import BaseModel, Field

class IngredientBase(BaseModel):
    name: str = Field(..., max_length=100)
    is_fresh: bool = Field(default=False)

class IngredientCreate(IngredientBase):
    category_name: str | None = Field(default=None)

class IngredientRead(IngredientBase):
    id: int
    category_id: int | None

    class Config:
        from_attributes = True


class CategoryCreate(BaseModel):
    name: str = Field(..., max_length=100)


class CategoryRead(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
