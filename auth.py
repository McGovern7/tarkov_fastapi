from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
from models import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
import os

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRATION_TIME = 30

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')

class CreateUserRequest(BaseModel):
    username: str
    password: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ensure username doesn't already exist in User database
def get_user_by_name(db: Session, username: str) -> CreateUserRequest:
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: CreateUserRequest) -> str:
    hashed_password=pwd_context.hash(user.password), # hashing the password
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    return "complete"

@router.post("/", status_code=status.HTTP_201_CREATED)
def register_user(user: CreateUserRequest, db: Session = Depends(get_db)):
    db_user = get_user_by_name(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=401, detail="Profile with that username already registered.")
    return create_user(db=db, user=user)


def authenticate_user(username: str, password: str, db: Session) -> (CreateUserRequest | None):
    user = get_user_by_name(db, username=username)
    if not user: 
        return None
    # # case sensitive equality check && hash password, and verify with already hashed password from database
    if user.username != username or not pwd_context.verify(password, user.hashed_password):
        return None
    return user # both username and their hashed password are equal

# Encode JWT using encode, secret key, and algorithm
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire}) # know when jwt is expired
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # return an encoded jwt
    return encoded_jwt

# CREATE post for token
@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Incorrect username or password.', 
                            headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRATION_TIME)
    access_token = create_access_token(data={"sub": user.username, "id": user.id}, expires_delta=access_token_expires) # valid 30 minutes or add time delta
    return {'access_token': access_token, 'token_types': 'bearer'}


# decode the JWT
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        id: int = payload.get('id')
        if username is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='API Error: User not Found. Token is invalid or expired.')
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='JWT Error: Token is invalid or expired.')
    
@router.get("/verify-token/{token}")
async def verify_user_token(token: str):
    verify_token(token=token)
    return {"message": "Token is valid"}
