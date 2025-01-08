from pydantic import BaseModel, Field
from typing import Optional

# Схема для создания пользователя
class UserCreate(BaseModel):
    username: str = Field(...)
    password: str = Field(...)

# Схема для ответа (без пароля)
class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

# Схема для создания товара
class ItemCreate(BaseModel):
    name: str = Field(...)
    description: Optional[str] = Field(...)
    price: float = Field(...)

# Схема для отображения товара
class ItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float

    class Config:
        from_attributes = True
