from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud 
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/transactions/", response_model=schemas.Transaction)
def read_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    transactions = crud.get_transactions(db)
    return transactions