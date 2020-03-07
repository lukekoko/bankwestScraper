from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud 
import models
import schemas
from database import SessionLocal, engine
import datetime

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/transactions/", response_model=List[schemas.Transaction])
def read_transactions(startDate: datetime.date = None, endDate: datetime.date = None, type: str = None, db: Session = Depends(get_db)):
    transactions = crud.get_transactions(db, type, startDate, endDate)
    if transactions is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transactions

@app.get("/transactions/{transaction_id}", response_model=schemas.Transaction)
def read_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = crud.get_transaction(db, transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

