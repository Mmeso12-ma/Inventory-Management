from sqlalchemy.orm import Session
import models, schemas
#Product CRUD operations
def get_products(db:Session):
    return db.query(models.Product).all()
def create_product(db: Session, product:schemas.ProductCreate):
    db_product = models.Product(name=product.name, price=product.price, description=product.description)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
def update_product(db: Session, product_id:int, product:schemas.ProductCreate):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db.commit()
        db.refresh(db_product)
    return db_product
def delete_product(db: Session, product_id:int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product
#Transaction CRUD operations
def create_transaction(db: Session, transaction:schemas.TransactionCreate):
    db_transaction = models.Transaction(product_id=transaction.product_id, quantity=transaction.quantity, type=transaction.type)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction
def get_transactions(db:Session):
    return db.query(models.Transaction).all()
