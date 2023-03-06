from sqlalchemy.orm import Session

from schemas.users import UserCreate
from db.models.users import User
from core.hashing import Hasher


def create_new_user(user: UserCreate, db: Session):
    user = User(company_name=user.company_name,
                email=user.email,
                hashed_password=Hasher.get_password_hash(user.password),
                company_category=user.company_category,
                company_id=user.company_id)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
