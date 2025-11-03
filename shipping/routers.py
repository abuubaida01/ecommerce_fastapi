from fastapi import APIRouter, Depends, HTTPException, status
from db.config import session
from account.models import User
from account.dependency import get_current_user
from shipping import schemas as sc
from shipping.models import ShippingAddress
from shipping import services as ss

router = APIRouter()

@router.post("/address", response_model=sc.Out)
async def create_user_address(
  session: session, 
  data: sc.Create,
  user: User = Depends(get_current_user), 
  ): 

  return await ss.create_shipping_address(session, user.id, data)


@router.get("/address", response_model=list[sc.Out])
async def list_user_addresses(
  session: session, 
  user: User = Depends(get_current_user)
  ) -> list[sc.Out]:

  return await ss.list_user_address(session, user.id) 



@router.get("/address/{address_id}", response_model=sc.Out)
async def get_user_address(
  session: session, 
  address_id: int,
  user: User = Depends(get_current_user)
  ) -> sc.Out:

  return await ss.get_user_shipping_address(session, user.id, address_id)
 


@router.patch("/address/{address_id}", response_model=sc.Out)
async def update_user_shipping_address(
  session: session, 
  address_id: int, 
  data: sc.Update,
  user: User = Depends(get_user_address)
  ): 
  return await ss.update_user_shipping_address(session, user.id, address_id, data)


@router.delete("/address/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_address(
  session: session,
  address_id: int, 
  user: User = Depends(get_current_user)
  ) -> dict:
  
  return await ss.delete_user_shipping_address(session, user.id, address_id)