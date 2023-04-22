from sqlalchemy import Column,Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from db.base_class import Base

class User(Base):
    id = Column(Integer, primary_key=True,index=True)
    company_id = Column(Integer, nullable=False, unique=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    company_name = Column(String, nullable=False, unique=True, index=True)
    company_category = Column(String, nullable=False)
    merch_lat = Column(String, nullable=False)
    merch_long = Column(String, nullable=False)


