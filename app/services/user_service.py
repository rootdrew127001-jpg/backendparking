from datetime import timedelta
from fastapi import HTTPException, status
from sqlmodel import Session, select
from app.models.user import User
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.core.config import settings


class UserService:
    def __init__(self, db: Session):
        self.db = db


    def register_user(self, username: str, email: str, password: str) -> User:
        existing_user = self.db.exec(select(User).where(User.username == username)).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )

        new_user = User(
            username=username,
            email=email,
            hashed_password=hash_password(password),
        )

        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user


    def authenticate_user(self, username: str, password: str) -> str:
        user = self.db.exec(select(User).where(User.username == username)).first()
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )


        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username},
            expires_delta=access_token_expires
        )
        return access_token


    def get_user(self, username: str) -> User | None:
        return self.db.exec(select(User).where(User.username == username)).first()
