from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Category
from schemas import CategoryCreate, CategoryResponse
from typing import List
router = APIRouter(prefix="/categories", tags=["Categories"])
@router.post("/", response_model=CategoryResponse)
def create_category(category: CategoryCreate, db: Session= Depends(get_db)):
    existing_category = db.query(Category).filter(category.name == category.name).first()
    if existing_category:
        raise HTTPException(status_code=400, detail="Category already exists")
    new_category = Category(name=category.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category
@router.get("/", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()
@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category=db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category
@router.put("/{category_name}", response_model=CategoryResponse)
def update_category(category_name: str, updated: CategoryCreate, db:Session = Depends(get_db)):
    category = db.query(Category).filter(Category.name == category_name).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category.id=updated.id
    db.commit()
    db.refresh(category)
    return category
@router.delete("/{category_name}")
def delete_category(category_name: str, db:Session=Depends(get_db)):
    category = db.query(Category).filter(Category.name == category_name).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return{"message": "Category deleted successfully"}