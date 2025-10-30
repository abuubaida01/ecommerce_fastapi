from fastapi import status, HTTPException
from sqlalchemy  import select
from sqlalchemy.ext.asyncio import AsyncSession
from cart.models import CartItem
from product.models import Product
from . import schemas as sc
from sqlalchemy.orm import selectinload

async def add_to_cart(
    session: AsyncSession, 
    user_id: int, 
    data: sc.CartItemCreate
  ):

  product = await session.get(Product, data.product_id)
  if not product: 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
  
  if product.stock_quantity < data.quantity: 
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient stock")
  
  stmt = select(CartItem).where(CartItem.user_id == user_id, CartItem.product_id == data.product_id)
  result = await session.execute(stmt)
  item = result.scalar_one_or_none()

  if item: 
    item.quantity += data.quantity
    item.price = product.price

  else: 
    item = CartItem(
      user_id=user_id, 
      product_id=data.product_id, 
      quantity = data.quantity,
      price = product.price 
    )

    session.add(item)
  
  await session.commit()
  await session.refresh(item)
  return sc.CartItemOut(
    id=item.id, 
    product_id=item.product_id,
    product_title=product.title,
    quantity=item.quantity,
    user_id=item.user_id,
    price=product.price,
    total=round(product.price * item.quantity, 2)
  )


async def list_user_cart(
    session: AsyncSession,
    user_id: int
  ) -> sc.CartSummary: 

  stmt = select(CartItem).where(CartItem.user_id==user_id).options(selectinload(CartItem.product))
  result = await session.execute(stmt)
  cart_items = result.scalars().all()

  cart_data: list[sc.CartItemOut] = []
  total_quantity = 0
  total_price = 0.0

  for item in cart_items: 
    if not item.product: 
      continue 

    price = item.price 
    quantity = item.quantity
    total = price * quantity
    total_price += total
    total_quantity += quantity 

    cart_data.append(sc.CartItemOut(
      id=item.id,
      product_id=item.product_id, 
      product_title = item.product.title,
      quantity=quantity,
      price=price,
      total=total 
    ))

    return sc.CartSummary(
      items=cart_data,
      total_quantity=total_quantity,
      total_price=total_price
    )