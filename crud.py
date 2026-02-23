from sqlite3 import _AggregateProtocol
from sqlalchemy import func
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
def update_product(db: Session, product_name:str, product:schemas.ProductCreate):
    db_product = db.query(models.Product).filter(models.Product.name == product_name).first()
    if db_product:
        db_product.id = product.id
        db_product.description = product.description
        db_product.price = product.price
        db.commit()
        db.refresh(db_product)
    return db_product
def delete_product(db: Session, product_name:str):
    db_product = db.query(models.Product).filter(models.Product.name == product_name).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product
#Transaction CRUD operations
def create_transaction(db: Session, transaction:schemas.TransactionCreate):
    db_transaction = models.Transaction(product_name=transaction.product_name, quantity=transaction.quantity, type=transaction.type)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction
def get_transactions(db:Session):
    return db.query(models.Transaction).all()
TRANSACTION_IN = 'purchase'
TRANSACTION_OUT = 'sale'
def calculate_stock_from_transactions(db: Session, product:models.Product):
    total_in = 0
    total_out = 0
    #sum all trasactions (in=positive, out=negative)

    for t in product.transaction:
        if t.type == TRANSACTION_IN:
            total_in += t.quantity
        elif t.type == TRANSACTION_OUT:
            total_out += t.quantity
    if getattr (product, "quantity", None) is not None:
        return product.quantity
    stock = total_in - total_out
    return {'product_id': product.id, 'product_name': product.name, 'stock': stock, 'total_in': total_in, 'total_out': total_out}
def get_product_stock(db: Session, product_name:str):
    product = db.query(models.Product).filter(models.Product.name == product_name).first()
    if not product:
        return None
    total_in = sum(t.quantity for t in product.transaction if t.type == TRANSACTION_IN)
    total_out = sum(t.quantity for t in product.transaction if t.type == TRANSACTION_OUT)
    stock = product.quantity if getattr (product, "quantity", None) is not None else (total_in - total_out)
    return {'product_id': product.id, 'product_name': product.name, 'stock': stock, 'total_in': total_in, 'total_out': total_out}
def get_all_product_stocks(db: Session):
   rows = (db.query(models.Transaction.product_name,models.Transaction.type,  func.sum(models.Transaction.quantity).label('total')).group_by(models.Transaction.product_name, models.Transaction.type).all())
   aggregrated: dict[str, dict[str, int]] = {}
   for product_name, t_type, total in rows:
       aggregrated.setdefault(product_name, {'TRANSACTION_IN': 0, 'TRANSACTION_OUT': 0})
       if t_type in (TRANSACTION_IN, TRANSACTION_OUT):
           aggregrated[product_name][t_type] = int(total)
   products = db.query(models.Product).all()
   stock_report = []
   for product in products:
       totals = aggregrated.get(str(product.name), {'TRANSACTION_IN': 0, 'TRANSACTION_OUT': 0})
       total_in = totals['TRANSACTION_IN']
       total_out = totals['TRANSACTION_OUT']
       stock = (product.quantity if getattr (product, "quantity", None) is not None else (total_in - total_out))
       stock_report.append({'product_id': product.id, 'product_name': product.name, 'stock': stock, 'total_in': total_in, 'total_out': total_out})
   return stock_report

