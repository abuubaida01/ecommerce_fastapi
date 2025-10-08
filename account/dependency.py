from fastapi import Depends, Request, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from .utils import decode_token
from sqlalchemy import select
from .models import User
from db.config import session

async def get_current_user(session: session, request: Request): 
  token = request.cookies.get("access_token")
  
  if not token: 
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST, 
      detail="missing access token", 
      headers={"WWW-Authenticate": "Bearer"}
    )
  
  payload = decode_token(token)

  user_id = payload.get('sub')
  if not user_id: 
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )
  
  stmt = select(User).where(User.id == int(user_id))
  result = await session.scalars(stmt)
  user = result.first()

  if not user:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED, 
      detail="User not found",
      headers={"WWW-Authenticate": "Bearer"}
    ) 

  return user

async def require_admin(user: User = Depends(get_current_user)):
  if not user.is_admin:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
  return user
  