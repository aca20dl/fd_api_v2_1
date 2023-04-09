from datetime import datetime
from typing import List

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Numeric, ClauseList, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY, JSONB

from db.base_class import Base

class Customer(Base):
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    job = Column(String, nullable=False)
    dob = Column(String, nullable=False)
    numberOfTransactions = Column(Integer, nullable=False)
    transactions_per_week = Column(Integer, nullable=False)
    transactions_time_frame = Column(ARRAY(DateTime), nullable=False)
    types_of_merchants = Column(JSONB, nullable=False)

