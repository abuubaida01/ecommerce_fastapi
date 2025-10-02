from account.models import User, RefreshToken
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy import Select
from .schemas import UserCreate
from .utils import hash_password

async def create_user(session: AsyncSession, user: UserCreate): 
  
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
