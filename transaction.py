from sys import prefix
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from database import get_db
from models import Product, Transaction
from schemas import TransactionCreate, TransactionResponse
from datetime import datetime, date
from typing import List
import math
import decimal
router = APIRouter(prefix="/transactions", tags=["transactions"])
@router.post("/", response_model=TransactionResponse)
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
@router.get("/by-date/{query_date}", response_model=List[TransactionResponse])
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