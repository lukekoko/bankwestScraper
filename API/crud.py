from sqlalchemy.orm import Session

import models   
import schemas
import datetime

def get_transactions(db: Session, transactionType: str = None, startDate: datetime.date = None, endDate: datetime.date = None):
    transactions = db.query(models.Transactions)
    if (transactionType is not None and (transactionType.lower() == "debit" or transactionType.lower() == 'credit')):
        transactions = transactions.filter(models.Transactions.transactionType == transactionType)
    if (startDate is not None or endDate is not None):
        if (startDate is None):
            transactions = transactions.filter(models.Transactions.date <= endDate)
        elif (endDate is None):
            transactions = transactions.filter(models.Transactions.date >= startDate)
        else:
            transactions = transactions.filter(models.Transactions.date.between(startDate, endDate))
    return transactions.order_by(models.Transactions.date.desc()).all()

def get_transaction(db: Session, transaction_id: int):
    return db.query(models.Transactions).filter(models.Transactions.id == transaction_id).first()
