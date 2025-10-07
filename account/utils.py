from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(given_plan_password: str, real_hashed_password: str):
    return pwd_context.verify(given_plan_password, real_hashed_password)