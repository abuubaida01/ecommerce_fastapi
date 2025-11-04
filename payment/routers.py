from fastapi import APIRouter, Depends, HTTPException, status
from db.config import session
from account.models import User
from account.dependency import get_current_user
from payment.schemas import PaymentOut
from payment.services import get_payment_by_order_id, list_payments_by_user

router = APIRouter()

@router.get("/{order_id}", response_model=PaymentOut)
async def get_payment_status_by_order(
  session: session,
  order_id: int,
  user: User = Depends(get_current_user)
):
  payment = await get_payment_by_order_id(session, order_id, user.id)
  if not payment:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
  return payment

@router.get("", response_model=list[PaymentOut])
async def get_all_payments_by_user(
  session: session,
  user: User = Depends(get_current_user)
):
  payments =  await list_payments_by_user(session, user.id)
  return payments