from email.policy import HTTP
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine, Base
from security import hash_password, verify_password, create_access_token, decode_token
from datetime import datetime, timedelta
from auth import router as auth_router
from products import require_role, router as products_router
Base.metadata.create_all(bind=engine)
app = FastAPI(title="Inventory Management API")

#Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
            #Transaction Endpoints
@app.post("/transactions/", response_model=schemas.Transaction)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db), current_user: models.User = Depends(require_role(["admin", "manager", "clerk"]))):
    return crud.create_transaction(db=db, transaction=transaction)
@app.get("/transactions/", response_model=list[schemas.Transaction])
def read_transactions(db: Session = Depends(get_db)):
    return crud.get_transactions(db)
@app.get("/products/{product_id}/stock")
def get_product_stock(product_id: int, db: Session = Depends(get_db)):
    stock_info = crud.get_product_stock(db=db, product_id=product_id)
    if not stock_info:
        raise HTTPException(status_code=404, detail="Product not found")
    return stock_info
@app.get("/inventory/")
def get_inventory(db: Session = Depends(get_db)):
    return crud.get_all_product_stocks(db)
app.include_router(auth_router)
app.include_router(products_router)

