from typing import Optional, List, Dict
from pydantic import BaseModel
from datetime import date, datetime


class CustomerCreate(BaseModel):
    first_name: str
    surname: str
    gender: str
    job: str
    dob: str
    numberOfTransactions: int
    transactions_per_week: int
    transactions_time_frame: list
    types_of_merchants: dict

class CustomerUpdate(BaseModel):
    numberOfTransactions: int
    transactions_per_week: float
    transactions_time_frame: List[str]
    types_of_merchants: Dict[str, int]

    class Config:
        orm_mode = True
