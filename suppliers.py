from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Supplier
from schemas import SupplierCreate, SupplierResponse
router = APIRouter(prefix="/suppliers", tags=["suppliers"])
@router.post("/", response_model=SupplierResponse)
def create_supplier(supplier: SupplierCreate, db: Session = Depends(get_db)):
    existing_supplier = db.query(Supplier).filter(Supplier.name == supplier.name).first()
    if existing_supplier:
        raise HTTPException(status_code=400, detail="Supplier with this name already exists.")
    new_supplier = Supplier(name=supplier.name, contact_info=supplier.contact_info)
    db.add(new_supplier)
    db.commit()
    db.refresh(new_supplier)
    return new_supplier
@router.get("/", response_model=List[SupplierResponse])
def get_suppliers(db: Session = Depends(get_db)):
    suppliers = db.query(Supplier).all()
    return suppliers
@router.get("/{supplier_name}", response_model=SupplierResponse)
def get_supplier(supplier_name: str, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(Supplier.name == supplier_name).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found.")
    return supplier
@router.put("/{supplier_name}", response_model=SupplierResponse)
def update_supplier(supplier_name: str, supplier_update: SupplierCreate, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(Supplier.name == supplier_name).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found.")
    supplier.name = supplier_update.name
    supplier.contact_info = supplier_update.contact_info
    db.commit()
    db.refresh(supplier)
    return supplier
@router.delete("/{supplier_name}")
def delete_supplier(supplier_name: str, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(Supplier.name == supplier_name).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found.")
    db.delete(supplier)
    db.commit()
    return {"detail": "Supplier deleted successfully."}