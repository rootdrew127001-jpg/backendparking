from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlmodel import Session
from app.db.session import get_session
from app.services.user_service import UserService
from app.core.security import decode_access_token
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"])


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")


@router.post("/register", response_model=User)
def register(
    username: str,
    email: str,
    password: str,
    db: Session = Depends(get_session),
):
    service = UserService(db)
    return service.register_user(username, email, password)


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_session),
):

    service = UserService(db)
    access_token = service.authenticate_user(
        username=form_data.username,
        password=form_data.password,
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_session),
) -> User:
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    service = UserService(db)
    user = service.get_user(username)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user


@router.get("/me", response_model=User)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user
