from typing import Optional, List, Dict
from pydantic import BaseModel
from datetime import date, datetime
from pydantic import BaseModel
from typing import List, Dict

class CustomerBase(BaseModel):
    first_name: str
    surname: str
    gender: str
    job: str
    dob: str

class CustomerCreate(CustomerBase):
    credit_card_numbers: List[str]
    number_of_transactions: int
    transaction_dates: List[str]
    #transactions_per_week: int
    transactions_time_frame: Dict[str, str]
    types_of_merchants: Dict[str, int]
    #avg_transaction_per_category: Dict[str, float]
    ip_addresses: Dict[str, int]
    transactions_per_week: Dict[str, int]


class CustomerUpdate(CustomerBase):
    credit_card_numbers: List[str]
    number_of_transactions: int
    transaction_dates: List[str]
    #transactions_per_week: float
    transactions_time_frame: Dict[str, str]
    types_of_merchants: Dict[str, int]
    #avg_transaction_per_category: Dict[str, float]
    ip_addresses: Dict[str, int]
    transactions_per_week: Dict[str, int]


    class Config:
        orm_mode = True
