from math import prod
import categories
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from datetime import date
from sqlalchemy import func
from models import Product, Transaction, Category, Supplier
import suppliers
import transaction
router = APIRouter(prefix="/reports", tags=["reports"])
@router.get("/daily/{query_date}")
def daily_report(query_date: date, db: Session = Depends(get_db)):
    transactions = db.query(Transaction).filter(
        func.date(Transaction.timestamp) == query_date
    ).all()
    products = db.query(Product).all()
    suppliers = db.query(Supplier).all()
    categories= db.query(Category).all()
    total_sales = sum(t.total_price for t in transactions if t.type == 'sale')
    total_purchases = sum(t.total_price for t in transactions if t.type == 'purchase')
    return{
    "date": query_date,
    "total_sales": total_sales,
    "total_purchases": total_purchases,
    "transactions": transactions,
    "products": products,
    "suppliers": suppliers,
    "categories": categories
}
@router.get("/monthly/{year}/{month}")
def monthly_report(year: int, month: int, db: Session = Depends(get_db)):
    transactions = db.query(Transaction).filter(
        func.extract('year', Transaction.timestamp) == year,
        func.extract('month', Transaction.timestamp) == month
    ).all()
    products = db.query(Product).filter(func.extract('year', Product.created_at) == year,
        func.extract('month', Product.created_at) == month)
    suppliers = db.query(Supplier).filter(
        func.extract('year', Supplier.created_at) == year,  
        func.extract('month', Supplier.created_at) == month
    )
    categories= db.query(Category).filter(
        func.extract('year', Category.created_at) == year,
        func.extract('month', Category.created_at) == month
    )
    total_sales = sum(t.total_price for t in transactions if t.type == 'sale')
    total_purchases = sum(t.total_price for t in transactions if t.type == 'purchase')
    return{
    "year": year,
    "month": month,
    "total_sales": total_sales,
    "total_purchases": total_purchases,
    "transactions": transactions,
    "products": products,
    "suppliers": suppliers,
    "categories": categories
}   
@router.get("/yearly/{year}")
def yearly_report(year: int, db: Session = Depends(get_db)):
    transactions=db.query(Transaction).filter(
        func.extract('year', Transaction.timestamp) == year
    ).all()
    products = db.query(Product).filter(
        func.extract('year', Product.created_at) == year
    ).all() 
    suppliers = db.query(Supplier).filter(
        func.extract('year', Supplier.created_at) == year  
    ).all()
    categories= db.query(Category).filter(
        func.extract('year', Category.created_at) == year
    ).all()
    total_sales = sum(t.total_price for t in transactions if t.type == 'sale')
    total_purchases = sum(t.total_price for t in transactions if t.type == 'purchase')
    return{
    "year": year,
    "total_sales": total_sales,
    "total_purchases": total_purchases,
    "transactions": transactions,
    "products": products,
    "suppliers": suppliers,
    "categories": categories
}