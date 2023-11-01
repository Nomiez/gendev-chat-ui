from __future__ import annotations

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.schemas.token_schema import TokenData
from app.repositories.user_repository import user_repository
from app.schemas.user_schema import UserSchema
from app.utils.config import settings
import secrets

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token', auto_error=False)

# SECRET KEY
SECRET_KEY = settings.secret_key

# ALGORITHM
ALGORITHM = settings.algorithm

# EXPIRE TIME
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        return TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception


def get_current_user(token: str = Depends(oauth2_scheme)) -> UserSchema | None:
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    if token is None:
        return None
    token = verify_token(token, credentials_exception)
    user = user_repository.get_user_by_id(token.user_id)
    if not user:
        raise credentials_exception
    return user


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify(plain_password: str, salt: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password + salt, hashed_password)


def generate_salt() -> str:
    return secrets.token_urlsafe(32)


def get_access_token(user_credentials: OAuth2PasswordRequestForm) -> str:
    user = user_repository.get_user_from_username(user_credentials.username)

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    if not verify(user_credentials.password, user.salt, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    return create_access_token(data={"user_id": user.user_id})


def is_valid_user(user: UserSchema | None) -> None:
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized to access this resource")
