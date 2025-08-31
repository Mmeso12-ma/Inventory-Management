from pydantic import BaseModel
from datetime import datetime
class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: float
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
    