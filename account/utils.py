from passlib.context import CryptContext
from decouple import config
from datetime import timedelta, datetime, timezone
from jose import jwt, ExpiredSignatureError, JWTError
from fastapi import HTTPException

JWT_SECRET_KEY = config("JWT_SECRET_KEY") 
JWT_ALGORITHM = config("JWT_ALGORITHM") 
JWT_ACCESS_TOKEN_TIME_MIN = config("JWT_ACCESS_TOKEN_TIME_MIN", cast=int) 
EMAIL_VERIFICATION_TOKEN_TIME_HOUR = config("EMAIL_VERIFICATION_TOKEN_TIME_HOUR", cast=int) 
EMAIL_PASSWORD_RESET_TOKEN_TIME_HOUR = config("EMAIL_PASSWORD_RESET_TOKEN_TIME_HOUR", cast=int) 

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(given_plan_password: str, real_hashed_password: str):
    return pwd_context.verify(given_plan_password, real_hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None): 
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=JWT_ACCESS_TOKEN_TIME_MIN))
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, JWT_ALGORITHM)

def decode_token(token):
    try:
        return jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM )
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
  