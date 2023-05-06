from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from db.models.customer import Customer

from db.base_class import Base

class Transaction(Base):
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    customer = relationship("Customer")
    date_and_time = Column(String, nullable=False)
    cc_number = Column(String, nullable=False)
    merchant = Column(String, nullable=False)
    merchant_category = Column(String, nullable=False)
    amount = Column(Numeric, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    street = Column(String, nullable=False)
    zip = Column(String, nullable=False)
    ip_address = Column(String, nullable=True)
    latitude = Column(String, nullable=False)
    longitude = Column(String, nullable=False)
    city_population = Column(Integer, nullable=False)
    transaction_number = Column(String, nullable=False)
    unix_time = Column(String, nullable=False)
    merchant_latitude = Column(String, nullable=False)
    merchant_longitude = Column(String, nullable=False)
    device_latitude = Column(String, nullable=True)
    device_longitude = Column(String, nullable=True)
    ml_prob = Column(Numeric, nullable =True)
    rb_prob = Column(Numeric, nullable=True)
    is_fraud = Column(Integer, nullable=True)


