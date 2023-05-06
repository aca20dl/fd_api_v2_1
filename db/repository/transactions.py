from sqlalchemy.orm import Session
from sqlalchemy import and_, cast, Integer

from schemas.transactions import TransactionCreate
from db.models.transactions import Transaction
from db.models.customer import Customer


def create_new_transaction(transaction: TransactionCreate,customer: Customer, db: Session):
    transaction_object = Transaction(
        customer = customer,
        date_and_time= transaction.date_and_time,
        cc_number= transaction.cc_number,
        merchant= transaction.merchant,
        merchant_category= transaction.merchant_category,
        amount= transaction.amount,
        city= transaction.city,
        state= transaction.state,
        street = transaction.street,
        zip= transaction.zip,
        ip_address = transaction.ip_address,
        latitude= transaction.latitude,
        longitude = transaction.longitude,
        city_population= transaction.city_population,
        transaction_number= transaction.transaction_number,
        unix_time= transaction.unix_time,
        merchant_latitude= transaction.merchant_latitude,
        merchant_longitude= transaction.merchant_longitude,
        device_latitude = transaction.device_latitude,
        device_longitude = transaction.device_longitude,
        ml_prob = transaction.ml_prob,
        rb_prob = transaction.rb_prob,
        is_fraud= transaction.is_fraud)
    db.add(transaction_object)
    db.commit()
    db.refresh(transaction_object)
    return transaction_object
def update_transaction_fraud_value(transaction_id: int,ml_prob, rb_prob, new_fraud_value: int, db: Session):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if transaction:
        transaction.is_fraud = new_fraud_value
        transaction.rb_prob = rb_prob
        transaction.ml_prob = ml_prob
        db.commit()
        return transaction
    return None



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
    transactions = db.query(Transaction).filter(
        cast(Transaction.unix_time, Integer) > (int(unix_time) - int(threshold)),
        cast(Transaction.unix_time, Integer) < int(unix_time)
    )
    return transactions
def retrieve_transactions_by_cc_number(cc_number, db: Session):
    transactions = db.query(Transaction).filter(Transaction.cc_number == cc_number).all()

    return transactions

def list_transactions(db: Session):
    transactions = db.query(Transaction).all()
    return transactions

