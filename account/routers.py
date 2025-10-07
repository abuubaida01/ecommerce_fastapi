from fastapi import APIRouter, HTTPException, status
from . import services
from . import schemas 
from db.config import session
from .utils import verify_password

router = APIRouter(tags=['Account'])

@router.post("/register", response_model=schemas.UserResponse)
async def register(session: session, user: schemas.UserCreate):
  return await services.create_user(session, user)

@router.post("/login")
async def login(session: session, user_login: schemas.UserLogin): 
  user = await services.authenticate_user(session, user_login)

  