import email
from functools import total_ordering
from os import name
from pydantic import BaseModel, EmailStr
from datetime import datetime
class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    quantity: int 
class ProductCreate(ProductBase):
    pass
class Product(ProductBase):
    id: int
    class Config:
        orm_mode = True
class TransactionBase(BaseModel):
    product_id: int
    quantity: int
    type: str  # 'purchase' or 'sale'
    total_price: float
    contact_info: str
    timestamp: datetime | None = None
class TransactionCreate(TransactionBase):
    pass
class TransactionResponse(TransactionBase):
    id: int
    timestamp: datetime 
    class Config:
        orm_mode = True

class CategoryCreate(BaseModel):
    id: int
    name: str
class CategoryResponse(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True
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
        orm_mode = True
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