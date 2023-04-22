from typing import Optional, List
from pydantic import BaseModel, EmailStr


# Properties required during user creation
class UserCreate(BaseModel):
    company_id: int
    company_name: str
    email: EmailStr
    password: str
    company_category: str
    merch_lat: str
    merch_long: str


class ShowUser(BaseModel):
    company_id: int
    company_name: str
    email: EmailStr
    company_category: str
    merch_lat: str
    merch_long: str

    class Config():
        orm_mode = True
