from pydantic import BaseModel
from typing import Optional

from db.models.customer import Customer
from schemas.customer import CustomerBase

class TransactionBase(BaseModel):
    date_and_time: str
    cc_number: str
    merchant: str
    merchant_category: str
    amount: float
    city: str
    state: str
    street: str
    zip: str
    ip_address: str
    latitude: str
    longitude: str
    city_population: int
    job: str
    transaction_number: str
    unix_time: str
    merchant_latitude: str
    merchant_longitude: str
    device_latitude: str
    device_longitude: str
    ml_prob: float
    rb_prob: float
    is_fraud: int

class TransactionCreate(TransactionBase):
    customer: Optional[Customer] = None

    class Config:
        arbitrary_types_allowed = True

class TransactionUpdate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    customer: Optional[Customer] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ShowTransaction(Transaction):
    first_name: str
    surname: str
    gender: str
    dob: str
    customer: Optional[CustomerBase] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True