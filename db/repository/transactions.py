from sqlalchemy.orm import Session

from schemas.transactions import TransactionCreate
from db.models.transactions import Transaction


def create_new_transaction(transaction: TransactionCreate, db: Session):
    transaction_object = Transaction(
    first_name = transaction.first_name,
    surname = transaction.surname,
    gender = transaction.gender,
    date_and_time= transaction.date_and_time,
    cc_number= transaction.cc_number,
    merchant= transaction.merchant,
    merchant_category= transaction.merchant_category,
    amount= transaction.amount,
    city= transaction.city,
    state= transaction.state,
    street = transaction.street,
    zip= transaction.zip,
    latitude= transaction.latitude,
    longitude = transaction.longitude,
    city_population= transaction.city_population,
    job= transaction.job,
    dob= transaction.dob,
    transaction_number= transaction.transaction_number,
    unix_time= transaction.unix_time,
    merchant_latitude= transaction.merchant_latitude,
    merchant_longitude= transaction.merchant_longitude,
    is_fraud= transaction.is_fraud)
    db.add(transaction_object)
    db.commit()
    db.refresh(transaction_object)
    return transaction_object

def retrieve_transaction_by_id(id:int, db:Session):
    transaction = db.query(Transaction).filter(Transaction.id == id).first()
    return transaction

def retrieve_transactions_by_merchant(merchant: str, db:Session):
    transactions = db.query(Transaction).filter(Transaction.merchant == merchant)
    return transactions

def retrieve_transaction_by_name(first_name: str, surname: str, dob:str, db:Session):
    transaction = db.query(Transaction).filter(Transaction.first_name == first_name & Transaction.surname == surname &
                                               Transaction.dob == dob)
    return transaction

def retrieve_transactions_by_fraud_value(is_fraud: int, db:Session):
    transactions = db.query(Transaction).filter(Transaction.is_fraud == is_fraud)
    return transactions

def retrieve_transactions_by_time(unix_time, threshold,  db:Session):
    transactions = db.query(Transaction).filter(Transaction.unix_time > (unix_time - threshold) &
                                                Transaction.unix_time < unix_time)
    return transactions

def list_transactions(db: Session):
    transactions = db.query(Transaction).all()
    return transactions