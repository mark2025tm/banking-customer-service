from sqlalchemy.orm import Session
from . import models, schemas

def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = models.Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer).filter(
        models.Customer.customer_id == customer_id
    ).first()

def get_all_customers(db: Session):
    return db.query(models.Customer).all()
