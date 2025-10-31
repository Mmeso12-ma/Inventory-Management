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
def get_product_stock(db: Session, product_id:int):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        return None
    total_in = 0
    total_out = 0
    #sum all trasactions (in=positive, out=negative)

    for t in product.transaction:
        if t.type == 'purchase':
            total_in += t.quantity
        elif t.type == 'out':
            total_out -= t.quantity
    stock = product.quantity if getattr (product, "quantity", None) is not None else (total_in - total_out)
    return {'product_id': product.id, 'product_name': product.name, 'stock': stock, 'total_in': total_in, 'total_out': total_out}
def get_all_product_stocks(db: Session):
    products = db.query(models.Product).all()
    stock_report = []
    for product in products:
        total_in = 0
        total_out = 0

        for t in product.transaction:
            if t.type == 'in':
                stock += t.quantity
            elif t.type == 'out':
                stock -= t.quantity
            stock = product.quantity if getattr (product, "quantity", None) is not None else (total_in - total_out)
        stock_report.append({'product_id': product.id, 'name': product.name, 'stock': stock})
    return stock_report