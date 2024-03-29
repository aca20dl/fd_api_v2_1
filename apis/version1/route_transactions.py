from typing import List

from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from starlette.templating import Jinja2Templates

from db.session import get_db
from db.models.transactions import Transaction
from schemas.transactions import TransactionCreate, ShowTransaction
from db.repository.transactions import create_new_transaction, retrieve_transaction_by_id, list_transactions
router = APIRouter()
templates = Jinja2Templates(directory="Templates")



@router.post("/create-transaction/", response_model=ShowTransaction)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    transaction = create_new_transaction(transaction=transaction, db=db)
    return transaction


@router.get("/get/{id}", response_model=ShowTransaction)
def read_transaction(id: int, db: Session = Depends(get_db)):
    transaction = retrieve_transaction_by_id(id=id, db=db)
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Transaction with this id {id} does not exist")
    return transaction


@router.get("/all", response_model=List[ShowTransaction])
def read_transactions(db: Session = Depends(get_db)):
    print(List[ShowTransaction])
    transactions = list_transactions(db=db)
    return transactions


