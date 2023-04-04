from sqlalchemy.orm import Session

from db.models.users import User

def get_user_by_email(email:str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    return user

def get_user_by_id(id: str, db: Session):
    user = db.query(User).filter(User.company_id == id).first()
    return user


