from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import  Product, Category, Supplier, Transaction, User
from schemas import ProductCreate, Product
from security import oauth2_scheme, decode_token
router = APIRouter(prefix="/products", tags=["products"])
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user= db.query(User).filter(User.email == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
# Product Endpoints
@router.post("/", response_model=Product)
def create_product(product: ProductCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_product = Product(name=product.name, description=product.description, price=product.price, user_id=current_user.id)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product
@router.get("/", response_model=list[Product])
def read_products(db:Session = Depends(get_db)):
    products = db.query(Product).all()
    return products
@router.get("/{product_id}", response_model=Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db), current_user:
                    User = Depends(get_current_user)):
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        if product.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this product")
        db.delete(product)
        db.commit()
        return 
# 204 No Content
@router.put("/{product_id}", response_model=Product)
def update_product(product_id: int, updated_product: ProductCreate, db: Session = Depends
                    (get_db), current_user: User = Depends(get_current_user)):
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        if product.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to update this product")
        product.name = updated_product.name
        product.description = updated_product.description
        product.price = updated_product.price
        db.commit()
        db.refresh(product)
        return product
@router.get("/me/", response_model=list[Product])
def read_own_products(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    products = db.query(Product).filter(Product.user_id == current_user.id).all()
    return products
