from datetime import datetime
from typing import List, Dict

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Numeric, ClauseList, DateTime
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, JSON

from db.base_class import Base

class Customer(Base):
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    job = Column(String, nullable=False)
    dob = Column(String, nullable=False)
    credit_card_numbers = Column(ARRAY(String), nullable=False)
    number_of_transactions = Column(Integer, nullable=False)
    transaction_dates= Column(ARRAY(String), nullable=False)
    #transactions_per_week = Column(Integer, nullable=False)
    transactions_time_frame = Column(JSON)
    types_of_merchants = Column(JSONB, nullable=False)
    ip_addresses = Column(JSONB, nullable=False)
    transactions_per_week = Column(JSONB, nullable=False)



