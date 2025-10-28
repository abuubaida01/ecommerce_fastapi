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


async def verify_refresh_token(session: AsyncSession, token: str): 
  query = await session.scalars(select(RefreshToken).where(token == RefreshToken.token))
  object = query.first()
  
  if object and not object.revoked: 
    expires_at = object.expires_at

    if expires_at.tzinfo is None: 
      expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at > datetime.now(timezone.utc):
      user_stmt =select(User).where(User.id == object.user_id)
      query = await session.scalars(user_stmt)
      object = query.first()
      return object

  return None 


async def create_email_verification_token(user_id: int): 
  token = utils.create_email_verification_token(user_id=user_id) 
  link = f"localhost:8000/link={token}"
  return {"message": "token send succesfully", "link": link}
  


async def verify_email_token(session: AsyncSession, token: str): 
  user_id = utils.verify_email_token_and_get_user_id(token=token, token_type="verify_email")
  
  if not user_id: 
    raise HTTPException(detail="Invalid or expire token", status_code=status.HTTP_400_BAD_REQUEST)
  
  stmt = select(User).where(user_id == User.id)
  result = await session.scalars(stmt)
  user = result.first() 

  if not user: 
    raise HTTPException(detail="User not found", status_code=status.HTTP_400_BAD_REQUEST)

  user.is_verified = True 
  session.add(user)
  await session.commit()
  return {"msg": "Email verifid successfully"}



async def update_and_verify_new_password(session: AsyncSession, user: User, data: schemas.ChangePassword): 
  if not utils.verify_password(data.old_password, user.hashed_password): 
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Old password is incorrect")
  
  user.hashed_password = utils.hash_password(data.new_password)
  session.add(user) 
  await session.commit()

  return {"msg": "Password changed successfully"}



# to check and get data via email
async def get_user_via_email(session: AsyncSession, email: str): 
  stmt = select(User).where(User.email == email)
  result = await session.scalars(stmt)
  user = result.first() 
  if not user: 
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found with this email")
  
  return user


async def create_resent_password_email(session: AsyncSession, data: schemas.ForgetPassword): 
  user = await get_user_via_email(session, data.email)
  token = utils.create_email_verification_token(user_id=user.id, action="password_reset") 
  link = f"localhost:8000/link={token}"
  return {"message": "token send succesfully", "link": link}



async def verify_token_and_reset_password(session: AsyncSession, data: schemas.ResetPassword): 
  user_id = utils.verify_email_token_and_get_user_id(token=data.token, token_type="password_reset")
  
  if not user_id: 
    raise HTTPException(detail="Invalid or expire token", status_code=status.HTTP_400_BAD_REQUEST)
  
  stmt = select(User).where(user_id == User.id)
  result = await session.scalars(stmt)
  user = result.first() 

  if not user: 
    raise HTTPException(detail="User not found", status_code=status.HTTP_400_BAD_REQUEST)

  user.hashed_password = utils.hash_password(data.new_password) 
  session.add(user)
  await session.commit()
  return {"msg": "Reset password successfully"}



async def revoke_refresh_token(session: AsyncSession, token: str): 
  stmt = select(RefreshToken).where(RefreshToken.token== token)
  result = await session.scalars(stmt)
  db_token = result.first()

  if db_token: 
    db_token.revoked = True
    await session.commit()
  

async def make_admin(session: AsyncSession, user: User): 
  if not user: 
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only authenticated users can promote themselves to admin")
  
  user.is_admin = True 
  session.add(user)
  await session.commit()
  await session.refresh(user)
  return user