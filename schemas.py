from pydantic import BaseModel
from typing import Optional

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

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    is_available: Optional[bool] = None
    category_id: Optional[int] = None

class UserCreate(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True