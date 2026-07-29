from pydantic import BaseModel

class ItemCreate(BaseModel):
    name: str
    price: float
    is_available: bool = True
    category_id: int

class ItemResponse(ItemCreate):
    id: int

    class Config:
        from_attributes = True

class CategoryCreate(BaseModel):
    name: str

class CategoryResponse(CategoryCreate):
    id: int

    class Config:
        from_attributes = True