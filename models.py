from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean
from database import Base
from sqlalchemy.orm import relationship
from datetime import datetime
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Float, index=True)
    category_id = Column(Integer, ForeignKey('category.id'))
    supplier_id = Column(Integer, ForeignKey('suppliers.id'))
    category = relationship("Category", back_populates="products")
    supplier = relationship("Supplier", back_populates="products")
    transactions = relationship("Transaction", back_populates="product")
class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    type = Column(String, nullable=False)  # 'purchase' or 'sale'
    timestamp = Column(DateTime, default=datetime.utcnow)
    product = relationship("Product", back_populates="transactions")
class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    products = relationship("Product", secondary="product_categories", back_populates="categories")
class Supplier(Base):
    __tablename__ = 'supplier'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    contact_info = Column(Integer, index=True)
    products = relationship("Product", secondary="product_suppliers", back_populates="suppliers")
class User(Base):
    __tablename__= 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique = True, index = True, nullable=False)
    hashed_password= Column(String, nullable=False)
    is_active = Column(Boolean, default = True)
    date_created= Column(DateTime, default = datetime.utcnow)
    email= Column(String, unique= True, nullable= False, index= True)


