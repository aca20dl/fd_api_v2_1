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
    numberOfTransactions: int
    transactions_per_week: int
    transactions_time_frame: List[str]
    types_of_merchants: Dict[str, int]

class CustomerUpdate(CustomerBase):
    numberOfTransactions: int
    transactions_per_week: float
    transactions_time_frame: List[str]
    types_of_merchants: Dict[str, int]

    class Config:
        orm_mode = True
