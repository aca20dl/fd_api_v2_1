from typing import Optional
from pydantic import BaseModel
from datetime import date, datetime


# This will be used to validate data while creating a transaction

class TransactionCreate(BaseModel):
    first_name: str
    surname: str
    gender: str
    date_and_time: str
    cc_number: str
    merchant: str
    merchant_category: str
    amount: float
    city: str
    state: str
    street: str
    zip: str
    latitude: str
    longitude: str
    city_population: int
    job: str
    dob: str
    transaction_number: str
    unix_time: str
    merchant_latitude: str
    merchant_longitude: str
    is_fraud: int


class ShowTransaction(BaseModel):
    id: int
    first_name: str
    surname: str
    gender: str
    date_and_time: str
    cc_number: str
    merchant: str
    merchant_category: str
    amount: float
    city: str
    state: str
    street: str
    zip: str
    latitude: str
    longitude: str
    city_population: int
    job: str
    dob: str
    transaction_number: str
    unix_time: str
    merchant_latitude: str
    merchant_longitude: str
    is_fraud: int

    class Config():
        orm_mode = True

