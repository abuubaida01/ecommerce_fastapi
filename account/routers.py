from fastapi import APIRouter, HTTPException, status, Depends, Request
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


@router.post('/refresh')
async def refresh_token(session: session, request: Request): 
  token = request.cookies.get("refresh_token")
  if not token: 
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing refresh token")
  
  user = await services.verify_refresh_token(session, token) 
  if not user: 
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired refresh token")
  
  token = await services.create_token(session, user)
  response = JSONResponse(content={"message": "Token refreshed successfully"})
  
  response.set_cookie(
    key="access_token",
    value=token['access_token'],
    httponly=True, 
    secure=True, 
    samesite="lax",
    max_age=60*60*24*2
  )

  response.set_cookie(
    key="refresh_token",
    value=token['refresh_token'],
    httponly=True, 
    secure=True, 
    samesite="lax",
    max_age=60*60*24*7
  )

  return response 


@router.post("/send-verification-email")
async def send_verification_email(user_id: int): 
  return await services.create_email_verification_token(user_id)

@router.get("/verify-email")
async def verify_email(session: session, token:str): 
  return await services.verify_email_token(session, token)

@router.put('/change-password')
async def change_user_password(session: session, data: schemas.ChangePassword, user: User = Depends(dep.get_current_user)): 
  return await services.update_and_verify_new_password(session, user, data) 


@router.post("/send-reset-password-email")
async def send_reset_password_email(session: session, data: schemas.ForgetPassword): 
  return await services.create_resent_password_email(session, data)


@router.post("/reset-password")
async def reset_password(session: session, data: schemas.ResetPassword): 
  return await services.verify_token_and_reset_password(session, data)



@router.get('/admin')
async def admin(user: User = Depends(dep.require_admin)): 
  return {"msg": f"Welcome admin {user.email}"}


@router.post("/logout")
async def logout(session: session, request: Request, user: User = Depends(dep.get_current_user)): 
  refresh_token = request.cookies.get("refresh_token")
  if refresh_token: 
    await services.revoke_refresh_token(session, refresh_token)

  response  = JSONResponse(content={'detail': "logged out"})
  response.delete_cookie('refresh_token')
  response.delete_cookie('access_token') 
  return response
   
@router.put("/make-me-admin", response_model=schemas.UserOut)
async def make_admin(session: session, user: User = Depends(dep.get_current_user)):
  return await services.make_admin(session, user)

