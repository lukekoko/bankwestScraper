from typing import List

from pydantic import BaseModel

import datetime

class TransactionBase(BaseModel):
    account: str
    date: str
    description: str
    transactionType: str
    balance: float
    transactionAmount: float

class Transaction(TransactionBase):
    id: int
    class Config:
        orm_mode = True