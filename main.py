from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine, Base
Base.metadata.create_all(bind=engine)
app = FastAPI(title="Inventory Management API")
#Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
#Product Endpoints
@app.get("/")
def read_root():
    return {"message": "Welcome to the Inventory Management API"}
@app.get("/products/", response_model=list[schemas.Product])
def read_products(db: Session = Depends(get_db)):
    products = crud.get_products(db)
    return products
@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db=db, product=product)
@app.put("/products/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    updated = crud.update_product(db=db, product_id=product_id, product=product)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated
@app.delete("/products/{product_id}", response_model=schemas.Product)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_product(db=db, product_id=product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"detail": "Product deleted"}
            #Transaction Endpoints
@app.post("/transactions/", response_model=schemas.Transaction)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
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
@app.get("/invetory/")
def get_inventory(db: Session = Depends(get_db)):
    return crud.get_all_product_stocks(db)