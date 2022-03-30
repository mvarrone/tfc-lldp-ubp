import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from db.users.get_users_available import get_users_from_db

load_dotenv()
# SECRET_KEY: to get a string like this run: openssl rand -hex 32
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))


class Token(BaseModel):
    access_token: str
    token_type: str
    # exp_arg: str = None


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


def crypto_context():
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context


def oauth2scheme():
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
    return oauth2_scheme


oauth2_scheme = oauth2scheme()

fake_users_db, qusers = get_users_from_db()


def verify_password(plain_password, hashed_password):
    pwd_context = crypto_context()
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    pwd_context = crypto_context()
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    # -180 min == -3 hs (UTC-03:00 --> Argentina)
    exp_arg = expire - timedelta(minutes=60*3)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM), exp_arg


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    credentials_exception_expired = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Signature has expired.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    credentials_exception_not_enough_segments = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not enough segments",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError as e:
        if e.args[0] == "Signature has expired.":
            raise credentials_exception_expired
        if "Not enough segments" in str(e.args[0]):
            raise credentials_exception_not_enough_segments
        else:
            raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_fastapi_info_just_root(request: Request):
    return {
        'method': request.method,
        'path': request.url.path,
        'scheme': request.url.scheme,
        'host': request.client.host,
        'port': request.client.port,
    }


def get_fastapi_info(request: Request, current_user: User = Depends(get_current_active_user)):
    return {
        'method': request.method,
        'path': request.url.path,
        'scheme': request.url.scheme,
        'host': request.client.host,
        'port': request.client.port,
        'username': current_user.username
    }
