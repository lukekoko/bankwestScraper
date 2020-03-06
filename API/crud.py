from sqlalchemy.orm import Session

import models   
import schemas

def get_transactions(db: Session):
    return db.query(models.Transactions)
