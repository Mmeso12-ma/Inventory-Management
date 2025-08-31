from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from database import Base
from sqlalchemy.orm import relationship
from datetime import datetime
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Float, index=True)
    transactions = relationship("Transaction", back_populates="product")
class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    type = Column(String, nullable=False)  # 'purchase' or 'sale'
    timestamp = Column(DateTime, default=datetime.utcnow)
    product = relationship("Product", back_populates="transactions")
