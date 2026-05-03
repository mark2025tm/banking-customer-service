from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .db import SessionLocal, engine, Base
from . import crud, schemas
from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import Response
import time

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Customer Service")

REQUESTS = Counter("customer_requests_total", "Total Requests")
LATENCY = Histogram("customer_request_latency_seconds", "Latency")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health():
    return {"status": "UP", "service": "customer-service"}

@app.post("/customers", response_model=schemas.CustomerResponse)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    start = time.time()
    REQUESTS.inc()
    result = crud.create_customer(db, customer)
    LATENCY.observe(time.time() - start)
    return result

@app.get("/customers/{customer_id}", response_model=schemas.CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = crud.get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.get("/customers")
def list_customers(db: Session = Depends(get_db)):
    return crud.get_all_customers(db)

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")
