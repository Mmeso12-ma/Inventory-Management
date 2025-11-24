import email
from functools import total_ordering
from os import name
from tkinter.messagebox import NO
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from datetime import datetime
class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    quantity: int = 0
class ProductCreate(ProductBase):
    pass
class Product(ProductBase):
    id: int
    created_at: Optional[datetime] = None
    class Config:
        from_attributes = True
class TransactionBase(BaseModel):
    product_name: str
    quantity: int
    type: str  # 'purchase' or 'sale'
    total_price: float
    contact_info: Optional[str] = None
    timestamp: datetime | None = None
class TransactionCreate(TransactionBase):
    pass
class TransactionResponse(TransactionBase):
    id: int
    timestamp: datetime | None = None
    class Config:
        from_attribues = True

class CategoryCreate(BaseModel):
    name: str
class CategoryResponse(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True
class SupplierBase(BaseModel):
    name: str
    contact_info : str | None = None
    email: EmailStr
    address: str | None = None
class SupplierCreate(BaseModel):
    name: str
    contact_info : str
class SupplierResponse(BaseModel):
    id: int
    name: str
    contact_info: str | None = None
    class Config:
        from_attributes = True
class UserBase(BaseModel):
    email:EmailStr
   
class UserCreate(UserBase):
    email: EmailStr
    username: str
    password: str
    role : str 
class UserOut(UserBase):
    id: int
    is_active:bool
    email: EmailStr
    role:str
    class Config:
        from_attributes = True
 

class Token(BaseModel):
    access_token: str
    token_type: str