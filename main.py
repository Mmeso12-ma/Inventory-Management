from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine, Base, get_db
from .security import hash_password, verify_password, create_access_token, decode_token
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
# token system
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "auth/token")
# finds a user using email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email== email).first()
#register route
@app.post("/auth/register", response_model= schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user=get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = models.User(email=user.email, hashed_password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
#login route
@app.post("/auth/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code= 401, detail = "Invalid credentials")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
#current user dependency
def get_current_user(token: str=Depends(oauth2_scheme), db: Session=Depends(get_db)):
    payload = decode_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail= "Invalid token")
    user= get_user_by_email(db, payload["sub"])
    if not user:
        raise HTTPException(status_code=401, detail="user not found")
    return user
@app.get("/products/secure")
def secure_products(current_user: models.User= Depends(get_current_user)):
    return ("msg": f"Hi {current_user.email}, here are your products")