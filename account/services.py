from account.models import User, RefreshToken
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy import Select
from . import schemas
from .utils import hash_password, verify_password

async def create_user(session: AsyncSession, user: schemas.UserCreate): 
  
  # check if user already exist
  stmt = Select(User).where(User.email == user.email)
  result = await session.scalars(stmt)
  
  if result and result.first(): 
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email already register")

  # create user
  new_user = User(
    email = user.email, 
    hashed_password = hash_password(user.password)
  )

  session.add(new_user)
  await session.commit()
  await session.refresh(new_user)
  
  return new_user


async def authenticate_user(session: AsyncSession, user_login: schemas.UserLogin): 
  stmt = Select(User).where(User.email == user_login.email)
  user = await session.scalar(stmt)

  if not user or not verify_password(user_login.password, user.hashed_password): 
    raise HTTPException(status=status.HTTP_400_BAD_REQUEST, detail="User email or password mismatched")
  
  return user
 
