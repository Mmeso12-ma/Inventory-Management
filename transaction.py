from sys import prefix
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from database import get_db
from models import Product, Transaction
from schemas import TransactionCreate, TransactionResponse
from datetime import datetime, date
from typing import List
router = APIRouter(prefix="/transactions", tags=["transactions"])
@router.post("/", response_model=TransactionResponse)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
# get the product by ID
    product = db.query(Product).filter(Product.id == transaction.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
# calculate total price
    total_price = product.price * transaction.quantity
# create transaction record
    new_transaction = Transaction(
        product_id=transaction.product_id,
        quantity=transaction.quantity,
        type=transaction.type,
        total_price=total_price
    ) 
#update product quantity
    if transaction.type == 'purchase':
        product.quantity += transaction.quantity
    elif transaction.type == 'sale':
        if product.quantity < transaction.quantity:
            raise HTTPException(status_code=400, detail="Insufficient product quantity for sale")
        product.quantity -= transaction.quantity
    else:
        raise HTTPException(status_code=400, detail="Invalid transaction type")
# commit changes to the database
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction
@router.get("/by-date/{query_date}", response_model=List[TransactionResponse])
def get_transactions_by_date(query_date: date, db:Session = Depends(get_db)):
    transactions = db.query(Transaction).filter(
        func.date(Transaction.timestamp) == query_date
    ).all()
    if not transactions:
        raise HTTPException(status_code=404, detail="No transaction found for this date")
    return transactions