from typing import List, Optional

from pydantic import BaseModel

import datetime

class TransactionBase(BaseModel):
    account: str
    date: datetime.date
    description: str
    transactionType: str
    balance: float
    transactionAmount: Optional[float] = ...

class Transaction(TransactionBase):
    id: int
    class Config:
        orm_mode = True