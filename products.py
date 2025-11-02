from auth import settings
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import  Product as ProductModel, Category, Supplier, Transaction, User
from schemas import ProductCreate, Product as ProductSchema
from security import oauth2_scheme, decode_token, require_role, get_current_user
router = APIRouter(prefix="/products", tags=["products"])

# Product Endpoints
@router.post("/", response_model=ProductSchema)
def create_product(product: ProductCreate, db: Session = Depends(get_db), current_user: User = Depends(require_role(["admin", "manager", "clerk"]))):
    new_product = ProductModel(name=product.name, description=product.description, price=product.price, user_id=current_user.id)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product
@router.get("/", response_model=list[ProductSchema])
def read_products(db:Session = Depends(get_db)):
    products = db.query(ProductSchema).all()
    return products
@router.get("/{product_name}", response_model=ProductSchema)
def read_product(product_name: str, db: Session = Depends(get_db)):
    product =db.query(ProductModel).filter(ProductModel.name == product_name).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
@router.delete("/{product_name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_name: str, db: Session = Depends(get_db), current_user:
                    User = Depends(get_current_user)):
        product = db.query(ProductModel).filter(ProductModel.name == product_name).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        if product.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this product")
        db.delete(product)
        db.commit()
        return 
# 204 No Content
@router.put("/{product_name}", response_model=ProductSchema)
def update_product(product_name: str, updated_product: ProductCreate, db: Session = Depends
                    (get_db), current_user: User = Depends(get_current_user)):
        product = db.query(ProductModel).filter(ProductModel.name == product_name).first()
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
@router.get("/me/", response_model=list[ProductSchema])
def read_own_products(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    products = db.query(ProductModel).filter(ProductModel.user_id == current_user.id).all()
    return products
