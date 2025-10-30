from fastapi import APIRouter, Depends, HTTPException, status
from account.dependency import get_current_user
from account.models import User
from db.config import session
from . import schemas as sc
from . import services as ss

router = APIRouter()

@router.post('/add', response_model=sc.CartItemOut)
async def add_item_to_cart(
  session: session, 
  item: sc.CartItemCreate,
  user: User = Depends(get_current_user)
): 
  return await ss.add_to_cart(session=session, user_id=user.id, data=item)


@router.get("", response_model=sc.CartSummary)
async def list_user_cart_items(
  session: session, 
  user: User = Depends(get_current_user)
  ): 
  return await ss.list_user_cart(session, user.id)