from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from shipping import schemas as sc
from .models import ShippingAddress

async def create_shipping_address(
    session: AsyncSession,
    user_id: int,
    data: sc.Create
  ) -> sc.Out: 
  
  address = ShippingAddress(user_id=user_id, **data.model_dump())
  session.add(address)
  await session.commit()
  await session.refresh(address)
  return address



async def list_user_address(
    session: AsyncSession, 
    user_id: int
  )-> list[sc.Out]: 

  stmt = select(ShippingAddress).where(ShippingAddress.user_id == user_id)
  result = await session.execute(stmt)
  return result.scalars().all()
  

async def get_user_shipping_address(
    session: AsyncSession, 
    user_id: int, 
    address_id: int
  ) -> sc.Out: 

  address = await session.get(ShippingAddress, address_id)
  
  if not address or address.user_id != user_id:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")

  return address 


async def update_user_shipping_address(
    session: AsyncSession, 
    user_id: int, 
    address_id: int,
    data: sc.Update
  ) -> sc.Out: 
  address = await session.get(ShippingAddress, address_id)

  if not address or address.user_id != user_id: 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="address  not found or not authorized")
  

  # update address 
  for key, value in data.model_dump(exlude_unset=True).items():
    setattr(address, key, value)
  
  await session.commit()
  await session.refresh(address)

  return address




async def delete_user_shipping_address(
    session: AsyncSession, 
    user_id: int, 
    address_id: int,
  )-> dict: 
  address = await session.get(ShippingAddress, address_id)

  if not address or address.user_id != user_id: 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="address  not found or not authorized")
  
  await session.delete(address)
  await session.commit()
  return {"message": "address deleted"}
