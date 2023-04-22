from sqlalchemy.orm import Session

from schemas.users import UserCreate
from db.models.users import User
from core.hashing import Hasher


def create_new_user(user: UserCreate, db: Session):
    user = User(company_name=user.company_name,
                email=user.email,
                hashed_password=Hasher.get_password_hash(user.password),
                company_category=user.company_category,
                company_id=user.company_id,
                merch_lat=user.merch_lat,
                merch_long=user.merch_long)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def list_users(db : Session):
    users = db.query(User).all()
    return users

def get_user_from_id(db: Session, id: int):
    merchant = db.query(User).filter(id == User.id).first()
    return merchant
