from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Numeric

from database import Base

class Transactions(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    account = Column(String)
    date = Column(DateTime)
    description = Column(String)
    transactionType = Column(String)
    balance = Column(Numeric)
    transactionAmount = Column(Numeric)