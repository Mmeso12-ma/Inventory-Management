from email.policy import default
from operator import is_
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
    created_at= Column(DateTime(timezone=True), default=datetime.utcnow)
class Supplier(Base):
    __tablename__ = 'suppliers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    contact_info = Column(String, index=True)
    products = relationship("Product",back_populates="suppliers")
    email=(Column(String, unique= True, nullable= False, index= True))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
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
    quantity=Column(Integer, nullable= False,  default=0)
    created_at= Column(DateTime(timezone=True), default=datetime.utcnow)
class Transaction(Base):
    __tablename__ = 'transaction'
    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, ForeignKey('products.name'), nullable=True)
    quantity = Column(Integer, nullable=False)
    type = Column(String, nullable=False)  # 'purchase' or 'sale'
    timestamp = Column(DateTime, default=datetime.utcnow)
    contact_info = Column(String, index=True)
    total_price = Column(Float, nullable=True)
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
    role= Column(String, nullable= False, default= 'clerk')
class Employee(Base):
    __tablename__= 'employee'
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    position = Column(String, index=True, nullable=False)
    contact_info = Column(String, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    is_active = Column(Boolean, default=True)


