from pydantic import BaseModel, EmailStr
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
    class Config:
        orm_mode = True
class TransactionBase(BaseModel):
    product_id: int
    quantity: int
    type: str  # 'purchase' or 'sale'
class TransactionCreate(TransactionBase):
    pass
class Transaction(TransactionBase):
    id: int
    timestamp: datetime 
    class Config:
        orm_mode = True
class CategoryBase(BaseModel):
    name: str
class CategoryCreate(CategoryBase):
    pass
class Category(CategoryBase):
    id: int
    class Config:
        orm_mode = True
class SupplierBase(BaseModel):
    name: str
    contact_info: int
class SupplierCreate(SupplierBase):
    pass    
class Supplier(SupplierBase):
    id: int
    class Config:
        orm_mode = True
class UserBase(BaseModel):
    email:EmailStr
   
class UserCreate(UserBase):
    email: EmailStr
    username: str
    password: str
    role : str = "clerk"
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