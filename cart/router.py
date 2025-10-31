from fastapi import APIRouter, Depends, HTTPException, status
from account.dependency import get_current_user
from account.models import User
from db.config import session
from . import schemas as sc
from . import services as ss
from typing import Union

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


@router.patch("/increase/{product_id}", response_model=sc.CartItemOut)
async def increase_product_quantity(
  product_id: int, 
  session: session, 
  user: User = Depends(get_current_user)
  ): 
  return await ss.change_cart_item_qunatity_by_product(session, user.id, product_id, delta=1)



@router.patch("/decrease/{product_id}", response_model=Union[sc.CartItemOut, dict])
async def decrease_product_quantity(
  product_id: int, 
  session: session, 
  user: User = Depends(get_current_user)
  ): 
  return await ss.change_cart_item_qunatity_by_product(session, user.id, product_id, delta=-1)



@router.delete("/delete/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cart_item_delete(
  session: session, 
  item_id: int, 
  user: User = Depends(get_current_user)
  ): 

  return await ss.delete_user_cart_item(session, item_id)