from email.policy import default
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean, Table
from database import Base
from sqlalchemy.orm import relationship
from datetime import datetime
# Association table for many-to-many relationship between Products and Categories
product_category = Table(
    'product_category', 
    Base.metadata,
    Column('product_id', Integer, ForeignKey('products.id')),
    Column('category_id', Integer, ForeignKey('category.id'))   
)
class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    products = relationship("Product", secondary=product_category, back_populates="category")
class Supplier(Base):
    __tablename__ = 'suppliers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    contact_info = Column(Integer, index=True)
    products = relationship("Product",back_populates="suppliers")
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Float, index=True)
    category_id = Column(Integer, ForeignKey('category.id'))
    suppliers_id = Column(Integer, ForeignKey('suppliers.id'))
    category = relationship("Category",secondary=product_category,  back_populates="products")
    suppliers = relationship("Supplier", back_populates="products")
    transaction = relationship("Transaction", back_populates="products")
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="products")
    quantity=Column(Integer)
class Transaction(Base):
    __tablename__ = 'transaction'
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    type = Column(String, nullable=False)  # 'purchase' or 'sale'
    timestamp = Column(DateTime, default=datetime.utcnow)
    contact_info = Column(Integer, index=True)
    total_price = Column(Float, nullable=False)
    products = relationship("Product", back_populates="transaction")
class User(Base):
    __tablename__= 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique = True, index = True, nullable=False)
    hashed_password= Column(String, nullable=False)
    is_active = Column(Boolean, default = True)
    date_created= Column(DateTime, default = datetime.utcnow)
    email= Column(String, unique= True, nullable= False, index= True)
    products = relationship("Product", back_populates="user")
    role= Column(String)


