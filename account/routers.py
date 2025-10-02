from fastapi import APIRouter
from .services import create_user
from .schemas import UserCreate, UserResponse
from db.config import session

router = APIRouter(tags=['Account'])

@router.post("/register", response_model=UserResponse)
async def register(session: session, user: UserCreate):
  return await create_user(session, user)
