# services/auth_service.py

from sqlalchemy.orm import Session
from models.user import User
from schemas.auth import UserCreate
from core.security import get_password_hash, verify_password, create_access_token


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user_data: UserCreate):
    hashed_pw = get_password_hash(user_data.password)
    user = User(email=user_data.email, hashed_password=hashed_pw)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def login_user(user: User):
    token_data = {"sub": str(user.id)}
    token = create_access_token(data=token_data)
    return {"access_token": token, "token_type": "bearer"}
