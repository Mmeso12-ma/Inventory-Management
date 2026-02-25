from sys import prefix
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from database import get_db
from models import Product, Transaction
from schemas import TransactionCreate, TransactionResponse, StockResponse
from datetime import datetime, date
from typing import List
import math
import decimal
import auth
from auth import require_role
router = APIRouter(prefix="/transactions", tags=["transactions"])
@router.post("/", response_model=TransactionResponse, dependencies=[Depends(require_role(["admin", "staff"]))])
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    try:
        qty = int(transaction.quantity)
    except (TypeError, ValueError):
        raise HTTPException(status_code=400, detail="Quantity must be an integer")
    if qty <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be positive")
# get the product by ID
    product = db.query(Product).filter(Product.name == transaction.product_name).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    # ensure product.quantity is initialized on the instance (not on the model class)
    if getattr(product, "quantity", None) is None:
        product.quantity = 0
# calculate total price
    total_price = product.price * qty
# create transaction record
    new_transaction = Transaction(
        product_name=transaction.product_name,
        quantity=qty,
        type=transaction.type,
        total_price=total_price)
#create transaction record
    new_transaction = Transaction(
        product_name = transaction.product_name,
        quantity = qty,
        type = transaction.type,
        total_price = total_price
    )
#update product quantity
    if transaction.type == 'purchase': 
        product.quantity = product.quantity + qty
    elif transaction.type == 'sale':
        if product.quantity < qty:
            raise HTTPException(status_code=400, detail="Insufficient product quantity for sale")
        product.quantity = product.quantity - qty
    else:
        raise HTTPException(status_code=400, detail="Invalid transaction type")
# commit changes to the database
    db.add(new_transaction)
    db.add(product)
    db.commit()
    db.refresh(new_transaction)
    return TransactionResponse.model_validate(new_transaction, from_attributes=True).model_dump()
@router.get("/by-date/{query_date}", response_model=List[TransactionResponse], dependencies=[Depends(require_role(["admin"]))])
def get_transactions_by_date(query_date: date, db:Session = Depends(get_db)):
    transactions = db.query(Transaction).filter(
        func.date(Transaction.timestamp) == query_date
    ).all()
    if not transactions:
        raise HTTPException(status_code=404, detail="No transaction found for this date")
    return [
       TransactionResponse.model_validate(t, from_attributes=True).model_dump()
       for t in transactions
    ]
@router.get("/", response_model=List[StockResponse], dependencies=[Depends(require_role(["admin", "staff"]))])
def get_all_stock(db:Session = Depends(get_db)):
    products = db.query(Product).all()
    transactions = db.query(Transaction).all()
    product_map = {p.name: p for p in products}
    stock_report = []
    for t in transactions:
        product = product_map.get(t.product_name)
        if not product:
            continue
        stock_report.append({
            'product_id': product.id,
            'product_name': product.name,
            'stock': product.quantity if getattr(product, "quantity", None) is not None else 0,
            'total_in': sum(t.quantity for t in product.transaction if t.type == 'purchase'),
            'total_out': sum(t.quantity for t in product.transaction if t.type == 'sale')
        })
    return stock_report
@router.get("/product/{product_name}", response_model=StockResponse, dependencies=[Depends(require_role(["admin", "staff"]))])
def get_stock_for_product(product_name:str, db:Session = Depends(get_db)):
    product = db.query(Product).filter(Product.name == product_name).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {
        'product_id': product.id,
        'product_name': product.name,
        'stock': product.quantity if getattr(product, "quantity", None) is not None else 0,
        'total_in': sum(t.quantity for t in product.transaction if t.type == 'purchase'),
        'total_out': sum(t.quantity for t in product.transaction if t.type == 'sale')
    }