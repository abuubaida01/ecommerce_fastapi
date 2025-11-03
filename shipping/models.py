from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from db.base import Base 
from account.models import User
from typing import TYPE_CHECKING

class ShippingAddress(Base): 
  __tablename__ = "shipping_address"
  id: Mapped[int] = mapped_column(primary_key=True, index=True)
  user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
  name: Mapped[str] = mapped_column(String(255), nullable=False)
  address_line1: Mapped[str] = mapped_column(String(255), nullable=False)
  address_line2: Mapped[str| None] = mapped_column(String(255), nullable=True)

  city: Mapped[str] = mapped_column(String(100), nullable=False)
  state: Mapped[str] = mapped_column(String(100), nullable=False)
  pin_code: Mapped[str] = mapped_column(String(20), nullable=False)
  country: Mapped[str] = mapped_column(String(100), nullable=False)

  user: Mapped["User"] = relationship("User", back_populates="shipping_address")