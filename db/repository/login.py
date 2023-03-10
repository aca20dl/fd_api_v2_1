from sqlalchemy.orm import Session

from db.models.users import User

def get_user(username:str, db: Session):
    user = db.query(User).filter(User.company_id == username).first()
    return user

