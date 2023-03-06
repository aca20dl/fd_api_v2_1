from typing import Optional
from pydantic import BaseModel
from datetime import date, datetime


# This will be used to validate data while creating a transaction

class TransactionCreate(BaseModel):
    id: int
    first_name: str
    surname: str
    gender: str
    date_and_time: str
    cc_number: int
    merchant: str
    merchant_category: str
    amount: int
    city: str
    state: str
    zip: str
    latitude: int
    longitude: int
    city_population: int
    job: str
    dob: str
    transaction_number: int
    unix_time: int
    merchant_latitude: int
    merchant_longitude: int
    is_fraud: bool


class ShowTransaction(BaseModel):
    id: int
    first_name: str
    surname: str
    gender: str
    date_and_time: str
    cc_number: int
    merchant: str
    merchant_category: str
    amount: int
    city: str
    state: str
    zip: str
    latitude: int
    longitude: int
    city_population: int
    job: str
    dob: str
    transaction_number: int
    unix_time: int
    merchant_latitude: int
    merchant_longitude: int
    is_fraud: bool

    class Config():
        orm_mode = True

