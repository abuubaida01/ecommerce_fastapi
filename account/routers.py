from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from . import services
from . import schemas 
from db.config import session
from . import dependency as dep 
from .models import User


router = APIRouter(tags=['Account'])

@router.post("/register", response_model=schemas.UserResponse)
async def register(session: session, user: schemas.UserCreate):
  return await services.create_user(session, user)

@router.post("/login")
async def login(session: session, user_login: schemas.UserLogin): 
  user = await services.authenticate_user(session, user_login)

  if not user: 
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid credentials")
  
  tokens = await services.create_token(session, user)
  response = JSONResponse(content={"message": "Login successfully"})

  # set access_token into the cookie
  response.set_cookie(
    key="access_token",
    value=tokens['access_token'],
    httponly=True, 
    secure=True, 
    samesite="lax",
    max_age=60*60*24*1 # one day correct expiry time not a token expiery time
  )

  # set refresh_token into the cookie
  response.set_cookie(
    key="refresh_token", 
    value=tokens['refresh_token'],
    httponly=True, 
    secure=True, 
    samesite="lax",
    max_age=60*60*24*7 # for 7 days this cookie should be valid
  )
  return response

@router.get("/me", response_model=schemas.UserOut)
async def me(user: User =Depends(dep.get_current_user)): 
  return user


