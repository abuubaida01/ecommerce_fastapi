from account.models import User, RefreshToken
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy import select
from . import schemas
from . import utils
import uuid
from decouple import config
from datetime import datetime, timezone, timedelta


async def create_user(session: AsyncSession, user: schemas.UserCreate): 
  
  # check if user already exist
  stmt = select(User).where(User.email == user.email)
  result = await session.scalars(stmt)
  
  if result and result.first(): 
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email already register")

  # create user
  new_user = User(
    email = user.email, 
    hashed_password = utils.hash_password(user.password)
  )

  session.add(new_user)
  await session.commit()
  await session.refresh(new_user)
  
  return new_user


async def authenticate_user(session: AsyncSession, user_login: schemas.UserLogin):
  stmt = select(User).where(User.email == user_login.email)
  result = await session.scalars(stmt)
  user = result.first()

  if not user or not utils.verify_password(user_login.password, user.hashed_password):
    return None
  
  return user

 

async def create_token(session: AsyncSession, user: User): 
  access_token = utils.create_access_token(data={"sub": str(user.id)})
  JWT_REFRESH_TOKEN_TIME_DAY = config("JWT_REFRESH_TOKEN_TIME_DAY", cast=int) 
  refresh_token_str = str(uuid.uuid4())

  expires_at = datetime.now(timezone.utc) + timedelta(days=JWT_REFRESH_TOKEN_TIME_DAY)
  
  refresh_token = RefreshToken(
    user_id=user.id, 
    token=refresh_token_str, 
    expires_at=expires_at
  )
  session.add(refresh_token)
  await session.commit()
  return {
    "access_token": access_token, 
    "refresh_token": refresh_token_str,
    "token_type": "bearer"
  }

