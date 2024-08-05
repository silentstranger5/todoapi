import jwt

from datetime import datetime, timedelta, timezone
from fastapi import status, Depends, APIRouter, Header, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from typing import Annotated

from . import crud, database, schemas

# API router
router = APIRouter(prefix="/auth")

# Cryptographical context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Authentication parameters
# Get secret key with `python -c 'import secrets; print(secrets.token_hex())'`
SECRET_KEY = "cd3e75d88de2107e3c42db147ebf4efdf5ef587fdbbfa4ac8a511c60121d50d6"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password: str, hashed_password: str):
    """Verify that hash of plain_password is hashed_password"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    """Get hash of a password"""
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str, db: Session):
    """Get user from database and verify his password"""
    user = crud.get_user(db, username)
    if not user:
        return False
    if not verify_password(password, str(user.password)):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
    db: Session = Depends(database.get_db)
):
    """Get current user by authorization header"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authorized", 
        headers={"WWW-Authenticate": "Bearer"}
    )

    # Check presense of authentication header
    if not authorization:
        raise credentials_exception

    # Authentication header must be in format
    # Authentication: Bearer TOKEN
    auth_data = authorization.split()
    if len(auth_data) != 2 or auth_data[0] != "Bearer":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Authorization header format",
            headers={"WWW-Authenticate": "Bearer"}
        )
    token = auth_data[1]

    # Check if the token denotes a valid user
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception
    user = crud.get_user(db, username)
    if user is None:
        raise credentials_exception
    return user


@router.post("/register")
async def register(user: schemas.UserInput, db: Session = Depends(database.get_db)):
    """Register a user"""
    db_user = crud.get_user(db, user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
    crud.create_user(db, user)
    return {"message": "Registration is successful"}


@router.post("/token")
async def get_token(user: schemas.UserInput, db: Session = Depends(database.get_db)):
    """Get authentication token"""
    db_user = authenticate_user(user.username, user.password, db)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect user name or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.username}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="Bearer")
